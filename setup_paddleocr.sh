#!/bin/bash
# ========================================================================
# PaddleOCR Installation Script for Nexus (Ubuntu 24.04 Fixed)
# ========================================================================
# Author: Levy (Agent Faza)
# Date: 2026-02-17
# 
# This script sets up PaddleOCR using a virtual environment.
# Run this script with: sudo bash setup_paddleocr.sh
# ========================================================================

set -e  # Exit on error

# Check for root if [ "$EUID" -eq 0 ]; then echo -e "\033[0;31m❌ Do not run this script as root (sudo)!
   echo -e "\033[0;31mRun it as your normal user. The script will ask for sudo when needed."
   exit 1
fi

COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_CYAN='\033[0;36m'
COLOR_NC='\033[0m' # No Color

echo -e "${COLOR_CYAN}=======================================================================${COLOR_NC}"
echo -e "${COLOR_CYAN}PaddleOCR Installation Script for Nexus${COLOR_NC}"
echo -e "${COLOR_CYAN}=======================================================================${COLOR_NC}"
echo ""

# Function to print section headers
print_header() {
    echo ""
    echo -e "${COLOR_YELLOW}━━━ $1 ━━━${COLOR_NC}"
    echo ""
}

# Function to print success message
print_success() {
    echo -e "${COLOR_GREEN}✅ $1${COLOR_NC}"
}

# Function to print error message
print_error() {
    echo -e "${COLOR_RED}❌ $1${COLOR_NC}"
}

# Function to print info message
print_info() {
    echo -e "${COLOR_CYAN}ℹ️  $1${COLOR_NC}"
}

# Step 1: Create Virtual Environment
print_header "Step 1: Create Virtual Environment"

if [ -d "paddle_env" ]; then
    echo -e "${COLOR_CYAN}ℹ️ Virtual environment 'paddle_env' already exists. Skipping creation.${COLOR_NC}"
else
    print_info "Creating virtual environment 'paddle_env'..."

    if command -v python3-venv &> /dev/null; then
        python3-venv paddle_env || {
            print_error "Failed to create venv with python3-venv"
            print_info "Trying with python3 -m venv..."
            python3 -m venv paddle_env || {
                print_error "Failed to create virtual environment"
                exit 1
            }
        }
    else
        print_info "python3-venv not found, trying with python3 -m venv..."
        python3 -m venv paddle_env || {
            print_error "Failed to create virtual environment"
            exit 1
        }
    fi

print_success "Virtual environment 'paddle_env' created"
print_info "To activate in your terminal: source paddle_env/bin/activate"
print_info "You will see (paddle_env) in your prompt"

# Step 2: Install System Dependencies (Ubuntu 24.04 Fixed)
print_header "Step 2: Install System Dependencies"

print_info "Requesting sudo permissions for system libraries..."
echo ""

sudo apt-get update -qq
# FIXED for Ubuntu 24.04: Replaced libgl1-mesa-glx with libgl1 (compatible with Noble)
sudo apt-get install -y ffmpeg libsm6 libxext6 libxrender1 libgl1 \
    libglib2.0-0 libgthread-2.0-0 libgomp1 libfontconfig1 libgbm1 > /dev/null 2>&1

print_success "System dependencies installed"

# Step 3: Activate Virtual Environment and Install Python Packages
print_header "Step 3: Activate Virtual Environment and Install Python Packages"

print_info "Activating virtual environment..."
source paddle_env/bin/activate || {
    print_error "Failed to activate virtual environment"
    exit 1
}

print_success "Virtual environment activated (you should see (paddle_env) in prompt)"
print_info "Upgrading pip inside virtual environment..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Step 4: Install PaddlePaddle (CPU)
print_header "Step 4: Install PaddlePaddle (CPU)"

print_info "Installing PaddlePaddle (CPU)..."
pip install paddlepaddle-cpu > /dev/null 2>&1

print_success "PaddlePaddle installed"

# Step 5: Install PaddleOCR
print_header "Step 5: Install PaddleOCR"

print_info "Installing PaddleOCR..."
pip install "paddleocr>=2.0.1" > /dev/null 2>&1

print_success "PaddleOCR installed"

# Deactivate virtual environment
deactivate
print_info "Virtual environment deactivated"

# Step 6: Verify Installation
print_header "Step 6: Verify PaddlePaddle Installation"

print_info "Running verification tests..."
paddle_env/bin/python -c "
import sys
try:
    import paddle
    print(f'✅ PaddlePaddle version: {paddle.__version__}')
    
    # Run PaddlePaddle checks
    print('Running PaddlePaddle health checks...')
    paddle.utils.run_check()
    
    print('✅ PaddlePaddle is installed and working correctly!')
    sys.exit(0)
except ImportError as e:
    print(f'❌ Failed to import PaddlePaddle: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ PaddlePaddle check failed: {e}')
    sys.exit(1)
" || {
    print_error "PaddlePaddle verification failed"
    exit 1
}

if [ $? -eq 0 ]; then
    print_success "PaddlePaddle verification passed!"
else
    echo ""
    echo -e "${COLOR_RED}=======================================================================${COLOR_NC}"
    print_error "PaddlePaddle Installation Failed"
    echo -e "${COLOR_RED}=======================================================================${COLOR_NC}"
    exit 1
fi

# Step 7: Clean Up Old Containers
print_header "Step 7: Clean Up Old Containers"

echo "Stopping and removing old containers..."
docker stop tesseract easyocr 2>/dev/null || true
docker rm tesseract easyocr 2>/dev/null || true

print_success "Old containers removed"

# Step 8: Create Test Script
print_header "Step 8: Create Test Script"

cat > test_paddleocr.py << 'EOF'
#!/usr/bin/env python3
"""PaddleOCR Test Script

Tests PaddleOCR with a sample receipt image.
Author: Levy (Agent Faza)
Date: 2026-02-17
"""

import sys
import os

def main():
    """Run PaddleOCR test."""
    print("="*70)
    print("PaddleOCR Quick Test")
    print("="*70)
    
    # Check if PaddleOCR is available
    try:
        from paddleocr import PaddleOCR
        print("✅ PaddleOCR imported successfully!")
    except ImportError as e:
        print(f"❌ Failed to import PaddleOCR: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure virtual environment is activated:")
        print("   source paddle_env/bin/activate")
        print("2. Check if PaddleOCR is installed:")
        print("   pip show paddleocr")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    
    # Initialize PaddleOCR
    print("\nInitializing PaddleOCR (CPU mode, English, angle classifier)...")
    try:
        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        print("✅ PaddleOCR initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize PaddleOCR: {e}")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("PaddleOCR is ready to use!")
    print("="*70)
    
    print("\nUsage:")
    print("  from paddleocr import PaddleOCR")
    print("  ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)")
    print("  result = ocr.ocr('receipt.jpg', cls=True)")
    print("  for line in result:")
    print("      text = line[1]")
    print("      confidence = line[1][1]")
    
    print("\nTo test with a receipt image:")
    print("  python3 /home/ai-dev/.openclaw/workspace/test_paddleocr_detailed.py")

if __name__ == "__main__":
    main()
EOF

print_success "Test script created: test_paddleocr.py"

# Final Summary
echo ""
echo -e "${COLOR_CYAN}=======================================================================${COLOR_NC}"
echo -e "${COLOR_GREEN}✅ PaddleOCR Installation Complete!${COLOR_NC}"
echo -e "${COLOR_CYAN}=======================================================================${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}🚀 What's Next:${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}1. Activate Virtual Environment:${COLOR_NC}"
echo -e "${COLOR_CYAN}   source paddle_env/bin/activate${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}2. Test PaddleOCR:${COLOR_NC}"
echo -e "${COLOR_CYAN}   python3 test_paddleocr.py${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}3. Run Quick OCR Test:${COLOR_NC}"
echo -e "${COLOR_CYAN}   paddleocr --image_dir test_receipt.jpg --use_angle_cls true --lang en --use_gpu false${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}4. Integrate into Nexus Bag Module:${COLOR_NC}"
echo -e "${COLOR_CYAN}   Update modules/bag/ocr.py to use PaddleOCR${COLOR_NC}"
echo -e "${COLOR_CYAN}   Process receipts with PaddleOCR instead of OpenAI Vision${COLOR_NC}"
echo ""
echo -e "${COLOR_YELLOW}Note: Virtual environment isolates PaddleOCR from system Python${COLOR_NC}"
echo -e "${COLOR_YELLOW}      This prevents conflicts and installation issues${COLOR_NC}"
