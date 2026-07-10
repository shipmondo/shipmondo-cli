package main

import (
	_ "embed"
	"fmt"
	"os"
	"strings"
)

// version is stamped at build time via -ldflags "-X main.version=...".
var version = "dev"

// embeddedSpec is the copy of the API spec bundled into the binary. It is used
// only as an offline fallback when the remote spec cannot be downloaded and no
// local cache exists (see source.go).
//
//go:embed openapi.json
var embeddedSpec []byte

//go:embed SKILL.md
var skillMarkdown string

func main() {
	args := os.Args[1:]
	if len(args) == 0 {
		printHelp(loadedSpec())
		return
	}

	switch args[0] {
	case "-h", "--help", "help":
		printHelp(loadedSpec())
		return
	case "-v", "--version", "version":
		fmt.Printf("shipmondo %s\n", version)
		return
	case "commands":
		fmt.Println(string(loadedSpec().CatalogJSON()))
		return
	case "openapi":
		os.Stdout.Write(loadSpecBytes())
		fmt.Println()
		return
	case "setup":
		runSetup(skillMarkdown, args[1:])
		return
	case "update":
		runUpdate()
		return
	case "reload":
		runReload()
		return
	}

	spec := loadedSpec()
	module := args[0]
	commands, ok := spec.Dispatch[module]
	if !ok {
		fail(fmt.Sprintf("Unknown resource '%s'. Run 'shipmondo commands' for the catalog.", module))
	}

	if len(args) < 2 {
		fmt.Fprintf(os.Stderr, "Resource '%s' requires an action. Available actions:\n", module)
		for _, c := range spec.Catalog[module] {
			fmt.Fprintf(os.Stderr, "  %-24s %s\n", c.Name, c.Summary)
		}
		os.Exit(1)
	}

	action := args[1]
	cmd, ok := commands[action]
	if !ok {
		fail(fmt.Sprintf("Unknown action '%s' for resource '%s'. Run 'shipmondo commands'.", action, module))
	}

	runCommand(cmd, args[2:])
}

// loadedSpec resolves the active spec (cache → download → bundled fallback)
// and parses it into the command tree.
func loadedSpec() *Spec {
	spec, err := loadSpec(loadSpecBytes())
	if err != nil {
		fmt.Fprintf(os.Stderr, `{"error": "Failed to load API spec", "details": "%s"}`+"\n", err)
		os.Exit(1)
	}
	return spec
}

func printHelp(spec *Spec) {
	var b strings.Builder
	b.WriteString("Shipmondo CLI — agent-native interface to the Shipmondo API\n\n")
	b.WriteString("Usage: shipmondo <resource> <action> [options]\n\n")
	b.WriteString("Global commands:\n")
	b.WriteString("  commands            Machine-readable catalog of every resource and action\n")
	b.WriteString("  openapi             Print the raw embedded OpenAPI schema\n")
	b.WriteString("  setup <target>      Install the agent skill (claude|copilot|cursor|windsurf|export)\n")
	b.WriteString("  reload              Clear the cached API spec and fetch a fresh copy\n")
	b.WriteString("  update              Update to the latest released version\n")
	b.WriteString("  version             Print the CLI version\n\n")
	b.WriteString("Common options (per action):\n")
	b.WriteString("  --data <json>       JSON body for POST/PUT/PATCH requests\n")
	b.WriteString("  --query <json>      Raw JSON object of query parameters\n")
	b.WriteString("  --json / --text     Output mode (JSON is the default)\n")
	b.WriteString("  --debug             Print raw request/response to stderr\n")
	b.WriteString("  --open-pdf          Decode and open any base64 PDFs in the response\n")
	b.WriteString("  --help-json         Print the machine-readable schema for an action\n\n")
	b.WriteString("Discovery: run 'shipmondo commands' for the full catalog, and\n")
	b.WriteString("'shipmondo <resource> <action> --help-json' for a single action's schema.\n\n")
	b.WriteString("Resources: ")
	b.WriteString(strings.Join(spec.ModuleOrder, ", "))
	b.WriteString("\n")
	fmt.Print(b.String())
}
