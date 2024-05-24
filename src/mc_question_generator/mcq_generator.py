from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings('ignore')
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
from langchain.chains import LLMChain
# from langchain.callbacks import get_openai_callback
import os
import json
import pandas as pd
import traceback
from langchain_google_genai import ChatGoogleGenerativeAI

# llm=ChatOpenAI(model="gpt-3.5-turbo",temperature=0.6)
llm=ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.7)



TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{RESPONSE_JSON}

"""

mcq_prompt=PromptTemplate(
    template=TEMPLATE,
    input_variables=['text','number','subject','tone','RESPONSE_JSON']
)

mcq_chain=LLMChain(llm=llm,prompt=mcq_prompt,output_key="quiz",verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

eval_prompt_temp=PromptTemplate(
    template=TEMPLATE2,
    input_variables=['subject','quiz']
)

review_chain=LLMChain(llm=llm,prompt=eval_prompt_temp,output_key="review",verbose=True)

generate_evaluate_chain=SequentialChain(chains=[mcq_chain,review_chain],input_variables=["text","number","subject","tone","RESPONSE_JSON"],output_variables=["quiz", "review"], verbose=True,)





# messi_path=r"D:\MCQ-GENERATOR\data.txt"

# with open(messi_path,'r') as file:
#     text=file.read()

# with get_openai_callback() as cb:
#     response=generate_evaluate_chain(
#         {
#         "text": text,
#         "number": 10,
#         "subject": "Lionel Messi",
#         "tone": "Simple",
#         "RESPONSE_JSON": json.dumps(RESPONSE_JSON)
#         }
#     )

# quiz=response.get('quiz')
# # Remove the leading '### RESPONSE_JSON\n'
# json_str = quiz.lstrip('### RESPONSE_JSON\n')

# final_quiz=json.loads(json_str)




