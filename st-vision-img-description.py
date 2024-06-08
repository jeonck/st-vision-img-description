import streamlit as st
import requests
import base64
import json
import os
import dotenv
dotenv.load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]
api_url = os.environ["OPENAI_API_URL"]
# The base URL for your Azure OpenAI resource. e.g. "https://<your resource name>.openai.azure.com"

# OpenAI API 설정
OPENAI_API_URL = api_url
OPENAI_API_KEY = api_key

# 이미지 URL을 통한 Vision API 호출 함수
def get_vision_result(image_url):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {"role": "system", "content": "You must answer in Korean and summarize in three sentences."},
            {"role": "user", "content": [{"type": "text", "text": "What’s in this image?"}, {"type": "image_url", "image_url": image_url}]}
        ],
        "max_tokens": 300
    }
    response = requests.post(OPENAI_API_URL, headers=headers, data=json.dumps(data))
    return response.json()

# Streamlit UI 설정
st.title("이미지 해석 앱")
st.write("OpenAI의 Vision API를 사용하여 이미지를 해석합니다.")

# 이미지 업로드 또는 URL 입력 받기
upload_option = st.radio("이미지를 업로드 하시겠습니까 아니면 URL을 입력 하시겠습니까?", ("업로드", "URL 입력"))

if upload_option == "업로드":
    uploaded_file = st.file_uploader("이미지를 업로드 하세요", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        image_base64 = base64.b64encode(image_bytes).decode()
        image_url = f"data:image/jpeg;base64,{image_base64}"
else:
    image_url = st.text_input("이미지 URL을 입력하세요")

# 이미지 분석 버튼
if st.button("이미지 분석"):
    if image_url:
        result = get_vision_result(image_url)
        st.write("이미지 분석 결과:")
        st.json(result)
    else:
        st.write("이미지를 업로드하거나 URL을 입력하세요.")
