from dataclasses import dataclass
import streamlit as st

@dataclass
class AppState:
    @staticmethod
    def initialize():
        if 'image_data' not in st.session_state:
            st.session_state.image_data = None
        if 'display_image' not in st.session_state:
            st.session_state.display_image = False
        if 'image' not in st.session_state:
            st.session_state.image = None
        if 'selected_color' not in st.session_state:
            st.session_state.selected_color = "#ff0000"
        if 'color_change_mode' not in st.session_state:
            st.session_state.color_change_mode = False