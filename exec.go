package main

import (
	"encoding/json"
	"fmt"
	"net/url"
	"os"
	"strconv"
	"strings"
)

// runCommand parses the flags for a resolved command, validates required
// parameters, performs the request and prints the result. `args` are the
// tokens following `shipmondo <module> <command>`.
func runCommand(c *Command, args []string) {
	// Value-bearing flags known to this command.
	valueFlag := map[string]bool{"--query": true}
	if c.hasBody() {
		valueFlag["--data"] = true
	}
	queryByFlag := map[string]string{}
	for _, p := range c.Params {
		if p.In == "query" {
			flag := "--" + strings.ReplaceAll(p.Name, "_", "-")
			queryByFlag[flag] = p.Name
			valueFlag[flag] = true
		}
	}

	var positionals []string
	flagVals := map[string]string{}
	jsonOutput := true
	debug := false
	openPDF := false
	helpJSON := false

	for i := 0; i < len(args); i++ {
		a := args[i]
		if strings.HasPrefix(a, "--") {
			name := a
			val := ""
			hasEq := false
			if idx := strings.IndexByte(a, '='); idx >= 0 {
				name = a[:idx]
				val = a[idx+1:]
				hasEq = true
			}
			switch name {
			case "--debug":
				debug = true
			case "--open-pdf":
				openPDF = true
			case "--help-json":
				helpJSON = true
			case "--json":
				jsonOutput = true
			case "--text":
				jsonOutput = false
			default:
				if !valueFlag[name] {
					fail(fmt.Sprintf("Unknown option '%s'", name))
				}
				if !hasEq {
					i++
					if i >= len(args) {
						fail(fmt.Sprintf("Option '%s' requires a value", name))
					}
					val = args[i]
				}
				flagVals[name] = val
			}
		} else {
			positionals = append(positionals, a)
		}
	}

	if helpJSON {
		fmt.Println(string(c.HelpJSON()))
		return
	}

	pathParams := c.pathParams()
	if len(positionals) > len(pathParams) {
		fail(fmt.Sprintf("Unexpected extra argument '%s'", positionals[len(pathParams)]))
	}

	// Validate required parameters in declaration order.
	for _, p := range c.Params {
		if !p.Required {
			continue
		}
		if p.In == "path" {
			idx := paramIndex(pathParams, p.Name)
			if idx < 0 || idx >= len(positionals) {
				fail(fmt.Sprintf("Missing required Argument '%s'", p.Name))
			}
		} else if p.In == "query" {
			flag := "--" + strings.ReplaceAll(p.Name, "_", "-")
			if _, ok := flagVals[flag]; !ok {
				fail(fmt.Sprintf("Missing required Option '%s'", flag))
			}
		}
	}

	// Build the endpoint by substituting path parameters positionally.
	endpoint := c.Endpoint
	for i, p := range pathParams {
		val := ""
		if i < len(positionals) {
			val = positionals[i]
		}
		endpoint = strings.ReplaceAll(endpoint, "{"+p.Name+"}", val)
	}

	// Assemble query parameters: explicit flags first, then the --query
	// fallback object which overrides on key collisions.
	q := url.Values{}
	for flag, name := range queryByFlag {
		if v, ok := flagVals[flag]; ok {
			q.Set(name, v)
		}
	}
	if raw, ok := flagVals["--query"]; ok {
		var m map[string]interface{}
		if err := json.Unmarshal([]byte(raw), &m); err != nil {
			fail("Invalid JSON in --query")
		}
		for k, v := range m {
			q.Set(k, toQueryString(v))
		}
	}

	// Request body for write methods.
	var body []byte
	if c.hasBody() {
		if raw, ok := flagVals["--data"]; ok && raw != "" {
			var probe interface{}
			if err := json.Unmarshal([]byte(raw), &probe); err != nil {
				fail("Invalid JSON in --data")
			}
			body = []byte(raw)
		}
	}

	resp := doRequest(c.Method, endpoint, q, body, debug)

	if openPDF {
		extractAndOpenPDFs(resp)
	}

	if jsonOutput {
		trimmed := strings.TrimSpace(string(resp))
		if trimmed == "" {
			fmt.Println("{}")
		} else {
			fmt.Println(trimmed)
		}
	} else {
		fmt.Println("Success. Run with --json to see data.")
	}
}

func paramIndex(params []Param, name string) int {
	for i, p := range params {
		if p.Name == name {
			return i
		}
	}
	return -1
}

func toQueryString(v interface{}) string {
	switch t := v.(type) {
	case string:
		return t
	case bool:
		if t {
			return "true"
		}
		return "false"
	case float64:
		return strconv.FormatFloat(t, 'g', -1, 64)
	case nil:
		return ""
	default:
		b, _ := json.Marshal(t)
		return string(b)
	}
}

// fail prints a JSON error to stderr and exits 1.
func fail(message string) {
	b, _ := json.Marshal(map[string]string{"error": message})
	fmt.Fprintln(os.Stderr, string(b))
	os.Exit(1)
}
