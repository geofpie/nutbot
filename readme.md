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
├── cron.log               # Optional: captures logs from each run
```

## ⚙️ Setup

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/nutbot.git
cd nutbot
```

### 2. Set Up Your Secrets

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and insert your:
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
