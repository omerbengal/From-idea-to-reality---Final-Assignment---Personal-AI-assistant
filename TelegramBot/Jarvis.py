# import requests
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# # Constants
# BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'


# # Commands
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         'Hello, I am Jarvis, your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
#     )


# def remove_escape_characters(text: str) -> str:
#     return text.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\').replace('\\"', '"')


# # Responses
# def handle_response(text: str) -> str:
#     response = requests.get(f"http://127.0.0.1:8000/Jarvis?request={text}")
#     response_text = remove_escape_characters(response.text).strip('"')  # nopep8
#     print(response_text)
#     return response_text


# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type = update.message.chat.type
#     text = update.message.text
#     # print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
#     if message_type == 'private':
#         response = handle_response(text)
#         await update.message.reply_text(response)


# # Errors
# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # print(f'Update {update} caused error {context.error}')
#     await update.message.reply_text('OOPS! An error occurred. Please try again.')


# # Main
# if __name__ == '__main__':
#     # print('Starting bot...')
#     app = Application.builder().token(BOT_TOKEN).build()

#     # Commands
#     app.add_handler(CommandHandler('start', start_command))

#     # Messages
#     app.add_handler(MessageHandler(filters.TEXT, handle_message))

#     # Errors
#     app.add_error_handler(error)

#     # print('Polling...')
#     app.run_polling(poll_interval=3)

########################################################################################################

# import requests
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# import os
# import logging
# from telegram.error import TimedOut
# import time

# # Set up logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Constants
# BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'
# BOT_VERSION = "v2.3"
# VIDEO_PATH = "./BirthdayCardGenerator/birthday_card.mp4"

# # Commands


# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         f'Hello, I am Jarvis (version {BOT_VERSION}), your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
#     )


# async def test_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await send_video(update, context, VIDEO_PATH)


# def remove_escape_characters(text: str) -> str:
#     return text.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\').replace('\\"', '"')

# # Responses


# def handle_response(text: str) -> dict:
#     # For testing purposes, always return a video response
#     return {
#         "type": "video",
#         "content": VIDEO_PATH
#     }
#     # Uncomment the below lines and comment out the above return statement when you want to use the actual API
#     # response = requests.get(f"http://127.0.0.1:8000/Jarvis?request={text}")
#     # response_json = response.json()
#     # return response_json


# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     message_type = update.message.chat.type
#     text = update.message.text
#     if message_type == 'private':
#         try:
#             response = handle_response(text)

#             if response.get('type') == 'text':
#                 await update.message.reply_text(remove_escape_characters(response['content']))
#             elif response.get('type') == 'video':
#                 await send_video(update, context, response['content'])
#             else:
#                 await update.message.reply_text("Sorry, I don't know how to handle this response type.")
#         except Exception as e:
#             logger.error(f"Error in handle_message: {str(e)}", exc_info=True)
#             await update.message.reply_text(f"An error occurred while processing your message: {str(e)}")


# async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_path: str):
#     try:
#         # Check if the file exists
#         if not os.path.exists(video_path):
#             logger.error(f"Video file not found: {video_path}")
#             await update.message.reply_text(f"Sorry, I couldn't find the video file at {video_path}.")
#             return

#         # Check file size
#         file_size = os.path.getsize(video_path)
#         logger.info(
#             f"Attempting to send video: {video_path}, Size: {file_size} bytes")

#         if file_size > 50 * 1024 * 1024:  # 50MB in bytes
#             await update.message.reply_text("The video file is too large to send (>50MB).")
#             return

#         # Check file permissions
#         if not os.access(video_path, os.R_OK):
#             logger.error(f"No read permission for file: {video_path}")
#             await update.message.reply_text("Sorry, I don't have permission to read the video file.")
#             return

#         # Attempt to send the video
#         start_time = time.time()
#         with open(video_path, 'rb') as video_file:
#             await context.bot.send_video(
#                 chat_id=update.effective_chat.id,
#                 video=video_file,
#                 filename=os.path.basename(video_path),
#                 read_timeout=300,  # 5 minutes
#                 write_timeout=300,  # 5 minutes
#                 connect_timeout=60
#             )
#         end_time = time.time()
#         logger.info(
#             f"Video sent successfully. Time taken: {end_time - start_time:.2f} seconds")

#     except TimedOut as e:
#         logger.error(
#             f"Timeout error while sending video: {str(e)}", exc_info=True)
#         await update.message.reply_text("The video upload timed out. Please try again or contact the bot administrator.")
#     except Exception as e:
#         logger.error(f"Error in send_video: {str(e)}", exc_info=True)
#         await update.message.reply_text(f"An error occurred while sending the video: {str(e)}")

# # Errors


# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     logger.error(
#         f"Update {update} caused error {context.error}", exc_info=True)
#     await update.message.reply_text(f'An error occurred: {context.error}')

# # Main
# if __name__ == '__main__':
#     app = Application.builder().token(BOT_TOKEN).build()

#     # Commands
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('testvideo', test_video_command))

#     # Messages
#     app.add_handler(MessageHandler(filters.TEXT, handle_message))

#     # Errors
#     app.add_error_handler(error)

#     print(f'Starting bot version {BOT_VERSION}...')
#     # Print the absolute path of the video file
#     print(f"Video file path: {os.path.abspath(VIDEO_PATH)}")
#     app.run_polling(poll_interval=3)

########################################################################################################

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from telegram.error import TimedOut
import time

# Constants
BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'
VIDEO_PATH = "./BirthdayCardGenerator/birthday_card.mp4"

# Commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello, I am your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
    )


async def test_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_video(update, context, VIDEO_PATH)


def remove_escape_characters(text: str) -> str:
    return text.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\').replace('\\"', '"')

# Responses


def handle_response(text: str) -> dict:
    # response = requests.get(f"http://127.0.0.1:8000/Jarvis?request={text}")
    # response_json = response.json()
    # return response_json

    # For testing purposes, always return a video response
    return {
        "type": "video",
        "content": VIDEO_PATH
        # "type": "text",
        # "content": "Hi"
    }


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # Send a "Loading response" message to the user and store the message object
    loading_message = await update.message.reply_text("Loading response...")

    try:
        response = handle_response(text)

        if response.get('type') == 'text':
            # Edit the "Loading response" message with the actual response
            await loading_message.edit_text(remove_escape_characters(response['content']))
        elif response.get('type') == 'video':
            # Edit the "Loading response" message and then send the video
            await loading_message.edit_text("Sending video...")
            await send_video(update, context, response['content'])
        else:
            await loading_message.edit_text("Sorry, I don't know how to handle this response type.")
    except Exception as e:
        await loading_message.edit_text(f"An error occurred while processing your message: {str(e)}")


async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_path: str):
    try:
        if not os.path.exists(video_path):
            await update.message.reply_text(f"Sorry, I couldn't find the video file at {video_path}.")
            return

        file_size = os.path.getsize(video_path)
        if file_size > 50 * 1024 * 1024:  # 50MB in bytes
            await update.message.reply_text("The video file is too large to send (>50MB).")
            return

        with open(video_path, 'rb') as video_file:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video_file,
                filename=os.path.basename(video_path),
                read_timeout=300,  # 5 minutes
                write_timeout=300,  # 5 minutes
                connect_timeout=60
            )
    except TimedOut as e:
        await update.message.reply_text("The video upload timed out. Please try again or contact the bot administrator.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while sending the video: {str(e)}")

# Errors


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'An error occurred: {context.error}')

# Main
if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('testvideo', test_video_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    app.run_polling(poll_interval=3)
