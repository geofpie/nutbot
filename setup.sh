#!/bin/bash

# === Nutbot All-in-One Setup Script ===

echo "🧠 Nutbot Installer"
echo "------------------------"

# === CONFIG ===
REPO_URL="https://github.com/geofpie/nutbot"
TARGET_DIR="/root/nutbot"
IMAGE_NAME="nutbot"

# === 1. Clone or Update Repo ===
if [ -d "$TARGET_DIR" ]; then
    echo "📁 Repo already exists. Pulling latest changes..."
    cd "$TARGET_DIR" && git pull
else
    echo "📥 Cloning repository into $TARGET_DIR..."
    git clone "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR" || exit
fi

# === 2. Prompt for .env creation ===
if [ ! -f .env ]; then
    echo "⚙️ Setting up your .env file..."
    read -p "🔍 Enter the URL to monitor: " MONITOR_URL
    read -p "🤖 Enter your Telegram Bot Token: " TELEGRAM_BOT_TOKEN
    read -p "💬 Enter your Telegram Chat ID: " TELEGRAM_CHAT_ID

    cat <<EOF > .env
MONITOR_URL=$MONITOR_URL
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID
EOF
    echo "✅ .env file created."
else
    echo "✅ .env file already exists. Skipping setup."
fi

# === 3. Build Docker image ===
echo "🐳 Building Docker image..."
docker build -t "$IMAGE_NAME" .

# === 4. Run a test ===
echo "🚀 Running a test check..."
docker run --rm --env-file .env -v "$TARGET_DIR":/app "$IMAGE_NAME"

# === 5. Add Cron Job ===
CRON_JOB="0 */4 * * * docker run --rm --env-file $TARGET_DIR/.env -v $TARGET_DIR:/app $IMAGE_NAME >> $TARGET_DIR/cron.log 2>&1"
echo "🕒 Setting up cron job (every 4 hours)..."

# Avoid duplicate cron entry
(crontab -l 2>/dev/null | grep -v "$IMAGE_NAME" ; echo "$CRON_JOB") | crontab -

echo "✅ All done! Nutbot is installed and scheduled."
