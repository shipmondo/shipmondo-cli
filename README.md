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

Here is the updated section for your `README.md`. It broadens the scope to reflect the universal agent support and organizes the commands clearly for the user.

## 🤖 AI Agent Integration

This CLI is natively designed to be operated by autonomous AI agents. We provide built-in commands that automatically inject the Shipmondo API schemas, routing rules, and execution context directly into your favorite AI coding assistant or agent framework using the open Agent Skills standard.

### Supported Agents & IDEs

Run the setup command for your preferred tool to install the Shipmondo skill into your current workspace:

* **Claude Code:** `shipmondo setup claude`
* **GitHub Copilot (VS Code):** `shipmondo setup copilot`
* **Cursor IDE:** `shipmondo setup cursor`
* **Windsurf IDE:** `shipmondo setup windsurf`

### Generic Export (Other AI Tools)

If you are building a custom agent or using an AI not listed above, you can export the standard-compliant Agent Skill folder directly to your current directory:

```bash
shipmondo setup export

```

This will generate a `./shipmondo` folder containing the `SKILL.md` instructions, ready to be dropped into any Agent Skills-compatible workflow.


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