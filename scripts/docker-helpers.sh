#!/bin/bash
# Docker helper functions for Levy

# List all running containers
docker-running() {
    docker ps
}

# List all containers (including stopped)
docker-all() {
    docker ps -a
}

# View container logs
docker-log() {
    local container=$1
    local lines=${2:-100}
    
    if [ -z "$container" ]; then
        echo "Usage: docker-log <container-name> [lines]"
        return 1
    fi
    
    docker logs --tail "$lines" "$container"
}

# Follow container logs
docker-follow() {
    local container=$1
    
    if [ -z "$container" ]; then
        echo "Usage: docker-follow <container-name>"
        return 1
    fi
    
    docker logs -f "$container"
}

# Restart container
docker-restart() {
    local container=$1
    
    if [ -z "$container" ]; then
        echo "Usage: docker-restart <container-name>"
        return 1
    fi
    
    docker restart "$container"
    docker ps | grep "$container"
}

# Execute command in container
docker-exec() {
    local container=$1
    local command=${2:-"sh"}
    
    if [ -z "$container" ]; then
        echo "Usage: docker-exec <container-name> [command]"
        return 1
    fi
    
    docker exec -it "$container" "$command"
}

# Show container stats
docker-stats() {
    docker stats --no-stream
}

# Clean up unused images and containers
docker-cleanup() {
    echo "Removing stopped containers..."
    docker container prune -f
    
    echo "Removing unused images..."
    docker image prune -a -f
    
    echo "Cleanup complete!"
}

# Check service status (AAC stack)
docker-check() {
    echo "=== AAC Services Status ==="
    echo ""
    
    for service in portainer n8n qdrant code-server overseer; do
        status=$(docker ps --format "{{.Names}}" | grep -c "^$service$" || echo "0")
        if [ "$status" -gt 0 ]; then
            echo "✅ $service: running"
        else
            echo "❌ $service: stopped"
        fi
    done
    
    echo ""
    echo "Total running: $(docker ps | wc -l)"
}

# Restart all AAC services
docker-restart-all() {
    echo "Restarting all AAC services..."
    cd ~/stack
    docker compose restart
    echo "Done!"
}
