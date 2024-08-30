import yaml, os
from datetime import datetime
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from asr import sense_voice
from tts import chattts
from tts import sambert_dashscope
from tts import sambert

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from langchain.embeddings import HuggingFaceEmbeddings

from sys_prompt import get_sys_prompt

with open("secrets/cfg.yaml", "r", encoding='utf-8') as file:
    conf = yaml.safe_load(file)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or conf["api"]["openai_api_key"]
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or conf["api"]["openai_base_url"]
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME") or conf["api"]["openai_model_name"]

ai_name = conf["ai"]["ai_name"]


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
    
# save chroma
embedding_function = HuggingFaceEmbeddings(
            model_name="shibing624/text2vec-base-chinese",
            model_kwargs={"device": "cuda"},
            encode_kwargs={"batch_size": 1, "normalize_embeddings": True},
        )
vectorstore = Chroma(embedding_function)
retriever = vectorstore.as_retriever(search_kwargs=dict(k=1))
memory = VectorStoreRetrieverMemory(retriever=retriever)
print(memory.load_memory_variables())

# Set up the LangChain, passing in Message History
sys_prompt = get_sys_prompt(conf)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", sys_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)
llm = ChatOpenAI(
    api_key = OPENAI_API_KEY,
    base_url = OPENAI_BASE_URL,
    model_name = OPENAI_MODEL_NAME, 
    temperature = 0.8, 
    top_p = 1,
    max_tokens = 256)

chain = (prompt | llm)
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: memory,
    input_messages_key="question",
    history_messages_key="history",
)

config = {"configurable": {"session_id": USER_SESSION_ID}}
response = chain_with_history.stream({"question": prompt}, config)
for r in response:
    print(r.content, end=" ")