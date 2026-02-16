#!/bin/bash
# GitHub helper functions for Levy

# List repositories
gh-repos() {
    gh repo list --limit 20
}

# Create new repository
gh-new() {
    local name=$1
    local private=${2:-true}
    
    if [ -z "$name" ]; then
        echo "Usage: gh-new <repo-name> [private|public]"
        return 1
    fi
    
    gh repo create "$name" --"$private" --clone
    cd "$name"
}

# Pull request from current branch
gh-pr() {
    local title=$1
    local body=${2:-""}
    
    gh pr create --title "$title" --body "$body"
}

# View issues
gh-issues() {
    local repo=${1:-.}
    gh issue list --repo "$repo" --limit 10
}

# Create issue
gh-issue() {
    local title=$1
    local body=${2:-""}
    gh issue create --title "$title" --body "$body"
}

# Check auth status
gh-check() {
    gh auth status
}

# Sync fork with upstream
gh-sync() {
    local upstream=$1
    
    if [ -z "$upstream" ]; then
        echo "Usage: gh-sync <upstream-repo>"
        return 1
    fi
    
    git fetch upstream main
    git checkout main
    git merge upstream/main
    git push
}
