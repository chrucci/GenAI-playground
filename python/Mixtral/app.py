# Just runs .complete to make sure the LLM is listening
from llama_index.llms.ollama import Ollama

llm = Ollama(model="mixtral", request_timeout=360.0)
response = llm.complete("Who is Yngwie Malmsteen?")
print(response)
