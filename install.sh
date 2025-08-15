#!/usr/bin/env bash
# ------------------------------------------------------------
#  install.sh – drop-in installer for CodeSqueeze
#  Linux (any distro) + macOS
#  Places the script in a read-only system directory
#  Supports:  CodeSqueeze --delete
# ------------------------------------------------------------
set -euo pipefail

GREEN='\033[1;32m'
CYAN='\033[1;36m'
RED='\033[1;31m'
RESET='\033[0m'

# Detect OS and choose install prefix
case "$(uname -s)" in
    Linux*)  INSTALL_DIR="/opt/CodeSqueeze" ;;
    Darwin*) INSTALL_DIR="/usr/local/CodeSqueeze" ;;
    *)       echo -e "${RED}Unsupported OS${RESET}"; exit 1 ;;
esac

WRAPPER_PATH="/usr/local/bin/CodeSqueeze"

echo -e "${GREEN}🔧 Installing CodeSqueeze to ${INSTALL_DIR}${RESET}"

# Ensure we have privileges to write to INSTALL_DIR
if [[ ! -w "$(dirname "$INSTALL_DIR")" ]]; then
    echo -e "${CYAN}Requesting sudo to create ${INSTALL_DIR}${RESET}"
    sudo mkdir -p "$INSTALL_DIR"
else
    mkdir -p "$INSTALL_DIR"
fi

# Download the latest CodeSqueeze.py
curl -fsSL https://raw.githubusercontent.com/cyberytti/CodeSqueeze/main/CodeSqueeze.py \
     -o "${INSTALL_DIR}/CodeSqueeze.py"

# Make it read-only
chmod 644 "${INSTALL_DIR}/CodeSqueeze.py"

# Wrapper template (identical for both sudo and non-sudo cases)
wrapper_body() {
cat <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

# Determine correct install dir
case "$(uname -s)" in
    Linux*) INSTALL_DIR="/opt/CodeSqueeze" ;;
    Darwin*) INSTALL_DIR="/usr/local/CodeSqueeze" ;;
    *) echo "Unsupported OS"; exit 1 ;;
esac

if [[ "${1:-}" == "--delete" ]]; then
    echo "🧹 Uninstalling CodeSqueeze..."
    sudo rm -f "$INSTALL_DIR/CodeSqueeze.py"
    sudo rm -f "/usr/local/bin/CodeSqueeze"
    echo "✅ CodeSqueeze removed."
else
    exec uv run "${INSTALL_DIR}/CodeSqueeze.py" "$@"
fi
EOF
}

# Write wrapper
if [[ ! -w "$(dirname "$WRAPPER_PATH")" ]]; then
    echo -e "${CYAN}Requesting sudo to write wrapper to ${WRAPPER_PATH}${RESET}"
    wrapper_body | sudo tee "$WRAPPER_PATH" >/dev/null
    sudo chmod +x "$WRAPPER_PATH"
else
    wrapper_body > "$WRAPPER_PATH"
    chmod +x "$WRAPPER_PATH"
fi

# Install UV if missing
if ! command -v uv >/dev/null 2>&1; then
    echo -e "${GREEN}📦 Installing UV (fast Python package manager)...${RESET}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # shellcheck disable=SC1090
    source "$HOME/.cargo/env"
fi

echo -e "${GREEN}✅ Installation complete!${RESET}"
echo -e "Run:  CodeSqueeze --help"
echo -e "Run:  CodeSqueeze --delete   (to uninstall)"