#!/bin/bash
# Flask RESTful API Server Startup Script

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
PORT=5000
HOST="0.0.0.0"
DEBUG="true"
USE_SQLITE=false

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"

# Check for local venv and activate if needed
if [ -d "$VENV_DIR" ]; then
    if [ -z "$VIRTUAL_ENV" ]; then
        echo -e "${BLUE}[INFO]${NC} Activating local virtual environment: $VENV_DIR"
        source "$VENV_DIR/bin/activate"
    elif [ "$VIRTUAL_ENV" != "$VENV_DIR" ]; then
        echo -e "${YELLOW}[WARNING]${NC} Different venv is active: $VIRTUAL_ENV"
        echo -e "${BLUE}[INFO]${NC} Switching to local venv: $VENV_DIR"
        deactivate 2>/dev/null || true
        source "$VENV_DIR/bin/activate"
    fi
fi

# Detect Python command (works with venv)
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo -e "${RED}[ERROR]${NC} Python not found. Please install Python 3."
    exit 1
fi

# Detect pip command (works with venv)
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
elif command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
else
    PIP_CMD="$PYTHON_CMD -m pip"
fi

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
${GREEN}Flask RESTful API Server${NC}

Usage: $0 [OPTIONS]

Options:
    -p, --port PORT          Port to run on (default: 5000)
    -h, --host HOST          Host to bind to (default: 0.0.0.0)
    -d, --debug              Enable debug mode (default: enabled)
    -s, --sqlite             Use SQLite instead of PostgreSQL
    --install-deps           Install/update dependencies
    --run-tests              Run tests before starting
    --help                   Show this help message

Examples:
    # Start server with defaults (PostgreSQL, port 5000)
    $0

    # Start server with SQLite database
    $0 --sqlite

    # Start on different port
    $0 --port 8080

    # Install dependencies and start
    $0 --install-deps

    # Run tests then start server
    $0 --run-tests

    # Start with SQLite on port 8080
    $0 --sqlite --port 8080

Environment Variables:
    DATABASE_URL             Override database URL
    FLASK_ENV                Flask environment (development/production)
    LOGLEVEL                 Logging level (DEBUG/INFO/WARNING/ERROR)

EOF
    exit 0
}

# Function to check if we're in a virtual environment
check_venv() {
    if [ -n "$VIRTUAL_ENV" ]; then
        if [ "$VIRTUAL_ENV" = "$VENV_DIR" ]; then
            print_success "Using local virtual environment: venv/"
        else
            print_success "Using virtual environment: $VIRTUAL_ENV"
        fi
        return 0
    else
        print_warning "No virtual environment found in project root"
        print_info "Create one with: ./setup-venv.sh"
        print_info "Or manually: python3 -m venv venv && source venv/bin/activate"
        echo ""
        return 1
    fi
}

# Function to check if dependencies are installed
check_dependencies() {
    print_info "Checking dependencies..."

    if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
        print_warning "Flask not found. Installing dependencies..."
        install_dependencies
    else
        print_success "Dependencies are installed"
    fi
}

# Function to install dependencies
install_dependencies() {
    print_info "Installing dependencies from app/requirements.txt..."
    $PIP_CMD install -r app/requirements.txt --upgrade --quiet
    print_success "Dependencies installed successfully"
}

# Function to run tests
run_tests() {
    print_info "Running test suite..."
    if DATABASE_URL="sqlite:///:memory:" $PYTHON_CMD -m pytest tests/ -v --tb=short; then
        print_success "All tests passed!"
    else
        print_error "Tests failed. Aborting server start."
        exit 1
    fi
}

# Parse command line arguments
INSTALL_DEPS=false
RUN_TESTS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -h|--host)
            HOST="$2"
            shift 2
            ;;
        -d|--debug)
            DEBUG="true"
            shift
            ;;
        -s|--sqlite)
            USE_SQLITE=true
            shift
            ;;
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --run-tests)
            RUN_TESTS=true
            shift
            ;;
        --help)
            show_usage
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Print banner
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Flask RESTful API Server Starter    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check virtual environment
check_venv

# Show Python info
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
print_info "Using: $PYTHON_VERSION"
echo ""

# Install dependencies if requested
if [ "$INSTALL_DEPS" = true ]; then
    install_dependencies
else
    check_dependencies
fi

# Run tests if requested
if [ "$RUN_TESTS" = true ]; then
    run_tests
fi

# Configure database
if [ "$USE_SQLITE" = true ]; then
    export DATABASE_URL="sqlite:///data.db"
    print_info "Using SQLite database: data.db"
else
    if [ -z "$DATABASE_URL" ]; then
        print_warning "Using PostgreSQL (make sure it's running)"
        print_info "PostgreSQL config: postgres:magical_password@0.0.0.0/db"
        print_info "To use SQLite instead, run with --sqlite flag"
    else
        print_info "Using custom DATABASE_URL: $DATABASE_URL"
    fi
fi

# Print server configuration
echo ""
print_info "Server Configuration:"
echo "  Host:     $HOST"
echo "  Port:     $PORT"
echo "  Debug:    $DEBUG"
echo "  Database: ${DATABASE_URL:-PostgreSQL (from config.py)}"
echo ""

print_info "Starting Flask server..."
echo ""

# Export Flask environment variables
export FLASK_APP=app/app.py
if [ "$DEBUG" = "true" ]; then
    export FLASK_ENV=development
    export FLASK_DEBUG=1
else
    export FLASK_ENV=production
    export FLASK_DEBUG=0
fi

# Start the server
print_success "Server is running on http://$HOST:$PORT"
print_info "Press Ctrl+C to stop the server"
echo ""
print_info "Available endpoints:"
echo "  POST   /register           - Register new user"
echo "  POST   /user               - Login (get JWT token)"
echo "  GET    /user               - Get current user info (requires auth)"
echo "  POST   /store/<name>       - Create store (requires auth)"
echo "  GET    /store/<name>       - Get store details"
echo "  DELETE /store/<name>       - Delete store (requires auth)"
echo "  GET    /stores             - List all stores"
echo "  POST   /item/<name>        - Create item (requires auth)"
echo "  GET    /item/<name>        - Get item details (requires auth)"
echo "  PUT    /item/<name>        - Update/create item (requires auth)"
echo "  DELETE /item/<name>        - Delete item (requires auth)"
echo "  GET    /items              - List all items (requires auth)"
echo ""
echo -e "${YELLOW}────────────────────────────────────────${NC}"
echo ""

# Run the Flask application
cd "$SCRIPT_DIR"
$PYTHON_CMD -m flask run --host="$HOST" --port="$PORT"
