##################################
# TO RUN:
#   streamlit run app.py
##################################

import os
import openai
import sys
import streamlit as st

sys.path.append("../..")

from langchain.llms import OpenAI
from pathlib import Path
from files import FileSystem
from controller import PdfQuestionController


# persist_directory = 'docs/chroma/'

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.environ["OPENAI_API_KEY"]

llm_name = "gpt-3.5-turbo"
save_folder = "./docs/"
file_name = ""

controller = PdfQuestionController(save_folder)
file_sys = FileSystem(save_folder)
answerer = None

# UI
st.set_page_config(page_title="Search a PDF", page_icon="🫵")
st.title("Rucci Q&A thing")

option = st.sidebar.selectbox(
    "Which document would you like to search?", file_sys.getPdfFiles(), index=0
)

if option:
    file_name = option
    controller = PdfQuestionController(save_folder)

st.text(f"The current file is {file_name}")

message = st.chat_message("assistant")
message.write(f"Your answers from '{file_name}' will appear below:")
prompt = st.chat_input(placeholder=f"ask a question about this pdf file")

if prompt:
    user_message = st.chat_message("user")
    user_message.write(prompt)

    if answerer is None:
        answerer = controller.get_answerer(file_name)
    answer_chain = answerer.get_qa_chain()
    result = answer_chain.run(prompt)
    message.write(result)
    print(f"Here's your answer: {result}")

File = st.sidebar.file_uploader(label="Upload file", type=["pdf", "docx"])

if File:
    st.markdown("**The file is sucessfully Uploaded.**")

    save_path = Path(save_folder, File.name)

    st.write(save_path)

    with open(save_path, mode="wb") as w:
        w.write(File.getvalue())

    if save_path.exists():
        st.success(f"File {File.name} is successfully saved!")

    answerer = controller.get_answerer(File.name)
