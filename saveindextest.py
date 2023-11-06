import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document,  download_loader
from llama_index.llms import OpenAI
import openai
from llama_index import SimpleDirectoryReader

openai.api_key = st.secrets.openai_key

def read_url_list(file_path):
    try:
        with open(file_path, 'r') as file:
            url_list = file.read().splitlines()
        return url_list
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
url_list = read_url_list(".\Data\PageList.txt")

def load_data():
    #reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
    loader = BeautifulSoupWebReader()
    # docs = loader.load_data(urls=['https://www.rcgov.org/departments/mayor-s-office-city-council/mayor-s-office.html', 'https://www.rcgov.org/departments/mayor-s-office-city-council/city-council.html',
    #                                 'https://www.rcgov.org/departments.html', 'https://www.rcgov.org/departments/finance.html'])
    docs = loader.load_data(urls=url_list)
    #docs = reader.load_data()
    service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the City of Rapid City and your job is to answer citizen questions. Assume that all questions are related to the City of Rapid City. Keep your answers simple and based on facts – do not hallucinate features."))
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index

index = load_data()
index.storage_context.persist("testindex")

