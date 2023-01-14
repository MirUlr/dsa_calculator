
from pathlib import Path

import streamlit as st
from PIL import Image

from hero import Hero
from twinkle import Twinkle


@st.cache
def dummy_char():
    return Hero(name="Alrik", attribute_values=[8] * 8, skill_values=[8] * 59)


skill_groups = [
        "Körpertalente", "Gesellschaftstalente", "Naturtalente", "Wissenstalente", "Handwerkstalente"
]

image = Image.open(Path.cwd() / "resources" / "dsa_logo.png")
st.sidebar.image(image)

st.markdown(
    """
    # Erschaffe einen Heldy
    """
)

choice = st.selectbox(
    "Was soll erschaffen werden?",
    ["Profaner Charakter", "Geweihty", "Magiey"]
)
name = st.text_input("Wie soll der Name lauten?")

st.markdown("## Attribute eingeben:")
with st.expander("Hier eingeben"):
    dummy = dummy_char()
    attributes = dummy.attributes
    a_values = [st.number_input(label=a, min_value=1, max_value=25, value=8) for a in attributes]

st.markdown("## Fertigkeiten eingeben:")
with st.expander("Hier eingeben"):
    tabs = st.tabs(skill_groups)
    for tab in tabs:
        with tab:
            st.markdown("Foo Bar Baz")

if choice in ["Geweihty", "Magiey"]:
    st.markdown(f"## Fähigkeiten des {choice} eingeben:")
    with st.expander("Hier eingeben"):
        pass
