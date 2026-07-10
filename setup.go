package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// runSetup installs the embedded Agent Skill (SKILL.md) into the target
// AI tool's skills directory.
func runSetup(skill string, args []string) {
	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "Usage: shipmondo setup <claude|copilot|cursor|windsurf|export> [--local]")
		os.Exit(1)
	}

	target := args[0]
	global := true
	for _, a := range args[1:] {
		switch a {
		case "--local":
			global = false
		case "--global":
			global = true
		}
	}

	content := strings.TrimSpace(skill)

	home, _ := os.UserHomeDir()
	cwd, _ := os.Getwd()

	write := func(dir, tool string) {
		if err := os.MkdirAll(dir, 0o755); err != nil {
			fail(fmt.Sprintf("Could not create %s: %v", dir, err))
		}
		file := filepath.Join(dir, "SKILL.md")
		if err := os.WriteFile(file, []byte(content), 0o644); err != nil {
			fail(fmt.Sprintf("Could not write %s: %v", file, err))
		}
		fmt.Printf("✅ Shipmondo skill successfully installed to: %s\n", file)
		fmt.Printf("%s will automatically load these instructions when relevant.\n", tool)
	}

	switch target {
	case "claude":
		dir := filepath.Join(cwd, ".claude", "skills", "shipmondo")
		if global {
			dir = filepath.Join(home, ".claude", "skills", "shipmondo")
		}
		write(dir, "Claude Code")
	case "copilot":
		dir := filepath.Join(cwd, ".github", "skills", "shipmondo")
		if global {
			dir = filepath.Join(home, ".copilot", "skills", "shipmondo")
		}
		write(dir, "GitHub Copilot")
	case "cursor":
		write(filepath.Join(cwd, ".cursor", "skills", "shipmondo"), "Cursor's agent")
	case "windsurf":
		write(filepath.Join(cwd, ".windsurf", "skills", "shipmondo"), "Windsurf's Cascade agent")
	case "export":
		dir := filepath.Join(cwd, "shipmondo")
		file := filepath.Join(dir, "SKILL.md")
		if _, err := os.Stat(file); err == nil {
			fmt.Fprintln(os.Stderr, "ℹ️ The shipmondo/SKILL.md file already exists in this directory.")
			os.Exit(0)
		}
		if err := os.MkdirAll(dir, 0o755); err != nil {
			fail(fmt.Sprintf("Could not create %s: %v", dir, err))
		}
		if err := os.WriteFile(file, []byte(content), 0o644); err != nil {
			fail(fmt.Sprintf("Could not write %s: %v", file, err))
		}
		fmt.Printf("✅ Exported standard Agent Skill folder to: %s/\n", dir)
		fmt.Println("This folder is now ready to be dropped into any Agent Skills-compatible workflow.")
	default:
		fail(fmt.Sprintf("Unknown setup target '%s'. Use: claude, copilot, cursor, windsurf, or export.", target))
	}
}
