import streamlit as st
from openai import OpenAI
from utils import process_retrieve_summary_task
from utils import process_retrieve_questions_task

st.title("Youtube Video Assistant")

assistant_task = st.sidebar.selectbox("Choose Tasks", ["Questions Creator","Summary Generator"])

open_api_key = st.sidebar.text_input("Enter OpenAI API Key", type='password')
st.sidebar.markdown("[Get OpenAI API Key](https://openai.platform.com/account/keys)")

if open_api_key:
    client = OpenAI(api_key=open_api_key)

if assistant_task == "Summary Generator":
    with st.form("summary_create_form"):
        st.subheader("Summarize youtube videos by uploading the URL")
        youtube_url = st.text_input("Enter the Youtube video link to create summary")
        language = st.selectbox("Choose the language in which summary is to be created", ["English(UK)", "Spanish", "French"])
        submitted = st.form_submit_button("Submit")
        if not open_api_key:
            st.info("Please enter your OpenAI API key to continue")
        elif submitted:
            summary = process_retrieve_summary_task(client, youtube_url)
            st.write("----")
            st.write("#### Below is the summary created:")
            st.write(summary)            
        
if assistant_task == "Questions Creator":
    with st.form("questions_create_form"):
        st.subheader("Generate queries from the Youtube video by uploading URL")
        youtube_url = st.text_input("Enter the Youtube video link to create questions")
        submitted = st.form_submit_button("Submit")
        if not open_api_key:
            st.info("Please enter your OpenAI API key to continue")
        elif submitted:
            questions_list = process_retrieve_questions_task(client, youtube_url)
            if questions_list:
                st.write("----")
                st.write("#### Below are the questions:")
                st.write(questions_list)