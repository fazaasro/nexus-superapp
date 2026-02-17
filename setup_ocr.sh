#!/bin/bash
# ========================================================================
# OCR Installation Script for Nexus
# ========================================================================
# Author: Levy (Agent Faza)
# Date: 2026-02-17
# 
# This script sets up OCR capability on the VPS.
# Run this script with: sudo bash setup_ocr.sh
# ========================================================================

set -e  # Exit on error

COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_YELLOW='\033[1;33m'
COLOR_NC='\033[0m' # No Color

echo -e "${COLOR_GREEN}=======================================================================${COLOR_NC}"
echo -e "${COLOR_GREEN}Nexus OCR Installation Script${COLOR_NC}"
echo -e "${COLOR_GREEN}=======================================================================${COLOR_NC}"
echo ""

# Function to print section headers
print_header() {
    echo ""
    echo -e "${COLOR_YELLOW}━━━ $1 ━━━${COLOR_NC}"
    echo ""
}

# Step 1: Install Python package manager
print_header "Step 1: Installing python3-pip"

apt-get update -qq
apt-get install -y python3-pip python3-pil > /dev/null 2>&1

echo -e "${COLOR_GREEN}✅ python3-pip installed${COLOR_NC}"

# Step 2: Install EasyOCR (native)
print_header "Step 2: Installing EasyOCR (Native, No Docker)"

pip3 install easyocr > /dev/null 2>&1

echo -e "${COLOR_GREEN}✅ EasyOCR installed successfully${COLOR_NC}"

# Step 3: Verify installation
print_header "Step 3: Verifying EasyOCR Installation"

python3 -c "
import easyocr
print(f'✅ EasyOCR version: {easyocr.__version__}')
print('✅ EasyOCR import successful')
"

# Step 4: Clean up old containers
print_header "Step 4: Cleaning Up Old OCR Containers"

echo "Stopping and removing old containers..."
docker stop tesseract easyocr 2>/dev/null || true
docker rm tesseract easyocr 2>/dev/null || true

echo -e "${COLOR_GREEN}✅ Old containers removed${COLOR_NC}"

# Step 5: Update docker-compose.yml (remove OCR services)
print_header "Step 5: Updating docker-compose.yml"

COMPOSE_FILE="/home/ai-dev/stack/docker-compose.yml"

if [ -f "$COMPOSE_FILE" ]; then
    # Create backup
    cp "$COMPOSE_FILE" "${COMPOSE_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    
    # Remove EasyOCR and Tesseract sections
    sed -i '/easyocr:/,/d' "$COMPOSE_FILE"
    sed -i '/tesseract:/,/d' "$COMPOSE_FILE"
    
    echo -e "${COLOR_GREEN}✅ docker-compose.yml cleaned${COLOR_NC}"
else
    echo -e "${COLOR_RED}❌ docker-compose.yml not found${COLOR_NC}"
fi

# Step 6: Test EasyOCR
print_header "Step 6: Testing EasyOCR (Native)"

python3 << 'EOF'
import easyocr
import sys

try:
    print("Initializing EasyOCR reader...")
    reader = easyocr.Reader(['en'], gpu=False)
    print("✅ EasyOCR reader initialized successfully!")
    print("")
    print("📊 EasyOCR is ready to use!")
    print("")
    print("Usage:")
    print("  import easyocr")
    print("  reader = easyocr.Reader(['en'], gpu=False)")
    print("  result = reader.readtext('receipt.jpg')")
    print("  text = result[0][1]  # Extracted text")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${COLOR_GREEN}=======================================================================${COLOR_NC}"
    echo -e "${COLOR_GREEN}✅ EasyOCR Installation Complete!${COLOR_NC}"
    echo -e "${COLOR_GREEN}=======================================================================${COLOR_NC}"
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Update Nexus OCR module to use native EasyOCR:"
    echo "      from easyocr import Reader"
    echo "      reader = Reader(['en'], gpu=False)"
    echo ""
    echo "   2. Test OCR with receipt images"
    echo "      python3 /home/ai-dev/.openclaw/workspace/test_ocr_native.py"
    echo ""
    echo "   3. Send OCR text to GLM-4 for interpretation"
    echo "      python3 /home/ai-dev/.openclaw/workspace/modules/bag/service.py"
    echo ""
else
    echo ""
    echo -e "${COLOR_RED}=======================================================================${COLOR_NC}"
    echo -e "${COLOR_RED}❌ Installation Failed${COLOR_NC}"
    echo -e "${COLOR_RED}=======================================================================${COLOR_NC}"
    echo ""
    echo "Please check the errors above and run again."
    exit 1
fi
