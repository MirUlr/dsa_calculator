
from pathlib import Path

import streamlit as st
from PIL import Image


image = Image.open(Path.cwd() / "resources" / "dsa_logo.png")
st.sidebar.image(image)

st.markdown(
    """
    # Probenrechner: Das schwarze Auge
    Herzlich wilkommen bla bla
    
    ## Wie funktioniert das?
    
    ## Was muss ich wissen?
    """
)
