from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


async def generate_article_certificate(fullname, article, issue, volume, year, date, **kwargs):
    # Open the certificate template
    img = Image.open("data/articles/article_certificate.jpg")
    if img.mode != 'RGB':
        img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    output_directory = Path("media/articles")
    output_path = output_directory / f'article_{fullname.split()[0]}.jpg'

    # Ensure the output directory exists
    output_directory.mkdir(parents=True, exist_ok=True)

    # Define font sizes and load fonts
    font_sizes = {
        'name': 150,
        'title': 90,
        'regular': 75,
        'small': 75
    }

    fonts = {}
    try:
        for key, size in font_sizes.items():
            fonts[key] = ImageFont.truetype("data/fonts/GreatVibes-Regular.ttf", size)
    except:
        return {'ok': False, 'result': "Font loading failed, using default font"}

    color = (27, 66, 107)

    # Center and adjust fullname
    name_y = 1010
    img_width = img.width
    name_font = fonts['name']
    name_text = fullname
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_width = name_bbox[2] - name_bbox[0]

    # Adjust name font size if too wide
    while name_width > img_width * 0.7 and font_sizes['name'] > 50:
        font_sizes['name'] -= 10
        name_font = ImageFont.truetype("data/fonts/GreatVibes-Regular.ttf", font_sizes['name'])
        name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
        name_width = name_bbox[2] - name_bbox[0]

    name_x = (img_width - name_width) // 2
    draw.text((name_x, name_y), name_text, font=name_font, fill=color)

    # Center and adjust article title with dynamic sizing
    title_y = 1320  # Adjusted up from 1306 to maintain consistent vertical alignment
    title_font = fonts['title']

    # Calculate available width for article (accounting for quotes)
    available_width = img_width * 0.6  # Keep 60% constraint for quotes

    # Handle article length with adjusted vertical positioning
    if len(article) < 30:  # For short articles
        font_sizes['title'] = 110  # Increase size for short articles
        title_y = 1310  # Slight adjustment for larger font to maintain vertical centering
    else:  # For longer articles
        font_sizes['title'] = 90  # Start with default size

    title_font = ImageFont.truetype("data/fonts/GreatVibes-Regular.ttf", font_sizes['title'])
    title_bbox = draw.textbbox((0, 0), article, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]

    # Adjust font size if needed
    while title_width > available_width and font_sizes['title'] > 30:
        font_sizes['title'] -= 5
        title_font = ImageFont.truetype("data/fonts/GreatVibes-Regular.ttf", font_sizes['title'])
        title_bbox = draw.textbbox((0, 0), article, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]

    # If still too long, truncate with ellipsis
    title_text = article
    if title_width > available_width:
        while title_width > available_width and len(title_text) > 3:
            title_text = title_text[:-1]
            title_bbox = draw.textbbox((0, 0), title_text + "...", font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
        title_text = title_text + "..."

    # Calculate final position for title (centered between quotes)
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_width) // 2 - 40

    # Calculate vertical centering adjustment based on font size
    title_height = title_bbox[3] - title_bbox[1]
    title_y_offset = title_height // 2
    final_title_y = title_y - title_y_offset // 2  # Adjust vertical position based on text height

    draw.text((title_x, final_title_y), title_text, font=title_font, fill=color)

    # Add issue and year
    issue_x = 1520
    issue_y = 1448
    issue_year_x = 1780
    issue_year_y = 1448
    issue_text = f"{issue}({volume})"
    issue_year = f"{year}"
    draw.text((issue_x, issue_y), issue_text, font=fonts['regular'], fill=color)
    draw.text((issue_year_x, issue_year_y), issue_year, font=fonts['regular'], fill=color)

    # Add date
    date_x = 778
    date_y = 1885
    draw.text((date_x, date_y), date, font=fonts['small'], fill=color)

    # Save the image
    img.save(output_path)

    return {'ok': True, 'result': output_path}