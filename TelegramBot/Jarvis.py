# if using mac, need to perform: "brew install ffmpeg"
import json

import telegram
from moviepy.editor import ImageSequenceClip
import requests
import re
from datetime import datetime, timedelta
from telegram import Update
import pytz
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TimedOut
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np

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
VIDEO_PATH = "../BirthdayCardGenerator/birthday_card.mp4"
TEXT_FILE_PATH = "../BirthdayCardGenerator/birthday_message.txt"
VOICE_DOWNLOAD_PATH = "./voice_messages/"
ISRAEL_TZ = pytz.timezone('Asia/Jerusalem')


# Helper Functions
def parse_reminder(text: str):
    match = re.search(
        r"remind me to (.+) at (\d{2}:\d{2})", text, re.IGNORECASE)
    if match:
        task = match.group(1)
        time_str = match.group(2)
        return task, time_str
    return None, None


def get_time_difference(time_str):
    now = datetime.now(ISRAEL_TZ)
    # format = '%d %b %Y %H:%M:%S'
    reminder_time = ISRAEL_TZ.localize(datetime.strptime(
        time_str, "%H:%M").replace(year=now.year, month=now.month, day=now.day))
    if reminder_time < now:
        reminder_time += timedelta(days=1)
    return (reminder_time - now).total_seconds()


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    print(job)
    await context.bot.send_message(job.chat_id, text=f"⏰ Reminder: {job.data['task']}")


# Ensure voice messages directory exists
os.makedirs(VOICE_DOWNLOAD_PATH, exist_ok=True)


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, I am Jarvis, your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?')


async def test_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide the name for the birthday card.")
    context.user_data['awaiting_name'] = True


async def start_auth_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['authenticated'] = False
    uid = str(update.effective_user.id)
    if uid:
        response = requests.get(
            f"http://127.0.0.1:8000/Jarvis/start_auth_flow?uid={uid}")
        auth_url = response.text
        context.user_data['awaiting_auth_code'] = True
        await update.message.reply_text(f"Please click the following link to authenticate: {auth_url}\n\nOnce you have authenticated, please go to the url, copy the code, and send it here.")
    else:
        context.user_data['awaiting_auth_code'] = False
        context.user_data['authenticated'] = False
        await update.message.reply_text("Sorry, I couldn't find your user ID.")


async def finish_auth_flow(update: Update, context: ContextTypes.DEFAULT_TYPE, auth_code: str, loading_message: telegram.Message):
    uid = str(update.effective_user.id)
    if uid:
        response = requests.get(
            f"http://127.0.0.1:8000/Jarvis/finish_auth_flow?uid={uid}&code={auth_code}")
        if response.text:
            await loading_message.edit_text("Authentication was successful!\nNow checking the validity of your credentials...")
            await setup_credentials(update, context, uid)
        else:
            context.user_data['authenticated'] = False
            await loading_message.edit_text("Authentication failed. Please try again.")
    else:
        context.user_data['authenticated'] = False
        await loading_message.edit_text("Sorry, I couldn't find your user ID.")


async def setup_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE, uid: str):
    response = requests.get(
        f"http://127.0.0.1:8000/Jarvis/setup_credentials?uid={uid}")
    if response.text:
        await update.message.reply_text("Credentials setup successfully!")
        context.user_data['authenticated'] = True
    else:
        await update.message.reply_text("Failed to setup credentials. Please try again.")
        context.user_data['authenticated'] = False


# New function to handle voice messages
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


# Responses
def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> str:
    uid = str(update.effective_user.id)
    if uid:
        response = requests.get(
            f"http://127.0.0.1:8000/Jarvis/get_response?request={text}&uid={uid}")
        # return response.text.strip('"')  # Clean up the response text
        response_text = response.text.strip('"')
        formatted_response = response_text.replace("\\n", "\n")
        return formatted_response
    else:
        return "Sorry, I couldn't find your user ID."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Send a "Loading response" message to the user and store the message object
    loading_message = await update.message.reply_text("Loading response...")

    try:
        if context.user_data.get('awaiting_auth_code'):
            context.user_data['awaiting_auth_code'] = False
            await finish_auth_flow(update, context, text, loading_message)

        elif context.user_data.get('awaiting_name'):
            context.user_data['awaiting_name'] = False

            # Edit loading message before generating birthday text
            await loading_message.edit_text("Generating birthday message...")
            await generate_birthday_text(update, context, text)

            # Edit loading message before generating video
            await loading_message.edit_text("Creating birthday video...")
            await generate_video(update, context)

            # Send the video and edit the loading message again
            await send_video(update, context, VIDEO_PATH)
            await loading_message.edit_text("Video sent!")

        else:
            task, time_str = parse_reminder(text)

            if task and time_str:
                seconds_until_reminder = get_time_difference(time_str)
                if seconds_until_reminder > 0:
                    # Adding the job to the queue
                    job = context.job_queue.run_once(
                        send_reminder, seconds_until_reminder, chat_id=update.message.chat_id, name=f"reminder_{task}", data={"task": task})
                    print(job)

                    # Edit loading message before sending reminder confirmation
                    await loading_message.edit_text(f"Reminder set for {time_str} to: {task}!")
                else:
                    await loading_message.edit_text("The time you provided is in the past. Please provide a future time.")
            else:
                # Edit loading message before handling generic response
                if context.user_data.get('authenticated'):
                    response = handle_response(update, context, text)
                    await loading_message.edit_text(response)
                else:
                    await loading_message.edit_text("Sorry, you need to authenticate first. Please use the /authentication command.")

    except Exception as e:
        await loading_message.edit_text(f"An error occurred while processing your message: {str(e)}")


async def generate_birthday_text(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str):
    prompt = f"""Generate a heartfelt and creative birthday message for {name}.
    The message should be totally generic so it could fit anyone.
    The message should always start with Happy birthday {name}!
    The message should be no more than 5 lines (not including the starting line).
    Make sure that each line is not longer than 75 characters.
    Do not add an ending to the message like: Best wishes... From...
    Seperate each line."""

    try:
        messages = [
            {"role": "system", "content": "You are a birthday card generator."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )

        birthday_message = response.choices[0].message.content.strip()

        with open(TEXT_FILE_PATH, 'w') as f:
            f.write(birthday_message)

        await update.message.reply_text(f"Birthday message generated: {birthday_message}")

    except Exception as e:
        await update.message.reply_text(f"Error generating birthday text: {str(e)}")


async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Generating video, please wait...")

        def get_birthday_message(file_path: str) -> str:
            try:
                with open(file_path, 'r') as file:
                    return file.read().strip()
            except Exception as e:
                print(f"Error reading the text file: {e}")
                return "Happy Birthday!"

        birthday_message = get_birthday_message(TEXT_FILE_PATH)

        def create_confetti(width: int, height: int, num_particles: int) -> list:
            confetti = []
            for _ in range(num_particles):
                x = random.randint(0, width)
                y = random.randint(0, height)
                size = random.randint(10, 30)
                color = (random.randint(0, 255), random.randint(
                    0, 255), random.randint(0, 255))
                confetti.append((x, y, size, color))
            return confetti

        def create_frame(base_image: Image, confetti: list, frame_number: int) -> np.ndarray:
            frame_array = base_image.copy()
            draw_element = ImageDraw.Draw(frame_array)

            for x, y, size, color in confetti:
                wrapped_y = (y + frame_number *
                             10) % (frame_array.height + size)
                draw_element.rectangle(
                    [x, wrapped_y, x + size, wrapped_y + size], fill=color)

            return np.array(frame_array)

        images = ['../BirthdayCardGenerator/Blue.jpg', '../BirthdayCardGenerator/Green.jpg', '../BirthdayCardGenerator/Orange.jpg',
                  '../BirthdayCardGenerator/Pink.jpg', '../BirthdayCardGenerator/Purple.jpg', '../BirthdayCardGenerator/Red.jpg',
                  '../BirthdayCardGenerator/LightBlue.jpg']
        base_image = Image.open(random.choice(images))

        draw = ImageDraw.Draw(base_image)

        font_path = "BirthdayCardGenerator/Rubik-VariableFont_wght.ttf"
        font_size_first_line = 200
        font_size_remaining_text = 140

        font_first_line = ImageFont.truetype(font_path, font_size_first_line)
        font_remaining_text = ImageFont.truetype(
            font_path, font_size_remaining_text)

        img_width, img_height = base_image.size

        lines = birthday_message.split("\n", 1)
        first_line = lines[0]
        remaining_text = lines[1] if len(lines) > 1 else ""

        first_line_bbox = draw.textbbox(
            (0, 0), first_line, font=font_first_line)
        first_line_width = first_line_bbox[2] - first_line_bbox[0]
        first_line_height = first_line_bbox[3] - first_line_bbox[1]

        first_line_position = (
            (img_width - first_line_width) // 2, img_height // 5)

        draw.text(first_line_position, first_line,
                  font=font_first_line, fill="white")

        if remaining_text:
            remaining_lines = remaining_text.split("\n")
            line_spacing = 30
            extra_space_between_first_and_remaining = 250

            remaining_text_position = (
                first_line_position[0],
                first_line_position[1] + first_line_height +
                extra_space_between_first_and_remaining
            )

            for idx, line in enumerate(remaining_lines):
                line_bbox = draw.textbbox(
                    (0, 0), line, font=font_remaining_text)
                line_width = line_bbox[2] - line_bbox[0]
                line_position = (
                    (img_width - line_width) // 2,
                    remaining_text_position[1] + idx *
                    (font_size_remaining_text + line_spacing)
                )

                draw.text(line_position, line,
                          font=font_remaining_text, fill="white")

        confetti = create_confetti(img_width, img_height, 100)

        frames = []
        for i in range(300):
            frame = create_frame(base_image, confetti, i)
            frames.append(frame)

        clip = ImageSequenceClip(frames, fps=30)
        clip.write_videofile(VIDEO_PATH)

        await update.message.reply_text("Video generated successfully!")

    except Exception as e:
        await update.message.reply_text(f"Error generating video: {str(e)}")


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

            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(TEXT_FILE_PATH):
                os.remove(TEXT_FILE_PATH)

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

    # Handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('testvideo', test_video_command))
    app.add_handler(CommandHandler('authentication', start_auth_flow))
    # Add voice handler
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    # Add text handler
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))
    # Errors
    app.add_error_handler(error)

    app.run_polling(poll_interval=3)
