import requests
import re
from datetime import datetime, timedelta
from telegram import Update
import pytz
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Constants
BOT_TOKEN = "7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14"
ISRAEL_TZ = pytz.timezone('Asia/Jerusalem')

# Helper Functions
def parse_reminder(text: str):
    match = re.search(r"remind me to (.+) at (\d{2}:\d{2})", text, re.IGNORECASE)
    if match:
        task = match.group(1)
        time_str = match.group(2)
        return task, time_str
    return None, None

def get_time_difference(time_str):
    now = datetime.now(ISRAEL_TZ)
    format = '%d %b %Y %H:%M:%S'
    reminder_time = ISRAEL_TZ.localize(datetime.strptime(time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day))
    if reminder_time < now:
        reminder_time += timedelta(days=1)
    return (reminder_time - now).total_seconds()

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    print(job)
    await context.bot.send_message(job.chat_id, text=f"⏰ Reminder: {job.data['task']}")

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello, I am Jarvis, your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
    )

# Responses
def handle_response(text: str) -> str:
    response = requests.get(f"http://127.0.0.1:8000/Jarvis?request={text}")
    return response.text.strip('"')  # Clean up the response text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    task, time_str = parse_reminder(text)

    if task and time_str:
        seconds_until_reminder = get_time_difference(time_str)
        if seconds_until_reminder > 0:
            # Adding the job to the queue
            job = context.job_queue.run_once(send_reminder, seconds_until_reminder, chat_id=update.message.chat_id, name=f"reminder_{task}", data={"task": task})
            print(job)
            await update.message.reply_text(f"Reminder set for {time_str} to: {task}!!!!!!!")
        else:
            await update.message.reply_text("The time you provided is in the past. Please provide a future time.")
    else:
        response = handle_response(text)
        await update.message.reply_text(response)

# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('OOPS! An error occurred. Please try again.')

# Main
if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    app.run_polling(poll_interval=3)
