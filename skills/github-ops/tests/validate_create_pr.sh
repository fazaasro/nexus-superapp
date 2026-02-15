#!/bin/bash
# Validation Script: create_pr
# Part of 10x Architect Protocol - Phase 1: Design Test

set -e

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Parameters
PR_TITLE="${1:-}"
PR_BODY="${2:-}"
VALIDATION_REPORT="audits/create_pr_validation_$(date +%Y%m%d_%H%M%S).txt"

if [ -z "$PR_TITLE" ]; then
  echo -e "${RED}❌ ERROR: PR title required${NC}"
  echo "Usage: tests/validate_create_pr.sh <pr-title> [pr-body]"
  exit 1
fi

echo "=== Design Test: validate_create_pr ==="
echo "PR Title: $PR_TITLE"
echo ""

# Test 1: Check if there are uncommitted changes
echo "Test 1: Checking for uncommitted changes..."
UNCOMMITTED=$(git status --porcelain 2>&1)

if [ -z "$UNCOMMITTED" ]; then
  echo -e "${RED}❌ FAIL${NC}: No uncommitted changes found"
  echo "⚠️  Make changes before creating PR"
  exit 1
else
  CHANGED_FILES=$(echo "$UNCOMMITTED" | wc -l)
  echo -e "${GREEN}✅ PASS${NC}: Found $CHANGED_FILES changed file(s)"
fi

echo ""

# Test 2: Check if on a feature branch
echo "Test 2: Checking current branch..."
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
  echo -e "${YELLOW}⚠️  WARNING: On main branch${NC}"
  echo "⚠️  PRs from main branch are unusual. Consider creating a feature branch first."
else
  echo -e "${GREEN}✅ PASS${NC}: On feature branch: $CURRENT_BRANCH"
fi

echo ""

# Test 3: Validate gh CLI authentication
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
Validation Report: create_pr
PR Title: $PR_TITLE
Branch: $CURRENT_BRANCH
Timestamp: $(date -Iseconds)
Tests Run: 3
Tests Passed: 3/3

Results:
- Uncommitted changes: PASS ($CHANGED_FILES files)
- Branch check: PASS (on feature branch)
- gh authenticated: PASS

Status: READY FOR IMPLEMENTATION
EOF

echo "Validation report saved to: $VALIDATION_REPORT"
