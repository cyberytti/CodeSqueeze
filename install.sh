#!/usr/bin/env bash
# ------------------------------------------------------------
#  install.sh – universal installer for CodeSqueeze
#  Linux (any distro) + macOS
#  Installs into /opt/CodeSqueeze  (Linux)
#              or /usr/local/CodeSqueeze (macOS)
#  Supports:  CodeSqueeze --delete
# ------------------------------------------------------------
set -euo pipefail

GREEN='\033[1;32m'
CYAN='\033[1;36m'
RED='\033[1;31m'
RESET='\033[0m'

# Detect OS and set install prefix
case "$(uname -s)" in
    Linux*)  INSTALL_DIR="/opt/CodeSqueeze" ;;
    Darwin*) INSTALL_DIR="/usr/local/CodeSqueeze" ;;
    *)       echo -e "${RED}Unsupported OS${RESET}"; exit 1 ;;
esac

WRAPPER_PATH="/usr/local/bin/CodeSqueeze"
USER_BIN="$HOME/.local/bin"
UV_PATH="$USER_BIN/uv"

echo -e "${GREEN}🔧 Installing CodeSqueeze to ${INSTALL_DIR}${RESET}"

# Ensure we have privileges to write to INSTALL_DIR
if [[ ! -w "$(dirname "$INSTALL_DIR")" ]]; then
    echo -e "${CYAN}Requesting sudo to create ${INSTALL_DIR}${RESET}"
    sudo mkdir -p "$INSTALL_DIR"
else
    mkdir -p "$INSTALL_DIR"
fi

# Download latest CodeSqueeze.py
curl -fsSL https://raw.githubusercontent.com/cyberytti/CodeSqueeze/main/CodeSqueeze.py \
     -o "${INSTALL_DIR}/CodeSqueeze.py"
chmod 644 "${INSTALL_DIR}/CodeSqueeze.py"

# Install UV for the current user (not root)
if [[ ! -x "$UV_PATH" ]]; then
    echo -e "${GREEN}📦 Installing UV to $USER_BIN${RESET}"
    mkdir -p "$USER_BIN"
    curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$USER_BIN" sh
fi

# Ensure ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    case "$SHELL" in
        */zsh*)
            echo 'export PATH="'"$USER_BIN"':$PATH"' >> ~/.zshrc ;;
        */bash*)
            echo 'export PATH="'"$USER_BIN"':$PATH"' >> ~/.bashrc ;;
        *) ;;
    esac
    export PATH="$USER_BIN:$PATH"
fi

# Write wrapper script
wrapper_body() {
cat <<EOF
#!/usr/bin/env bash
set -euo pipefail

case "\$(uname -s)" in
    Linux*)  INSTALL_DIR="/opt/CodeSqueeze" ;;
    Darwin*) INSTALL_DIR="/usr/local/CodeSqueeze" ;;
    *) echo "Unsupported OS"; exit 1 ;;
esac

if [[ "\${1:-}" == "--delete" ]]; then
    echo "🧹 Uninstalling CodeSqueeze..."
    sudo rm -f "\$INSTALL_DIR/CodeSqueeze.py"
    sudo rm -f /usr/local/bin/CodeSqueeze
    echo "✅ CodeSqueeze removed."
else
    exec uv run "\$INSTALL_DIR/CodeSqueeze.py" "\$@"
fi
EOF
}

if [[ ! -w "$(dirname "$WRAPPER_PATH")" ]]; then
    echo -e "${CYAN}Requesting sudo to write wrapper to ${WRAPPER_PATH}${RESET}"
    wrapper_body | sudo tee "$WRAPPER_PATH" >/dev/null
    sudo chmod +x "$WRAPPER_PATH"
else
    wrapper_body > "$WRAPPER_PATH"
    chmod +x "$WRAPPER_PATH"
fi

echo -e "${GREEN}✅ Installation complete!${RESET}"
echo -e "Run:  CodeSqueeze --help"
echo -e "Run:  CodeSqueeze --delete   (to uninstall)"