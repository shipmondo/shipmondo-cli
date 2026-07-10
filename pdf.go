package main

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

// extractAndOpenPDFs recursively searches a JSON response for base64-encoded
// PDF strings (they begin with the "%PDF" magic → "JVBERi0" in base64),
// decodes them to temp files and opens each in the system viewer.
func extractAndOpenPDFs(body []byte) {
	var data interface{}
	if err := json.Unmarshal(body, &data); err != nil {
		fmt.Fprintln(os.Stderr, `{"error": "Could not parse response for PDF extraction"}`)
		return
	}

	found := 0
	var walk func(node interface{})
	walk = func(node interface{}) {
		switch v := node.(type) {
		case map[string]interface{}:
			for _, val := range v {
				if s, ok := val.(string); ok && strings.HasPrefix(s, "JVBERi0") {
					saveAndOpen(s)
					found++
				} else {
					walk(val)
				}
			}
		case []interface{}:
			for _, item := range v {
				walk(item)
			}
		}
	}
	walk(data)

	if found == 0 {
		fmt.Fprintln(os.Stderr, "⚠️ No base64 PDFs were found in this API response.")
	}
}

func saveAndOpen(b64 string) {
	raw, err := base64.StdEncoding.DecodeString(b64)
	if err != nil {
		fmt.Fprintf(os.Stderr, `{"error": "Failed to decode PDF string", "details": "%s"}`+"\n", err)
		return
	}
	f, err := os.CreateTemp("", "shipmondo_label_*.pdf")
	if err != nil {
		fmt.Fprintf(os.Stderr, `{"error": "Failed to write PDF file", "details": "%s"}`+"\n", err)
		return
	}
	path := f.Name()
	if _, err := f.Write(raw); err != nil {
		f.Close()
		fmt.Fprintf(os.Stderr, `{"error": "Failed to write PDF file", "details": "%s"}`+"\n", err)
		return
	}
	f.Close()

	fmt.Fprintf(os.Stderr, "📄 [PDF Extracted] Opening: %s\n", path)
	openFile(path)
}

func openFile(path string) {
	var cmd *exec.Cmd
	switch runtime.GOOS {
	case "darwin":
		cmd = exec.Command("open", path)
	case "windows":
		cmd = exec.Command("rundll32", "url.dll,FileProtocolHandler", filepath.Clean(path))
	default:
		cmd = exec.Command("xdg-open", path)
	}
	if err := cmd.Start(); err != nil {
		fmt.Fprintf(os.Stderr, `{"error": "Could not launch PDF viewer", "details": "%s"}`+"\n", err)
	}
}
