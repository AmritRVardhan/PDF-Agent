from src import LLMConnection
from src import IngestPDF
from src import embeddings
import pickle
import os


def main():
    # def ok_so_this_works():
    #     OpenAIClient = LLMConnection.LLMModel()
    #     response = OpenAIClient.get_completion(prompt="Just respond with Hi!")
    #     print(response)
    
    if os.path.exists("chunk.pkl"):
        print("Reading from pickle file")
        with open("chunk.pkl", 'rb') as file:
            sub_chunks = pickle.load(file)

    else:
        sub_chunks = IngestPDF.chunkify()
        with open("chunk.pkl", 'wb') as file:
            pickle.dump(sub_chunks, file)
            print("Successfully wrote pickle file")

    chromaDBClient = embeddings.EmbeddingGenerator(persist_directory="./db/")

    if chromaDBClient.add_data_now == 1:
        chromaDBClient.add_data(documents=sub_chunks)

    # _dict = chromaDBClient.get_details_about_collection()
    queries = ["What is the name of the company?",
             "Who is the CEO of the company?",
             "What is their vacation policy?",
             "What is the termination policy?"]
    prompt_dict = {}
    
    for query in queries:
        response = chromaDBClient.search(query=query, top_k=3)
        res = ""
        for res_str in response['documents']:
            for r in res_str:
                res  = res + "|||" + r
        prompt_dict[query]={"text":res, "distances":response["distances"]}
    print(prompt_dict)
   
    
    # openAIEmbeddings = embeddings.EmbeddingGenerator(
    #     collection_name="OpenAIdocument_chunks",
    #     model="OpenAI",
    #     persist_directory="./db/"
    #     )
    
    # if openAIEmbeddings.add_data_now == 1:
    #     openAIEmbeddings.add_data(documents=sub_chunks)
    # prompt_dict = {}
    # for query in queries:
    #     prompt_dict["query"] = openAIEmbeddings.search(query=query, top_k=10)
    
    # print(prompt_dict)
    system_message = '''You would be provided a prompt containing dict with a query whose values are dict containtin
                        text and confidence. The text is delimited by "|||" to map to confidence. 
                        The confidence is in cosine distance, so the lower 
                        it is the more similar it is. The format of embeddings is not perfect, so give me the answer in 1-5 lines. Reformat the answer as needed to make sense.
                        If the distances for each text in between "|||" is
                        higher than 0.5, exclude it from your answer. If all the distances
                        are higher than 0.5, respond with "Data Not Available" and their corresponding embedding values. 
                        The result should be a structire JSON that pairs each questions with
                        its corresponding answer. 
                     '''
    OpenAIClient = LLMConnection.LLMModel()
    response = OpenAIClient.get_completion(prompt=str(prompt_dict), system_message=system_message)
    print(response)


if __name__ == "__main__":
    main()