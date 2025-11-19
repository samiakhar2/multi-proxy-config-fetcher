#!/usr/bin/env bash

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════════════════════════════"
echo " 🧙‍♂️ Multi Wizard - Complete Setup"
echo "═════════════════════════════════════════════"
echo " 👽 Designed by: Anonymous"
echo "═════════════════════════════════════════════"
echo ""

REPO_URL="https://github.com/4n0nymou3/multi-proxy-config-fetcher.git"
INSTALL_DIR="$HOME/multi-proxy-config-fetcher"
VENV_DIR="$INSTALL_DIR/venv"

detect_platform() {
    if command -v termux-info >/dev/null 2>&1; then
        echo "termux"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OS" == "Windows_NT" ]] || uname -s | grep -q "MINGW\|MSYS\|CYGWIN"; then
        echo "windows"
    else
        echo "unknown"
    fi
}

print_status() {
    echo -e "${CYAN}[INFO]${NC} $1"
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

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

setup_repository() {
    print_status "Setting up repository..."
    
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Directory exists. Pulling latest changes..."
        cd "$INSTALL_DIR"
        git fetch --all
        git reset --hard origin/main
        git pull origin main
    else
        print_status "Cloning repository..."
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
    
    print_success "Repository setup complete!"
}

create_directory_structure() {
    print_status "Creating directory structure..."
    
    mkdir -p "$INSTALL_DIR/configs"
    mkdir -p "$INSTALL_DIR/assets"
    mkdir -p "$INSTALL_DIR/logs"
    mkdir -p "$INSTALL_DIR/src"
    
    print_success "Directory structure created!"
}

setup_python_environment() {
    print_status "Setting up Python environment..."
    
    if [ "$PLATFORM" = "termux" ]; then
        if ! check_command python; then
            pkg install -y python
        fi
        PYTHON_CMD="python"
        PIP_CMD="pip"
    else
        if check_command python3; then
            PYTHON_CMD="python3"
            PIP_CMD="pip3"
        elif check_command python; then
            PYTHON_CMD="python"
            PIP_CMD="pip"
        else
            print_error "Python not found!"
            exit 1
        fi
    fi
    
    print_status "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR" 2>/dev/null || {
        print_warning "venv module not available, installing globally..."
        VENV_DIR=""
    }
    
    if [ -n "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
        source "$VENV_DIR/bin/activate"
        print_success "Virtual environment activated!"
    fi
    
    print_status "Upgrading pip..."
    $PIP_CMD install --upgrade pip setuptools wheel
    
    print_status "Installing Python dependencies..."
    $PIP_CMD install -r "$INSTALL_DIR/requirements.txt"
    
    print_success "Python environment ready!"
}

install_xray() {
    print_status "Installing Xray-core..."
    
    if check_command xray; then
        print_success "Xray already installed!"
        return 0
    fi
    
    case $PLATFORM in
        linux|macos)
            bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install >/dev/null 2>&1 || {
                print_warning "Auto-install failed, trying manual method..."
                local xray_version=$(curl -s "https://api.github.com/repos/XTLS/Xray-core/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
                local os_type=$(uname -s | tr '[:upper:]' '[:lower:]')
                local arch_type=$(uname -m)
                
                if [ "$arch_type" = "x86_64" ]; then
                    arch_type="64"
                elif [ "$arch_type" = "aarch64" ]; then
                    arch_type="arm64-v8a"
                fi
                
                local download_url="https://github.com/XTLS/Xray-core/releases/download/${xray_version}/Xray-${os_type}-${arch_type}.zip"
                
                if check_command wget; then
                    wget -q "$download_url" -O /tmp/xray.zip
                elif check_command curl; then
                    curl -sL "$download_url" -o /tmp/xray.zip
                else
                    print_error "Neither wget nor curl found!"
                    return 1
                fi
                
                unzip -q /tmp/xray.zip -d /tmp/xray
                
                if [ "$PLATFORM" = "macos" ]; then
                    sudo mv /tmp/xray/xray /usr/local/bin/
                else
                    sudo mv /tmp/xray/xray /usr/local/bin/ 2>/dev/null || mv /tmp/xray/xray "$HOME/.local/bin/"
                fi
                
                chmod +x /usr/local/bin/xray 2>/dev/null || chmod +x "$HOME/.local/bin/xray"
                rm -rf /tmp/xray /tmp/xray.zip
            }
            ;;
        termux)
            local arch=$(uname -m)
            local xray_arch=""
            
            case $arch in
                aarch64) xray_arch="arm64-v8a" ;;
                armv7l) xray_arch="arm32-v7a" ;;
                x86_64) xray_arch="64" ;;
                *) print_error "Unsupported architecture: $arch"; return 1 ;;
            esac
            
            print_status "Detecting latest Xray version..."
            local xray_version=$(curl -s "https://api.github.com/repos/XTLS/Xray-core/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
            
            if [ -z "$xray_version" ]; then
                print_error "Failed to detect Xray version!"
                return 1
            fi
            
            local download_url="https://github.com/XTLS/Xray-core/releases/download/${xray_version}/Xray-linux-${xray_arch}.zip"
            print_status "Downloading Xray from: $download_url"
            
            if ! curl -L "$download_url" -o "$PREFIX/tmp/xray.zip"; then
                print_error "Failed to download Xray!"
                return 1
            fi
            
            if [ ! -f "$PREFIX/tmp/xray.zip" ]; then
                print_error "Download failed: xray.zip not found!"
                return 1
            fi
            
            print_status "Extracting Xray..."
            if ! unzip -q "$PREFIX/tmp/xray.zip" -d "$PREFIX/tmp/xray"; then
                print_error "Failed to extract Xray!"
                rm -f "$PREFIX/tmp/xray.zip"
                return 1
            fi
            
            if [ ! -f "$PREFIX/tmp/xray/xray" ]; then
                print_error "Xray binary not found after extraction!"
                rm -rf "$PREFIX/tmp/xray" "$PREFIX/tmp/xray.zip"
                return 1
            fi
            
            mv "$PREFIX/tmp/xray/xray" "$PREFIX/bin/xray"
            chmod +x "$PREFIX/bin/xray"
            rm -rf "$PREFIX/tmp/xray" "$PREFIX/tmp/xray.zip"
            ;;
        windows)
            print_warning "Please install Xray manually from: https://github.com/XTLS/Xray-core/releases"
            return 1
            ;;
    esac
    
    if check_command xray; then
        print_success "Xray installed successfully!"
        xray version
    else
        print_error "Xray installation failed!"
        return 1
    fi
}

install_singbox() {
    print_status "Installing Sing-box..."
    
    if check_command sing-box; then
        print_success "Sing-box already installed!"
        return 0
    fi
    
    case $PLATFORM in
        linux)
            bash <(curl -fsSL https://sing-box.app/install.sh) >/dev/null 2>&1 || {
                print_warning "Auto-install failed, trying package manager..."
                if check_command apt; then
                    sudo apt install -y sing-box
                elif check_command pacman; then
                    sudo pacman -S --noconfirm sing-box
                elif check_command yum; then
                    sudo yum install -y sing-box
                fi
            }
            ;;
        macos)
            if check_command brew; then
                brew install sing-box
            else
                print_error "Homebrew not found! Install from: https://brew.sh"
                return 1
            fi
            ;;
        termux)
            pkg install -y sing-box
            ;;
        windows)
            print_warning "Please install Sing-box manually from: https://sing-box.sagernet.org"
            return 1
            ;;
    esac
    
    if check_command sing-box; then
        print_success "Sing-box installed successfully!"
        sing-box version
    else
        print_error "Sing-box installation failed!"
        return 1
    fi
}

install_dependencies_termux() {
    print_status "Installing Termux dependencies..."
    
    pkg update -y
    pkg upgrade -y
    pkg install -y git python cronie curl unzip
    
    print_success "Termux dependencies installed!"
}

install_dependencies_linux() {
    print_status "Installing Linux dependencies..."
    
    if check_command apt; then
        sudo apt update -y
        sudo apt install -y git python3 python3-pip python3-venv cron wget curl unzip
    elif check_command pacman; then
        sudo pacman -Syu --noconfirm
        sudo pacman -S --noconfirm git python python-pip cronie wget curl unzip
    elif check_command yum; then
        sudo yum update -y
        sudo yum install -y git python3 python3-pip cronie wget curl unzip
    elif check_command dnf; then
        sudo dnf update -y
        sudo dnf install -y git python3 python3-pip cronie wget curl unzip
    else
        print_error "Unsupported package manager!"
        exit 1
    fi
    
    print_success "Linux dependencies installed!"
}

install_dependencies_macos() {
    print_status "Installing macOS dependencies..."
    
    if ! check_command brew; then
        print_status "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install git python wget curl
    
    print_success "macOS dependencies installed!"
}

create_runner_script() {
    print_status "Creating runner script..."
    
    local activate_cmd=""
    if [ -n "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
        activate_cmd="source \"$VENV_DIR/bin/activate\""
    fi
    
    cat > "$INSTALL_DIR/run.sh" << EOF
#!/usr/bin/env bash

set -e

cd "$INSTALL_DIR"

$activate_cmd

LOG_DIR="$INSTALL_DIR/logs"
mkdir -p "\$LOG_DIR"

TIMESTAMP=\$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="\$LOG_DIR/run_\$TIMESTAMP.log"

exec > >(tee -a "\$LOG_FILE")
exec 2>&1

echo "════════════════════════════════════════════════════════════════"
echo "  Multi Proxy Config Fetcher - Pipeline Execution"
echo "  Started at: \$(date)"
echo "════════════════════════════════════════════════════════════════"
echo ""

run_step() {
    local step_name="\$1"
    local step_cmd="\$2"
    
    echo "➤ [\$(date +%H:%M:%S)] Running: \$step_name"
    
    if eval "\$step_cmd"; then
        echo "✓ [\$(date +%H:%M:%S)] Completed: \$step_name"
        echo ""
        return 0
    else
        echo "✗ [\$(date +%H:%M:%S)] Failed: \$step_name"
        echo ""
        return 1
    fi
}

run_step "Fetch Configs" "$PYTHON_CMD src/fetch_configs.py"

run_step "Enrich Configs" "$PYTHON_CMD src/enrich_configs.py configs/proxy_configs.txt configs/location_cache.json"

run_step "Rename Configs" "$PYTHON_CMD src/rename_configs.py configs/location_cache.json configs/proxy_configs.txt configs/proxy_configs.txt"

run_step "Test with Xray" "$PYTHON_CMD src/xray_config_tester.py configs/proxy_configs.txt configs/proxy_configs_tested.txt"

run_step "Convert to Sing-box" "$PYTHON_CMD src/config_to_singbox.py"

run_step "Test with Sing-box" "$PYTHON_CMD src/config_tester.py configs/singbox_configs_all.json configs/singbox_configs_tested.json"

run_step "Security Filter" "$PYTHON_CMD src/security_filter.py"

run_step "Generate Xray Balanced Config" "$PYTHON_CMD src/xray_balancer.py"

run_step "Generate Charts" "$PYTHON_CMD src/generate_charts.py"

echo "════════════════════════════════════════════════════════════════"
echo "  🎉 Pipeline completed successfully!"
echo "  Finished at: \$(date)"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Output files location:"
echo "   - configs/proxy_configs.txt"
echo "   - configs/proxy_configs_tested.txt"
echo "   - configs/singbox_configs_all.json"
echo "   - configs/singbox_configs_tested.json"
echo "   - configs/singbox_configs_secure.json"
echo "   - configs/xray_loadbalanced_config.json"
echo "   - configs/xray_secure_loadbalanced_config.json"
echo ""

find "\$LOG_DIR" -name "run_*.log" -mtime +7 -delete 2>/dev/null || true

EOF

    chmod +x "$INSTALL_DIR/run.sh"
    print_success "Runner script created!"
}

setup_cron_linux() {
    print_status "Setting up cron job for Linux..."
    
    local cron_entry="0 */12 * * * cd $INSTALL_DIR && bash run.sh >> logs/cron.log 2>&1"
    
    if ! check_command crontab; then
        print_error "crontab not found!"
        return 1
    fi
    
    (crontab -l 2>/dev/null | grep -v "multi-proxy-config-fetcher"; echo "$cron_entry") | crontab -
    
    if check_command systemctl; then
        sudo systemctl enable cron 2>/dev/null || sudo systemctl enable cronie 2>/dev/null || true
        sudo systemctl start cron 2>/dev/null || sudo systemctl start cronie 2>/dev/null || true
    fi
    
    print_success "Cron job configured! (runs every 12 hours)"
}

setup_cron_macos() {
    print_status "Setting up LaunchAgent for macOS..."
    
    mkdir -p "$HOME/Library/LaunchAgents"
    
    cat > "$HOME/Library/LaunchAgents/com.anonymous.multiproxy.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.anonymous.multiproxy</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$INSTALL_DIR/run.sh</string>
    </array>
    
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Hour</key>
            <integer>8</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Hour</key>
            <integer>20</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>
    
    <key>StandardOutPath</key>
    <string>$INSTALL_DIR/logs/launchd.log</string>
    
    <key>StandardErrorPath</key>
    <string>$INSTALL_DIR/logs/launchd_error.log</string>
    
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF
    
    launchctl unload "$HOME/Library/LaunchAgents/com.anonymous.multiproxy.plist" 2>/dev/null || true
    launchctl load "$HOME/Library/LaunchAgents/com.anonymous.multiproxy.plist"
    
    print_success "LaunchAgent configured! (runs at 08:00 and 20:00)"
}

setup_cron_termux() {
    print_status "Setting up cron for Termux..."
    
    mkdir -p "$PREFIX/var/spool/cron/crontabs"
    
    local cron_entry="0 */12 * * * cd $INSTALL_DIR && bash run.sh >> logs/cron.log 2>&1"
    
    (crontab -l 2>/dev/null | grep -v "multi-proxy-config-fetcher"; echo "$cron_entry") | crontab -
    
    if ! pgrep -x "crond" > /dev/null; then
        crond
        print_status "Started crond daemon"
    fi
    
    print_success "Cron job configured! (runs every 12 hours)"
}

create_management_script() {
    print_status "Creating management script..."
    
    cat > "$INSTALL_DIR/manage.sh" << 'EOFMANAGE'
#!/usr/bin/env bash

INSTALL_DIR="$HOME/multi-proxy-config-fetcher"
cd "$INSTALL_DIR"

case "$1" in
    start)
        echo "🚀 Starting pipeline..."
        bash run.sh
        ;;
    status)
        echo "📊 System Status:"
        echo ""
        if command -v xray >/dev/null 2>&1; then
            echo "✓ Xray: $(xray version | head -1)"
        else
            echo "✗ Xray: Not installed"
        fi
        
        if command -v sing-box >/dev/null 2>&1; then
            echo "✓ Sing-box: $(sing-box version | head -1)"
        else
            echo "✗ Sing-box: Not installed"
        fi
        
        echo ""
        echo "📁 Output files:"
        ls -lh configs/*.txt configs/*.json 2>/dev/null | awk '{print "   ", $9, "-", $5}'
        
        echo ""
        echo "📝 Recent logs:"
        ls -lt logs/*.log 2>/dev/null | head -3 | awk '{print "   ", $9}'
        ;;
    logs)
        if [ -f "logs/cron.log" ]; then
            tail -50 logs/cron.log
        else
            echo "No cron logs found"
        fi
        ;;
    clean)
        echo "🧹 Cleaning old logs..."
        find logs -name "*.log" -mtime +7 -delete 2>/dev/null
        echo "✓ Done!"
        ;;
    update)
        echo "🔄 Updating repository..."
        git fetch --all
        git reset --hard origin/main
        git pull origin main
        echo "✓ Updated!"
        ;;
    help|*)
        echo "Multi Wizard - Management Script"
        echo ""
        echo "Usage: bash manage.sh [command]"
        echo ""
        echo "Commands:"
        echo "  start   - Run the pipeline manually"
        echo "  status  - Show system status and files"
        echo "  logs    - Show recent cron logs"
        echo "  clean   - Remove old log files"
        echo "  update  - Update repository from GitHub"
        echo "  help    - Show this help message"
        ;;
esac
EOFMANAGE

    chmod +x "$INSTALL_DIR/manage.sh"
    print_success "Management script created!"
}

print_final_instructions() {
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "  🎉 Multi Wizard Installation Complete!"
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "📁 Installation directory: $INSTALL_DIR"
    echo ""
    echo "🔧 Management commands:"
    echo "   cd $INSTALL_DIR"
    echo "   bash manage.sh start    # Run pipeline now"
    echo "   bash manage.sh status   # Check system status"
    echo "   bash manage.sh logs     # View logs"
    echo "   bash manage.sh clean    # Clean old logs"
    echo "   bash manage.sh update   # Update from GitHub"
    echo ""
    echo "⏰ Automatic execution:"
    if [ "$PLATFORM" = "macos" ]; then
        echo "   Configured via LaunchAgent (08:00 & 20:00)"
    else
        echo "   Configured via cron (every 12 hours)"
    fi
    echo ""
    echo "📂 Output files will be in: $INSTALL_DIR/configs/"
    echo "📝 Logs will be in: $INSTALL_DIR/logs/"
    echo ""
    echo "💡 To run the pipeline now:"
    echo "   cd $INSTALL_DIR && bash run.sh"
    echo ""
    echo "════════════════════════════════════════════════════════════════"
}

main() {
    PLATFORM=$(detect_platform)
    
    print_status "Detected platform: $PLATFORM"
    echo ""
    
    if [ "$PLATFORM" = "unknown" ]; then
        print_error "Unsupported platform!"
        exit 1
    fi
    
    if [ "$PLATFORM" = "windows" ]; then
        print_error "Windows detected! Please use WSL2 or Git Bash."
        print_status "Install WSL2: https://docs.microsoft.com/windows/wsl/install"
        exit 1
    fi
    
    case $PLATFORM in
        termux)
            install_dependencies_termux
            ;;
        linux)
            install_dependencies_linux
            ;;
        macos)
            install_dependencies_macos
            ;;
    esac
    
    setup_repository
    create_directory_structure
    setup_python_environment
    
    install_xray
    install_singbox
    
    create_runner_script
    create_management_script
    
    case $PLATFORM in
        termux)
            setup_cron_termux
            ;;
        linux)
            setup_cron_linux
            ;;
        macos)
            setup_cron_macos
            ;;
    esac
    
    print_final_instructions
}

main "$@"