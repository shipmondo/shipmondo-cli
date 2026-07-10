package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"strings"
)

// This file derives the CLI's command surface at runtime from the OpenAPI
// spec: the command tree, the `commands` catalog and the per-command
// `--help-json` metadata. Syncing with the API is therefore nothing more than
// updating openapi.json — no code changes required.

// kv is an ordered key/value pair from a JSON object.
type kv struct {
	Key string
	Val json.RawMessage
}

// Param is a single path or query parameter of an operation.
type Param struct {
	Name        string
	In          string // "path" or "query"
	Required    bool
	Type        string // mapped type string: str/int/bool/float
	Description string
}

// Command is one invocable action: `shipmondo <Module> <Name>`.
type Command struct {
	Module     string
	Name       string
	Method     string // upper-case HTTP verb
	Endpoint   string // path template, e.g. /shipments/{id}
	Summary    string
	Params     []Param
	PayloadRaw json.RawMessage // resolved requestBody schema, or nil
}

func (c *Command) hasBody() bool {
	return c.Method == "POST" || c.Method == "PUT" || c.Method == "PATCH"
}

func (c *Command) pathParams() []Param {
	var out []Param
	for _, p := range c.Params {
		if p.In == "path" {
			out = append(out, p)
		}
	}
	return out
}

// Spec holds the parsed catalog and dispatch table for the embedded API spec.
type Spec struct {
	raw         []byte
	ModuleOrder []string
	Catalog     map[string][]*Command          // module -> commands, in encounter order
	Dispatch    map[string]map[string]*Command // module -> command name -> command (last wins)
}

type opDetails struct {
	Summary     string       `json:"summary"`
	Parameters  []specParam  `json:"parameters"`
	RequestBody *specReqBody `json:"requestBody"`
}

type specParam struct {
	Name        string `json:"name"`
	In          string `json:"in"`
	Required    bool   `json:"required"`
	Description string `json:"description"`
	Schema      struct {
		Type string `json:"type"`
	} `json:"schema"`
}

type specReqBody struct {
	Content map[string]struct {
		Schema json.RawMessage `json:"schema"`
	} `json:"content"`
}

// loadSpec parses the embedded OpenAPI document and builds the command tree.
func loadSpec(data []byte) (*Spec, error) {
	s := &Spec{
		raw:      data,
		Catalog:  map[string][]*Command{},
		Dispatch: map[string]map[string]*Command{},
	}

	top := map[string]json.RawMessage{}
	if err := json.Unmarshal(data, &top); err != nil {
		return nil, fmt.Errorf("parse spec: %w", err)
	}
	pathsRaw, ok := top["paths"]
	if !ok {
		return nil, fmt.Errorf("spec has no paths")
	}
	paths, err := orderedObject(pathsRaw)
	if err != nil {
		return nil, fmt.Errorf("parse paths: %w", err)
	}

	// Group endpoints by module, preserving first-occurrence module order and
	// path order within each module.
	type pathEntry struct {
		path    string
		methods json.RawMessage
	}
	groups := map[string][]pathEntry{}
	for _, p := range paths {
		parts := splitPath(p.Key)
		if len(parts) == 0 {
			continue
		}
		module := strings.ReplaceAll(parts[0], "-", "_")
		if _, seen := groups[module]; !seen {
			s.ModuleOrder = append(s.ModuleOrder, module)
		}
		groups[module] = append(groups[module], pathEntry{p.Key, p.Val})
	}

	for _, module := range s.ModuleOrder {
		for _, pe := range groups[module] {
			parts := splitPath(pe.path)
			resource := parts[0]

			methods, err := orderedObject(pe.methods)
			if err != nil {
				continue
			}
			for _, m := range methods {
				method := strings.ToLower(m.Key)
				switch method {
				case "get", "post", "put", "delete", "patch":
				default:
					continue
				}

				var det opDetails
				if err := json.Unmarshal(m.Val, &det); err != nil {
					continue
				}

				cmdName := deriveCmdName(resource, method, parts)
				summary := det.Summary
				if summary == "" {
					summary = fmt.Sprintf("%s %s", strings.ToUpper(method), pe.path)
				}
				summary = strings.ReplaceAll(summary, `"`, "'")

				cmd := &Command{
					Module:   module,
					Name:     cmdName,
					Method:   strings.ToUpper(method),
					Endpoint: pe.path,
					Summary:  summary,
				}

				for _, p := range det.Parameters {
					desc := strings.ReplaceAll(p.Description, `"`, "'")
					desc = strings.ReplaceAll(desc, "\n", " ")
					cmd.Params = append(cmd.Params, Param{
						Name:        p.Name,
						In:          p.In,
						Required:    p.Required,
						Type:        mapType(p.Schema.Type),
						Description: desc,
					})
				}

				if det.RequestBody != nil {
					if c, ok := det.RequestBody.Content["application/json"]; ok && len(c.Schema) > 0 {
						cmd.PayloadRaw = resolveRaw(s.raw, c.Schema, map[string]bool{})
					}
				}

				s.Catalog[module] = append(s.Catalog[module], cmd)
				if s.Dispatch[module] == nil {
					s.Dispatch[module] = map[string]*Command{}
				}
				s.Dispatch[module][cmdName] = cmd // last definition wins on name collisions
			}
		}
	}

	return s, nil
}

// deriveCmdName maps an HTTP method and path to a CLI action name.
func deriveCmdName(resource, method string, parts []string) string {
	if len(parts) == 1 {
		switch method {
		case "get":
			if resource == "account" {
				return "get"
			}
			return "list"
		case "post":
			return "create"
		default:
			return method
		}
	}

	var sub []string
	for _, p := range parts[1:] {
		if !strings.Contains(p, "{") {
			sub = append(sub, strings.ReplaceAll(p, "-", "_"))
		}
	}
	if len(sub) > 0 {
		name := strings.Join(sub, "_")
		if method == "put" || method == "patch" || method == "delete" {
			name = method + "_" + name
		}
		return name
	}
	switch method {
	case "get":
		return "get"
	case "put", "patch":
		return "update"
	case "delete":
		return "delete"
	default:
		return method
	}
}

// CatalogJSON renders the `shipmondo commands` output (indent-2, ordered).
func (s *Spec) CatalogJSON() []byte {
	var b bytes.Buffer
	b.WriteByte('{')
	for i, module := range s.ModuleOrder {
		if i > 0 {
			b.WriteByte(',')
		}
		b.Write(mustJSON(module))
		b.WriteByte(':')
		b.WriteByte('[')
		for j, c := range s.Catalog[module] {
			if j > 0 {
				b.WriteByte(',')
			}
			entry := struct {
				Command     string `json:"command"`
				Description string `json:"description"`
				Method      string `json:"method"`
				Endpoint    string `json:"endpoint"`
			}{c.Name, c.Summary, c.Method, c.Endpoint}
			eb, _ := json.Marshal(entry)
			b.Write(eb)
		}
		b.WriteByte(']')
	}
	b.WriteByte('}')

	var out bytes.Buffer
	if err := json.Indent(&out, b.Bytes(), "", "  "); err != nil {
		return b.Bytes()
	}
	return out.Bytes()
}

// HelpJSON renders the machine-readable schema for a single command.
func (c *Command) HelpJSON() []byte {
	var pb bytes.Buffer
	pb.WriteByte('{')
	for i, p := range c.Params {
		if i > 0 {
			pb.WriteByte(',')
		}
		flag := "Positional Argument"
		if p.In == "query" {
			flag = "--" + strings.ReplaceAll(p.Name, "_", "-")
		}
		meta := struct {
			CLIFlag     string `json:"cli_flag"`
			Location    string `json:"location"`
			Type        string `json:"type"`
			Required    bool   `json:"required"`
			Description string `json:"description"`
		}{flag, p.In, p.Type, p.Required, p.Description}
		mb, _ := json.Marshal(meta)
		pb.Write(mustJSON(p.Name))
		pb.WriteByte(':')
		pb.Write(mb)
	}
	pb.WriteByte('}')

	payload := json.RawMessage("null")
	if c.PayloadRaw != nil {
		payload = c.PayloadRaw
	}

	parent := struct {
		Command       string          `json:"command"`
		Description   string          `json:"description"`
		Method        string          `json:"method"`
		Endpoint      string          `json:"endpoint"`
		Parameters    json.RawMessage `json:"parameters"`
		PayloadSchema json.RawMessage `json:"payload_schema"`
	}{
		Command:       fmt.Sprintf("shipmondo %s %s", c.Module, c.Name),
		Description:   c.Summary,
		Method:        c.Method,
		Endpoint:      c.Endpoint,
		Parameters:    json.RawMessage(pb.Bytes()),
		PayloadSchema: payload,
	}

	out, _ := json.MarshalIndent(parent, "", "  ")
	return out
}

// resolveRaw recursively inlines $ref pointers, preserving key order and
// breaking reference cycles with a placeholder.
func resolveRaw(spec, node json.RawMessage, seen map[string]bool) json.RawMessage {
	trimmed := bytes.TrimSpace(node)
	if len(trimmed) == 0 {
		return node
	}
	switch trimmed[0] {
	case '{':
		pairs, err := orderedObject(trimmed)
		if err != nil {
			return node
		}
		for _, p := range pairs {
			if p.Key == "$ref" {
				var ref string
				if err := json.Unmarshal(p.Val, &ref); err != nil {
					break
				}
				if seen[ref] {
					return json.RawMessage(`{"$ref": "[Circular Reference]"}`)
				}
				next := copySet(seen)
				next[ref] = true
				target := refLookup(spec, ref)
				if target == nil {
					target = json.RawMessage("{}")
				}
				return resolveRaw(spec, target, next)
			}
		}
		var b bytes.Buffer
		b.WriteByte('{')
		for i, p := range pairs {
			if i > 0 {
				b.WriteByte(',')
			}
			b.Write(mustJSON(p.Key))
			b.WriteByte(':')
			b.Write(resolveRaw(spec, p.Val, copySet(seen)))
		}
		b.WriteByte('}')
		return json.RawMessage(b.Bytes())
	case '[':
		var arr []json.RawMessage
		if err := json.Unmarshal(trimmed, &arr); err != nil {
			return node
		}
		var b bytes.Buffer
		b.WriteByte('[')
		for i, el := range arr {
			if i > 0 {
				b.WriteByte(',')
			}
			b.Write(resolveRaw(spec, el, copySet(seen)))
		}
		b.WriteByte(']')
		return json.RawMessage(b.Bytes())
	default:
		return node
	}
}

// refLookup resolves a "#/a/b/c" JSON pointer to its raw value in the spec.
func refLookup(spec json.RawMessage, ref string) json.RawMessage {
	parts := strings.Split(ref, "/")
	if len(parts) <= 1 {
		return nil
	}
	cur := spec
	for _, p := range parts[1:] {
		var m map[string]json.RawMessage
		if err := json.Unmarshal(cur, &m); err != nil {
			return nil
		}
		v, ok := m[p]
		if !ok {
			return nil
		}
		cur = v
	}
	return cur
}

// orderedObject decodes a JSON object into ordered key/value pairs.
func orderedObject(data json.RawMessage) ([]kv, error) {
	dec := json.NewDecoder(bytes.NewReader(data))
	tok, err := dec.Token()
	if err != nil {
		return nil, err
	}
	if d, ok := tok.(json.Delim); !ok || d != '{' {
		return nil, fmt.Errorf("expected JSON object")
	}
	var out []kv
	for dec.More() {
		keyTok, err := dec.Token()
		if err != nil {
			return nil, err
		}
		key, ok := keyTok.(string)
		if !ok {
			return nil, fmt.Errorf("expected string key")
		}
		var raw json.RawMessage
		if err := dec.Decode(&raw); err != nil {
			return nil, err
		}
		out = append(out, kv{Key: key, Val: raw})
	}
	if _, err := dec.Token(); err != nil { // consume closing '}'
		return nil, err
	}
	return out, nil
}

func mapType(t string) string {
	switch t {
	case "string":
		return "str"
	case "integer":
		return "int"
	case "boolean":
		return "bool"
	case "number":
		return "float"
	default:
		return "str"
	}
}

func splitPath(p string) []string {
	var out []string
	for _, s := range strings.Split(p, "/") {
		if s != "" {
			out = append(out, s)
		}
	}
	return out
}

func mustJSON(v interface{}) []byte {
	b, _ := json.Marshal(v)
	return b
}

func copySet(m map[string]bool) map[string]bool {
	n := make(map[string]bool, len(m))
	for k := range m {
		n[k] = true
	}
	return n
}
