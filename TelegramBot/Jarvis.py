import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# Constants
BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello, I am Jarvis, your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
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
    app.add_handler(CommandHandler('start', start_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # print('Polling...')
    app.run_polling(poll_interval=3)
