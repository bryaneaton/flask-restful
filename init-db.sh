#!/bin/bash
# Database initialization script

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Activate venv if it exists
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
fi

# Detect Python command
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}[ERROR]${NC} Python not found."
    exit 1
fi

# Parse arguments
USE_SQLITE=false
DROP_EXISTING=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --sqlite)
            USE_SQLITE=true
            shift
            ;;
        --drop)
            DROP_EXISTING=true
            shift
            ;;
        --help)
            cat << EOF
${GREEN}Database Initialization Script${NC}

Usage: $0 [OPTIONS]

Options:
    --sqlite        Use SQLite instead of PostgreSQL
    --drop          Drop existing tables before creating (CAUTION!)
    --help          Show this help message

Examples:
    # Initialize PostgreSQL database (default)
    $0

    # Initialize SQLite database
    $0 --sqlite

    # Drop and recreate all tables (WARNING: deletes all data!)
    $0 --drop

EOF
            exit 0
            ;;
        *)
            echo -e "${RED}[ERROR]${NC} Unknown option: $1"
            exit 1
            ;;
    esac
done

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Database Initialization Script      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Set database URL
if [ "$USE_SQLITE" = true ]; then
    export DATABASE_URL="sqlite:///data.db"
    echo -e "${BLUE}[INFO]${NC} Using SQLite database: data.db"
else
    echo -e "${BLUE}[INFO]${NC} Using PostgreSQL (from config.py)"
fi

# Create initialization Python script
INIT_SCRIPT=$(cat <<'PYTHON_EOF'
import sys
sys.path.insert(0, '.')

from app.app import app
from app.db import db
from app.models.user import UserModel
from app.models.store import StoreModel
from app.models.item import ItemModel

with app.app_context():
    if DROP_EXISTING:
        print("⚠️  Dropping all existing tables...")
        db.drop_all()
        print("✓ Tables dropped")

    print("Creating database tables...")
    db.create_all()
    print("✓ Tables created successfully")

    # Check what tables exist
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"\n✓ Database initialized with {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
PYTHON_EOF
)

# Run initialization
if [ "$DROP_EXISTING" = true ]; then
    echo -e "${YELLOW}[WARNING]${NC} --drop flag specified. This will DELETE ALL DATA!"
    read -p "Are you sure you want to continue? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "Aborted."
        exit 0
    fi
    echo "$INIT_SCRIPT" | DROP_EXISTING=true $PYTHON_CMD
else
    echo "$INIT_SCRIPT" | DROP_EXISTING=false $PYTHON_CMD
fi

echo ""
echo -e "${GREEN}✓ Database initialization complete!${NC}"
echo ""
