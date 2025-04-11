import os
import hashlib
import asyncio
from datetime import datetime
import re
from telegram import Bot
from dotenv import load_dotenv
load_dotenv()

# === CONFIG ===
URL = "https://form.gov.sg/6570150dc8854600121bb6b7"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HASH_FILE = "status_hash.txt"
SCREENSHOT_FILE = "screenshot.png"

# === FUNCTIONS ===

from playwright.async_api import async_playwright

def clean_text(text):
    # Remove inline scripts or JS code blocks
    text = re.sub(r"\(function\(\)\{.*?\}\)\(\);", "", text, flags=re.DOTALL)
    text = re.sub(r"window\.__CF\$cv\$params.*", "", text)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"[ \t]+", " ", text)  # remove excessive spacing
    text = text.strip()
    return text

async def get_form_text():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(URL, timeout=30000)

        # Optional: wait for specific text or element
        try:
            await page.wait_for_selector("body", timeout=10000)
            await asyncio.sleep(2)  # Let JS fully render
        except:
            print("⚠️ Page body not fully loaded.")

        # Get all visible text
        text_content = await page.text_content("body")

        # Screenshot
        await page.screenshot(path=SCREENSHOT_FILE, full_page=True)

        await browser.close()
        return text_content.strip() if text_content else ""
    
def get_text_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def load_last_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            return f.read().strip()
    return None

def save_current_hash(h: str):
    with open(HASH_FILE, "w") as f:
        f.write(h)

async def send_telegram_alert(message: str):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    with open(SCREENSHOT_FILE, "rb") as photo:
        await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)

# === MAIN ===

async def main():
    raw_text = await get_form_text()
    current_text = clean_text(raw_text)    
    print("\n--- Extracted Page Text ---\n")
    print(current_text)
    print("\n---------------------------\n")

    current_hash = get_text_hash(current_text)
    previous_hash = load_last_hash()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if current_hash != previous_hash:
        print("🔔 Change detected in form status.")
        save_current_hash(current_hash)

        message = (
            f"⚠️ The form page has changed.\n\n"
            f"Either the status changed or the page content was updated.\n"
            f"📅 Checked: {timestamp}\n"
            f"🔗 {URL}"
        )
        await send_telegram_alert(message)
    else:
        print("✅ No change in form content. No message sent.")
        
# === RUN ===

if __name__ == "__main__":
    asyncio.run(main())