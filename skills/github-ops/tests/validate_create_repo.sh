#!/bin/bash
# Validation Script: create_repo
# Part of 10x Architect Protocol - Phase 1: Design Test

set -e

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Parameters
REPO_NAME="${1:-}"
VALIDATION_REPORT="audits/create_repo_validation_$(date +%Y%m%d_%H%M%S).txt"

if [ -z "$REPO_NAME" ]; then
  echo -e "${RED}❌ ERROR: Repository name required${NC}"
  echo "Usage: tests/validate_create_repo.sh <repo-name>"
  exit 1
fi

echo "=== Design Test: validate_create_repo ==="
echo "Repository: $REPO_NAME"
echo ""

# Test 1: Check if repository exists
echo "Test 1: Checking if repository already exists..."
REPO_EXISTS=$(gh repo view "$REPO_NAME" 2>&1)

if echo "$REPO_EXISTS" | grep -q "not found"; then
  echo -e "${GREEN}✅ PASS${NC}: Repository '$REPO_NAME' does not exist"
else
  echo -e "${RED}❌ FAIL${NC}: Repository '$REPO_NAME' already exists"
  echo "⚠️  Use 'clone_repo fazaasro $REPO_NAME' instead"
  exit 1
fi

echo ""

# Test 2: Validate repository name format
echo "Test 2: Validating repository name format..."
if [[ "$REPO_NAME" =~ ^[a-z0-9][a-z0-9_-]*$ ]]; then
  echo -e "${GREEN}✅ PASS${NC}: Repository name format is valid"
else
  echo -e "${RED}❌ FAIL${NC}: Repository name contains invalid characters"
  exit 1
fi

echo ""

# Test 3: Check gh CLI authentication
echo "Test 3: Verifying gh CLI authentication..."
if gh auth status 2>&1 | grep -q "Logged in"; then
  echo -e "${GREEN}✅ PASS${NC}: gh CLI is authenticated"
else
  echo -e "${RED}❌ FAIL${NC}: gh CLI not authenticated"
  echo "Run: gh auth login"
  exit 1
fi

echo ""

echo "=== Design Test Complete ==="
echo ""
echo "All tests passed. Proceeding to implementation phase."
echo ""

# Write validation report
mkdir -p "$(dirname "$VALIDATION_REPORT")"
cat > "$VALIDATION_REPORT" << EOF
Validation Report: create_repo
Repository: $REPO_NAME
Timestamp: $(date -Iseconds)
Tests Run: 3
Tests Passed: 3/3

Results:
- Repository exists: PASS
- Name format: PASS
- gh authenticated: PASS

Status: READY FOR IMPLEMENTATION
EOF

echo "Validation report saved to: $VALIDATION_REPORT"
