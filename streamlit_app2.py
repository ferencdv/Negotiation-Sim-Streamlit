# filename: debate_app.py
import streamlit as st
import debatemanager
from PIL import Image
import io
import json
import ststreamer
from contextlib import redirect_stdout

# Set the page configuration as the very first command
st.set_page_config(page_title="Seeking Common Ground: Negotiation Simulation", layout="wide")

# Custom CSS to specifically enhance the title size and style the byline
st.markdown("""
<style>
h1 {
    font-size: 40px !important; /* Adjust the size as needed for the title */
}
/* Custom CSS for the byline */
.byline {
    font-size: 16px !important; /* Smaller font size for the byline */
    color: #666; /* Lighter text color */
    font-style: italic; /* Italicize text */
}
</style>
""", unsafe_allow_html=True)

# Your main title
st.title("Seeking Common Ground: Negotiation Simulations")

# Byline under the title, using inline CSS for styling
st.markdown('<div style="font-size: 16px; color: #666; font-style: italic;">Adapted from Tom Evslin Debate Team app</div>', unsafe_allow_html=True)


# Custom CSS to increase text size globally
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Assuming you have a CSS file named 'style.css' with the desired font sizes
local_css('style.css')


# The International Atomic Energy Agency (IAEA) is seeking to negotiate immediate and unfettered access to the Zaporizhia Nuclear Power Plant (NPP) in Ukraine. This demand comes after two years of unauthorized control of the plant by Russian forces. The IAEA emphasizes the critical importance of conducting a thorough inspection to assess the plant's safety and operational integrity, ensuring compliance with international nuclear safety standards. Given the prolonged period of occupation, it is imperative for the IAEA to verify the plant's condition and to ensure the safety of the surrounding region. The IAEA insists on a swift resolution to this matter, underscoring the urgency of the situation and the need for cooperation from Russian officials to grant access without further delay.

# Hardwire the API key
st.session_state['api_key'] = <put your API here>

# Function to create and load the debate team
def create_debate_team(api_key):
    dm = debatemanager.debate(api_key)
    dm.load_team()
    return dm
    
# Function to capture the console output
def capture_console_output(func, *args, **kwargs):
    f = ststreamer.ObservableStringIO()

    with redirect_stdout(f):

        func(*args, **kwargs)
    output = f.getvalue()
    return output

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None
if 'dm' not in st.session_state:
    st.session_state['dm'] = None

# Define paths for your images directly as specified
logo_image_path = 'logo_image.jpg'  # Path to your logo image
russia_flag_path = 'russia_flag.jpg'  # Path to Russia flag image
iaea_flag_path = 'iaea_logo.png'  # Path to IAEA logo image
chat_manager_flag_path = 'judge.png'  # Path to Chat Manager image

# Load the logo image
logo_image = Image.open(logo_image_path)

# Use Streamlit columns to display the logo and the title next to each other
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo_image, width=210)  # Adjust the width as needed
with col2:
    # Use HTML to style the text color, underline, and make it bold for the title
    st.markdown("<h1 style='color: darkred; text-decoration: underline; font-weight: bold;'>IAEA Negotiatiating Immediate Zaporizhzhia Nuclear Power Plant Access</h1>", unsafe_allow_html=True)
    # Adding the byline directly under the title with smaller, italicized text
    st.markdown("<h2 style='color: darkred; font-size: 18px; font-style: italic;'>Adapted from Tom Evslin Debate Team app</h2>", unsafe_allow_html=True)
    
# If API key is provided, create and load the debate team
if st.session_state['api_key'] and st.session_state['dm'] is None:
    with st.spinner("Creating debate team..."):
        st.session_state['dm'] = create_debate_team(st.session_state['api_key'])


# Once the debate team is created, ask for a debate proposition
if st.session_state['dm']:
    default_position = "The International Atomic Energy Agency (IAEA) is seeking to negotiate immediate and unfettered access to the Zaporizhia Nuclear Power Plant (NPP) in Ukraine. This demand comes after two years of unauthorized control of the plant by Russian forces. The IAEA emphasizes the critical importance of conducting a thorough inspection to assess the plant's safety and operational integrity, ensuring compliance with international nuclear safety standards. Given the prolonged period of occupation, it is imperative for the IAEA to verify the plant's condition and to ensure the safety of the surrounding region. The IAEA insists on a swift resolution to this matter, underscoring the urgency of the situation and the need for cooperation from Russian officials to grant access without further delay."
    proposition = st.text_input("Enter a negotiation position:", value=default_position)
    if proposition and proposition != default_position:
        full_proposition = f"Negotiate the position that {proposition}"
        with st.spinner(f"Negotiating the position: {proposition}. Please be patient."):
            # Redirect console output and perform the debate
            output = capture_console_output(st.session_state['dm'].do_debate, full_proposition)
