import streamlit as st
import google.generativeai as genai

# タイトルと説明の表示
st.title("💬 Gemini Chatbot")
st.write(
    "This is a chatbot using Google's Gemini API. Please provide your API key to start."
)

# Gemini APIキーの入力
gemini_api_key = st.text_input("Gemini API Key", type="password")

# セッションの初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# APIキーが入力された場合の処理
if gemini_api_key:
    try:
        # Geminiクライアントの設定
        genai.configure(api_key=gemini_api_key)

        # モデルの定義
        model = genai.GenerativeModel(model_name='gemini-1.5-pro')

        # チャット履歴の表示
        st.subheader("Chat History")
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # ユーザー入力
        prompt = st.chat_input("Enter your message:")
        if prompt:
            # ユーザーのメッセージを保存
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Gemini APIを使用して応答を生成
            try:
                response = model.generate_content(contents=[prompt])
                assistant_reply = response.text  # 応答を取得

                # 応答を保存
                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

                # 応答の表示
                with st.chat_message("assistant"):
                    st.markdown(assistant_reply)

            except Exception as e:
                st.error(f"Error occurred while generating response: {e}")

    except Exception as e:
        st.error(f"Failed to configure the Gemini API: {e}")
else:
    st.info("Please provide your Gemini API key to start the chatbot.", icon="🗝️")
