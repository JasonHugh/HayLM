import yaml, os
from datetime import datetime
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
import streamlit as st
from audiorecorder import audiorecorder
from asr import sense_voice
from tts import chattts
from tts import sambert_dashscope
from tts import sambert

from sys_prompt import get_sys_prompt

with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or conf["api"]["openai_api_key"]
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or conf["api"]["openai_base_url"]
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME") or conf["api"]["openai_model_name"]

ai_name = conf["ai"]["ai_name"]
st.set_page_config(page_title=ai_name, page_icon="🧚")
st.title("🧚 "+ai_name)

# custom css
audio_style = """<style>
    [data-testid="element-container"] > iframe{
        position: fixed;
        bottom: 55px;
        z-index: 999;
        width: 42px;
    }
    [data-testid="stBottomBlockContainer"] {
        padding-left: 6.1rem
    }
</style>"""
st.write(audio_style, unsafe_allow_html=True)
audio = audiorecorder("🎙️", "🛑")

USER_SESSION_ID = "any"

# Set up memory
db_path = "db"
if not os.path.exists(db_path):
    os.makedirs(db_path)
msgs = StreamlitChatMessageHistory()
# msgs = SQLChatMessageHistory(
#     session_id=USER_SESSION_ID, connection_string="sqlite:///db/"+USER_SESSION_ID+".db"
# )
if len(msgs.messages) == 0:
    msgs.add_ai_message("""
我是{ai_name}，你的虚拟玩伴，能够与你智能互动，学习并适应你的性格特点，陪伴你快乐成长。快来和我聊天吧！
""".format(ai_name=ai_name))

# Set up the LangChain, passing in Message History
sys_prompt = get_sys_prompt(conf)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | ChatOpenAI(
    api_key = OPENAI_API_KEY,
    base_url = OPENAI_BASE_URL,
    model_name = OPENAI_MODEL_NAME, 
    temperature = 0.8, 
    top_p = 1,
    max_tokens = 256)
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history",
)

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    type = msg.type
    if type == "AIMessageChunk":
        type = "ai"
    st.chat_message(type).write(msg.content)

# ASR Start
asr_text = ""

asr_model = sense_voice.load_asr_model()

if len(audio) > 0:
    audio_folder = "audio"
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
    audio_path = "{}/{}.wav".format(audio_folder, datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    audio.export(audio_path, format="wav")

    # get asr text
    asr_text = sense_voice.get_asr_text(asr_model, os.path.abspath(audio_path))
    print("User: "+asr_text)
    os.remove(audio_path)

# ASR End

# tts_model = sambert.load_tts_model()
# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input() or asr_text:
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": USER_SESSION_ID}}
    response = chain_with_history.stream({"question": prompt}, config)
    reponse_text = ''
    print(msgs)
    with st.chat_message("ai"):
        # st.write_stream(response)
        placeholder = st.empty()
        for r in response:
            reponse_text += r.content
            placeholder.markdown(reponse_text)
            print(r)
        # get tts
        with st.spinner('Generating audio...'):
            audio_path = sambert_dashscope.get_tts_audio(reponse_text)
            # audio_path = sambert.get_tts_audio(tts_model, reponse_text)
        st.audio(audio_path, format="audio/wav", loop=False, autoplay=True)
