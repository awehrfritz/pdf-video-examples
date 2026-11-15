"""Write a PowerPoint file with embedded video, for converting to PDF with LibreOffice.

08-libreoffice-click.pptx: two slides, with clip.mp4 and clip2.mp4, played on click.
The poster is an empty frame, as in the LaTeX examples (without a poster,
python-pptx adds a loudspeaker icon).

Run:  uv run --no-project --with python-pptx --with pillow python make-pptx.py
"""
import io

from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches

poster = Image.new("RGB", (1600, 900), "white")
ImageDraw.Draw(poster).rectangle([0, 0, 1599, 899], outline="black", width=3)
poster_png = io.BytesIO()
poster.save(poster_png, "PNG")

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)  # 16:9
blank = prs.slide_layouts[6]

for video in ["clip.mp4", "clip2.mp4"]:
    slide = prs.slides.add_slide(blank)
    slide.shapes.add_movie(
        video,
        Inches(0.667), Inches(0.375), Inches(12), Inches(6.75),  # 16:9, as the clips
        poster_frame_image=poster_png,
        mime_type="video/mp4",
    )

prs.save("08-libreoffice-click.pptx")
