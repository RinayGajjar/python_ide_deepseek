import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 🎨 Custom Styling for Dark Mode UI
st.markdown("""
    <style>
        .main { background-color: #1a1a1a; color: #ffffff; }
        .sidebar .sidebar-content { background-color: #2d2d2d; }
        .stTextInput textarea { color: #ffffff !important; }
        .stSelectbox div[data-baseweb="select"] { color: white !important; background-color: #3d3d3d !important; }
        .stSelectbox svg { fill: white !important; }
        .stSelectbox option { background-color: #2d2d2d !important; color: white !important; }
        div[role="listbox"] div { background-color: #2d2d2d !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 🎮 App Title
st.title("🔥 Valorant Rank-Up Coach")
st.caption("🚀 AI-powered gaming assistant for improving your Valorant skills! 🎯")

# 🛠️ Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Choose Model")
    selected_model = st.selectbox("Select LLM Model", ["deepseek-r1:1.5b", "deepseek-r1:3b"], index=0)
    st.divider()
    st.markdown("### 🏆 Coaching Features")
    st.markdown("""
    - 🎯 Aim & Crosshair Training
    - 🔥 Game Sense & Strategy
    - 🛠️ Role & Agent Mastery
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

# 🔹 Load LLM
llm_engine = ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",
    temperature=0.7
)

# 🧠 System Prompt - AI Persona
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are a professional Valorant coach helping a player improve their skills. "
    "You provide guidance on aim training, crosshair placement, team coordination, and game sense. "
    "Focus on giving **practical and concise tips**."
)

# 💾 Session State - Chat History
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm your Valorant Coach! 🎮 How can I help you rank up?"}]

# 📦 Chat Container (Persistent Messages)
chat_container = st.container()

with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ✍️ User Input Field
user_query = st.chat_input("Ask me anything about Valorant strategies, agent selection, or game mechanics...")

# 🔹 Generate AI Response Function
def generate_response(prompt):
    try:
        response = prompt | llm_engine | StrOutputParser()
        ai_response = response.invoke({})
        
        # 🛑 Prevent Unwanted DeepSeek Intros
        if "I'm DeepSeek" in ai_response:
            ai_response = "Let's focus on improving your Valorant gameplay! 🎯"

        return ai_response

    except Exception as e:
        print(f"🚨 AI Error: {e}")
        return "⚠️ AI is currently unavailable. Please try again later!"

# 🔹 Build Chat Prompt
def build_prompt():
    prompt_seq = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_seq.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_seq.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate(prompt_seq)

# 🚀 Process User Input
if user_query:
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    with st.spinner("Thinking..."):
        prompt = build_prompt()
        ai_response = generate_response(prompt)

    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    st.rerun()
