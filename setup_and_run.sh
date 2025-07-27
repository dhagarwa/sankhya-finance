#!/bin/bash

# Sankhya Finance - Setup and Run Script
# This script will create a fresh conda environment and run the application

set -e  # Exit on any error

echo "🚀 SANKHYA FINANCE - Setup and Run"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ENV_NAME="sankhya-finance-env"

echo -e "${BLUE}📋 Step 1: Checking for existing environment...${NC}"
if conda env list | grep -q "$ENV_NAME"; then
    echo -e "${YELLOW}⚠️  Found existing environment '$ENV_NAME'. Removing it...${NC}"
    conda env remove -n "$ENV_NAME" -y
    echo -e "${GREEN}✅ Removed existing environment${NC}"
else
    echo -e "${GREEN}✅ No existing environment found${NC}"
fi

echo -e "${BLUE}📋 Step 2: Creating new conda environment...${NC}"
conda create -n "$ENV_NAME" python=3.10 -y
echo -e "${GREEN}✅ Created new environment '$ENV_NAME'${NC}"

echo -e "${BLUE}📋 Step 3: Activating environment and installing dependencies...${NC}"
# Activate environment and install dependencies
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
echo -e "${GREEN}✅ Activated environment '$ENV_NAME'${NC}"

echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed successfully${NC}"

echo -e "${BLUE}📋 Step 4: Setting up environment variables...${NC}"
if [ ! -f .env ]; then
    if [ -f env.example ]; then
        cp env.example .env
        echo -e "${YELLOW}⚠️  Created .env file from env.example${NC}"
        echo -e "${YELLOW}    Please edit .env with your actual API keys for full functionality${NC}"
    else
        echo -e "${RED}❌ No env.example file found${NC}"
    fi
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

echo -e "${BLUE}📋 Step 5: Running Sankhya Finance...${NC}"
echo "=================================="
echo ""

# Run the application
python src/main.py

echo ""
echo -e "${GREEN}🎉 Sankhya Finance session completed!${NC}"
echo -e "${BLUE}To run again manually:${NC}"
echo -e "  conda activate $ENV_NAME"
echo -e "  python src/main.py"
echo "" 