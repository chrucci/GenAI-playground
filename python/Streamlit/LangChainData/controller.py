from loader import PdfLoader
from ask import QuestionAnswerer

class PdfQuestionController:
    
    #constructor
    def __init__(self, save_folder):
        self.save_folder = save_folder
    
    #get answerer
    def get_answerer(self, file_name):
        path = f"{self.save_folder}{file_name}"
        print(f"loading from {path}")
        vectordb = PdfLoader().load(path)
        self.answerer = QuestionAnswerer(vectordb)
        return self.answerer