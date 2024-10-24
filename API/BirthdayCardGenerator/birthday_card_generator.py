import sys
import os
import threading

from PIL import Image, ImageDraw, ImageFont
import random
import numpy as np
from moviepy.editor import ImageSequenceClip

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from API.open_ai_singleton import OpenAISingleton


class BirthdayCardGenerator:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(BirthdayCardGenerator, cls).__new__(cls)
        return cls._instance

    def _generate_birthday_text(self, name: str) -> str:
        prompt = f"""Generate a heartfelt and creative birthday message for {name}.
        The message should be totally generic so it could fit anyone.
        The message should always start with Happy birthday {name}!
        The message should be no more than 5 lines (not including the starting line).
        Make sure that each line is not longer than 75 characters.
        Do not add an ending to the message like: Best wishes... From...
        Separate each line."""

        try:
            messages = [
                {"role": "system", "content": "You are a birthday card generator."},
                {"role": "user", "content": prompt}
            ]

            birthday_message = OpenAISingleton().get_response_str(messages, 0.7).strip()

            return birthday_message

        except Exception as e:
            raise Exception(f"Error generating birthday text: {str(e)}")

    def generate_video(self, name: str):
        try:


            birthday_message = self._generate_birthday_text(name)


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


            images = ['./BirthdayCardGenerator/Blue.webp', './BirthdayCardGenerator/Green.webp',
                      './BirthdayCardGenerator/Orange.webp', './BirthdayCardGenerator/Pink.webp',
                      './BirthdayCardGenerator/Purple.webp', './BirthdayCardGenerator/Red.webp',
                      './BirthdayCardGenerator/LightBlue.webp']
            base_image = Image.open(random.choice(images))

            draw = ImageDraw.Draw(base_image)

            font_path = "./BirthdayCardGenerator/Rubik-VariableFont_wght.ttf"
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
            clip.write_videofile("./BirthdayCardGenerator/birthday_card.mp4")


        except Exception as e:
            raise Exception(f"Error generating birthday video: {str(e)}")
