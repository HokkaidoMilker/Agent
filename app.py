import os
import streamlit as st

# ============================================================
# 将 Streamlit Cloud Secrets 注入到环境变量
# dashscope / langchain 等库通过 os.environ 读取 API Key，
# 而 Streamlit Cloud 的 secrets 只存在于 st.secrets，需要手动注入
# ============================================================
try:
    for key, value in st.secrets.items():
        os.environ[key] = str(value)
except Exception:
    pass  # 本地开发时 st.secrets 可能不存在

# ============================================================
# 登录认证
# ============================================================
APP_PASSWORD = os.environ.get("APP_PASSWORD", "")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 智扫通机器人智能客服")
    st.divider()
    password_input = st.text_input("请输入访问密码", type="password")

    if password_input:
        if password_input == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("密码错误，请重试")
    st.stop()

# ============================================================
# 主应用
# ============================================================
from agent.tools.react_agent import ReactAgent

# 标题
st.title("智扫通机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])
# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)


        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk


        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": response_messages[-1]})