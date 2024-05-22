from setuptools import setup, find_packages

setup(
    name='mcqgenerator',
    version='0.1',
    packages=find_packages(),
    install_requires=['langchain','langchain_community','langchain_openai','python-dotenv','streamlit'],
 
    # Metadata
    author='Dipak Adhikari',
    author_email='adhikarydeepak2002@gmail.com',
)
