#!/bin/bash
# ========================================================================
# PaddleOCR Installation Script for Nexus
# ========================================================================
# Author: Levy (Agent Faza)
# Date: 2026-02-17
# 
# This script sets up PaddleOCR using a virtual environment.
# Run this script with: sudo bash setup_paddleocr.sh
# ========================================================================

set -e  # Exit on error

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

# Step 1: Create and Activate Virtual Environment
print_header "Step 1: Create and Activate Virtual Environment"

# Check if venv is available
if ! command -v python3-venv &> /dev/null; then
    print_info "python3-venv not found, trying with python3 -m venv..."
    python3 -m venv paddle_env || {
        print_error "Failed to create virtual environment with python3 -m venv"
        exit 1
    }
else
    python3-venv paddle_env || {
        print_error "Failed to create virtual environment with python3-venv"
        exit 1
    }
fi

print_success "Virtual environment 'paddle_env' created"
print_info "To activate in your terminal: source paddle_env/bin/activate"
print_info "You will see (paddle_env) in your prompt"

# Step 2: Install System Dependencies (ffmpeg, libsm6, etc.)
print_header "Step 2: Install System Dependencies"

apt-get update -qq
apt-get install -y ffmpeg libsm6 libxext6 libxrender1 libgl1-mesa-glx \
    libglib2.0-0 libgthread-2.0-0 libgomp1 libfontconfig1 libgbm1 \
    > /dev/null 2>&1

print_success "System dependencies installed"

# Step 3: Activate Virtual Environment and Install PaddlePaddle (CPU)
print_header "Step 3: Activate Virtual Environment and Install PaddlePaddle (CPU)"

# Activate the virtual environment
source paddle_env/bin/activate || {
    print_error "Failed to activate virtual environment"
    exit 1
}

print_success "Virtual environment activated (you should see (paddle_env) in prompt)"

# Upgrade pip inside the virtual environment
print_info "Upgrading pip inside virtual environment..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install PaddlePaddle (CPU version, defaults to CPU if no GPU dependencies found)
print_info "Installing PaddlePaddle (CPU)..."
pip install paddlepaddle-cpu > /dev/null 2>&1

print_success "PaddlePaddle installed"

# Step 4: Install PaddleOCR
print_header "Step 4: Install PaddleOCR"

print_info "Installing PaddleOCR..."
pip install "paddleocr>=2.0.1" > /dev/null 2>&1

print_success "PaddleOCR installed"

# Deactivate virtual environment
deactivate
print_info "Virtual environment deactivated"

# Step 5: Verify Installation
print_header "Step 5: Verify PaddlePaddle Installation"

print_info "Running verification tests..."
python3 paddle_env/bin/python -c "
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

# Step 6: Clean Up Old Containers
print_header "Step 6: Clean Up Old Containers"

docker stop tesseract easyocr 2>/dev/null || true
docker rm tesseract easyocr 2>/dev/null || true

print_success "Old containers removed"

# Step 7: Test PaddleOCR CLI
print_header "Step 7: Test PaddleOCR CLI"

print_info "To test PaddleOCR with a sample image:"
echo ""
echo -e "${COLOR_GREEN}paddleocr --image_dir ./your_test_image.jpg --use_angle_cls true --lang en --use_gpu false${COLOR_NC}"
echo ""
echo -e "${COLOR_YELLOW}Note: You need to activate the virtual environment first:${COLOR_NC}"
echo -e "${COLOR_CYAN}source paddle_env/bin/activate${COLOR_NC}"
echo ""

# Step 8: Create Test Script
print_header "Step 8: Create Test Script"

cat > test_paddleocr.py << 'EOF'
#!/usr/bin/env python3
"""Test PaddleOCR with a sample image."""

from PIL import Image, ImageDraw, ImageFont
import base64
import sys
import os

def create_test_image():
    """Create a test receipt image."""
    print("Creating test receipt image...")
    
    try:
        img = Image.new('RGB', (600, 800), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        y = 50
        
        # Merchant
        draw.text((50, y), "SUPERMARKET", fill='black', font=font)
        y += 40
        
        # Date
        from datetime import datetime
        draw.text((50, y), datetime.now().strftime("%Y-%m-%d %H:%M"), fill='black', font=font)
        y += 40
        
        # Items
        draw.text((50, y), "1. MILK 1L", fill='black', font=font)
        y += 30
        draw.text((450, y), "$2.99", fill='black', font=font)
        y += 40
        
        draw.text((50, y), "2. BREAD", fill='black', font=font)
        y += 30
        draw.text((450, y), "$1.50", fill='black', font=font)
        y += 40
        
        # Separator
        draw.line([(50, y), (550, y)], fill='gray', width=2)
        y += 50
        
        # Total
        draw.text((50, y), "TOTAL", fill='black', font=font)
        y += 30
        draw.text((450, y), "$4.49", fill='black', font=font)
        
        test_path = "/tmp/test_receipt.jpg"
        img.save(test_path, "JPEG", quality=95)
        
        print(f"Test image created: {test_path}")
        return test_path
        
    except ImportError:
        print("PIL not available. Skipping image generation.")
        return None
    except Exception as e:
        print(f"Failed to create test image: {e}")
        return None

def test_ocr(image_path):
    """Test OCR with PaddleOCR."""
    print("Testing OCR with PaddleOCR...")
    
    try:
        from paddleocr import PaddleOCR
        
        # Initialize PaddleOCR (CPU)
        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
        print("PaddleOCR initialized (use_angle_cls=True, lang='en', use_gpu=False)")
        
        # Read image
        if not os.path.exists(image_path):
            print(f"Error: Image file not found: {image_path}")
            return
        
        # Run OCR
        result = ocr.ocr(image_path, cls=True)
        
        # Display results
        print("\n" + "="*70)
        print("OCR Results:")
        print("="*70)
        
        if result:
            print(f"Detected {len(result)} regions")
            
            for i, line in enumerate(result):
                if len(line) > 0:
                    text = line[0][1] if len(line[0]) > 1 else ""
                    confidence = line[0][2] if len(line[0]) > 2 else 0
                    print(f"{i+1}. Text: \"{text}\" (Confidence: {confidence:.2f})")
                else:
                    print(f"{i+1}. Empty region")
            
            print("\n" + "="*70)
            print("✅ PaddleOCR Test Complete!")
            print("="*70)
        else:
            print("No text detected")
            
    except ImportError:
        print("Error: PaddleOCR not installed")
        print("Please install with: pip install paddleocr")
    except Exception as e:
        print(f"Error during OCR: {e}")

if __name__ == "__main__":
    print("="*70)
    print("PaddleOCR Test Script")
    print("="*70)
    
    # Create test image
    test_image = create_test_image()
    
    if test_image:
        # Test OCR
        test_ocr(test_image)
    else:
        print("Skipping OCR test (no test image)")
EOF

print_success "Test script created: test_paddleocr.py"

# Final Summary
echo ""
echo -e "${COLOR_GREEN}=======================================================================${COLOR_NC}"
echo -e "${COLOR_GREEN}✅ PaddleOCR Installation Complete!${COLOR_NC}"
echo -e "${COLOR_GREEN}=======================================================================${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}🚀 What's Next:${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}1. Activate Virtual Environment:${COLOR_NC}"
echo -e "${COLOR_CYAN}   source paddle_env/bin/activate${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}2. Test PaddleOCR CLI:${COLOR_NC}"
echo -e "${COLOR_CYAN}   paddleocr --image_dir test_receipt.jpg --use_angle_cls true --lang en --use_gpu false${COLOR_NC}"
echo ""
echo -e "${COLOR_CYAN}3. Run Test Script:${COLOR_NC}"
echo -e "${COLOR_CYAN}   source paddle_env/bin/activate${COLOR_NC}"
echo -e "${COLOR_CYAN}   python3 test_paddleocr.py${COLOR_NC}"
echo ""
echo -e "${COLOR_YELLOW}⚠️  Note: Virtual environment isolates PaddleOCR from system Python${COLOR_NC}"
echo -e "${COLOR_YELLOW}   This prevents conflicts and installation issues${COLOR_NC}"
echo ""
