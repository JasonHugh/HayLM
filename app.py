import streamlit as st
from lmdeploy import GenerationConfig, ChatTemplateConfig
from lmdeploy import pipeline, TurbomindEngineConfig

from sys_prompt import get_sys_prompt
import yaml

import os
# download HayLM model to the base_path directory using git tool
base_path = './HayLM-model'
os.system(f'git clone https://code.openxlab.org.cn/hayhu/HayLM.git {base_path}')
os.system(f'cd {base_path} && git lfs pull')

with open("cfg.yaml", "r") as file:
    conf = yaml.safe_load(file)
ai_name = conf["ai"]["ai_name"]

# model_name_or_path = "/root/learning/InternLM/XTuner/merged_20b-w4a16-4bit" 
model_name_or_path = "./HayLM-model" 
model_template = "internlm2"
model_format = "hf"
# model_format = "awq"

st.set_page_config(page_title=ai_name, page_icon="🧚")
st.title("🧚 "+ai_name)

@st.cache_resource
def load_model():
    backend_config = TurbomindEngineConfig(cache_max_entry_count=0.2, model_format=model_format)
    pipe = pipeline(model_name_or_path, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_template))
    return pipe


def main():
    # torch.cuda.empty_cache()
    print('load model begin.')
    pipe = load_model()
    print('load model end.')

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [{
            'role': 'system',
            'content': get_sys_prompt(conf)
        },{
            'role': 'assistant',
            'content': '我是{}，你的虚拟玩伴，能够与你智能互动，学习并适应你的性格特点，陪伴你快乐成长。快来和我聊天吧！'.format(ai_name)
        }]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message['role'] in ('user', 'assistant'):
            with st.chat_message(message['role'], avatar=message.get('avatar')):
                st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input('What is up?'):
        # Display user message in chat message container
        with st.chat_message('user'):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt,
        })
        gen_config = GenerationConfig(top_p=0.8, top_k=40, temperature=0.8, max_new_tokens=1024)
        reponse_text = ''
        with st.chat_message('assistant'):
            placeholder = st.empty()
            for response in pipe.stream_infer(st.session_state.messages, gen_config=gen_config):
                reponse_text += response.text
                placeholder.markdown(reponse_text)
        
        # Add robot response to chat history
        st.session_state.messages.append({
            'role': 'assistant',
            'content': reponse_text, 
        })


if __name__ == '__main__':
    main()