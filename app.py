import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import re

# ====== CONFIGURATION ======
# Paths relative to this file
ASSETS_DIR = Path(__file__).parent / "assets"
TEMPLATE_PATH = ASSETS_DIR / "template.png"
FONT_PATH = ASSETS_DIR / "font.ttf"

# Default text settings (adjust these to fit your template)
NAME_X, NAME_Y = 750, 700
FONT_SIZE = 80
FONT_COLOR = "#000000"

# ====== PAGE SETUP ======
st.set_page_config(page_title="Certificate Generator", page_icon="🎓", layout="centered")

st.title("🎓 University Certificate Generator")
st.caption("Made for students | Download your certificate instantly")

# ====== CHECK ASSETS ======
if not TEMPLATE_PATH.exists():
    st.error("❌ Template missing! Admin: add 'template.png' to the 'assets' folder.")
    st.stop()

# ====== USER INPUT ======
user_name = st.text_input("Enter Your Full Name", placeholder="e.g., Md. Tanvir Hasan")

if st.button("✨ Generate Certificate"):
    if not user_name.strip():
        st.warning("Please enter your name.")
    else:
        try:
            # Load template
            template = Image.open(TEMPLATE_PATH)
            cert = template.copy()
            draw = ImageDraw.Draw(cert)

            # Load font
            if FONT_PATH.exists():
                font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
            else:
                # Fallback to default (you can improve this if needed)
                font = ImageFont.load_default()
                st.info("ℹ️ Using default font. For better look, add 'font.ttf' to assets.")

            # Draw name
            draw.text((NAME_X, NAME_Y), user_name, fill=FONT_COLOR, font=font)

            # Show preview
            st.image(cert, use_column_width=True)

            # Prepare download
            img_bytes = io.BytesIO()
            cert.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            # Safe filename
            safe_name = re.sub(r"[^\w\s-]", "", user_name).strip().replace(" ", "_")

            # Download button
            st.download_button(
                label="📥 Download Certificate (PNG)",
                data=img_bytes,
                file_name=f"{safe_name}_certificate.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please contact admin.")