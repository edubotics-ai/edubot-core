from dotenv import load_dotenv
import os

load_dotenv()

# API Keys - Loaded from the .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

opening_message = f"Hey, What Can I Help You With?\n\nYou can me ask me questions about the course logistics, course content, about the final project, or anything else!"

# Prompt Templates

openai_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

openai_prompt_template_with_history = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use the history to answer the question if you can.
Chat History:
{chat_history}
Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

tinyllama_prompt_template = """
<|im_start|>system
Assistant is an intelligent chatbot designed to help students with questions regarding the course. Only answer questions using the context below and if you're not sure of an answer, you can say "I don't know". Always give a breif and concise answer to the question. Use the history to answer the question if you can.

Context:
{context}
<|im_end|>
<|im_start|>user
Question: Who is the instructor for this course?
<|im_end|>
<|im_start|>assistant
The instructor for this course is Prof. Thomas Gardos.
<|im_end|>
<|im_start|>user
Question: {question}
<|im_end|>
<|im_start|>assistant
"""

tinyllama_prompt_template_with_history = """
<|im_start|>system
Assistant is an intelligent chatbot designed to help students with questions regarding the course. Only answer questions using the context below and if you're not sure of an answer, you can say "I don't know". Always give a breif and concise answer to the question.

Chat History:
{chat_history}
Context:
{context}
<|im_end|>
<|im_start|>user
Question: Who is the instructor for this course?
<|im_end|>
<|im_start|>assistant
The instructor for this course is Prof. Thomas Gardos.
<|im_end|>
<|im_start|>user
Question: {question}
<|im_end|>
<|im_start|>assistant
"""


# Model Paths

LLAMA_PATH = "storage/models/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf"
MISTRAL_PATH = "storage/models/mistral-7b-v0.1.Q4_K_M.gguf"
