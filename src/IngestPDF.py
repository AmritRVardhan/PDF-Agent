from pypdf import PdfReader
import os
import re

# Retrieval can be made better by https://www.anthropic.com/news/contextual-retrieval
# The basic idea here is to have one chunk of embedding for each section, if the tokens are exceeding, we can have embeddings for each sub-section
# The variables wouldnt be hard coded eg, to 2048 here for OPenAI embeddings.

def read_pdf(pdf_path="C:\\Users\\amrit\\Downloads\\handbook.pdf"):
    reader = PdfReader(pdf_path)
    return reader


def get_delimiters(data):
    number_of_pages = len(data.pages)
    pattern = "[0-9]\.[0-9]+"
    ans = []
    for i in range(3, number_of_pages):
        matches = re.findall(pattern, data.pages[i].extract_text())
        if matches:
            ans.append(matches)
    delimiters = [x for i in ans for x in i]
    return delimiters


def get_whole_pdf_as_text(pdfObject):
    text = ""
    for i in range(len(pdfObject.pages)):
        text += pdfObject.pages[i].extract_text()
    return text


def get_chunks(delimiters, text):
    answer = []
    chunk_str = ""
    starting_index, ending_index = 0, 0
    for i, numbers in enumerate(delimiters):      
        if i != 0:
            answer.append(chunk_str)
            chunk_str = ""
        
        starting_index = text.index(numbers)
        if i < len(delimiters)-1:
            ending_index = text.index(delimiters[i+1])
        if i == len(delimiters)-1:
            chunk_str = ""
            ending_index = text.find("California Policies")
            chunk_str += text[starting_index:ending_index]
            answer.append(chunk_str)
        
        chunk_str += text[starting_index:ending_index]
        
        
    return answer


def get_sub_chunks(chunks):
    sub_chunks = []
    for item in chunks:
        if len(item)<2048:
            sub_chunks.append(item)
            continue
        chunk_str = item
        starting_index = 0
        while len(chunk_str) > 2048:
            ending_index = chunk_str[starting_index:starting_index+2048].rfind("\n")
            sub_chunks.append(chunk_str[starting_index: ending_index])
            starting_index = ending_index
            chunk_str = chunk_str[ending_index:]

        sub_chunks.append(chunk_str)

    return sub_chunks


def chunkify():
    #Read the pdf
    pdfObject = read_pdf()

    #get section headers
    delimiters = get_delimiters(pdfObject)
    delimiters = delimiters[:-1]

    text = get_whole_pdf_as_text(pdfObject)

    #recursive search for 1.0 to exclude TOC
    text = text[text.find("1.0", text.find("1.0")+1):] 

    chunks = get_chunks(delimiters, text)
    sub_chunks = get_sub_chunks(chunks)

    #Write in a file for sanity check
    if os.path.exists("chunks.txt"):
        os.remove("chunks.txt")
    with open("chunks.txt", "w") as f:
        for item in sub_chunks:
            f.write(item+"\n")

    return sub_chunks
