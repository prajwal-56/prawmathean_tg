import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ParseMode

# ENV stuff
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

# logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Yo Sup?\n\nI'm Ps official telegram bot btw.\n\n Try sending /whoami`")
    print(f"used or using start")

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply = f"<b>FullName :</b> {update.effective_user.full_name}\n<b>ID:</b> {update.effective_user.id} \n Thanks, Bye."

    await update.message.reply_text(reply, parse_mode=ParseMode.HTML)

    print(f"used or using whoami")

async def idk_how_to_respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Um..idk how to respond that. sry")
    print("Used idk how to respond")

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    print(f"This is app : {app}")
    app.add_handler(CommandHandler("start" , start))
    app.add_handler(CommandHandler("whoami" , whoami))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, idk_how_to_respond))    
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    print(f"The bot is polling...")

if __name__ == "__main__":
    main()