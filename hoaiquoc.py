import streamlit as st
from google import genai
from google.genai import types

# Khởi tạo Gemini client
client = genai.Client(api_key="AIzaSyCPga9Jgjp1kixII-SIVDfNVZWHeBo3Hz0")

# Ví dụ để huấn luyện AI phản hồi theo phong cách riêng
examples = [
    {
        "parts": [
            {"text": "input: Who are you?"},
            {"text": "output: I am a chatbot of Ho  aiQuoc"},
        ]
    },
    {
        "parts": [
            {"text": "input: What's your name?"},
            {"text": "output: My name is Nguyen Hoai Quoc"},
        ]
    }
]

st.title("Chatbot HoaiQuoc")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận input từ người dùng
if prompt := st.chat_input("Nhập nội dung của bạn..."):
    # Lưu tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tạo prompt đầy đủ từ ví dụ + input
    fullPrompt = []
    for example in examples:
        for part in example["parts"]:
            fullPrompt.append(part)
    fullPrompt.append({"text": f"input: {prompt}"})
    fullPrompt.append({"text": "output:"})

    # Gọi Gemini để phản hồi
    response_stream = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=fullPrompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            system_instruction="You are a chatbot of HoaiQuoc. Your name is Nguyen Hoai Quoc"
        )
    )

    # Hiển thị phản hồi dạng streaming
    full_response = ""
    with st.chat_message("assistant"):
        response_container = st.empty()
        for chunk in response_stream:
            full_response += chunk.text
            response_container.markdown(full_response)

    # Lưu phản hồi vào lịch sử
    st.session_state.messages.append({"role": "assistant", "content": full_response})
