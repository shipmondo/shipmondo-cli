package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"runtime"
	"time"
)

// releaseAsset is the naming convention for published release binaries,
// e.g. shipmondo-darwin-arm64 or shipmondo-windows-amd64.exe.
func releaseAsset() string {
	name := fmt.Sprintf("shipmondo-%s-%s", runtime.GOOS, runtime.GOARCH)
	if runtime.GOOS == "windows" {
		name += ".exe"
	}
	return name
}

// runUpdate downloads the latest release binary for this platform and
// atomically replaces the running executable.
func runUpdate() {
	asset := releaseAsset()
	url := fmt.Sprintf("https://github.com/shipmondo/shipmondo-cli/releases/latest/download/%s", asset)

	fmt.Printf("🔄 Downloading the latest Shipmondo CLI (%s)...\n", asset)

	client := &http.Client{Timeout: 120 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		fail(fmt.Sprintf("Failed to download update: %v", err))
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		fail(fmt.Sprintf("Failed to download update: HTTP %d from %s", resp.StatusCode, url))
	}

	self, err := os.Executable()
	if err != nil {
		fail(fmt.Sprintf("Could not locate current executable: %v", err))
	}
	self, _ = filepath.EvalSymlinks(self)

	tmp, err := os.CreateTemp(filepath.Dir(self), ".shipmondo-update-*")
	if err != nil {
		fail(fmt.Sprintf("Could not create temp file: %v", err))
	}
	tmpPath := tmp.Name()

	if _, err := io.Copy(tmp, resp.Body); err != nil {
		tmp.Close()
		os.Remove(tmpPath)
		fail(fmt.Sprintf("Failed to write update: %v", err))
	}
	tmp.Close()

	if err := os.Chmod(tmpPath, 0o755); err != nil {
		os.Remove(tmpPath)
		fail(fmt.Sprintf("Failed to set permissions: %v", err))
	}

	if err := os.Rename(tmpPath, self); err != nil {
		os.Remove(tmpPath)
		fail(fmt.Sprintf("Failed to replace executable (try re-running with elevated permissions): %v", err))
	}

	fmt.Println("✅ Shipmondo CLI successfully updated!")
}
