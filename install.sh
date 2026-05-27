#!/bin/bash
set -e

# Visual formatting variables
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}📦 Starting Shipmondo CLI Installation...${NC}"

# 1. Ensure Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is required but was not found on this system.${NC}" >&2
    exit 1
fi

# 2. Check and provision pipx if missing
if ! command -v pipx &> /dev/null; then
    echo -e "${YELLOW}⚠️ pipx not found. Attempting to install pipx safely...${NC}"
    
    # Try system package managers first, but safely check if the package actually exists
    if command -v brew &> /dev/null; then
        echo -e "${GREEN}🍺 macOS/Homebrew detected. Installing pipx...${NC}"
        brew install pipx
    elif command -v apt-get &> /dev/null; then
        echo -e "${GREEN}🐧 Debian/Ubuntu detected. Installing pipx...${NC}"
        sudo apt-get update && sudo apt-get install -y pipx
    elif command -v dnf &> /dev/null && sudo dnf info pipx &> /dev/null; then
        echo -e "${GREEN}🎩 Fedora/RHEL detected. Installing pipx...${NC}"
        sudo dnf install -y pipx
    elif command -v pacman &> /dev/null; then
        echo -e "${GREEN}🔵 Arch Linux detected. Installing pipx...${NC}"
        sudo pacman -S --noconfirm pipx
    else
        # The Universal PEP-668 Fallback (Perfect for Amazon Linux 2023 and custom distros)
        echo -e "${YELLOW}⚠️ Package not found in OS manager. Bootstrapping pipx via isolated Python venv...${NC}"
        python3 -m venv ~/.local/share/pipx-venv
        ~/.local/share/pipx-venv/bin/pip install pipx
        mkdir -p ~/.local/bin
        ln -sf ~/.local/share/pipx-venv/bin/pipx ~/.local/bin/pipx
        
        # Inject it into the current script's PATH so the next steps don't fail
        export PATH="$HOME/.local/bin:$PATH"
    fi
    
    # Final sanity check
    if ! command -v pipx &> /dev/null; then
        echo -e "${RED}❌ Error: pipx installation failed. Please install pipx manually.${NC}" >&2
        exit 1
    fi
fi

# 3. Ensure pipx binary directory is appended to the system PATH hooks
echo -e "${GREEN}⚙️ Ensuring pipx environment PATH hooks are configured...${NC}"
pipx ensurepath --force

# 4. Perform the isolated app installation
echo -e "${GREEN}🚀 Installing shipmondo-cli in an isolated environment via pipx...${NC}"
pipx install "git+https://github.com/shipmondo/shipmondo-cli.git" --force

echo -e "${GREEN}✅ Shipmondo CLI successfully installed!${NC}"
echo -e "Note: If 'shipmondo' is not recognized immediately, restart your terminal window."
echo -e "Try running: ${YELLOW}shipmondo commands --json${NC}"