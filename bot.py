import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from yt_dlp import YoutubeDL

# Configure logging
logging.basicConfig(
    format=\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Ensure environment variables are set
if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN is not set. Please set the environment variable.")
    exit(1)

# --- yt-dlp configuration ---
# For OAuth2, yt-dlp manages the token data in its cache. The user needs to authorize it once.
# We will guide the user on how to do this manually for the first run.
# For a bot, it\'s tricky to do interactively. A common approach is to pre-authorize it
# or use a pre-generated cookies file. Given the user\'s request to avoid IP blocks,
# OAuth2 is generally more robust than static cookies, but requires initial manual setup.
# For a headless environment like Railway, pre-authorization or using a cookies file is key.
# Let\'s start with a basic yt-dlp config and address auth/cookies in the guide.

YDL_OPTS = {
    \'format\': \'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best\',
    \'outtmpl\': \'downloads/%(title)s.%(ext)s\',
    \'noplaylist\': True,
    \'concurrent_fragments\': 5, # Increase concurrent fragments for faster downloads
    \'fragment_retries\': 10, # Retry fragments more often
    \'retries\': 10, # Retry overall downloads more often
    \'extractor_retries\': \'auto\', # Automatically retry extractor failures
    \'ignoreerrors\': True, # Continue on download errors
    \'postprocessors\': [{
        \'key\': \'FFmpegVideoConvertor\',
        \'preferedformat\': \'mp4\',
    }],
    \'logger\': logger,
    \'progress_hooks\': [], # Will add progress hook later
    \'verbose\': True, # For debugging
    \'nocheckcertificate\': True, # Ignore SSL certificate errors
    \'geo_bypass\': True, # Bypass geographic restrictions
    \'throttledratelimit\': 100000000, # Max download rate (bytes/sec) - effectively unlimited
    \'socket_timeout\': 10, # Timeout for network operations
    \'source_address\': \'0.0.0.0\', # Bind to all interfaces (might help with some network issues)
    # For OAuth2, yt-dlp will prompt for authorization on first use if --username oauth2 is set.
    # This is problematic for a bot. We will explain how to pre-authorize or use cookies.
    # \'username\': \'oauth2\', # This would trigger interactive OAuth2 flow
    # \'password\': \'\', # Required with username oauth2
}

# --- Telegram Bot Handlers ---

async def start(update: Update, context) -> None:
    """Sends a welcome message when the command /start is issued."""
    await update.message.reply_text(\'Hello! Send me a YouTube link and I will try to download it for you.\')

async def download_video(update: Update, context) -> None:
    """Downloads a YouTube video from the provided link."""
    url = update.message.text
    chat_id = update.message.chat_id

    if not url.startswith((\'http://\', \'https://\')):
        await update.message.reply_text("Please send a valid URL.")
        return

    message = await update.message.reply_text(f"Downloading {url}...")

    try:
        # Create a temporary directory for downloads
        download_dir = f"downloads/{chat_id}"
        os.makedirs(download_dir, exist_ok=True)

        ydl_opts = YDL_OPTS.copy()
        ydl_opts[\'outtmpl\'] = os.path.join(download_dir, \'%(title)s.%(ext)s\')

        # Add a progress hook to update the user
        async def progress_hook(d):
            if d[\'status\'] == \'downloading\':
                if \'total_bytes\' in d and \'downloaded_bytes\' in d:
                    total = d.get(\'total_bytes\') or d.get(\'total_bytes_estimate\', 0)
                    downloaded = d.get(\'downloaded_bytes\', 0)
                    if total > 0:
                        percent = downloaded / total * 100
                        # Update the message with progress. Rate limit to avoid API spam.
                        # For a real bot, you\'d store the message_id and edit it.
                        # For now, we\'ll just log and send a final message.
                        logger.info(f"Download progress for {url}: {percent:.1f}%")
            elif d[\'status\'] == \'finished\':
                logger.info(f"Finished downloading: {d[\'filename\']}")

        ydl_opts[\'progress_hooks\'] = [progress_hook]

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)

        await update.message.reply_text("Download complete! Uploading video...")

        # Send the downloaded file
        if os.path.exists(filepath):
            with open(filepath, \'rb\') as f:
                await update.message.reply_video(video=f, caption=info.get(\'title\', \'\'))
            # Clean up the downloaded file and directory
            os.remove(filepath)
            # Remove the chat-specific download directory if it\'s empty
            try:
                os.rmdir(download_dir)
            except OSError: # Directory might not be empty if multiple downloads were attempted
                pass
        else:
            await update.message.reply_text("Error: Downloaded file not found.")

    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await update.message.reply_text(f"An error occurred during download: {e}")
    finally:
        # Clean up any remaining files in the chat-specific directory
        if os.path.exists(download_dir):
            for f in os.listdir(download_dir):
                os.remove(os.path.join(download_dir, f))
            try:
                os.rmdir(download_dir)
            except OSError:
                pass

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    logger.info("Bot started. Listening for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
