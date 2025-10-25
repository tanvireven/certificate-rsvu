import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import re

# ====== CONFIGURATION ======
ASSETS_DIR = Path(__file__).parent / "assets"
TEMPLATE_PATH = ASSETS_DIR / "template.png"
FONT_PATH = ASSETS_DIR / "font.ttf"

# ⚙️ Customize these to match your certificate design
NAME_X = 750      # Horizontal position
NAME_Y = 700      # Vertical position
FONT_SIZE = 60    # Font size
FONT_COLOR = "#000000"  # Text color 

# ====== PAGE SETUP ======
st.set_page_config(
    page_title="Certificate Generator",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Certificate by RSVU")
st.caption("Developed by Tanvir Even | President, RSVU")
st.caption("If any error occurs, Contact: 01608514747")

# ====== VALIDATE ASSETS ======
if not TEMPLATE_PATH.exists():
    st.error("❌ Missing certificate template! Admin: please upload 'template.png' to the 'assets' folder on GitHub.")
    st.stop()

# ====== USER INPUT ======
user_name = st.text_input(
    "Enter Your Full Name",
    placeholder="e.g.,  Tanvir Even",
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

            # Load font
            if FONT_PATH.exists():
                font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
            else:
                try:
                    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
                except OSError:
                    try:
                        font = ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE)
                    except OSError:
                        font = ImageFont.load_default()
                        st.info("ℹ️ Using basic font. Add 'font.ttf' to assets for better look.")

            # Draw name
            draw.text(
                (NAME_X, NAME_Y),
                user_name,
                fill=FONT_COLOR,
                font=font
            )

            # Display preview — ✅ FIXED: use_container_width
            st.image(cert, caption="Preview", use_container_width=True)

            # === Prepare downloads ===
            safe_name = re.sub(r"[^a-zA-Z0-9\s]", "", user_name).strip().replace(" ", "_")

            # PNG buffer
            png_buffer = io.BytesIO()
            cert.save(png_buffer, format="PNG")
            png_buffer.seek(0)

            # PDF buffer (PIL requires RGB mode for PDF)
            pdf_buffer = io.BytesIO()
            cert_rgb = cert.convert("RGB")  # Ensure RGB mode
            cert_rgb.save(pdf_buffer, format="PDF")
            pdf_buffer.seek(0)

            # === Download buttons ===
            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📥 Download as PNG",
                    data=png_buffer,
                    file_name=f"{safe_name}_certificate.png",
                    mime="image/png"
                )

            with col2:
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf_buffer,
                    file_name=f"{safe_name}_certificate.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please contact the admin to check the template or font file.")

# ====== ENHANCED FOOTER WITH SOCIAL LINKS ======
st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #555; font-size: 0.95rem; line-height: 1.6;">
    <p>👨‍💻 Robotics Society of Varendra University<br>
    Dept. of CSE, Varendra University | Rajshahi, Bangladesh</p>
    
    <p style="margin-top: 1rem; font-weight: 500; color: #1a3a6c;">
        💬 Have a suggestion or need help?
    </p>
    <p>
        <a href="https://www.facebook.com/tanvireven07" target="_blank" style="text-decoration: none; margin: 0 10px;">
            <i class="fab fa-facebook" style="color: #4267B2; font-size: 1.4rem;"></i><br>
            <span style="color: #333;">Facebook</span>
        </a>
        <a href="https://wa.me/8801608514747" target="_blank" style="text-decoration: none; margin: 0 10px;">
            <i class="fab fa-whatsapp" style="color: #25D366; font-size: 1.4rem;"></i><br>
            <span style="color: #333;">WhatsApp</span>
        </a>
    </p>
</div>

<!-- Load Font Awesome for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""", unsafe_allow_html=True)
