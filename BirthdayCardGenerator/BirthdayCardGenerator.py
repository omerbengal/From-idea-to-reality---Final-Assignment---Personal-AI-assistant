# Version 1 (regular image)
# from PIL import Image, ImageDraw, ImageFont
# import random

# # Load a random image
# images = ['BirthdayCardGenerator/Blue.jpg', 'BirthdayCardGenerator/Green.jpg', 'BirthdayCardGenerator/Orange.jpg',
#           'BirthdayCardGenerator/Pink.jpg', 'BirthdayCardGenerator/Purple.jpg', 'BirthdayCardGenerator/Red.jpg', 'BirthdayCardGenerator/LightBlue.jpg']
# image = Image.open(random.choice(images))

# # Create an ImageDraw object to draw on the image
# draw = ImageDraw.Draw(image)

# # Specify the path to your Rubik font file
# # Make sure to use the correct path and filename
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
# image.save('BirthdayCardGenerator/birthday_card.png')

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
from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
from moviepy.editor import ImageSequenceClip
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


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
        # Use modulo to wrap the y-position and create a looping effect
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
font_size = 200

# Load the Rubik font
font = ImageFont.truetype(font_path, font_size)

# Define the text
text = "Happy Birthday!"

# Get the size of the image
img_width, img_height = base_image.size

# Get the size of the text
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

# Calculate the position to center the text
position = ((img_width - text_width) // 2, (img_height - text_height) // 2)

# Add text to image
draw.text(position, text, font=font, fill="white")

# Create confetti
confetti = create_confetti(img_width, img_height, 100)

# Create frames
frames = []
for i in range(300):  # Create 300 frames for a 10-second video at 30 fps
    frame = create_frame(base_image, confetti, i)
    frames.append(frame)

# Convert frames to video
clip = ImageSequenceClip(frames, fps=30)

# Write the video file
clip.write_videofile("BirthdayCardGenerator/birthday_card.mp4")
