#!/bin/bash
set -e

# Shipmondo CLI installer (macOS / Linux / WSL).
# Downloads a single self-contained binary from GitHub Releases.
# Zero runtime dependencies.

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

REPO="shipmondo/shipmondo-cli"

echo -e "${GREEN}📦 Installing the Shipmondo CLI...${NC}"

os=$(uname -s | tr '[:upper:]' '[:lower:]')
arch=$(uname -m)
case "$arch" in
    x86_64|amd64) arch="amd64" ;;
    arm64|aarch64) arch="arm64" ;;
    *) echo -e "${RED}❌ Unsupported architecture: $arch${NC}" >&2; exit 1 ;;
esac
case "$os" in
    darwin|linux) ;;
    *) echo -e "${RED}❌ Unsupported OS: $os${NC}" >&2; exit 1 ;;
esac

asset="shipmondo-${os}-${arch}"
url="https://github.com/${REPO}/releases/latest/download/${asset}"

# Pick an install directory that is (or can be) on PATH.
if [ -w "/usr/local/bin" ] 2>/dev/null; then
    dir="/usr/local/bin"
    use_sudo=""
elif command -v sudo >/dev/null 2>&1 && [ -d "/usr/local/bin" ]; then
    dir="/usr/local/bin"
    use_sudo="sudo"
else
    dir="$HOME/.local/bin"
    mkdir -p "$dir"
    use_sudo=""
fi

tmp=$(mktemp)
echo -e "${GREEN}⬇️  Downloading ${asset}...${NC}"
if ! curl -fsSL "$url" -o "$tmp"; then
    echo -e "${RED}❌ Download failed from ${url}${NC}" >&2
    rm -f "$tmp"
    exit 1
fi
chmod +x "$tmp"
$use_sudo mv "$tmp" "$dir/shipmondo"

echo -e "${GREEN}✅ Shipmondo CLI installed to ${dir}/shipmondo${NC}"

case ":$PATH:" in
    *":$dir:"*) ;;
    *) echo -e "${YELLOW}⚠️  ${dir} is not on your PATH. Add this to your shell profile:${NC}"
       echo -e "    export PATH=\"$dir:\$PATH\"" ;;
esac

echo -e "Try running: ${YELLOW}shipmondo commands${NC}"
