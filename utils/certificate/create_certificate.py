from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


async def create_certificate(cert_id: int, fullname: str, course: str) -> dict:
    """
    Add text to the certificate image.

    Args:
        cert_id (int): Certificate id.
        fullname (str): Full name of the certificate receiver.
        course (str): Name of the course.
    """
    try:
        # Load the image
        image_path = "data/certificates/certificate.png"
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        output_directory = Path("media/certificates")

        cert_name = fullname.replace(" ", "").replace("'", "") + course.split()[0]
        output_path = output_directory / f'certificate_{cert_name}.png'

        # Ensure the output directory exists
        output_directory.mkdir(parents=True, exist_ok=True)

        # Load the font
        font_bronson_path = "data/fonts/BRONSON-Black.ttf"
        font_montserrat_path = "data/fonts/Montserrat-Bold.ttf"
        font_arial_path = "data/fonts/Arial.ttf"

        font_medium = ImageFont.truetype(font_montserrat_path, 60)
        font_small = ImageFont.truetype(font_arial_path, 50)  # Font for footer text

        # Define text content
        name_text = fullname.upper()
        completion_text = "For successfully completing the course"

        # Split course name into two lines
        course_lines = course.split(" ")
        if len(course_lines) == 2:
            course_text = [course_lines[0], course_lines[1]]
        elif len(course_lines) > 2:
            mid_index = len(course_lines) // 2
            course_text = [" ".join(course_lines[:mid_index]), " ".join(course_lines[mid_index:])]
        else:
            course_text = [course_lines[0], ""]

        # Define text color and positions
        image_width, image_height = image.size

        # Helper function to calculate text position
        def get_centered_position(text, font, y_offset):
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (image_width - text_width) // 2
            y = y_offset
            return x, y, text_width, text_height

        # Function to adjust font size dynamically for a long name
        def adjust_font_size_for_name(name, font_path, initial_size, max_width):
            temp_font = ImageFont.truetype(font_path, initial_size)
            line_width = get_centered_position(name, temp_font, 0)[2]
            while line_width > max_width:
                initial_size -= 5
                temp_font = ImageFont.truetype(font_path, initial_size)
                line_width = get_centered_position(name, temp_font, 0)[2]
            return temp_font

        # Calculate positions for centered text for fullname
        name_font_size = 280
        max_name_width = image_width * 0.8  # 80% of image width
        name_font = adjust_font_size_for_name(name_text, font_bronson_path, name_font_size, max_name_width)
        name_x, name_y, _, name_height = get_centered_position(name_text, name_font, image_height // 2 - 240)

        # Adjust completion text positioning
        completion_x, completion_y, _, completion_height = get_centered_position(completion_text, font_medium, name_y + name_height + 50)

        # Add text to image
        draw.text((name_x, name_y), name_text, font=name_font, fill=(38, 0, 116))
        draw.text((completion_x, completion_y), completion_text, font=font_medium, fill=(38, 0, 116))

        # Adjust font sizes for course lines to make widths equal
        def adjust_font_size_for_course_line(line, font_path, initial_size, target_width):
            temp_font = ImageFont.truetype(font_path, initial_size)
            line_width = get_centered_position(line, temp_font, 0)[2]
            while line_width > target_width:
                initial_size -= 5
                temp_font = ImageFont.truetype(font_path, initial_size)
                line_width = get_centered_position(line, temp_font, 0)[2]
            return temp_font

        # Calculate maximum width for course lines
        max_width = image_width * 0.8  # 80% of the image width, adjust as needed

        # Start with a larger font for both course name parts
        course_font_sizes = [260, 260]  # Start with the same size for both lines
        for idx, line in enumerate(course_text):
            course_font = adjust_font_size_for_course_line(line, font_bronson_path, course_font_sizes[idx], max_width)
            course_text[idx] = course_text[idx].upper()  # Optional: capitalize text if needed

        # Check if course text is balanced, if not adjust font sizes
        def balance_course_text(course_text, max_width):
            # Compare widths of the course text
            line1_width = get_centered_position(course_text[0], ImageFont.truetype(font_bronson_path, 260), 0)[2]
            line2_width = get_centered_position(course_text[1], ImageFont.truetype(font_bronson_path, 260), 0)[2]

            # If one line is significantly wider than the other, adjust font size
            if abs(line1_width - line2_width) > max_width * 0.1:  # Arbitrary tolerance for difference
                if line1_width > line2_width:
                    course_font_sizes[1] = int(course_font_sizes[1] * (line1_width / line2_width))  # Reduce font size of second line
                else:
                    course_font_sizes[0] = int(course_font_sizes[0] * (line2_width / line1_width))  # Reduce font size of first line
            return course_text, course_font_sizes

        course_text, course_font_sizes = balance_course_text(course_text, max_width)

        # Positioning course text
        course_y = completion_y + completion_height + 270
        for idx, line in enumerate(course_text):
            temp_font = adjust_font_size_for_course_line(line, font_bronson_path, course_font_sizes[idx], max_width)
            course_x, line_y, _, line_height = get_centered_position(line, temp_font, course_y + idx * 250)
            draw.text((course_x, line_y), line, font=temp_font, fill=(106, 21, 255))

        # Add footer text with today's date
        today = datetime.now().strftime("%d.%m.%Y")  # Format date as DD.MM.YYYY
        number = 99 + cert_id
        formatted_number = f"{number:05}"
        footer_text = f"Serial number DAC_{formatted_number}.Date: {today}"
        footer_x, footer_y, _, footer_height = get_centered_position(footer_text, font_small, image_height - 50)
        draw.text((footer_x, footer_y - 50), footer_text, font=font_small, fill=(218, 255, 1))

        # Save the modified image
        image.save(output_path)
        return {"status": "ok", "result": str(output_path)}

    except Exception as e:
        return {"status": "error", "result": f"An error occurred while adding text: {e}"}
