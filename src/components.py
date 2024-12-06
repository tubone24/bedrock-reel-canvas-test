import streamlit as st
from image_service import ImageService

class ImageControls:
    @staticmethod
    def render_color_picker():
        if st.session_state.color_change_mode:
            selected_color = st.color_picker("色を選択", st.session_state.selected_color, key="color_picker")
            st.session_state.selected_color = selected_color.upper()
            st.write(f"選択された色: {selected_color}")
            return selected_color
        return None

    @staticmethod
    def render_image_buttons():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("柴犬にする", on_click=lambda: ImageService.process_image("INPAINTING", {...}))
            st.button("背景を消す", on_click=lambda: ImageService.process_image("BACKGROUND_REMOVAL", {...}))