import streamlit as st
import streamlit.components.v1 as components
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
from constant import *

def remove_bg(image_data):
    try:
        output = remove(image_data)
        return output
    except Exception as e:
        st.error(f"Error removing background: {e}")
        return None

def home_page():
    st.title("Welcome to My Streamlit App")
    st.write(homepgIntroduction)

def image_editor_page():
    st.title("Image Editor")

    # Upload Image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_column_width=True)

        # Background Removal
        if st.checkbox("Remove Background"):
            output_image = remove_bg(uploaded_file.getvalue())
            if output_image is not None:
                output_image = Image.open(io.BytesIO(output_image))
                st.image(output_image, caption="Image without Background", use_column_width=True)
                buffered = io.BytesIO()
                output_image.save(buffered, format="PNG")
                st.download_button(
                    label="Download Image without Background",
                    data=buffered.getvalue(),
                    file_name="image_no_bg.png",
                    mime="image/png",
                )

        # Image Editing
        if st.checkbox("Edit Image"):
            edited_image = image.copy()
            brightness = st.slider("Brightness", 0.0, 2.0, 1.0)
            contrast = st.slider("Contrast", 0.0, 2.0, 1.0)
            sharpness = st.slider("Sharpness", 0.0, 2.0, 1.0)
            edited_image = ImageEnhance.Brightness(edited_image).enhance(brightness)
            edited_image = ImageEnhance.Contrast(edited_image).enhance(contrast)
            edited_image = ImageEnhance.Sharpness(edited_image).enhance(sharpness)
            st.image(edited_image, caption="Edited Image", use_column_width=True)
            buffered = io.BytesIO()
            edited_image.save(buffered, format="PNG")
            st.download_button(
                label="Download Edited Image",
                data=buffered.getvalue(),
                file_name="edited_image.png",
                mime="image/png",
            )

        # Crop Image
        if st.checkbox("Crop Image"):
            width, height = image.size
            left = st.slider("Left", 0, width, 0)
            top = st.slider("Top", 0, height, 0)
            right = st.slider("Right", 0, width, width)
            bottom = st.slider("Bottom", 0, height, height)
            cropped_image = image.crop((left, top, right, bottom))
            st.image(cropped_image, caption="Cropped Image", use_column_width=True)
            buffered = io.BytesIO()
            cropped_image.save(buffered, format="PNG")
            st.download_button(
                label="Download Cropped Image",
                data=buffered.getvalue(),
                file_name="cropped_image.png",
                mime="image/png",
            )

        # Apply Effects
        if st.checkbox("Apply Effects"):
            edited_image = image.copy()
            blur_radius = st.slider("Blur", 0, 10, 0)
            if blur_radius > 0:
                edited_image = edited_image.filter(ImageFilter.GaussianBlur(blur_radius))
            contour = st.checkbox("Apply Contour Effect")
            if contour:
                edited_image = edited_image.filter(ImageFilter.CONTOUR)
            detail = st.checkbox("Apply Detail Effect")
            if detail:
                edited_image = edited_image.filter(ImageFilter.DETAIL)
            edge_enhance = st.checkbox("Apply Edge Enhance Effect")
            if edge_enhance:
                edited_image = edited_image.filter(ImageFilter.EDGE_ENHANCE)
            sharpen = st.checkbox("Apply Sharpen Effect")
            if sharpen:
                edited_image = edited_image.filter(ImageFilter.SHARPEN)
            emboss = st.checkbox("Apply Emboss Effect")
            if emboss:
                edited_image = edited_image.filter(ImageFilter.EMBOSS)
            smooth = st.checkbox("Apply Smooth Effect")
            if smooth:
                edited_image = edited_image.filter(ImageFilter.SMOOTH)
            st.image(edited_image, caption="Edited Image with Effects", use_column_width=True)
            buffered = io.BytesIO()
            edited_image.save(buffered, format="PNG")
            st.download_button(
                label="Download Edited Image with Effects",
                data=buffered.getvalue(),
                file_name="edited_image_with_effects.png",
                mime="image/png",
            )

def another_page():
    st.title("Color Wheel")
    st.write("Select a color to get its HEX code.")

    color = st.color_picker("Pick a color", "#808080")

    st.write(f"The HEX code for the selected color is: {color}")

    st.write("Sample of the selected color:")
    st.markdown(
        f"""
        <div style="background-color: {color}; height: 100px; width: 100px; border-radius: 5px; border: 1px 808080;">
        </div>
        """,
        unsafe_allow_html=True
    )

def calculator_page():
    st.title("Calculator")

    equation = st.text_input("Enter your equation (e.g., 2+2):", "0")

    try:
        result = eval(equation)
        st.write(f"Result: {result}")
    except Exception as e:
        st.write(f"Error: {e}")

    # Instruction on how to use the calculator
    with st.expander("Instructions"):
        st.write("""
        - Use `+` for addition (e.g., `2 + 2`)
        - Use `-` for subtraction (e.g., `4 - 2`)
        - Use `*` for multiplication (e.g., `3 * 3`)
        - Use `/` for division (e.g., `10 / 2`)
        - Use `**` for powers (e.g., `2 ** 3` for 2^3)
        - Use `sqrt()` for square roots (e.g., `sqrt(16)`)
        """)

from constant import CANVAS_HTML  # Import the canvas HTML

def draw_on_image_page():
    st.title("Draw on Image")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        orig_width, orig_height = image.size

        # Sliders for canvas size
        canvas_width = st.slider("Canvas Width", min_value=100, max_value=orig_width, value=orig_width)
        canvas_height = st.slider("Canvas Height", min_value=100, max_value=orig_height, value=orig_height)

        # Color picker for drawing color
        draw_color = st.color_picker("Pick a color for drawing", "#000000")

        # Slider for brush width
        brush_width = st.slider("Brush Width", min_value=1, max_value=20, value=5)

        st.image(image, caption="Image to Draw On", use_column_width=True)
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Use the constant HTML string with f-string to inject dynamic values
        html_code = CANVAS_HTML.format(
            canvas_width=canvas_width,
            canvas_height=canvas_height,
            img_base64=img_base64,
            draw_color=draw_color,
            brush_width=brush_width
        )

        components.html(html_code, height=canvas_height + 100)  # Adjust the height to fit the canvas and controls



# Sidebar for navigation
st.sidebar.title("Maximo Weber")
st.sidebar.markdown("### Navigation")
page = st.sidebar.selectbox(
    "Go to", 
    ["Home", "Image Editor", "Color Wheel", "Draw on Image", "Calculator"]
)

# Page content
if page == "Home":
    home_page()
elif page == "Image Editor":
    image_editor_page()
elif page == "Color Wheel":
    another_page()
elif page == "Draw on Image":
    draw_on_image_page()
elif page == "Calculator":
    calculator_page()
