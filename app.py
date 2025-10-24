import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import re

# ====== CONFIGURATION ======
# Paths are relative to this script
ASSETS_DIR = Path(__file__).parent / "assets"
TEMPLATE_PATH = ASSETS_DIR / "template.png"
FONT_PATH = ASSETS_DIR / "font.ttf"

# ⚙️ Customize these to match your certificate design
NAME_X = 750      # Horizontal position (increase → move right)
NAME_Y = 700      # Vertical position (increase → move down)
FONT_SIZE = 60    # Font size (adjust based on your template)
FONT_COLOR = "#000000"  # Black text (use hex like "#2E8B57" for green)

# ====== PAGE SETUP ======
st.set_page_config(
    page_title="Certificate Generator",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Certificate by RSVU")
st.caption("Devoloped by Tanvir Even | President, RSVU")
st.caption("If any error occurs, Contact: 01608514747 ")

# ====== VALIDATE ASSETS ======
if not TEMPLATE_PATH.exists():
    st.error("❌ Missing certificate template! Admin: please upload 'template.png' to the 'assets' folder on GitHub.")
    st.stop()

# ====== USER INPUT ======
user_name = st.text_input(
    "Enter Your Full Name",
    placeholder="e.g., Md. Tanvir Hasan",
    help="Type your name exactly as you want it to appear"
)

# ====== GENERATE BUTTON ======
if st.button("✨ Generate Certificate"):
    if not user_name.strip():
        st.warning("⚠️ Please enter your name.")
    else:
        try:
            # Load certificate background
            template = Image.open(TEMPLATE_PATH)
            cert = template.copy()
            draw = ImageDraw.Draw(cert)

            # Load font: use custom font if available, else fallback
            if FONT_PATH.exists():
                font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
            else:
                # Try common system fonts (for better scaling)
                try:
                    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
                except OSError:
                    try:
                        font = ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE)
                    except OSError:
                        # Last resort: default font (small, but works)
                        font = ImageFont.load_default()
                        st.info("ℹ️ Using basic font. For best results, add 'font.ttf' to assets.")

            # Draw the name on the certificate
            draw.text(
                (NAME_X, NAME_Y),
                user_name,
                fill=FONT_COLOR,
                font=font
            )

            # Display preview
            st.image(cert, caption="Preview", use_column_width=True)

            # Prepare PNG for download
            img_buffer = io.BytesIO()
            cert.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Create safe filename (remove special characters)
            safe_name = re.sub(r"[^a-zA-Z0-9\s]", "", user_name).strip().replace(" ", "_")

            # Download button
            st.download_button(
                label="📥 Download Certificate (PNG)",
                data=img_buffer,
                file_name=f"{safe_name}_certificate.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please contact the admin to check the template or font file.")

# ====== FOOTER ======
st.markdown("---")
st.caption("👨‍💻 Developed for university students")
