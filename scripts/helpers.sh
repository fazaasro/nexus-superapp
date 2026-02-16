#!/bin/bash
# Main helper script loader for Levy

# Source all helper scripts
source ~/.openclaw/workspace/scripts/gh-helpers.sh
source ~/.openclaw/workspace/scripts/cf-helpers.sh
source ~/.openclaw/workspace/scripts/docker-helpers.sh

# Main help function
levy-help() {
    echo "=== Levy's Helper Commands ==="
    echo ""
    echo "GitHub (gh-*)"
    echo "  gh-check      - Check GitHub auth status"
    echo "  gh-repos      - List repositories"
    echo "  gh-new        - Create new repository"
    echo "  gh-pr         - Create pull request"
    echo "  gh-issues     - List issues"
    echo ""
    echo "Cloudflare (cf-*)"
    echo "  cf-tunnels    - List all tunnels"
    echo "  cf-info       - Show tunnel info"
    echo "  cf-route      - Create DNS route"
    echo "  cf-new        - Create new tunnel"
    echo "  cf-test       - Test URL"
    echo "  cf-restart    - Restart cloudflared"
    echo ""
    echo "Docker (docker-*)"
    echo "  docker-running - List running containers"
    echo "  docker-all    - List all containers"
    echo "  docker-log    - View container logs"
    echo "  docker-follow - Follow logs"
    echo "  docker-restart- Restart container"
    echo "  docker-exec   - Execute in container"
    echo "  docker-stats  - Show container stats"
    echo "  docker-cleanup- Remove unused resources"
    echo "  docker-check  - Check AAC service status"
    echo "  docker-restart-all - Restart all AAC services"
    echo ""
    echo "Other"
    echo "  levy-help     - Show this help"
}

# Auto-load helpers if running interactively
if [[ $- == *i* ]]; then
    levy-help
fi
