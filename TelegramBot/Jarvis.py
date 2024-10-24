# if using mac, need to perform: "brew install ffmpeg"
import json
import telegram
from moviepy.editor import ImageSequenceClip
import requests
from datetime import datetime, timedelta, time
from telegram import Update
import pytz
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder, \
    JobQueue
from telegram.error import TimedOut
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
import urllib.parse

import os

os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/opt/ffmpeg/bin/ffmpeg"

with open('../config.json') as config_file:
    config = json.load(config_file)

# Initialize the OpenAI client
client = OpenAI(
    api_key=config["OPEN_AI_API_KEY"]
)

# Constants
BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
VIDEO_PATH = "../API/BirthdayCardGenerator/birthday_card.mp4"
VOICE_DOWNLOAD_PATH = "./voice_messages/"
ISRAEL_TZ = pytz.timezone('Asia/Jerusalem')

# Ensure voice messages directory exists
os.makedirs(VOICE_DOWNLOAD_PATH, exist_ok=True)


# Helper Functions
async def update_authentication_user_data_based_on_setup_credentials(uid: str, context: ContextTypes.DEFAULT_TYPE):
    credentials_already_setup = await setup_credentials(uid)

    if credentials_already_setup:
        context.user_data['authenticated'] = True
        context.user_data['awaiting_auth_url'] = False
    else:
        context.user_data['authenticated'] = False
        context.user_data['awaiting_name'] = False


def process_api_response(response: requests.Response) -> str:
    if response.status_code == 200:
        response_text = response.text.strip('"')
        formatted_response = response_text.replace("\\n", "\n")
        return formatted_response
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


def add_job_to_queue(context: ContextTypes.DEFAULT_TYPE, callback, when: float | timedelta | datetime | time,
                     chat_id: int, name: str = None, data: dict = None):
    context.job_queue.run_once(
        callback,
        when=when,
        chat_id=chat_id,
        name=name,
        data=data
    )


async def stuff_before_each_response(uid: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    await make_sure_user_exists(uid)
    await update_authentication_user_data_based_on_setup_credentials(uid, context)


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_chat.id)
    await stuff_before_each_response(uid, context)

    if not context.user_data.get('authenticated'):
        await update.message.reply_text("Please authenticate first using the /authentication command.")
        return

    await update.message.reply_text(
        'Hello, I am Jarvis, your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?')


async def birthday_card_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_chat.id)
    await stuff_before_each_response(uid, context)

    if not context.user_data.get('authenticated'):
        await update.message.reply_text("Please authenticate first using the /authentication command.")
        return

    await update.message.reply_text("Please provide the name for the birthday card.")
    context.user_data['awaiting_name'] = True


async def hourly_events_reminder(context: ContextTypes.DEFAULT_TYPE):

    uid = context.job.chat_id

    response = requests.get(
        f"http://127.0.0.1:8000/Jarvis/get_two_hour_range_events?uid={str(uid)}")

    if response.text != "null":
        processed_response = process_api_response(response)
        await context.bot.send_message(uid, text=processed_response)

    # Schedule the next message
    add_job_to_queue(
        context=context,
        callback=hourly_events_reminder,
        when=timedelta(hours=1),
        chat_id=uid
    )


async def start_hourly_events_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = str(update.effective_chat.id)
    await stuff_before_each_response(uid, context)

    if not context.user_data.get('authenticated'):
        await update.message.reply_text("Please authenticate first using the /authentication command.")
        return

    add_job_to_queue(
        context=context,
        callback=hourly_events_reminder,
        when=0,  # == now
        chat_id=update.effective_chat.id
    )


async def daily_uncompleted_tasks_reminder(context: ContextTypes.DEFAULT_TYPE):
    uid = context.job.chat_id

    response = requests.get(
        f"http://127.0.0.1:8000/Jarvis/get_all_uncompleted_tasks?uid={str(uid)}")

    if response.text != "null":
        processed_response = process_api_response(response)
        await context.bot.send_message(uid, text=processed_response)

        # Calculate time until next 10:00 AM
        now = datetime.now(ISRAEL_TZ)
        target_time = now.replace(hour=10, minute=0, second=0, microsecond=0)

        if now >= target_time:
            target_time += timedelta(days=1)

        # Schedule the next message
        add_job_to_queue(
            context=context,
            callback=daily_uncompleted_tasks_reminder,
            when=target_time,
            chat_id=uid
        )


async def start_daily_uncompleted_tasks_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    uid = str(update.effective_chat.id)
    await stuff_before_each_response(uid, context)

    if not context.user_data.get('authenticated'):
        await update.message.reply_text("Please authenticate first using the /authentication command.")
        return

    add_job_to_queue(
        context=context,
        callback=daily_uncompleted_tasks_reminder,
        when=0,  # == now
        chat_id=update.effective_chat.id
    )


async def start_auth_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['authenticated'] = False
    uid = str(update.effective_user.id)
    if uid:
        response = requests.get(
            f"http://127.0.0.1:8000/Jarvis/start_auth_flow?uid={uid}")
        auth_url = process_api_response(response)
        context.user_data['awaiting_auth_url'] = True
        await update.message.reply_text(
            f"Please click the following link to authenticate via google: {auth_url}\n\nOnce you have been redirected, please copy the full url, and send it here.")
    else:
        context.user_data['awaiting_auth_url'] = False
        context.user_data['authenticated'] = False
        await update.message.reply_text("Sorry, I couldn't find your user ID.")


async def finish_auth_flow(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str,
                           loading_message: telegram.Message):
    uid = str(update.effective_user.id)
    if uid:
        encoded_url = urllib.parse.quote(url, safe='')
        response = requests.get(
            f"http://127.0.0.1:8000/Jarvis/finish_auth_flow",
            params={"uid": uid, "encoded_url": encoded_url} # Using params for passing the long full encoded_url
        )
        processed_response = process_api_response(response)
        response_as_bool = eval(processed_response.lower().capitalize())

        if response_as_bool:
            await loading_message.edit_text(
                "Authentication was successful!\nNow checking the validity of your credentials...")

            authenticated = await setup_credentials(uid)

            if authenticated:
                await update.message.reply_text("Credentials are valid!\nLet's start chatting!")
                context.user_data['authenticated'] = True
                await start_hourly_events_reminder(update, context)
                await start_daily_uncompleted_tasks_reminder(update, context)
            else:
                await update.message.reply_text("Failed to setup credentials. Please try to use the /authentication command again.")
                context.user_data['authenticated'] = False
        else:
            context.user_data['authenticated'] = False
            await loading_message.edit_text("Authentication failed. Please try to use the /authentication command again.")

    else:
        context.user_data['authenticated'] = False
        await loading_message.edit_text("Sorry, I couldn't find your user ID.")


async def setup_credentials(uid: str) -> bool:
    response = requests.get(
        f"http://127.0.0.1:8000/Jarvis/setup_credentials?uid={uid}")
    processed_response = process_api_response(response)
    return eval(processed_response.lower().capitalize())


async def make_sure_user_exists(uid: str) -> bool:
    response = requests.get(
        f"http://127.0.0.1:8000/Jarvis/make_sure_user_exists?uid={uid}")
    processed_response = process_api_response(response)
    return eval(processed_response.lower().capitalize())


# Handle voice messages
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Inform user that processing is starting
        await update.message.reply_text("I received your voice message. Processing...")

        # Get voice message file
        voice_file = await context.bot.get_file(update.message.voice.file_id)

        # Generate unique filename
        file_name = f"{VOICE_DOWNLOAD_PATH}{update.message.voice.file_id}.ogg"

        # Download voice message
        await voice_file.download_to_drive(file_name)

        # Transcribe with Whisper
        with open(file_name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # Process transcribed text
        transcribed_text = transcript.text
        response = handle_response(update, context, transcribed_text)
        await update.message.reply_text(response)

        # Log the voice message event
        user_id = str(update.effective_user.id)
        event_data = {
            "user_id": user_id,
            "event_name": "voice_message_transcribed",
            "event_details": f"Voice message transcribed for user {user_id}: {transcribed_text}"
        }
        response = requests.post(
            "http://127.0.0.1:8000/Jarvis/log_event", json=event_data)
        if response.status_code == 200:
            print("Event logged successfully")
        else:
            print(f"Failed to log event: {response.text}")

        # Clean up: delete the voice file
        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"Sorry, there was an error processing your voice message: {str(e)}")


# Assistant Response
def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> str:
    uid = str(update.effective_user.id)
    if uid:
        response = requests.get(
            f"http://127.0.0.1:8000/Jarvis/get_response?request={text}&uid={uid}")
        return process_api_response(response)
    else:
        return "Sorry, I couldn't find your user ID."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = str(update.effective_user.id)
    await stuff_before_each_response(uid, context)

    # Send a "Loading response" message to the user and store the message object
    loading_message = await update.message.reply_text("Loading response...")

    try:

        if context.user_data.get('awaiting_name'):
            context.user_data['awaiting_name'] = False

            # Edit loading message before generating birthday text
            await loading_message.edit_text("Generating birthday card video...\nPlease wait.")
            await generate_birthday_video(text)

            # Send the video and edit the loading message again
            await send_video(update, context, VIDEO_PATH)

        elif context.user_data.get('authenticated'):
            response = handle_response(update, context, text)
            await loading_message.edit_text(response)

        elif context.user_data.get('awaiting_auth_url'):
            context.user_data['awaiting_auth_url'] = False
            await finish_auth_flow(update, context, text, loading_message)


        else:
            await loading_message.edit_text(
                "Sorry, you need to authenticate first. Please use the /authentication command.")

    except Exception as e:
        await loading_message.edit_text(f"An error occurred while processing your message: {str(e)}")

async def generate_birthday_video(name: str):

    response = requests.get(
        f"http://127.0.0.1:8000/Jarvis/generate_birthday_video?name={name}")
    processed_response = process_api_response(response)
    response_as_bool = eval(processed_response.lower().capitalize())

    if not response_as_bool:
        raise Exception("Failed to generate birthday video")

async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_path: str):
    try:
        if not os.path.exists(video_path):
            await update.message.reply_text(f"Sorry, I couldn't find the video file at {video_path}.")
            return

        file_size = os.path.getsize(video_path)
        if file_size > 50 * 1024 * 1024:
            await update.message.reply_text("The video file is too large to send (>50MB).")
            return

        with open(video_path, 'rb') as video_file:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=video_file,
                filename=os.path.basename(video_path),
                read_timeout=300,
                write_timeout=300,
                connect_timeout=60
            )

            # Clean up: delete the video file
            if os.path.exists(video_path):
                os.remove(video_path)

            # Send API request to log the event
            user_id = str(update.effective_user.id)
            event_data = {
                "user_id": user_id,
                "event_name": "birthday_video_sent",
                "event_details": f"Birthday card video sent to {user_id}"
            }
            response = requests.post(
                "http://127.0.0.1:8000/Jarvis/log_event", json=event_data)
            if response.status_code == 200:
                print("Event logged successfully")
            else:
                print(f"Failed to log event: {response.text}")

    except TimedOut as e:
        await update.message.reply_text(
            "The video upload timed out. Please try again or contact the bot administrator.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while sending the video: {str(e)}")


# Errors
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:

    # Check if 'update' is an instance of Update
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("An error occurred while processing your request.")
    elif context.bot_data:
        # If we can't reply to the message, at least log to a default chat if set
        default_chat_id = context.bot_data.get("default_error_chat")
        if default_chat_id:
            await context.bot.send_message(chat_id=default_chat_id, text=f"An error occurred: {context.error}")


# Main
if __name__ == '__main__':
    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .job_queue(JobQueue())
        .build()
    )

    # Handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('birthday_card', birthday_card_command))
    app.add_handler(CommandHandler('authenticate', start_auth_flow))
    # Add voice handler
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    # Add text handler
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))
    # Errors
    app.add_error_handler(error_handler)

    app.run_polling(poll_interval=3)
