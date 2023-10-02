from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class QuestionAnswerer:
    default_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, 
    don't try to make up an answer. 
    Keep the answer as concise as possible. 
    If you can, please cite from which page or section your answers were derived.  
    Also, please site the source of the PDF.
    If you don't know, that's ok.  
    You can just say your don't know which page or section the material came from.  
    But please don't make up an answer.  
    Always compliment me at the end of the answer for asking such a great question. 
{context}
Question: {question}
Helpful Answer:"""
    def __init__(self, vectorbd, qa_propmpt_template = default_template) -> None:
        self.vectorbd = vectorbd
        self.qa_propmpt_template = qa_propmpt_template
        vector_db_len = vectorbd._collection.count()
        embedding_text = f"number of embeddings from pdf = {vector_db_len}"
        print(embedding_text)
        
    #get the question and answer chain
    def get_qa_chain(self, llm_name="gpt-3.5-turbo"):
        llm = ChatOpenAI(model_name=llm_name, temperature=0)
        
        return RetrievalQA.from_chain_type(
            llm,
            retriever=self.vectorbd.as_retriever(),
            return_source_documents=False,
            chain_type_kwargs={"prompt": PromptTemplate.from_template(self.qa_propmpt_template)}
        )