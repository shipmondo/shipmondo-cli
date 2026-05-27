# Shipmondo CLI

An agent-native Command Line Interface (CLI) for the Shipmondo API. Fully isolated via pipx and self-describing for seamless integration with AI agents like Claude Code.

---

## Requirements

* Python 3.8+ must be installed on your system.
---

## Quick Start / Installation

The installation scripts automatically handle provisioning an isolated environment (pipx) and registering the global binary symlinks.

### Mac / Linux / WSL
```bash
curl -fsSL https://raw.githubusercontent.com/shipmondo/shipmondo-cli/main/install.sh | bash
```

### Windows (PowerShell)
```powershell
Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/shipmondo/shipmondo-cli/main/install.ps1" -UseBasicParsing).Content
```

> **Note:** Restart your terminal window after installation if the shipmondo command is not immediately recognized.

---

## Configuration

Set your Shipmondo API credentials as environment variables in your profile (.bashrc, .zshrc, or Windows Environment Variables):

```bash
export SHIPMONDO_API_USER="your_api_user"
export SHIPMONDO_API_KEY="your_api_key"
```

---

## 🤖 AI Agent Integration (Claude Code)

This CLI is natively designed to be operated by autonomous AI agents like Anthropic's Claude Code. We provide a built-in command that automatically injects the Shipmondo API schemas, routing rules, and execution context directly into Claude's memory.

To install the Shipmondo skill into your current directory, run:

```bash
shipmondo setup claude

```

To install it globally so Claude can manage your Shipmondo account from any folder on your machine, use the global flag:

```bash
shipmondo setup claude --global

```

Once installed, simply launch Claude Code and prompt it naturally. For example: *"Fetch my latest Shipmondo orders,"* or *"Create a shipping label for order 12345."* Claude will autonomously discover the endpoints, format the JSON payloads, and execute the CLI commands on your behalf.

## Global Flags

The CLI includes two powerful global flags that modify runtime behavior across all resource commands:

### Debug Mode (--debug)
Appended to any command to print raw HTTP request headers, request bodies, and full API responses directly to stderr. This is crucial for local debugging or allowing AI agents to analyze API payloads when troubleshooting.
```bash
shipmondo account get --debug
```

### PDF Auto-Extraction (--open-pdf)
Automatically scans the API JSON response for base64-encoded PDF strings (common in shipping labels and commercial invoices). It decodes the data on the fly, saves it to a temporary system file, and launches your operating system's default PDF viewer instantly.
```bash
shipmondo labels get 12345 --open-pdf
```

---

## Usage & Examples

By default, all commands output raw, machine-readable JSON, making it highly optimized for data piping and AI workspace parsing.

### 1. Self-Discovery
List every available API module and endpoint subcommand mapped inside the engine:
```bash
shipmondo commands
```

### 2. Fetch Account Data
```bash
shipmondo account get
```

### 3. List Shipments with Query Filters
```bash
shipmondo shipments list --receiver-country-code DK
```

---

## Keeping Updated

Whenever the codebase updates or new API schemas are added, seamlessly upgrade your installation using the built-in update tool:

```bash
shipmondo update
```