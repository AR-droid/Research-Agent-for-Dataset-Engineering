#!/usr/bin/env bash
set -e

# Setup formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up ARES development environment...${NC}\n"

# 1. Check for required dependencies
check_dep() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: $1 is required but not installed.${NC}"
        echo "$2"
        exit 1
    fi
}

echo "Checking dependencies..."
check_dep "docker" "Please install Docker: https://docs.docker.com/get-docker/"
check_dep "docker-compose" "Please install Docker Compose: https://docs.docker.com/compose/install/"
check_dep "python3" "Please install Python 3.12+: https://www.python.org/downloads/"
check_dep "node" "Please install Node 20+: https://nodejs.org/"

# Validate versions roughly
PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
NODE_VERSION=$(node -v)

echo "Found Docker, Python $PYTHON_VERSION, Node $NODE_VERSION"

# 2. Setup environment variables
cd "$(dirname "$0")/.."
INFRA_DIR=$(pwd)
ROOT_DIR=$(dirname "$INFRA_DIR")

if [ ! -f "$INFRA_DIR/.env" ]; then
    echo -e "\n${YELLOW}Copying .env.example to .env...${NC}"
    cp "$INFRA_DIR/.env.example" "$INFRA_DIR/.env"
    echo -e "${GREEN}Created .env file. Please update it with your actual API keys later.${NC}"
else
    echo -e "\n${GREEN}.env file already exists.${NC}"
fi

# 3. Start infrastructure services
echo -e "\n${YELLOW}Starting infrastructure services (postgres, redis, minio)...${NC}"
docker-compose up -d postgres redis minio

# 4. Wait for PostgreSQL to be ready
echo -e "\n${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
until docker exec $(docker-compose ps -q postgres) pg_isready -U ares -d ares > /dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo -e "\n${GREEN}PostgreSQL is ready!${NC}"

# Success message
echo -e "\n${GREEN}==============================================${NC}"
echo -e "${GREEN}🎉 Infrastructure setup complete!${NC}"
echo -e "${GREEN}==============================================${NC}"
echo -e "Next steps:"
echo -e "1. Run ${YELLOW}make db-migrate${NC} to apply migrations."
echo -e "2. Run ${YELLOW}make dev${NC} to start all application services."
echo -e "3. Open ${YELLOW}http://localhost:3000${NC} for the frontend."
echo -e "4. Open ${YELLOW}http://localhost:8000/docs${NC} for API documentation."
