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

# import requests
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# import os
# from telegram.error import TimedOut
# import time

# # Constants
# BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'
# VIDEO_PATH = "./BirthdayCardGenerator/compressed_birthday_card.mp4"

# # Commands


# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         'Hello, I am your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
#     )


# async def test_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await send_video(update, context, VIDEO_PATH)


# def remove_escape_characters(text: str) -> str:
#     return text.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\').replace('\\"', '"')

# # Responses


# def handle_response(text: str) -> dict:
#     # response = requests.get(f"http://127.0.0.1:8000/Jarvis?request={text}")
#     # response_json = response.json()
#     # return response_json

#     # For testing purposes, always return a video response
#     return {
#         "type": "video",
#         "content": VIDEO_PATH
#         # "type": "text",
#         # "content": "Hi"
#     }


# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     # Send a "Loading response" message to the user and store the message object
#     loading_message = await update.message.reply_text("Loading response...")

#     try:
#         response = handle_response(text)

#         if response.get('type') == 'text':
#             # Edit the "Loading response" message with the actual response
#             await loading_message.edit_text(remove_escape_characters(response['content']))
#         elif response.get('type') == 'video':
#             # Edit the "Loading response" message and then send the video
#             await loading_message.edit_text("Sending video...")
#             await send_video(update, context, response['content'])
#         else:
#             await loading_message.edit_text("Sorry, I don't know how to handle this response type.")
#     except Exception as e:
#         await loading_message.edit_text(f"An error occurred while processing your message: {str(e)}")


# async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_path: str):
#     try:
#         if not os.path.exists(video_path):
#             await update.message.reply_text(f"Sorry, I couldn't find the video file at {video_path}.")
#             return

#         file_size = os.path.getsize(video_path)
#         if file_size > 50 * 1024 * 1024:  # 50MB in bytes
#             await update.message.reply_text("The video file is too large to send (>50MB).")
#             return

#         with open(video_path, 'rb') as video_file:
#             await context.bot.send_video(
#                 chat_id=update.effective_chat.id,
#                 video=video_file,
#                 filename=os.path.basename(video_path),
#                 read_timeout=300,  # 5 minutes
#                 write_timeout=300,  # 5 minutes
#                 connect_timeout=60
#             )
#     except TimedOut as e:
#         await update.message.reply_text("The video upload timed out. Please try again or contact the bot administrator.")
#     except Exception as e:
#         await update.message.reply_text(f"An error occurred while sending the video: {str(e)}")

# # Errors


# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

#     app.run_polling(poll_interval=3)
###############################################################################################

# import requests
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# import os
# from telegram.error import TimedOut
# import time
# import openai
# import json
# from openai import OpenAI

# # Initialize the OpenAI client
# client = OpenAI(
#     api_key="sk-dWq6WusvsEyySkgOjUa3ZUUv6LadNaNeCs35GZ8H6sT3BlbkFJMWTn7nLmAo0GH4S9F6DxAwwd5l8lxL49oeJCIAH8EA")

# # Constants
# BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'
# VIDEO_PATH = "./BirthdayCardGenerator/compressed_birthday_card.mp4"

# # Commands


# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         'Hello, I am your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
#     )


# # Inside /testvideo command
# async def test_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Please provide the name for the birthday card.")
#     # Set a flag that indicates we're waiting for the name input
#     context.user_data['awaiting_name'] = True


# # Define a new handler to check for name input and generate birthday text
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Check if we are waiting for the user's name
#     if context.user_data.get('awaiting_name'):
#         name = update.message.text
#         # Store the name and clear the flag
#         context.user_data['name'] = name
#         context.user_data['awaiting_name'] = False  # Reset the flag

#         # Call OpenAI API to generate birthday card text
#         await generate_birthday_text(update, context, name)

#         # Send the video after the text has been saved
#     #     await send_video(update, context, VIDEO_PATH)
#     # else:
#     #     # Handle other messages as usual
#     #     text = update.message.text
#     #     await update.message.reply_text(f"You said: {text}")


# async def generate_birthday_text(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> str:
#     prompt = f"""Generate a heartfelt and creative birthday message for {name}.
#     The message should be totally generic so it could fit anyone.
#     The message should always start with Happy birthday {name}!
#     The message should be no more than 5 lines (not including the starting line).
#     Do not add an ending to the message like: Best wishes... From...
#     Seperate each line."""

#     try:
#         # Create a message to send to the AI
#         messages = [
#             {"role": "system", "content": "You are a birthday card generator."},
#             {"role": "user", "content": prompt}
#         ]

#         # Call the OpenAI API to get the birthday message
#         response = client.chat.completions.create(
#             model="gpt-4",  # Ensure you're using the correct model
#             messages=messages,
#             temperature=0.7  # Adjust temperature for creativity
#         )

#         # Extract the generated text
#         birthday_message = response.choices[0].message.content.strip()

#         # Save the generated text to a file
#         file_path = f"./BirthdayCardGenerator/birthday_message.txt"
#         with open(file_path, 'w') as f:
#             f.write(birthday_message)

#         # Notify the user that the message was generated
#         await update.message.reply_text(f"{birthday_message}")

#     except Exception as e:
#         await update.message.reply_text(f"Error generating birthday text: {str(e)}")


# async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_path: str):
#     try:
#         if not os.path.exists(video_path):
#             await update.message.reply_text(f"Sorry, I couldn't find the video file at {video_path}.")
#             return

#         file_size = os.path.getsize(video_path)
#         if file_size > 50 * 1024 * 1024:  # 50MB in bytes
#             await update.message.reply_text("The video file is too large to send (>50MB).")
#             return

#         with open(video_path, 'rb') as video_file:
#             await context.bot.send_video(
#                 chat_id=update.effective_chat.id,
#                 video=video_file,
#                 filename=os.path.basename(video_path),
#                 read_timeout=300,  # 5 minutes
#                 write_timeout=300,  # 5 minutes
#                 connect_timeout=60
#             )
#     except TimedOut as e:
#         await update.message.reply_text("The video upload timed out. Please try again or contact the bot administrator.")
#     except Exception as e:
#         await update.message.reply_text(f"An error occurred while sending the video: {str(e)}")


# # Errors
# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

#     app.run_polling(poll_interval=3)
###############################################################################################

# import requests
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# import os
# from telegram.error import TimedOut
# import time
# import openai
# import json
# from openai import OpenAI
# from PIL import Image, ImageDraw, ImageFont
# import random
# import numpy as np
# from moviepy.editor import ImageSequenceClip
# import ffmpeg

# # Initialize the OpenAI client
# client = OpenAI(
#     api_key="sk-dWq6WusvsEyySkgOjUa3ZUUv6LadNaNeCs35GZ8H6sT3BlbkFJMWTn7nLmAo0GH4S9F6DxAwwd5l8lxL49oeJCIAH8EA")

# # Constants
# BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'
# # VIDEO_PATH = "./BirthdayCardGenerator/compressed_birthday_card.mp4"
# VIDEO_PATH = "./BirthdayCardGenerator/birthday_card.mp4"
# TEXT_FILE_PATH = "./BirthdayCardGenerator/birthday_message.txt"

# # Commands


# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         'Hello, I am your personal assistant. I can help you with a variety of tasks and answer your questions. What can I do for you?'
#     )


# async def test_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Please provide the name for the birthday card.")
#     context.user_data['awaiting_name'] = True


# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if context.user_data.get('awaiting_name'):
#         name = update.message.text
#         context.user_data['name'] = name
#         context.user_data['awaiting_name'] = False

#         await generate_birthday_text(update, context, name)
#         await generate_video(update, context)
#         await send_video(update, context, VIDEO_PATH)
#     else:
#         text = update.message.text
#         await update.message.reply_text(f"You said: {text}")


# async def generate_birthday_text(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> str:
#     prompt = f"""Generate a heartfelt and creative birthday message for {name}.
#     The message should be totally generic so it could fit anyone.
#     The message should always start with Happy birthday {name}!
#     The message should be no more than 5 lines (not including the starting line).
#     Do not add an ending to the message like: Best wishes... From...
#     Seperate each line."""

#     try:
#         messages = [
#             {"role": "system", "content": "You are a birthday card generator."},
#             {"role": "user", "content": prompt}
#         ]

#         response = client.chat.completions.create(
#             model="gpt-4",
#             messages=messages,
#             temperature=0.7
#         )

#         birthday_message = response.choices[0].message.content.strip()

#         with open(TEXT_FILE_PATH, 'w') as f:
#             f.write(birthday_message)

#         await update.message.reply_text(f"Birthday message generated: {birthday_message}")

#     except Exception as e:
#         await update.message.reply_text(f"Error generating birthday text: {str(e)}")


# async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         await update.message.reply_text("Generating video, please wait...")

#         # Video generation code (from the second file)
#         def get_birthday_message(file_path: str) -> str:
#             try:
#                 with open(file_path, 'r') as file:
#                     return file.read().strip()
#             except Exception as e:
#                 print(f"Error reading the text file: {e}")
#                 return "Happy Birthday!"

#         birthday_message = get_birthday_message(TEXT_FILE_PATH)

#         def create_confetti(width: int, height: int, num_particles: int) -> list[tuple[int, int, int, tuple[int, int, int]]]:
#             confetti = []
#             for _ in range(num_particles):
#                 x = random.randint(0, width)
#                 y = random.randint(0, height)
#                 size = random.randint(10, 30)
#                 color = (random.randint(0, 255), random.randint(
#                     0, 255), random.randint(0, 255))
#                 confetti.append((x, y, size, color))
#             return confetti

#         def create_frame(base_image: Image, confetti: list, frame_number: int) -> np.ndarray:
#             frame = base_image.copy()
#             draw = ImageDraw.Draw(frame)

#             for x, y, size, color in confetti:
#                 wrapped_y = (y + frame_number * 10) % (frame.height + size)
#                 draw.rectangle(
#                     [x, wrapped_y, x + size, wrapped_y + size], fill=color)

#             return np.array(frame)

#         images = ['BirthdayCardGenerator/Blue.jpg', 'BirthdayCardGenerator/Green.jpg', 'BirthdayCardGenerator/Orange.jpg',
#                   'BirthdayCardGenerator/Pink.jpg', 'BirthdayCardGenerator/Purple.jpg', 'BirthdayCardGenerator/Red.jpg', 'BirthdayCardGenerator/LightBlue.jpg']
#         base_image = Image.open(random.choice(images))

#         draw = ImageDraw.Draw(base_image)

#         font_path = "BirthdayCardGenerator/Rubik-VariableFont_wght.ttf"
#         font_size_first_line = 200
#         font_size_remaining_text = 140

#         font_first_line = ImageFont.truetype(font_path, font_size_first_line)
#         font_remaining_text = ImageFont.truetype(
#             font_path, font_size_remaining_text)

#         img_width, img_height = base_image.size

#         lines = birthday_message.split("\n", 1)
#         first_line = lines[0]
#         remaining_text = lines[1] if len(lines) > 1 else ""

#         first_line_bbox = draw.textbbox(
#             (0, 0), first_line, font=font_first_line)
#         first_line_width = first_line_bbox[2] - first_line_bbox[0]
#         first_line_height = first_line_bbox[3] - first_line_bbox[1]

#         first_line_position = (
#             (img_width - first_line_width) // 2, img_height // 5)

#         draw.text(first_line_position, first_line,
#                   font=font_first_line, fill="white")

#         if remaining_text:
#             remaining_lines = remaining_text.split("\n")
#             line_spacing = 30
#             extra_space_between_first_and_remaining = 250

#             remaining_text_position = (
#                 first_line_position[0], first_line_position[1] + first_line_height + extra_space_between_first_and_remaining)

#             for idx, line in enumerate(remaining_lines):
#                 line_bbox = draw.textbbox(
#                     (0, 0), line, font=font_remaining_text)
#                 line_width = line_bbox[2] - line_bbox[0]
#                 line_position = ((img_width - line_width) // 2,
#                                  remaining_text_position[1] + idx * (font_size_remaining_text + line_spacing))

#                 draw.text(line_position, line,
#                           font=font_remaining_text, fill="white")

#         confetti = create_confetti(img_width, img_height, 100)

#         frames = []
#         for i in range(300):
#             frame = create_frame(base_image, confetti, i)
#             frames.append(frame)

#         clip = ImageSequenceClip(frames, fps=30)

#         video_path = "BirthdayCardGenerator/birthday_card.mp4"
#         clip.write_videofile(video_path)

#         # compressed_video_path = VIDEO_PATH

#         # ffmpeg.input(video_path).output(
#         #     compressed_video_path,
#         #     vcodec='libx264',
#         #     crf=18,
#         #     preset='slow',
#         #     pix_fmt='yuv420p'
#         # ).run()

#         await update.message.reply_text("Video generated successfully!")

#     except Exception as e:
#         await update.message.reply_text(f"Error generating video: {str(e)}")


# async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE, video_path: str):
#     try:
#         if not os.path.exists(video_path):
#             await update.message.reply_text(f"Sorry, I couldn't find the video file at {video_path}.")
#             return

#         file_size = os.path.getsize(video_path)
#         if file_size > 50 * 1024 * 1024:
#             await update.message.reply_text("The video file is too large to send (>50MB).")
#             return

#         with open(video_path, 'rb') as video_file:
#             await context.bot.send_video(
#                 chat_id=update.effective_chat.id,
#                 video=video_file,
#                 filename=os.path.basename(video_path),
#                 read_timeout=300,
#                 write_timeout=300,
#                 connect_timeout=60
#             )
#     except TimedOut as e:
#         await update.message.reply_text("The video upload timed out. Please try again or contact the bot administrator.")
#     except Exception as e:
#         await update.message.reply_text(f"An error occurred while sending the video: {str(e)}")


# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(f'An error occurred: {context.error}')

# if __name__ == '__main__':
#     app = Application.builder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('testvideo', test_video_command))
#     app.add_handler(MessageHandler(filters.TEXT, handle_message))
#     app.add_error_handler(error)

#     app.run_polling(poll_interval=3)

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from telegram.error import TimedOut
import time
import openai
import json
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
from moviepy.editor import ImageSequenceClip
import ffmpeg

# Initialize the OpenAI client
client = OpenAI(
    api_key="sk-dWq6WusvsEyySkgOjUa3ZUUv6LadNaNeCs35GZ8H6sT3BlbkFJMWTn7nLmAo0GH4S9F6DxAwwd5l8lxL49oeJCIAH8EA")

# Constants
BOT_TOKEN = '7031319241:AAFkaIQ9kXdO4BNuOJUVlleyt40JHr1kR14'
VIDEO_PATH = "./BirthdayCardGenerator/birthday_card.mp4"
TEXT_FILE_PATH = "./BirthdayCardGenerator/birthday_message.txt"
VOICE_DOWNLOAD_PATH = "./voice_messages/"

# Ensure voice messages directory exists
os.makedirs(VOICE_DOWNLOAD_PATH, exist_ok=True)

# Commands


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello, I am your personal assistant. I can help you with a variety of tasks, answer your questions, and now I can also process voice messages! What can I do for you?'
    )


async def test_video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide the name for the birthday card.")
    context.user_data['awaiting_name'] = True

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
        await update.message.reply_text(f"I heard: {transcribed_text}")

        # Generate response using GPT
        messages = [
            {"role": "system", "content": "You are a helpful assistant responding to voice messages."},
            {"role": "user", "content": transcribed_text}
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )

        # Send response back to user
        await update.message.reply_text(response.choices[0].message.content)

        # Clean up: delete the voice file
        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"Sorry, there was an error processing your voice message: {str(e)}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_name'):
        name = update.message.text
        context.user_data['name'] = name
        context.user_data['awaiting_name'] = False

        await generate_birthday_text(update, context, name)
        await generate_video(update, context)
        await send_video(update, context, VIDEO_PATH)
    else:
        text = update.message.text
        await update.message.reply_text(f"You said: {text}")


async def generate_birthday_text(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> str:
    prompt = f"""Generate a heartfelt and creative birthday message for {name}.
    The message should be totally generic so it could fit anyone.
    The message should always start with Happy birthday {name}!
    The message should be no more than 5 lines (not including the starting line).
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
            frame = base_image.copy()
            draw = ImageDraw.Draw(frame)

            for x, y, size, color in confetti:
                wrapped_y = (y + frame_number * 10) % (frame.height + size)
                draw.rectangle(
                    [x, wrapped_y, x + size, wrapped_y + size], fill=color)

            return np.array(frame)

        images = ['BirthdayCardGenerator/Blue.jpg', 'BirthdayCardGenerator/Green.jpg', 'BirthdayCardGenerator/Orange.jpg',
                  'BirthdayCardGenerator/Pink.jpg', 'BirthdayCardGenerator/Purple.jpg', 'BirthdayCardGenerator/Red.jpg',
                  'BirthdayCardGenerator/LightBlue.jpg']
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
    except TimedOut as e:
        await update.message.reply_text("The video upload timed out. Please try again or contact the bot administrator.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred while sending the video: {str(e)}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'An error occurred: {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('testvideo', test_video_command))
    # Add voice handler
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    app.run_polling(poll_interval=3)
