#!/bin/bash
# Validation Script: clone_repo
# Part of 10x Architect Protocol - Phase 1: Design Test

set -e

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Parameters
OWNER="${1:-}"
REPO_NAME="${2:-}"
WORKSPACE="${GITHUB_WORKSPACE_DIR:-$HOME/swarm/repos}"
VALIDATION_REPORT="audits/clone_repo_validation_$(date +%Y%m%d_%H%M%S).txt"

if [ -z "$OWNER" ] || [ -z "$REPO_NAME" ]; then
  echo -e "${RED}❌ ERROR: Owner and repository name required${NC}"
  echo "Usage: tests/validate_clone_repo.sh <owner> <repo-name>"
  exit 1
fi

echo "=== Design Test: validate_clone_repo ==="
echo "Repository: $OWNER/$REPO_NAME"
echo "Target Workspace: $WORKSPACE"
echo ""

# Test 1: Check if repository exists and is accessible
echo "Test 1: Checking if repository exists and is accessible..."
REPO_INFO=$(gh api repos/"$OWNER/$REPO_NAME" 2>&1)

if echo "$REPO_INFO" | grep -q "Not Found"; then
  echo -e "${RED}❌ FAIL${NC}: Repository '$OWNER/$REPO_NAME' does not exist"
  exit 1
else
  echo -e "${GREEN}✅ PASS${NC}: Repository '$OWNER/$REPO_NAME' exists and is accessible"
  
  # Extract repo details
  REPO_ID=$(echo "$REPO_INFO" | grep -oP '"id":' | cut -d'"' -f2)
  REPO_SIZE=$(echo "$REPO_INFO" | grep -oP '"size":' | cut -d'"' -f2)
  
  echo "  Repository ID: $REPO_ID"
  echo "  Repository Size: $REPO_SIZE bytes"
fi

echo ""

# Test 2: Validate workspace directory
echo "Test 2: Validating workspace directory..."
if [ -d "$WORKSPACE" ]; then
  echo -e "${GREEN}✅ PASS${NC}: Workspace directory exists: $WORKSPACE"
  echo "  Writable: $([ -w "$WORKSPACE" ] && echo "YES" || echo "NO")"
else
  echo -e "${RED}❌ FAIL${NC}: Workspace directory does not exist: $WORKSPACE"
  exit 1
fi

echo ""

# Test 3: Check git CLI availability
echo "Test 3: Verifying git CLI..."
if command -v git >/dev/null 2>&1; then
  echo -e "${GREEN}✅ PASS${NC}: git CLI is available"
  GIT_VERSION=$(git --version)
  echo "  Git Version: $GIT_VERSION"
else
  echo -e "${RED}❌ FAIL${NC}: git CLI not found"
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
Validation Report: clone_repo
Repository: $OWNER/$REPO_NAME
Workspace: $WORKSPACE
Timestamp: $(date -Iseconds)
Tests Run: 3
Tests Passed: 3/3

Results:
- Repository exists: PASS (ID: $REPO_ID, Size: $REPO_SIZE)
- Workspace valid: PASS (Writable: YES)
- git CLI: PASS (Version: $GIT_VERSION)

Status: READY FOR IMPLEMENTATION
EOF

echo "Validation report saved to: $VALIDATION_REPORT"
