package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"time"
)

// defaultBaseURL is the Shipmondo production API. It can be overridden with
// SHIPMONDO_BASE_URL (useful for pointing at the sandbox server).
const defaultBaseURL = "https://app.shipmondo.com/api/public/v3"

// doRequest performs an authenticated API call. On any transport error or
// non-2xx response it prints a JSON error payload to stderr and exits 1.
// On success it returns the raw response body.
func doRequest(method, endpoint string, query url.Values, body []byte, debug bool) []byte {
	user := os.Getenv("SHIPMONDO_API_USER")
	key := os.Getenv("SHIPMONDO_API_KEY")
	if user == "" || key == "" {
		fmt.Fprintln(os.Stderr, `{"error": "Missing authentication. Set SHIPMONDO_API_USER and SHIPMONDO_API_KEY."}`)
		os.Exit(1)
	}

	base := os.Getenv("SHIPMONDO_BASE_URL")
	if base == "" {
		base = defaultBaseURL
	}

	target := base + endpoint
	if len(query) > 0 {
		target += "?" + query.Encode()
	}

	var reqBody io.Reader
	if body != nil {
		reqBody = bytes.NewReader(body)
	}
	req, err := http.NewRequest(method, target, reqBody)
	if err != nil {
		failRequest(nil, fmt.Sprintf("%v", err))
	}
	req.SetBasicAuth(user, key)
	req.Header.Set("Accept", "application/json")
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "shipmondo-cli")

	if debug {
		fmt.Fprintln(os.Stderr, "\n====== DEBUG: OUTGOING REQUEST ======")
		fmt.Fprintf(os.Stderr, "%s %s\n", method, target)
		fmt.Fprintf(os.Stderr, "Headers: %s\n", headerJSON(req.Header))
		if len(query) > 0 {
			fmt.Fprintf(os.Stderr, "Query Params: %s\n", query.Encode())
		}
		if body != nil {
			fmt.Fprintf(os.Stderr, "JSON Payload: %s\n", string(body))
		}
		fmt.Fprintln(os.Stderr, "=====================================")
	}

	client := &http.Client{Timeout: 120 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		failRequest(nil, fmt.Sprintf("%v", err))
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)

	if debug {
		fmt.Fprintln(os.Stderr, "====== DEBUG: INCOMING RESPONSE ======")
		fmt.Fprintf(os.Stderr, "Status Code: %d\n", resp.StatusCode)
		fmt.Fprintf(os.Stderr, "Headers: %s\n", headerJSON(resp.Header))
		fmt.Fprintf(os.Stderr, "Body: %s\n", string(respBody))
		fmt.Fprintln(os.Stderr, "======================================")
	}

	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		details := extractErrorDetails(respBody, resp.StatusCode)
		failRequest(&resp.StatusCode, details)
	}

	return respBody
}

// extractErrorDetails prefers the API's `error` field, otherwise falls back
// to the raw body or a generic HTTP message.
func extractErrorDetails(body []byte, status int) string {
	var obj map[string]json.RawMessage
	if err := json.Unmarshal(body, &obj); err == nil {
		if raw, ok := obj["error"]; ok {
			var s string
			if err := json.Unmarshal(raw, &s); err == nil {
				return s
			}
			return string(raw)
		}
	}
	if len(bytes.TrimSpace(body)) > 0 {
		return string(body)
	}
	return fmt.Sprintf("HTTP Error %d", status)
}

func headerJSON(h http.Header) string {
	flat := map[string]string{}
	for k := range h {
		flat[k] = h.Get(k)
	}
	b, _ := json.Marshal(flat)
	return string(b)
}

func failRequest(status *int, details string) {
	payload := struct {
		Error      string `json:"error"`
		StatusCode *int   `json:"status_code"`
		Details    string `json:"details"`
	}{
		Error:      "API Request Failed",
		StatusCode: status,
		Details:    details,
	}
	b, _ := json.Marshal(payload)
	fmt.Fprintln(os.Stderr, string(b))
	os.Exit(1)
}
