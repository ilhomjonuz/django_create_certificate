import asyncio
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

async def create_voucher_file(expiration_date: str, *args, **kwargs):
    # Define the paths for the base template and output
    base_pdf = Path("data/vouchers/voucher.png")
    output_directory = Path("data/files")
    output_pdf = output_directory / f"voucher_{expiration_date.replace('.', '_')}.png"

    # Ensure the output directory exists
    output_directory.mkdir(parents=True, exist_ok=True)

    # Open the base image
    img = Image.open(base_pdf)

    # Define the text to be added
    text1 = "Amal qilish muddati"
    text2 = f"{expiration_date} gacha"

    # Create a drawing context
    draw = ImageDraw.Draw(img)

    # Choose a smaller font size and ensure the font path is correct
    font1 = ImageFont.truetype("data/fonts/Helvetica-Bold-Font.ttf", 35)
    font2 = ImageFont.truetype("data/fonts/Helvetica-Bold-Font.ttf", 40)

    # Set the text color to a deep purple (#6A2C9C)
    text_color = (38, 0, 116)

    # Get size of the first text
    bbox1 = draw.textbbox((0, 0), text1, font=font1)
    text1_width = bbox1[2] - bbox1[0]
    text1_height = bbox1[3] - bbox1[1]

    # Get size of the second text
    bbox2 = draw.textbbox((0, 0), text2, font=font2)
    text2_width = bbox2[2] - bbox2[0]
    text2_height = bbox2[3] - bbox2[1]

    # Calculate the total height for both texts
    total_text_height = text1_height + text2_height

    # Position for the lower right corner, 10px padding from edges
    x_position = img.width - max(text1_width, text2_width) - 20
    y_position = img.height - total_text_height - 100  # Adjusted padding

    # Rotate the first text
    rotated_text1 = Image.new("RGBA", (text1_width, text1_height))
    rotated_draw1 = ImageDraw.Draw(rotated_text1)
    rotated_draw1.text((0, 0), text1, font=font1, fill=text_color)
    rotated_text1 = rotated_text1.rotate(15, expand=True)  # Rotate by 15 degrees

    # Rotate the second text
    rotated_text2 = Image.new("RGBA", (text2_width, text2_height))
    rotated_draw2 = ImageDraw.Draw(rotated_text2)
    rotated_draw2.text((0, 0), text2, font=font2, fill=text_color)
    rotated_text2 = rotated_text2.rotate(15, expand=True)  # Rotate by 15 degrees

    # Calculate the new bounding box size after rotation
    rotated_width1, rotated_height1 = rotated_text1.size

    # Ensure there's enough space around the rotated text by adjusting positions
    final_x1 = x_position - 20
    final_y1 = y_position

    final_x2 = x_position - 10
    final_y2 = y_position + rotated_height1 - 80  # Ensure enough space between the two texts

    # Paste the rotated texts onto the original image
    img.paste(rotated_text1, (final_x1, final_y1), rotated_text1)
    img.paste(rotated_text2, (final_x2, final_y2), rotated_text2)

    # Save the modified image
    img.save(output_pdf)

    # Return the path to the generated voucher
    return output_pdf
