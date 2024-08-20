import yaml, os
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
import streamlit as st

from sys_prompt import get_sys_prompt

with open("cfg.yaml", "r") as file:
    conf = yaml.safe_load(file)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or conf["api"]["openai_api_key"]
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or conf["api"]["openai_base_url"]
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME") or conf["api"]["openai_model_name"]

ai_name = conf["ai"]["ai_name"]
st.set_page_config(page_title=ai_name, page_icon="🧚")
st.title("🧚 "+ai_name)

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

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", get_sys_prompt(conf)),
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
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    response = chain_with_history.stream({"question": prompt}, config)
    with st.chat_message("ai"):
        st.write_stream(response)
