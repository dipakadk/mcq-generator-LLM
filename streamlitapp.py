import streamlit as st
import os
import json
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from src.mc_question_generator.utils import read_file, get_table_data
from src.mc_question_generator.mcq_generator import generate_evaluate_chain
from src.mc_question_generator.logger import logging

# Load JSON file
with open("D:\\MCQ-GENERATOR\\Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

st.title("MCQ Generator")
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload file (text, pdf and docx)")

    mcq_number =st.number_input("How many MCQ question you want to generate?",min_value=3,max_value=30)


    subject = st.text_input("Enter a subject", max_chars=20)

    tone = st.selectbox("Enter difficulty level: ", ['Beginner', 'Intermediate', 'Advanced'])

    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_number and subject and tone:
        with st.spinner("Loading"):
            try:
                text = read_file(uploaded_file)
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_number,
                        "subject": subject,
                        "tone": tone,
                        "RESPONSE_JSON": RESPONSE_JSON,  
                    }
                )
            except Exception as e:
                st.write("Error:", e)
            else:
                quiz = response.get("quiz")
                if quiz is not None:
                        table_data=get_table_data(quiz)

                        if table_data is not None:
                            # Check if table_data is not empty
                            if table_data:
                                df=pd.DataFrame(table_data)
                                st.table(df)
                            else:
                                st.error("No data available to display.")
                        else:
                            st.error("Error in the table data")

                else:
                    st.write(response)
