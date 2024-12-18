The sample output is stored in output.png.

I used ChromaDb for stroing vectors and used two different embeddings, as I was unsure if I would reach the token limit extremely fast. I have used text-embedding-ad-002 and SBERT(all-minilm-l6-v2) to get the top k query results. SBERT has been better in finding relevant embeddings.

I used the handbook for implementing RAG. The PDFIngest.py is specifically designed to extract only the data relevant to the sample questions.

Things I would want to do, given more time/API/Production.
- Take both the top-k results of both the embeddings and compare to baseline models to see if the culmination works better.
- Rerank the top-k search results to query text to improve results.
- Understand why is it hard to get the name of the company and CEO. This is understandably because of the name of the CEO present only twice and Zania is not a common name that ChatGpt would have be trained on. Regardless, top_k results should have given me the section of 1.1 where the CEO's name is present.


 PLEASE NOTE: THIS README WOULD BE UPDATED FURTHER.
