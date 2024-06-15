from typing import Final
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import pandas as pd


# Constants
BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'


# Commands
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'בשביל לבדוק זכאות של חייל מילואים לאירוע מסוים, אנא שלח/י הודעה בפורמט הבא:\n\n'
        '<שם אירוע>\n<פרט מזהה>\n\n'
        'דגשים:\n'
        'שם האירוע נדרש להיות זהה לזה שמופיע ברשימת אירועים (מוזמנים להריץ את הפקודה "/events" לקבלת רשימה של האירועים הקיימים\n)'
        'פרט מזהה הינו אחד מכמה אפשרויות:\n'
        '1. תעודת הזהות של משרת המילואים (בפורמט 9 ספרות)\n'
        '2. מספר הטלפון של משרת המילואים (בפורמט 10 ספרות עם מקף אחרי 3 הספרות הראשונות)\n'
        '3. מספר הטלפון של בת הזוג של משרת המילואים (בפורמט 10 ספרות עם מקף אחרי 3 הספרות הראשונות)\n\n'
        'דוגמה:\n'
        'פסח שוברים\n207827825\n\n'
        'דוגמה נוספת:\n'
        'שי ליולדת\n054-8111733\n\n'
        'לעזרה נוספת - ניתן לפנות לעומר בנגל: 054-8111733'
    )


def remove_escape_characters(text: str) -> str:
    return text.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\').replace('\\"', '"')


# Responses
def handle_response(text: str) -> str:
    response = requests.get(f"http://127.0.0.1:8000/Jarvis?request={text}")
    response_text = remove_escape_characters(response.text).strip('"')  # nopep8
    print(response_text)
    return response_text


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    # print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'private':
        response = handle_response(text)
        await update.message.reply_text(response)


# Errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # print(f'Update {update} caused error {context.error}')
    await update.message.reply_text('OOPS! An error occurred. Please try again.')


# Main
if __name__ == '__main__':
    # print('Starting bot...')
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # print('Polling...')
    app.run_polling(poll_interval=3)
