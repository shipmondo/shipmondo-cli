# Shipmondo CLI

An agent-native Command Line Interface (CLI) for the Shipmondo API. Distributed as a **single self-contained binary** with zero runtime dependencies, and self-describing for seamless integration with AI agents like Claude Code.

---

## Requirements

None. The CLI is a statically-linked binary. Just install and run.

---

## Quick Start / Installation

The install scripts download the correct prebuilt binary for your platform from GitHub Releases and place it on your PATH.

### Mac / Linux / WSL
```bash
curl -fsSL https://raw.githubusercontent.com/shipmondo/shipmondo-cli/main/install.sh | bash
```

### Windows (PowerShell)
```powershell
Invoke-Expression (Invoke-WebRequest -Uri "https://raw.githubusercontent.com/shipmondo/shipmondo-cli/main/install.ps1" -UseBasicParsing).Content
```

Or download a binary directly from the [Releases page](https://github.com/shipmondo/shipmondo-cli/releases/latest) and drop it anywhere on your PATH.

> **Note:** Restart your terminal window after installation if the `shipmondo` command is not immediately recognized.

---

## Configuration

Set your Shipmondo API credentials as environment variables in your profile (`.bashrc`, `.zshrc`, or Windows Environment Variables):

```bash
export SHIPMONDO_API_USER="your_api_user"
export SHIPMONDO_API_KEY="your_api_key"
```

To target the sandbox instead of production, set `SHIPMONDO_BASE_URL="https://sandbox.shipmondo.com/api/public/v3"`.

---

## API spec & caching

The CLI's command surface is driven by the Shipmondo OpenAPI spec:

* **First run** downloads the spec from the canonical URL and caches it locally (`~/Library/Caches/shipmondo/openapi.json` on macOS, `~/.cache/shipmondo/openapi.json` on Linux, `%LocalAppData%\shipmondo\openapi.json` on Windows). The download notice goes to stderr, so piped JSON output stays clean.
* **Subsequent runs** use the cached copy — no network call.
* **`shipmondo reload`** clears the cache and fetches a fresh copy. Run it whenever the API gains new endpoints.

This means the command surface can be updated **without redistributing the binary**: publish a new `openapi.json` and clients pick it up on their next `reload`. If the download ever fails and no cache exists, the CLI falls back to the copy bundled into the binary, so it always works offline. Override the source with `SHIPMONDO_SPEC_URL`.

---

## 🤖 AI Agent Integration

This CLI is natively designed to be operated by autonomous AI agents. Built-in commands inject the Shipmondo API schemas, routing rules, and execution context directly into your favorite AI coding assistant using the open Agent Skills standard.

### Supported Agents & IDEs

Run the setup command for your preferred tool to install the Shipmondo skill into your current workspace:

* **Claude Code:** `shipmondo setup claude`
* **GitHub Copilot (VS Code):** `shipmondo setup copilot`
* **Cursor IDE:** `shipmondo setup cursor`
* **Windsurf IDE:** `shipmondo setup windsurf`

### Generic Export (Other AI Tools)

Export the standard-compliant Agent Skill folder directly to your current directory:

```bash
shipmondo setup export
```

This generates a `./shipmondo` folder containing the `SKILL.md` instructions, ready to be dropped into any Agent Skills-compatible workflow.

---

## Global Flags

### Debug Mode (`--debug`)
Print raw HTTP request headers, request bodies, and full API responses to stderr — useful for local debugging or for AI agents analyzing payloads while troubleshooting.
```bash
shipmondo account get --debug
```

### PDF Auto-Extraction (`--open-pdf`)
Scan the API JSON response for base64-encoded PDF strings (common in shipping labels and commercial invoices), decode them, save to a temp file, and launch your OS's default PDF viewer.
```bash
shipmondo shipments labels 12345 --open-pdf
```

---

## Usage & Examples

By default, all commands output raw, machine-readable JSON, optimized for piping and AI parsing.

### 1. Self-Discovery
List every available resource and action:
```bash
shipmondo commands
```

Inspect a single action's exact schema (arguments, flags, JSON payload):
```bash
shipmondo shipments create --help-json
```

### 2. Fetch Account Data
```bash
shipmondo account get
```

### 3. List Shipments with Query Filters
```bash
shipmondo shipments list --receiver-country DK
```

### 4. Create Resources with a JSON Payload
```bash
shipmondo webhooks create --data '{"endpoint":"https://example.com","key":"secret","action":"shipment.create"}'
```

---

## Keeping Updated

Upgrade the **binary** in place to the latest release:

```bash
shipmondo update
```

To refresh only the **API spec** (new endpoints), use `shipmondo reload` — no reinstall needed.

---

## Building from Source

Requires Go 1.23+.

```bash
make build          # host binary → ./shipmondo
make dist           # cross-compile all platforms → ./dist
```

The CLI's entire command surface is generated at runtime from the OpenAPI spec — no code generation step. The `openapi.json` committed here is both the source served at the canonical spec URL and the offline fallback bundled into the binary. **To publish a new API version, commit an updated `openapi.json`**; installed clients pick it up on their next `shipmondo reload`, with no rebuild or redistribution required.

---

## Releasing (for maintainers)

Binary releases are automated by [.github/workflows/release.yml](.github/workflows/release.yml). Pushing a `v*` tag cross-compiles every platform and publishes a GitHub Release with the exact asset names that `install.sh`, `install.ps1`, and `shipmondo update` expect (`shipmondo-<os>-<arch>`, plus `.exe` on Windows).

To cut a release:

```bash
git checkout main
git pull
git tag v2.0.0            # bump to the next semver version
git push origin v2.0.0
```

The workflow then builds darwin/linux/windows for amd64 + arm64, attaches the binaries to the release, and stamps the tag into the binary (`shipmondo version`). Once it finishes, `https://github.com/shipmondo/shipmondo-cli/releases/latest/download/...` resolves, so the `curl … | bash` and PowerShell installers work immediately.

Notes:
* Tags **must** start with `v` to trigger the workflow.
* The first-ever release is what makes `releases/latest` resolvable — until then the install scripts have nothing to download.
* To build and publish manually instead of via CI: `make dist` then `gh release create v2.0.0 dist/* --generate-notes`.
