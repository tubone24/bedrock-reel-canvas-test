import json
import base64
from config import BEDROCK_CLIENT, IMAGE_CONFIG

class ImageService:
    @staticmethod
    def process_image(task_type, params):
        payload = {
            "taskType": task_type,
            "imageGenerationConfig": IMAGE_CONFIG,
            **params
        }

        try:
            response = BEDROCK_CLIENT.invoke_model(
                modelId='amazon.nova-canvas-v1:0',
                body=json.dumps(payload)
            )
            return json.loads(response.get('body').read())
        except Exception as e:
            raise Exception(f"画像処理エラー: {str(e)}")

    @staticmethod
    def update_session_state(response):
        if 'images' in response:
            st.session_state.image_data = response['images'][0]
            st.session_state.image = base64.b64decode(st.session_state.image_data)
            st.session_state.display_image = True
            st.session_state.image_data2 = base64.b64encode(st.session_state.image).decode("utf-8")