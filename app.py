import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io
import re

# ====== CONFIGURATION ======
ASSETS_DIR = Path(__file__).parent / "assets"
TEMPLATE_PATH = ASSETS_DIR / "template.png"
FONT_PATH = ASSETS_DIR / "font.ttf"

# ⚙️ Adjust to match your template
NAME_X = 750
NAME_Y = 700
FONT_SIZE = 60
FONT_COLOR = "#000000"

# ====== CUSTOM CSS FOR PROFESSIONAL UI ======
st.markdown("""
    <style>
    /* Main container padding */
    [data-testid="stAppViewContainer"] {
        padding: 1.5rem 1rem;
    }

    /* Title styling */
    h1 {
        text-align: center;
        color: #1a3a6c;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    /* Subtitle/caption styling */
    .stCaption {
        text-align: center;
        color: #555;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }

    /* Input field */
    .stTextInput > div > div > input {
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1a3a6c;
        box-shadow: 0 0 0 2px rgba(26, 58, 108, 0.2);
    }

    /* Generate button */
    .stButton > button {
        background: linear-gradient(135deg, #1a3a6c, #2c5282);
        color: white;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 58, 108, 0.3);
    }

    /* Certificate preview */
    .stImage > img {
        border-radius: 12px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
        margin: 1.5rem 0;
        border: 1px solid #eee;
    }

    /* Download buttons */
    .download-buttons {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
    }
    .download-buttons > div > button {
        flex: 1;
        padding: 0.75rem;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    .btn-png {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    .btn-pdf {
        background-color: #E53935 !important;
        color: white !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #eee;
        color: #666;
        font-size: 0.9rem;
        line-height: 1.5;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .download-buttons {
            flex-direction: column;
        }
        h1 {
            font-size: 1.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ====== PAGE SETUP ======
st.set_page_config(
    page_title="Certificate Generator",
    page_icon="🎓",
    layout="centered"
)

# ====== HEADER ======
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
    placeholder="e.g., Tanvir Even",
    help="Type your name exactly as you want it to appear"
)

# ====== GENERATE BUTTON ======
if st.button("✨ Generate Certificate"):
    if not user_name.strip():
        st.warning("⚠️ Please enter your name.")
    else:
        try:
            # Load and process certificate
            template = Image.open(TEMPLATE_PATH)
            cert = template.copy()
            draw = ImageDraw.Draw(cert)

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

            draw.text((NAME_X, NAME_Y), user_name, fill=FONT_COLOR, font=font)

            # Show preview
            st.image(cert, caption="Your Certificate Preview", use_container_width=True)

            # Prepare files
            safe_name = re.sub(r"[^a-zA-Z0-9\s]", "", user_name).strip().replace(" ", "_")

            png_buffer = io.BytesIO()
            cert.save(png_buffer, format="PNG")
            png_buffer.seek(0)

            pdf_buffer = io.BytesIO()
            cert_rgb = cert.convert("RGB")
            cert_rgb.save(pdf_buffer, format="PDF")
            pdf_buffer.seek(0)

            # Download buttons with custom styling
            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📥 PNG",
                    data=png_buffer,
                    file_name=f"{safe_name}_certificate.png",
                    mime="image/png",
                    key="png_btn"
                )

            with col2:
                st.download_button(
                    label="📄 PDF",
                    data=pdf_buffer,
                    file_name=f"{safe_name}_certificate.pdf",
                    mime="application/pdf",
                    key="pdf_btn"
                )

            # Inject custom button classes (via JS workaround)
            st.markdown("""
                <script>
                const buttons = window.parent.document.querySelectorAll('button');
                buttons.forEach(btn => {
                    if (btn.innerText.includes('PNG')) btn.className += ' btn-png';
                    if (btn.innerText.includes('PDF')) btn.className += ' btn-pdf';
                });
                </script>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please contact the admin to check the template or font file.")

# ====== FOOTER ======
st.markdown("""
    <div class="footer">
        <p>👨‍💻 Robotics Society of Varendra University<br>
        Dept. of CSE, Varendra University | Rajshahi, Bangladesh</p>
    </div>
""", unsafe_allow_html=True)
