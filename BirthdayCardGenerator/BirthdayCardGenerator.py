# Version 1 (regular image)
# from PIL import Image, ImageDraw, ImageFont
# import random
# import requests

# # Load a random image
# images = ['BirthdayCardGenerator/Blue.jpg', 'BirthdayCardGenerator/Green.jpg', 'BirthdayCardGenerator/Orange.jpg',
#           'BirthdayCardGenerator/Pink.jpg', 'BirthdayCardGenerator/Purple.jpg', 'BirthdayCardGenerator/Red.jpg', 'BirthdayCardGenerator/LightBlue.jpg']
# image = Image.open(random.choice(images))

# # Create an ImageDraw object to draw on the image
# draw = ImageDraw.Draw(image)

# # Specify the path to your Rubik font file
# font_path = "BirthdayCardGenerator/Rubik-VariableFont_wght.ttf"
# font_size = 200  # Adjust this value to make the font larger or smaller

# # Load the Rubik font
# font = ImageFont.truetype(font_path, font_size)

# # Define the text and its position
# text = "Happy Birthday!"

# # Get the size of the image
# img_width, img_height = image.size

# # Get the size of the text
# text_bbox = draw.textbbox((0, 0), text, font=font)
# text_width = text_bbox[2] - text_bbox[0]
# text_height = text_bbox[3] - text_bbox[1]

# # Calculate the position to center the text
# position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

# # Add text to image
# draw.text(position, text, font=font, fill="white")

# # Save the image
# image_path = 'BirthdayCardGenerator/birthday_card.png'
# image.save(image_path)

# # Upload the image to the temporary file upload website
# upload_url = "https://tmpfiles.org/api/v1/upload"
# with open(image_path, 'rb') as img_file:
#     files = {'file': img_file}
#     response = requests.post(upload_url, files=files)

# # Check if the upload was successful
# if response.status_code == 200:
#     json_response = response.json()
#     file_url = json_response.get('data', {}).get('url')
#     if file_url:
#         print(f"Image successfully uploaded: {file_url}")
#     else:
#         print("Failed to retrieve the file URL.")
# else:
#     print(f"Failed to upload image. Status code: {response.status_code}")

# Version 2 (animated GIF)
# from PIL import Image, ImageDraw, ImageFont
# import random


# def create_confetti(width, height, num_particles):
#     confetti = []
#     for _ in range(num_particles):
#         x = random.randint(0, width)
#         y = random.randint(0, height)
#         size = random.randint(5, 15)
#         color = (random.randint(0, 255), random.randint(
#             0, 255), random.randint(0, 255))
#         confetti.append((x, y, size, color))
#     return confetti


# def create_frame(base_image, confetti, frame_number):
#     frame = base_image.copy()
#     draw = ImageDraw.Draw(frame)

#     for x, y, size, color in confetti:
#         draw.rectangle([x, y + frame_number * 10, x + size,
#                        y + size + frame_number * 10], fill=color)

#     return frame


# # Load a random image
# images = ['BirthdayCardGenerator/Blue.jpg', 'BirthdayCardGenerator/Green.jpg', 'BirthdayCardGenerator/Orange.jpg',
#           'BirthdayCardGenerator/Pink.jpg', 'BirthdayCardGenerator/Purple.jpg', 'BirthdayCardGenerator/Red.jpg', 'BirthdayCardGenerator/LightBlue.jpg']
# base_image = Image.open(random.choice(images))

# # Create an ImageDraw object to draw on the image
# draw = ImageDraw.Draw(base_image)

# # Specify the path to your Rubik font file
# font_path = "BirthdayCardGenerator/Rubik-VariableFont_wght.ttf"
# font_size = 200

# # Load the Rubik font
# font = ImageFont.truetype(font_path, font_size)

# # Define the text
# text = "Happy Birthday!"

# # Get the size of the image
# img_width, img_height = base_image.size

# # Get the size of the text
# text_bbox = draw.textbbox((0, 0), text, font=font)
# text_width = text_bbox[2] - text_bbox[0]
# text_height = text_bbox[3] - text_bbox[1]

# # Calculate the position to center the text
# position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

# # Add text to image
# draw.text(position, text, font=font, fill="white")

# # Create confetti
# confetti = create_confetti(img_width, img_height, 100)

# # Create frames
# frames = []
# for i in range(20):  # Create 20 frames
#     frame = create_frame(base_image, confetti, i)
#     frames.append(frame)

# # Save as animated GIF
# frames[0].save('BirthdayCardGenerator/animated_birthday_card.gif',
#                save_all=True,
#                append_images=frames[1:],
#                duration=100,
#                loop=0)

# Version 3 (video)
# from PIL import Image, ImageDraw, ImageFont
# import random
# import numpy as np
# from moviepy.editor import ImageSequenceClip
# import ffmpeg  # Import ffmpeg-python


# def create_confetti(width: int, height: int, num_particles: int) -> list[tuple[int, int, int, tuple[int, int, int]]]:
#     confetti = []
#     for _ in range(num_particles):
#         x = random.randint(0, width)
#         y = random.randint(0, height)
#         size = random.randint(10, 30)
#         color = (random.randint(0, 255), random.randint(
#             0, 255), random.randint(0, 255))
#         confetti.append((x, y, size, color))
#     return confetti


# def create_frame(base_image: Image, confetti: list, frame_number: int) -> np.ndarray:
#     frame = base_image.copy()
#     draw = ImageDraw.Draw(frame)

#     for x, y, size, color in confetti:
#         wrapped_y = (y + frame_number * 10) % (frame.height + size)
#         draw.rectangle([x, wrapped_y, x + size, wrapped_y + size], fill=color)

#     return np.array(frame)


# # Load a random image
# images = ['BirthdayCardGenerator/Blue.jpg', 'BirthdayCardGenerator/Green.jpg', 'BirthdayCardGenerator/Orange.jpg',
#           'BirthdayCardGenerator/Pink.jpg', 'BirthdayCardGenerator/Purple.jpg', 'BirthdayCardGenerator/Red.jpg', 'BirthdayCardGenerator/LightBlue.jpg']
# base_image = Image.open(random.choice(images))

# # Create an ImageDraw object to draw on the image
# draw = ImageDraw.Draw(base_image)

# # Specify the path to your Rubik font file
# font_path = "BirthdayCardGenerator/Rubik-VariableFont_wght.ttf"
# font_size = 200

# # Load the Rubik font
# font = ImageFont.truetype(font_path, font_size)

# # Define the text
# text = "Happy Birthday!"

# # Get the size of the image
# img_width, img_height = base_image.size

# # Get the size of the text
# text_bbox = draw.textbbox((0, 0), text, font=font)
# text_width = text_bbox[2] - text_bbox[0]
# text_height = text_bbox[3] - text_bbox[1]

# # Calculate the position to center the text
# position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

# # Add text to image
# draw.text(position, text, font=font, fill="white")

# # Create confetti
# confetti = create_confetti(img_width, img_height, 100)

# # Create frames
# frames = []
# for i in range(300):  # Create 300 frames for a 10-second video at 30 fps
#     frame = create_frame(base_image, confetti, i)
#     frames.append(frame)

# # Convert frames to video
# clip = ImageSequenceClip(frames, fps=30)

# # Write the initial uncompressed video file
# video_path = "BirthdayCardGenerator/birthday_card_test.mp4"
# clip.write_videofile(video_path)

# # Compress the video using ffmpeg-python
# compressed_video_path = "BirthdayCardGenerator/compressed_birthday_card.mp4"

# ffmpeg.input(video_path).output(
#     compressed_video_path,
#     vcodec='libx264',  # Video codec
#     # CRF value for quality (lower is better, 18 is near-lossless)
#     crf=18,
#     preset='slow',     # Use slow preset for better compression
#     pix_fmt='yuv420p'  # Pixel format for compatibility
# ).run()

# print(f"Video compression completed! Saved as {compressed_video_path}")
##########################################################################################

from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
from moviepy.editor import ImageSequenceClip
import ffmpeg  # Import ffmpeg-python

# Function to read the birthday message from a file


def get_birthday_message(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading the text file: {e}")
        return "Happy Birthday!"  # Fallback to default text


# Use this path to get the generated birthday message
text_file_path = "BirthdayCardGenerator/birthday_message.txt"
# Call the function to get the birthday message from the file
birthday_message = get_birthday_message(text_file_path)


def create_confetti(width: int, height: int, num_particles: int) -> list[tuple[int, int, int, tuple[int, int, int]]]:
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
        draw.rectangle([x, wrapped_y, x + size, wrapped_y + size], fill=color)

    return np.array(frame)


# Load a random image
images = ['BirthdayCardGenerator/Blue.jpg', 'BirthdayCardGenerator/Green.jpg', 'BirthdayCardGenerator/Orange.jpg',
          'BirthdayCardGenerator/Pink.jpg', 'BirthdayCardGenerator/Purple.jpg', 'BirthdayCardGenerator/Red.jpg', 'BirthdayCardGenerator/LightBlue.jpg']
base_image = Image.open(random.choice(images))

# Create an ImageDraw object to draw on the image
draw = ImageDraw.Draw(base_image)

# Specify the path to your Rubik font file
font_path = "BirthdayCardGenerator/Rubik-VariableFont_wght.ttf"

# Load the Rubik font for the first line and remaining text
font_size_first_line = 200  # Bigger font size for the first line
font_size_remaining_text = 150  # Smaller font size for the remaining text

font_first_line = ImageFont.truetype(font_path, font_size_first_line)
font_remaining_text = ImageFont.truetype(font_path, font_size_remaining_text)

# Get the size of the image
img_width, img_height = base_image.size

# Split the birthday message into the first line and the remaining message
lines = birthday_message.split("\n", 1)
first_line = lines[0]  # "Happy birthday {name}!"
remaining_text = lines[1] if len(lines) > 1 else ""  # The rest of the message

# Get the size of the first line (bigger size)
first_line_bbox = draw.textbbox((0, 0), first_line, font=font_first_line)
first_line_width = first_line_bbox[2] - first_line_bbox[0]
first_line_height = first_line_bbox[3] - first_line_bbox[1]

# Calculate the position to center the first line higher on the card (around 1/4th of the height)
first_line_position = ((img_width - first_line_width) // 2, img_height // 5)

# Add the first line to the image
draw.text(first_line_position, first_line, font=font_first_line, fill="white")

# Add the remaining text if there is any
if remaining_text:
    # Split the remaining text into individual lines
    remaining_lines = remaining_text.split("\n")

    # Set line spacing
    line_spacing = 30  # Adjust the spacing between lines
    # Extra space between first line and remaining text
    extra_space_between_first_and_remaining = 250

    # Calculate the position for the first line of the remaining text (leave extra space after the first line)
    remaining_text_position = (
        first_line_position[0], first_line_position[1] + first_line_height + extra_space_between_first_and_remaining)

    # Draw each line of the remaining text with vertical spacing
    for idx, line in enumerate(remaining_lines):
        line_bbox = draw.textbbox((0, 0), line, font=font_remaining_text)
        line_width = line_bbox[2] - line_bbox[0]
        line_position = ((img_width - line_width) // 2,
                         remaining_text_position[1] + idx * (font_size_remaining_text + line_spacing))

        # Draw the line on the image
        draw.text(line_position, line, font=font_remaining_text, fill="white")

# Create confetti
confetti = create_confetti(img_width, img_height, 100)

# Create frames
frames = []
for i in range(300):  # Create 300 frames for a 10-second video at 30 fps
    frame = create_frame(base_image, confetti, i)
    frames.append(frame)

# Convert frames to video
clip = ImageSequenceClip(frames, fps=30)

# Write the initial uncompressed video file
video_path = "BirthdayCardGenerator/birthday_card_test.mp4"
clip.write_videofile(video_path)


Compress the video using ffmpeg-python
compressed_video_path = "BirthdayCardGenerator/compressed_birthday_card.mp4"

ffmpeg.input(video_path).output(
    compressed_video_path,
    vcodec='libx264',  # Video codec
    # CRF value for quality (lower is better, 18 is near-lossless)
    crf=18,
    preset='slow',     # Use slow preset for better compression
    pix_fmt='yuv420p'  # Pixel format for compatibility
).run()

print(f"Video compression completed! Saved as {compressed_video_path}")
