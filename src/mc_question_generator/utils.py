import os
import json
import traceback
import fitz
from docx import Document
import PyPDF2

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading PDF File")
    
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        raise Exception("File format not supported")

import ast
def get_table_data(quiz_str):
    try:
        quiz_dict = ast.literal_eval(quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            
            options=" | ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
                 ]
            )
            
            quiz_table_data.append({'MCQ':value["mcq"],'Choices': options, 'Correct':value["correct"]})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

