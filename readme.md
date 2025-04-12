# Nutbot 🧠📬  

A Telegram bot that monitors a webpage (like a form) and notifies you when it changes — so you can apply as soon as it's available.

## 🔍 What It Does

This bot was built to watch a specific FormSG application page. Whenever the page text changes (e.g., the form reopens), it captures a screenshot and sends a Telegram alert.

It runs inside Docker and checks the page at a regular interval using `cron` (currently every 4 hours). You’ll only get a Telegram message when a real change is detected.

## 📦 Features

- ✅ Checks form availability using Playwright (headless browser)
- ✅ Sends alerts + screenshots to your Telegram chat
- ✅ Smart: Only notifies when something actually changes
- ✅ Lightweight: Designed to run in Docker with minimal footprint
- ✅ Configurable: You control the interval via cron

## 📂 Project Structure

```
nutbot/
├── nutbot.py              # Main script
├── Dockerfile             # Docker container config
├── requirements.txt       # Python dependencies
├── .env.example           # Template for secrets
├── setup.sh               # Interactive installer script
├── cron.log               # Optional: captures logs from each run
```

## ⚙️ Automated Setup

### 1. Clone and Run the Installer Script

```bash
wget https://raw.githubusercontent.com/geofpie/nutbot/main/setup.sh
chmod +x setup.sh
./setup.sh
```

This script will:
- Clone the GitHub repo
- Prompt you to enter the form URL, Telegram Bot Token, and Chat ID
- Create a `.env` file for configuration
- Build the Docker image
- Run the bot once to verify
- Install a cron job that runs every 4 hours

### 2. Manual `.env` Setup (Optional)

If you're setting things up manually, your `.env` should look like:

```env
MONITOR_URL=your_website_url
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```
## ⚙️ Manual Setup

### 1. Clone the Repo

```bash
git clone https://github.com/geofpie/nutbot
cd nutbot
```

### 2. Set Up Your Secrets

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and insert your:
- `MONITOR_URL`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### 3. Build the Docker Image

```bash
docker build -t nutbot .
```

### 4. Run It Once (Manually)

```bash
docker run --rm --env-file .env -v "$PWD":/app nutbot
```

### 5. Schedule it with Cron

Edit your crontab:

```bash
crontab -e
```

Add:

```cron
0 */4 * * * docker run --rm --env-file /root/nutbot/.env -v /root/nutbot:/app nutbot >> /root/nutbot/cron.log 2>&1
```

✅ This runs every 4 hours.

## 🛠 Dependencies

- [Playwright](https://playwright.dev/python/)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Docker

## 🤖 Why I Built This

I just wanted a simple Telegram bot that notifies me when a specific government form reopens — so I can apply right away 😄

## 🧼 To-Do / Ideas

- [ ] Archive screenshots by timestamp  
- [ ] Add log rotation  
- [ ] Support multiple form URLs  
- [ ] Add `/check` command support via bot  

## 📬 Contact

Built with ❤️ by [geofpie](https://github.com/geofpie)