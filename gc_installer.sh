#!/usr/bin/env bash

echo "Выберите пользователя для установки:"

mapfile -t users < <(ls /home/)
for i in "${!users[@]}"; do
    printf "%d. %s\n" "$((i + 1))" "${users[$i]}"
done

read -rp "Введите номер пользователя: " user_choice

if ! [[ "$user_choice" =~ ^[0-9]+$ ]] || ((user_choice < 1 || user_choice > ${#users[@]})); then
    echo "Некорректный выбор."
    exit 1
fi

USERNAME="${users[$((user_choice - 1))]}"
INSTALL_DIR="/home/$USERNAME/.gc"
VENV_DIR="$INSTALL_DIR/venv"
SCRIPT_NAME="gc.py"
BIN_PATH="/usr/local/bin/gc"

echo "Этот скрипт установит gc в $INSTALL_DIR и создаст venv."
read -rp "Продолжить? [Y/n] " confirm

if [[ -z "$confirm" || "$confirm" =~ ^[Yy]$ ]]; then
    mkdir -p "$INSTALL_DIR"
    cp "$SCRIPT_NAME" "$INSTALL_DIR"
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install requests
    deactivate

echo '#!/usr/bin/env bash
VENV_PATH="'$VENV_DIR'"
SCRIPT_PATH="'$INSTALL_DIR'/'$SCRIPT_NAME'"

source "$VENV_PATH/bin/activate"
python3 "$SCRIPT_PATH" "$@"
deactivate' | sudo tee "$BIN_PATH" >/dev/null || { echo "Ошибка записи в $BIN_PATH"; exit 1; }



    sudo chmod +x "$BIN_PATH"
    echo "Установка завершена. Используйте команду 'gc'."
else
    echo "Установка отменена."
fi
