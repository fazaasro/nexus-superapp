#!/bin/bash
# ========================================================================
# PaddleOCR Installation Script for Nexus (Ubuntu 24.04 Fixed)
# ========================================================================
# Author: Levy (Agent Faza)
# Date: 2026-02-18
# ========================================================================

set -e  # Exit on error

COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_CYAN='\033[0;36m'
COLOR_NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${COLOR_YELLOW}━━━ $1 ━━━${COLOR_NC}"
    echo ""
}

# Check for root
if [ "$EUID" -eq 0 ]; then
  echo -e "${COLOR_RED}❌ Do not run this script as root (sudo)!${COLOR_NC}"
  echo "   Run it as your normal user. The script will ask for sudo when needed."
  exit 1
fi

print_header "Step 1: Create Virtual Environment"

if [ -d "paddle_env" ]; then
    echo -e "${COLOR_CYAN}ℹ️  Virtual environment 'paddle_env' already exists. Skipping creation.${COLOR_NC}"
else
    python3 -m venv paddle_env || {
        echo -e "${COLOR_RED}❌ Failed to create venv. Make sure python3-venv is installed.${COLOR_NC}"
        exit 1
    }
    echo -e "${COLOR_GREEN}✅ Virtual environment 'paddle_env' created${COLOR_NC}"
fi

print_header "Step 2: Install System Dependencies"
echo -e "${COLOR_CYAN}ℹ️  Requesting sudo permissions for system libraries...${COLOR_NC}"

sudo apt-get update
# FIXED: Replaced libgl1-mesa-glx with libgl1 for Ubuntu 24.04+
sudo apt-get install -y ffmpeg libsm6 libxext6 libxrender1 libgl1 \
    libglib2.0-0 libgomp1 libfontconfig1 libgbm1

echo -e "${COLOR_GREEN}✅ System dependencies installed${COLOR_NC}"

print_header "Step 3: Install Python Packages (CPU)"

source paddle_env/bin/activate

echo -e "${COLOR_CYAN}ℹ️  Upgrading pip...${COLOR_NC}"
pip install --upgrade pip setuptools wheel

echo -e "${COLOR_CYAN}ℹ️  Installing PaddlePaddle (CPU)...${COLOR_NC}"
pip install paddlepaddle

echo -e "${COLOR_CYAN}ℹ️  Installing PaddleOCR...${COLOR_NC}"
pip install "paddleocr>=2.0.1"

echo -e "${COLOR_GREEN}✅ Python packages installed${COLOR_NC}"

print_header "Step 4: Verify Installation"

python -c "
import paddle
print(f'✅ PaddlePaddle version: {paddle.__version__}')
paddle.utils.run_check()
" || {
    echo -e "${COLOR_RED}❌ Verification failed${COLOR_NC}"
    exit 1
}

echo ""
echo -e "${COLOR_GREEN}✅ SETUP COMPLETE${COLOR_NC}"
echo -e "${COLOR_CYAN}To start using it, run: source paddle_env/bin/activate${COLOR_NC}"
