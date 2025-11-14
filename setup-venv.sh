#!/bin/bash
# Virtual Environment Setup Helper

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

VENV_DIR="venv"

echo -e "${GREEN}Flask RESTful API - Virtual Environment Setup${NC}"
echo ""

# Check if venv exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Virtual environment already exists at: $VENV_DIR${NC}"
    echo ""
    echo "To activate it, run:"
    echo -e "${BLUE}  source $VENV_DIR/bin/activate${NC}"
    echo ""
    echo "To recreate it, first remove the existing one:"
    echo "  rm -rf $VENV_DIR"
    echo "  $0"
    exit 0
fi

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv $VENV_DIR

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create virtual environment${NC}"
    echo "Make sure python3-venv is installed:"
    echo "  sudo apt-get install python3-venv  # Ubuntu/Debian"
    echo "  sudo yum install python3-venv      # CentOS/RHEL"
    exit 1
fi

echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

# Activate and install dependencies
echo -e "${BLUE}Activating virtual environment and installing dependencies...${NC}"
source $VENV_DIR/bin/activate

pip install --upgrade pip
pip install -r app/requirements.txt

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "Virtual environment is now activated for this session."
echo ""
echo "To activate it in the future, run:"
echo -e "${BLUE}  source $VENV_DIR/bin/activate${NC}"
echo ""
echo "To deactivate when done:"
echo -e "${BLUE}  deactivate${NC}"
echo ""
echo "Now you can start the server:"
echo -e "${BLUE}  ./run.sh --sqlite${NC}"
