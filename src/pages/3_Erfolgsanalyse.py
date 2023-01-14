
from pathlib import Path

import streamlit as st
from PIL import Image


image = Image.open(Path.cwd() / "resources" / "dsa_logo.png")
st.sidebar.image(image)

st.markdown(
    """
    # Hat jemand Stochastik gesagt?
    """
)

