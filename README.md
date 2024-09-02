# HayLM

基于InternLM进行微调的一个儿童陪伴大模型

## 介绍

HayLM是专门为儿童训练的大模型，HayLM通过对InternLM的训练和微调，结合儿童心理学、教育学以及对话风格的数据训练，实现与儿童的智能互动，并在交流过程中不断学习和适应用户特性，成为一个伴随儿童成长的虚拟朋友。 

基于 InternLM 的大模型学习项目，欢迎大家也来参加书生大模型实战营项目（http://github.com/internLM/tutorial）

## 项目目标
- 打造一款具有高度智能互动能力的儿童陪伴产品，让儿童在快乐中成长。
- 结合儿童心理学、教育学原理，为儿童提供个性化、有针对性的陪伴和教育。
- 不断优化和升级模型，使其成为伴随儿童成长的虚拟朋友。

## 产品功能
- 日常陪伴：与儿童进行聊天，倾听儿童的心声，解答儿童的问题，陪伴儿童度过快乐时光。
- 教育辅导：针对儿童的学习需求，提供语文、数学、英语等学科辅导，助力儿童提高学习成绩。
- 习惯养成：通过设定目标和奖励机制，帮助儿童养成良好的生活习惯和学习习惯。
- 娱乐互动：提供故事、歌曲、游戏等多种娱乐形式，丰富儿童的课余生活。

## 架构图
![image](https://github.com/user-attachments/assets/8de4be90-a318-4b28-9972-a36801c9e418)

## 技术细节
- 数据收集与处理：收集大量儿童对话数据，结合儿童心理学、教育学原理，对数据进行筛选和处理，为模型训练提供高质量素材。
- 模型训练：使用Xtuner对InternLM 2.5 7B模型进行微调和训练，确保了模型和儿童的沟通风格。
- 模型测试：进行多场景、多年龄段的测试，确保模型的安全性和可靠性。
- 模型部署：使用LMdeploy部署openai server
- 记忆框架：使用Langchain等大模型框架，实现大模型的记忆功能
- 情绪识别：通过emotion2vec语音情感表征模型来识别儿童的情绪
- 交互模式：通过ASR和TTS技术，让儿童和HayLM可以实现语音沟通

## 对话效果示例
![image](https://github.com/user-attachments/assets/3800218c-393e-4f93-8977-30370166a5aa)
![image](https://github.com/user-attachments/assets/4bbe2477-ebd0-4dc6-9197-5edb87e81262)
![image](https://github.com/user-attachments/assets/5225d3f0-1e29-4e9b-b346-bc9ef5124e5b)

## 项目进度
- [x] HayLM儿童陪伴大模型训练
- [x] 儿童玩伴提示词
- [x] streamlit web
- [ ] ASR
  - [x] SenceVoice模型推理
  - [ ] 部署为server
- [ ] TTS
  - [x] Sambert模型推理
  - [x] chatTTS模型推理
  - [ ] 部署为server
- [ ] fastapi后端开发(working)
- [ ] sqlite+qdrant持久化记忆(working)
- [ ] 家长配置端web
  - [ ] 更改配置信息
  - [ ] 切换角色（玩伴/教师）
- [ ] 接入微信机器人
- [ ] 开发语音聊天硬件设备

## Requirements
Python 3.10
PyTorch 2.2.1
cu121

## 运行
```bash
pip install -r requirements.txt
streamlit run app.py
```
