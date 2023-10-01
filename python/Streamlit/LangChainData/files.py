
# class for interacting with the file system
import os
class FileSystem:
    
    # constructor
    def __init__(self, directory):
        self.directory = directory
    
    # retrieve a list of pdf files from the given directory
    def getPdfFiles(self):
        pdf_files = []
        for file in os.listdir(self.directory):
            if file.endswith(".pdf"):
                pdf_files.append(file)      
       
        # sort the list alphabetically
        pdf_files.sort()         
        return pdf_files