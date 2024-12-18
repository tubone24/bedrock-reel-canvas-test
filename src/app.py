import json
import boto3
import streamlit as st
import base64
import time
import random

S3_DESTINATION_BUCKET = "FIXME"
REGION = "us-east-1"
REEL_MODEL_ID = "amazon.nova-reel-v1:0"
CANVAS_MODEL_ID = "amazon.nova-canvas-v1:0"
PRO_MODEL_ID = "amazon.nova-pro-v1:0"
SLEEP_TIME = 30

bedrock_runtime = boto3.client("bedrock-runtime", REGION)

# セッション状態の初期化
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

st.set_page_config(layout="wide")

def process_image_inpainting_main_object(base_image, additional_prompt, base_prompt):
    canvas_payload = {
        "taskType": "INPAINTING",
        "inPaintingParams": {
            "text": additional_prompt,
            "negativeText": "bad quality, low res",
            "image": base_image,
            "maskPrompt": base_prompt,
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 720,
            "width": 1280,
        }
    }
    try:
        canvas_response = bedrock_runtime.invoke_model(
            modelId=CANVAS_MODEL_ID,
            body=json.dumps(canvas_payload)
        )
        response_body = json.loads(canvas_response.get('body').read())
        if 'images' in response_body:
            st.session_state.image_data = response_body['images'][0]
            st.session_state.image = base64.b64decode(st.session_state.image_data)
            st.session_state.display_image = True
            st.session_state.image_data2 = base64.b64encode(st.session_state.image).decode("utf-8")
            st.rerun()
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def process_image_outpainting_main_object(base_image, additional_prompt, base_prompt):
    canvas_payload = {
        "taskType": "OUTPAINTING",
        "outPaintingParams": {
            "text": additional_prompt,
            "negativeText": "bad quality, low res",
            "image": base_image,
            "maskPrompt": base_prompt,
            "outPaintingMode": "DEFAULT"
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": 720,
            "width": 1280,
        }
    }
    try:
        canvas_response = bedrock_runtime.invoke_model(
            modelId=CANVAS_MODEL_ID,
            body=json.dumps(canvas_payload)
        )
        response_body = json.loads(canvas_response.get('body').read())
        if 'images' in response_body:
            st.session_state.image_data = response_body['images'][0]
            st.session_state.image = base64.b64decode(st.session_state.image_data)
            st.session_state.display_image = True
            st.session_state.image_data2 = base64.b64encode(st.session_state.image).decode("utf-8")
            st.rerun()
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def process_image_remove_background(base_image):
    canvas_payload = {
        "taskType": "BACKGROUND_REMOVAL",
        "backgroundRemovalParams": {
            "image": base_image,
        }
    }
    try:
        canvas_response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            body=json.dumps(canvas_payload)
        )
        response_body = json.loads(canvas_response.get('body').read())
        if 'images' in response_body:
            st.session_state.image_data = response_body['images'][0]
            st.session_state.image = base64.b64decode(st.session_state.image_data)
            st.session_state.display_image = True
            st.session_state.image_data2 = base64.b64encode(st.session_state.image).decode("utf-8")
            st.rerun()
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def process_image_change_color(base_image, color):
    canvas_payload = {
        "taskType": "COLOR_GUIDED_GENERATION",
        "colorGuidedGenerationParams": {
            "colors": [color],
            "referenceImage": base_image,
            "text": "color change",
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "height": 720,
            "width": 1280,
            "seed": random.randint(0, 2147483648)
        }
    }
    try:
        canvas_response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            body=json.dumps(canvas_payload)
        )
        response_body = json.loads(canvas_response.get('body').read())
        if 'images' in response_body:
            st.session_state.image_data = response_body['images'][0]
            st.session_state.image = base64.b64decode(st.session_state.image_data)
            st.session_state.display_image = True
            st.session_state.image_data2 = base64.b64encode(st.session_state.image).decode("utf-8")
            st.rerun()
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def process_image_like_anime(base_image):
    canvas_payload = {
        "taskType": "IMAGE_VARIATION",
        "imageVariationParams": {
            "images": [base_image],
            "text": "anime style, japanese animation",
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "quality": "standard",
            "height": 720,
            "width": 1280,
            "seed": random.randint(0, 2147483648)
        }
    }
    try:
        canvas_response = bedrock_runtime.invoke_model(
            modelId='amazon.nova-canvas-v1:0',
            body=json.dumps(canvas_payload)
        )
        response_body = json.loads(canvas_response.get('body').read())
        if 'images' in response_body:
            st.session_state.image_data = response_body['images'][0]
            st.session_state.image = base64.b64decode(st.session_state.image_data)
            st.session_state.display_image = True
            st.session_state.image_data2 = base64.b64encode(st.session_state.image).decode("utf-8")
            st.rerun()
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")

def generate_video_with_nova_reel(prompt, input_image_base64, duration=6, fps=24, dimension="1280x720"):
    bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)
    model_input = {
        "taskType": "TEXT_VIDEO",
        "textToVideoParams": {
            "text": prompt,
            "images": [{
                "format": "png",
                "source": {
                    "bytes": input_image_base64
                }
            }]
        },
        "videoGenerationConfig": {
            "durationSeconds": duration,
            "fps": fps,
            "dimension": dimension,
            "seed": random.randint(0, 2147483648)
        }
    }
    invocation = bedrock_runtime.start_async_invoke(
        modelId=REEL_MODEL_ID,
        modelInput=model_input,
        outputDataConfig={"s3OutputDataConfig": {"s3Uri": f"s3://{S3_DESTINATION_BUCKET}"}}
    )
    return invocation["invocationArn"]

def download_and_display_video(bucket_name, video_key):
    s3_client = boto3.client('s3', region_name=REGION)
    try:
        local_file = f"temp_video_{int(time.time())}.mp4"
        s3_client.download_file(bucket_name, video_key, local_file)
        with open(local_file, 'rb') as video_file:
            video_bytes = video_file.read()
        st.video(video_bytes)
    except Exception as e:
        st.error(f"動画の取得に失敗しました: {str(e)}")

def wait_for_video_generation(invocation_arn):
    bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)
    while True:
        response = bedrock_runtime.get_async_invoke(
            invocationArn=invocation_arn
        )
        status = response["status"]
        st.write(f"ステータス: {status}")

        if status == "Completed":
            s3_prefix = invocation_arn.split('/')[-1]
            # 動画をダウンロードしてセッション状態に保存
            s3_client = boto3.client('s3', region_name=REGION)
            try:
                local_file = f"temp_video_{int(time.time())}.mp4"
                s3_client.download_file(S3_DESTINATION_BUCKET, f"{s3_prefix}/output.mp4", local_file)
                with open(local_file, 'rb') as video_file:
                    st.session_state.video_data = video_file.read()
                    st.session_state.video_generated = True
                    st.rerun()
            except Exception as e:
                st.error(f"動画の取得に失敗しました: {str(e)}")

        if status != "InProgress":
            break
        time.sleep(SLEEP_TIME)

def translate_and_enhance_prompt(prompt):
    client = boto3.client(
        "bedrock-runtime",
        region_name=REGION
    )

    body = [
            {
                "role": "user",
                "content": [{"text": f"以下の文言は生成AIの画像生成のText-Imageのプロンプトです。画像が生成しやすいように英語に翻訳の上、具体性がないものは具体的に描写できるように文言を足してください。また、出力は英語文そのもののみ出力してください。枕詞は不要です。\n\n{prompt}"}]
            }
    ]

    try:
        response = client.converse(
            modelId=PRO_MODEL_ID,
            messages=body,
        )
        translated_prompt = response['output']['message']['content'][0]['text']
        return translated_prompt
    except Exception as e:
        st.error(f"翻訳エラー: {str(e)}")
        return prompt

def main():
    st.title("🐰 Canvas 📷️/ Reel📺️ デモ 🐰")
    st.write("Amazonの最新モデルNova CanvasとNova Reelを試してみましょう！🐰🐰🐰")
    st.write("時差ボケで作ったアプリなので例外処理がいい加減です。エラーが起きたらやり直すこと")
    st.divider()

    # 左右のカラムを作成
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("元の画像")
        # 画像の表示を先に行う
        if 'display_image' in st.session_state and st.session_state.display_image:
            st.image(st.session_state.original_image)

        # プロンプト入力を画像の下に配置
        image_prompt = st.text_input("画像生成プロンプト")
        if st.button("画像を生成"):
            image_prompt = translate_and_enhance_prompt(image_prompt)
            st.write(f"生成AIの画像生成のText-Imageのプロンプト")
            st.write(image_prompt)

            canvas_payload = {
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": image_prompt,
                    "negativeText": "bad quality, low res",
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "quality": "standard",
                    "height": 720,
                    "width": 1280,
                    "seed": random.randint(0, 2147483648)
                }
            }

            try:
                canvas_response = bedrock_runtime.invoke_model(
                    modelId='amazon.nova-canvas-v1:0',
                    body=json.dumps(canvas_payload)
                )
                response_body = json.loads(canvas_response.get('body').read())
                if 'images' in response_body:
                    st.session_state.original_image_data = response_body['images'][0]
                    st.session_state.original_image = base64.b64decode(st.session_state.original_image_data)
                    st.session_state.display_image = True
                    st.session_state.image_data2 = base64.b64encode(st.session_state.original_image).decode("utf-8")
                    st.rerun()
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

    with right_col:
        st.subheader("加工後の画像")
        media_container = st.empty()
        if 'display_image' in st.session_state and st.session_state.display_image:
            # 加工後の画像または動画を表示
            if 'video_generated' in st.session_state and st.session_state.video_generated:
                media_container.video(st.session_state.video_data)
            elif 'image' in st.session_state and st.session_state.image is not None:
                media_container.image(st.session_state.image)

            # ボタンを3列に配置
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("柴犬にする"):
                    process_image_inpainting_main_object(
                        st.session_state.original_image_data,
                        f"Shiba Inu, cute dog, fluffy fur",
                        image_prompt,
                    )
                if st.button("背景を消す"):
                    process_image_remove_background(
                        st.session_state.original_image_data,
                    )

            with col2:
                if st.button("色を変える"):
                    st.session_state.color_change_mode = True
                if st.session_state.color_change_mode:
                    selected_color = st.color_picker("色を選択", st.session_state.selected_color, key="color_picker")
                    st.session_state.selected_color = selected_color.upper()
                    if st.button("決定"):
                        process_image_change_color(
                            st.session_state.original_image_data,
                            st.session_state.selected_color
                        )
                        st.session_state.color_change_mode = False

                if st.button("アニメ風にする"):
                    process_image_like_anime(
                        st.session_state.original_image_data,
                    )

            with col3:
                if st.button("メインオブジェクトを消す"):
                    process_image_outpainting_main_object(
                        st.session_state.original_image_data,
                        f"remove, erase {image_prompt}",
                        image_prompt,
                    )
                if st.button("動画を作成"):
                    invocation_arn = generate_video_with_nova_reel(
                        f"'{image_prompt}'. Move the eyes and ears in a cute way. We want to create movement, so we use pan/zoom to move the screen. The background is also moved.Move the eyes and ears in a cute way. We want to create movement, so we use pan/zoom to move the screen. The background is also moved.",
                        st.session_state.original_image_data
                    )
                    wait_for_video_generation(invocation_arn)
                    st.session_state.video_generated = True


if __name__ == "__main__":
    main()