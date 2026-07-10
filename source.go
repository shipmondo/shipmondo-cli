package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

// specURL is the canonical, always-available location of the OpenAPI spec.
// The CLI downloads it on first run, caches it locally, and serves every
// subsequent run from the cache until `shipmondo reload` is invoked. It can
// be overridden with SHIPMONDO_SPEC_URL.
const specURL = "https://raw.githubusercontent.com/shipmondo/shipmondo-cli/main/openapi.json"

func specSourceURL() string {
	if u := os.Getenv("SHIPMONDO_SPEC_URL"); u != "" {
		return u
	}
	return specURL
}

// specCachePath returns the on-disk location of the cached spec, e.g.
// ~/Library/Caches/shipmondo/openapi.json (macOS),
// ~/.cache/shipmondo/openapi.json (Linux),
// %LocalAppData%\shipmondo\openapi.json (Windows).
func specCachePath() string {
	dir, err := os.UserCacheDir()
	if err != nil || dir == "" {
		dir = os.TempDir()
	}
	return filepath.Join(dir, "shipmondo", "openapi.json")
}

// loadSpecBytes returns the active spec. It prefers a valid local cache;
// on a cache miss it downloads and caches the spec; if the download fails it
// falls back to the copy bundled into the binary so the CLI keeps working
// offline.
func loadSpecBytes() []byte {
	path := specCachePath()
	if data, err := os.ReadFile(path); err == nil && json.Valid(data) {
		return data
	}

	fmt.Fprintln(os.Stderr, "⬇️  Fetching Shipmondo API spec...")
	if data, err := downloadSpec(); err == nil {
		cacheSpec(path, data)
		return data
	} else {
		fmt.Fprintf(os.Stderr, "⚠️  Could not download API spec (%v); using bundled copy.\n", err)
	}
	return embeddedSpec
}

// downloadSpec fetches and validates the remote spec.
func downloadSpec() ([]byte, error) {
	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Get(specSourceURL())
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("HTTP %d from %s", resp.StatusCode, specSourceURL())
	}
	data, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	if !json.Valid(data) {
		return nil, fmt.Errorf("response was not valid JSON")
	}
	return data, nil
}

// cacheSpec writes the spec to disk atomically. Cache-write failures are
// non-fatal — the CLI still runs with the in-memory copy.
func cacheSpec(path string, data []byte) {
	if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
		fmt.Fprintf(os.Stderr, "⚠️  Could not create cache directory: %v\n", err)
		return
	}
	tmp := path + ".tmp"
	if err := os.WriteFile(tmp, data, 0o644); err != nil {
		fmt.Fprintf(os.Stderr, "⚠️  Could not write cache: %v\n", err)
		return
	}
	if err := os.Rename(tmp, path); err != nil {
		os.Remove(tmp)
		fmt.Fprintf(os.Stderr, "⚠️  Could not finalize cache: %v\n", err)
	}
}

// runReload deletes the cached spec and fetches a fresh copy.
func runReload() {
	path := specCachePath()
	if err := os.Remove(path); err != nil && !os.IsNotExist(err) {
		fail(fmt.Sprintf("Could not delete cached spec: %v", err))
	}

	data, err := downloadSpec()
	if err != nil {
		fail(fmt.Sprintf("Failed to fetch fresh API spec: %v", err))
	}
	cacheSpec(path, data)

	spec, err := loadSpec(data)
	if err != nil {
		fail(fmt.Sprintf("Fetched spec but failed to parse it: %v", err))
	}
	actions := 0
	for _, cmds := range spec.Catalog {
		actions += len(cmds)
	}
	fmt.Printf("✅ Reloaded API spec: %d resources, %d actions.\n", len(spec.ModuleOrder), actions)
	fmt.Printf("   Cached at %s\n", path)
}
