package main

import (
	_ "embed"
	"fmt"
	"os"
	"strings"
)

// logoArt is a truecolor half-block pixel-art rendering of the Shipmondo
// mark, sampled from the icon in logo-shipmondo-color.png.
//
//go:embed logo.ans
var logoArt string

// printBanner renders the Shipmondo mark. It only engages on a real
// terminal with color support, so piped/redirected output (scripts, CI,
// agents) stays plain.
func printBanner() {
	if !supportsColor() {
		return
	}

	fmt.Println()
	lines := strings.Split(strings.TrimRight(logoArt, "\n"), "\n")
	for _, line := range lines {
		fmt.Println("  " + line)
	}
	fmt.Println()
}

func supportsColor() bool {
	if os.Getenv("NO_COLOR") != "" || os.Getenv("TERM") == "dumb" {
		return false
	}
	info, err := os.Stdout.Stat()
	if err != nil {
		return false
	}
	return info.Mode()&os.ModeCharDevice != 0
}
