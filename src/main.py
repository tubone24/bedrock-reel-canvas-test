import streamlit as st
from state import AppState
from components import ImageControls
from image_service import ImageService

def main():
    st.title("Nova Canvas デモ")
    AppState.initialize()

    image_prompt = st.text_input("画像生成プロンプト")

    if st.button("画像を生成"):
        params = {
            "textToImageParams": {
                "text": image_prompt,
                "negativeText": "bad quality, low res"
            }
        }
        response = ImageService.process_image("TEXT_IMAGE", params)
        ImageService.update_session_state(response)

    if st.session_state.display_image:
        st.image(st.session_state.image)
        ImageControls.render_image_buttons()

if __name__ == "__main__":
    main()