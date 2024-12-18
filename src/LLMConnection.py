import os
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI


openai_api_key = os.environ["OPENAI_API_KEY"] 

class LLMModel:

    def __init__(self, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
    
    def get_completion(self, prompt=None, system_message=None, temperature=0):
        message = []
        try:
            if system_message:
                message.append({"role": "system", "content": system_message})
            message.append({"role":"user", "content":prompt})
            response = self.client.chat.completions.create(
                model=self.model,
                messages=message,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occured: {e}"
            
class CustomeOpenAIEmbeddings(OpenAIEmbeddings):
    def __init__(self, openai_api_key=openai_api_key):
        super().__init__(openai_api_key=openai_api_key)
        
    def _embed_documents(self, texts):
        embeddings = [
            self.client.create(input=text, model="text-embedding-ada-002").data[0].embedding 
            for text in texts
        ]
        return embeddings  # <--- use OpenAIEmbedding's embedding function
    # def embed_query(texts):
    #     return super().embed_documents(texts)
    
    def __call__(self, input):
        return self._embed_documents(input)
