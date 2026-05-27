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
    echo -e "${YELLOW}⚠️ pipx not found. Attempting to install pipx safely via system package manager...${NC}"
    
    if command -v brew &> /dev/null; then
        echo -e "${GREEN}🍺 macOS/Homebrew detected. Installing pipx...${NC}"
        brew install pipx
    elif command -v apt-get &> /dev/null; then
        echo -e "${GREEN}🐧 Debian/Ubuntu detected. Installing pipx...${NC}"
        sudo apt-get update && sudo apt-get install -y pipx
    elif command -v dnf &> /dev/null; then
        echo -e "${GREEN}🎩 Fedora/Amazon Linux 2023 detected. Installing pipx...${NC}"
        sudo dnf install -y pipx
    elif command -v yum &> /dev/null; then
        echo -e "${GREEN}🟡 CentOS/Amazon Linux 2 detected. Installing pipx...${NC}"
        sudo yum install -y pipx
    elif command -v pacman &> /dev/null; then
        echo -e "${GREEN}🔵 Arch Linux detected. Installing pipx...${NC}"
        sudo pacman -S --noconfirm pipx
    else
        echo -e "${RED}❌ Error: pipx is missing and could not be auto-installed.${NC}" >&2
        echo -e "Please install 'pipx' manually for your OS, then re-run this script." >&2
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