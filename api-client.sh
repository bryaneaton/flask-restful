#!/bin/bash
# Flask RESTful API Client Helper Script

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Default server URL
SERVER="http://localhost:5000"
TOKEN=""

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_usage() {
    cat << EOF
${GREEN}Flask RESTful API Client${NC}

Usage: $0 <command> [options]

Commands:
    register <username> <password>          Register a new user
    login <username> <password>             Login and get JWT token
    get-user                                Get current user info (requires token)

    create-store <name>                     Create a store (requires token)
    get-store <name>                        Get store details
    delete-store <name>                     Delete store (requires token)
    list-stores                             List all stores

    create-item <name> <price> <store_id>   Create item (requires token)
    get-item <name>                         Get item details (requires token)
    update-item <name> <price> <store_id>   Update item (requires token)
    delete-item <name>                      Delete item (requires token)
    list-items                              List all items (requires token)

Options:
    --server URL        Server URL (default: http://localhost:5000)
    --token TOKEN       JWT token for authenticated requests
    --help              Show this help message

Examples:
    # Register a new user
    $0 register john password123

    # Login and save token
    TOKEN=\$($0 login john password123 | jq -r '.access_token')

    # Create a store (using saved token)
    $0 --token "\$TOKEN" create-store "My Store"

    # Create an item
    $0 --token "\$TOKEN" create-item "Laptop" 999.99 1

    # List all items
    $0 --token "\$TOKEN" list-items

EOF
    exit 0
}

make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local auth=$4

    if [ -n "$auth" ]; then
        if [ -n "$data" ]; then
            curl -s -X "$method" \
                 -H "Content-Type: application/json" \
                 -H "Authorization: Bearer $auth" \
                 -d "$data" \
                 "$SERVER$endpoint" | jq '.' 2>/dev/null || echo "Error: Invalid response"
        else
            curl -s -X "$method" \
                 -H "Content-Type: application/json" \
                 -H "Authorization: Bearer $auth" \
                 "$SERVER$endpoint" | jq '.' 2>/dev/null || echo "Error: Invalid response"
        fi
    else
        if [ -n "$data" ]; then
            curl -s -X "$method" \
                 -H "Content-Type: application/json" \
                 -d "$data" \
                 "$SERVER$endpoint" | jq '.' 2>/dev/null || echo "Error: Invalid response"
        else
            curl -s -X "$method" \
                 -H "Content-Type: application/json" \
                 "$SERVER$endpoint" | jq '.' 2>/dev/null || echo "Error: Invalid response"
        fi
    fi
}

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --server)
            SERVER="$2"
            shift 2
            ;;
        --token)
            TOKEN="$2"
            shift 2
            ;;
        --help)
            show_usage
            ;;
        register)
            if [ -z "$2" ] || [ -z "$3" ]; then
                print_error "Usage: $0 register <username> <password>"
                exit 1
            fi
            print_info "Registering user: $2"
            make_request POST "/register" "{\"username\":\"$2\",\"password\":\"$3\"}"
            exit 0
            ;;
        login)
            if [ -z "$2" ] || [ -z "$3" ]; then
                print_error "Usage: $0 login <username> <password>"
                exit 1
            fi
            print_info "Logging in as: $2"
            make_request POST "/user" "{\"username\":\"$2\",\"password\":\"$3\"}"
            exit 0
            ;;
        get-user)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token> or login first"
                exit 1
            fi
            print_info "Getting user info"
            make_request GET "/user" "" "$TOKEN"
            exit 0
            ;;
        create-store)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token>"
                exit 1
            fi
            if [ -z "$2" ]; then
                print_error "Usage: $0 create-store <name>"
                exit 1
            fi
            print_info "Creating store: $2"
            make_request POST "/store/$2" "" "$TOKEN"
            exit 0
            ;;
        get-store)
            if [ -z "$2" ]; then
                print_error "Usage: $0 get-store <name>"
                exit 1
            fi
            print_info "Getting store: $2"
            make_request GET "/store/$2"
            exit 0
            ;;
        delete-store)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token>"
                exit 1
            fi
            if [ -z "$2" ]; then
                print_error "Usage: $0 delete-store <name>"
                exit 1
            fi
            print_info "Deleting store: $2"
            make_request DELETE "/store/$2" "" "$TOKEN"
            exit 0
            ;;
        list-stores)
            print_info "Listing all stores"
            make_request GET "/stores"
            exit 0
            ;;
        create-item)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token>"
                exit 1
            fi
            if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
                print_error "Usage: $0 create-item <name> <price> <store_id>"
                exit 1
            fi
            print_info "Creating item: $2"
            make_request POST "/item/$2" "{\"price\":$3,\"store_id\":$4}" "$TOKEN"
            exit 0
            ;;
        get-item)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token>"
                exit 1
            fi
            if [ -z "$2" ]; then
                print_error "Usage: $0 get-item <name>"
                exit 1
            fi
            print_info "Getting item: $2"
            make_request GET "/item/$2" "" "$TOKEN"
            exit 0
            ;;
        update-item)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token>"
                exit 1
            fi
            if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
                print_error "Usage: $0 update-item <name> <price> <store_id>"
                exit 1
            fi
            print_info "Updating item: $2"
            make_request PUT "/item/$2" "{\"price\":$3,\"store_id\":$4}" "$TOKEN"
            exit 0
            ;;
        delete-item)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token>"
                exit 1
            fi
            if [ -z "$2" ]; then
                print_error "Usage: $0 delete-item <name>"
                exit 1
            fi
            print_info "Deleting item: $2"
            make_request DELETE "/item/$2" "" "$TOKEN"
            exit 0
            ;;
        list-items)
            if [ -z "$TOKEN" ]; then
                print_error "Token required. Use --token <token>"
                exit 1
            fi
            print_info "Listing all items"
            make_request GET "/items" "" "$TOKEN"
            exit 0
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

show_usage
