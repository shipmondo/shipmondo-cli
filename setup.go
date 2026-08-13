package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// runSetup exports the embedded Agent Skill (SKILL.md) to a standard
// ./shipmondo folder in the current directory. Per-tool skill directories
// (Claude Code, Copilot, Cursor, Windsurf, ...) are informal conventions
// that each vendor can relocate without notice, so the CLI doesn't guess at
// them — see the README for how to point a given tool at the exported
// folder.
func runSetup(skill string, args []string) {
	if len(args) > 0 && args[0] != "export" {
		fail(fmt.Sprintf("Unknown setup target '%s'. Use: shipmondo setup export", args[0]))
	}

	content := strings.TrimSpace(skill)
	cwd, _ := os.Getwd()

	dir := filepath.Join(cwd, "shipmondo")
	file := filepath.Join(dir, "SKILL.md")
	if err := os.MkdirAll(dir, 0o755); err != nil {
		fail(fmt.Sprintf("Could not create %s: %v", dir, err))
	}
	if err := os.WriteFile(file, []byte(content), 0o644); err != nil {
		fail(fmt.Sprintf("Could not write %s: %v", file, err))
	}
	fmt.Printf("✅ Exported standard Agent Skill folder to: %s/\n", dir)
	fmt.Println("This folder is now ready to be dropped into any Agent Skills-compatible workflow.")
}
