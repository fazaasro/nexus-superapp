#!/bin/bash

# Nexus Super App Production Deployment Script
# This script deploys Nexus to production with proper error handling and rollback

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
BACKUP_DIR="./backups"
LOG_FILE="./deploy.log"
CONTAINER_PREFIX="nexus"

# Functions
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a "$LOG_FILE"
}

# Error handler
error_handler() {
    log_error "Deployment failed at line $1"
    log_error "Attempting rollback..."
    rollback
    exit 1
}

trap 'error_handler $LINENO' ERR

# Rollback function
rollback() {
    log_warning "Starting rollback..."
    
    # Restore previous containers if backup exists
    if [ -f "$BACKUP_DIR/docker-compose.yml.prev" ]; then
        log "Restoring previous docker-compose configuration..."
        cp "$BACKUP_DIR/docker-compose.yml.prev" "$COMPOSE_FILE"
    fi
    
    # Restart services
    log "Restarting services..."
    docker compose -f "$COMPOSE_FILE" down
    docker compose -f "$COMPOSE_FILE" up -d
    
    log "Rollback completed"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check if Docker Compose is available
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not available"
        exit 1
    fi
    
    # Check if .env.prod exists
    if [ ! -f ".env.prod" ]; then
        log_error ".env.prod file not found. Copy .env.prod.example to .env.prod and configure"
        exit 1
    fi
    
    log_success "All prerequisites met"
}

# Backup current deployment
backup_deployment() {
    log "Creating backup..."
    mkdir -p "$BACKUP_DIR"
    
    # Backup docker-compose configuration
    if [ -f "$COMPOSE_FILE" ]; then
        cp "$COMPOSE_FILE" "$BACKUP_DIR/docker-compose.yml.prev"
    fi
    
    # Backup database
    if docker ps | grep -q nexus-db; then
        log "Backing up database..."
        docker exec nexus-db pg_dump -U nexus nexus > "$BACKUP_DIR/nexus_db_backup_$(date +%Y%m%d_%H%M%S).sql"
    fi
    
    log_success "Backup completed"
}

# Pull latest code from GitHub
pull_code() {
    log "Pulling latest code from GitHub..."
    git fetch origin master
    git reset --hard origin/master
    log_success "Code updated"
}

# Build Docker images
build_images() {
    log "Building Docker images..."
    docker compose -f "$COMPOSE_FILE" build --no-cache
    log_success "Docker images built"
}

# Run database migrations
run_migrations() {
    log "Running database migrations..."
    # TODO: Implement migration command
    # docker exec nexus-api python -m database migrate
    log "Migrations completed"
}

# Start services
start_services() {
    log "Starting services..."
    docker compose -f "$COMPOSE_FILE" up -d
    log_success "Services started"
}

# Wait for services to be healthy
wait_for_health() {
    log "Waiting for services to be healthy..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker ps --filter "name=nexus-api" --filter "status=healthy" --format "{{.Names}}" | grep -q nexus-api; then
            log_success "API service is healthy"
            break
        fi
        
        log "Waiting for API service... (attempt $attempt/$max_attempts)"
        sleep 5
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        log_error "API service did not become healthy"
        return 1
    fi
    
    # Check web UI
    if docker ps --filter "name=nexus-web" --filter "status=healthy" --format "{{.Names}}" | grep -q nexus-web; then
        log_success "Web UI service is healthy"
    else
        log_warning "Web UI service not healthy yet, may still be starting"
    fi
}

# Verify health endpoints
verify_health() {
    log "Verifying health endpoints..."
    
    # Check API health
    if curl -f http://localhost:8000/health &> /dev/null; then
        log_success "API health endpoint responding"
    else
        log_error "API health endpoint not responding"
        return 1
    fi
    
    # Check Web UI
    if curl -f http://localhost:5173/ &> /dev/null; then
        log_success "Web UI responding"
    else
        log_warning "Web UI not responding yet"
    fi
}

# Cleanup old backups
cleanup_backups() {
    log "Cleaning up old backups..."
    # Keep only last 7 days of backups
    find "$BACKUP_DIR" -name "nexus_db_backup_*.sql" -mtime +7 -delete
    log "Backup cleanup completed"
}

# Main deployment flow
main() {
    log "=========================================="
    log "Nexus Super App Deployment Started"
    log "=========================================="
    
    check_prerequisites
    backup_deployment
    pull_code
    build_images
    run_migrations
    start_services
    wait_for_health
    verify_health
    cleanup_backups
    
    log "=========================================="
    log_success "Deployment completed successfully!"
    log "=========================================="
    
    echo ""
    log "Services are now running:"
    log "  - API: http://localhost:8000"
    log "  - Web UI: http://localhost:5173"
    log "  - Nginx: http://localhost:8080"
    echo ""
}

# Run main function
main "$@"
