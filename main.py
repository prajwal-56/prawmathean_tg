import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode
import asyncio
import glob
import socket
import time
from datetime import timedelta

import psutil

# ENV stuff
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])

# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Yo Sup?\n\nI'm Ps official telegram bot btw.\n\n Try sending /whoami`")
    print(f"used or using start")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply = f"<b>FullName :</b> {update.effective_user.full_name}\n<b>ID:</b> {update.effective_user.id} \n Thanks, Bye."

    await update.message.reply_text(reply, parse_mode=ParseMode.HTML)

    print(f"used or using whoami")

# for getting a quick glance of the system 
def read_stats() -> str:
    temps = []
    for p in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
        try:
            with open(p) as f:
                temps.append(int(f.read()) / 1000)
        except (OSError, ValueError):
            pass
    temp = f"{max(temps):.1f}C" if temps else "n/a"
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    up = timedelta(seconds=int(time.time() - psutil.boot_time()))
    return (
        f"____________STATS__________\n"
        f"{socket.gethostname()}\n"
        f"<b>Temp</b>   : {temp}\n"
        f"<b>CPU</b>    : {psutil.cpu_percent(interval=1):.0f}%\n"
        f"<b>RAM</b>    : {ram.percent:.0f}% ({ram.available / 2**20:.0f} MB avail)\n"
        f"<b>Disk</b>   : {disk.percent:.0f}%\n"
        f"<b>Uptime</b> : {up}"
        f""
        f"have a good day :)"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("using stats..")
    if update.effective_user.id != OWNER_ID:
        return
    text = await asyncio.to_thread(read_stats)
    await update.message.reply_text(f"<pre>{text}</pre>", parse_mode=ParseMode.HTML )

async def idk_how_to_respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Um..idk how to respond that. sry")
    print("Used idk how to respond")

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    print(f"This is app : {app}")
    app.add_handler(CommandHandler("start" , start))
    app.add_handler(CommandHandler("whoami" , whoami))
    app.add_handler(CommandHandler("stats" , stats))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, idk_how_to_respond))    
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    print(f"The bot is polling...")

if __name__ == "__main__":
    main()