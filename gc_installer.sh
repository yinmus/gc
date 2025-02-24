#!/usr/bin/env bash

set -x

INSTALL_DIR="/home/user/.gc"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_NAME="gc.py"
BIN_PATH="/usr/local/bin/gc"

echo "Этот скрипт установит gc в $INSTALL_DIR и создаст venv."
read -rp "Продолжить? [Y/n] " confirm

if [[ -z "$confirm" || "$confirm" =~ ^[Yy]$ ]]; then
    mkdir -p "$INSTALL_DIR"
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install requests
    deactivate

    echo '#!/usr/bin/env bash
VENV_PATH="'$VENV_DIR'"
SCRIPT_PATH="'$INSTALL_DIR'/'$SCRIPT_NAME'"

source "$VENV_PATH/bin/activate"
python3 "$SCRIPT_PATH" "$@"
deactivate' | sudo tee "$BIN_PATH" > /dev/null

    sudo chmod +x "$BIN_PATH"
    echo "Установка завершена. Используйте команду 'gc'."
else
    echo "Установка отменена."
fi
