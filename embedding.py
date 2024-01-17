from sentence_transformers import SentenceTransformer
import pandas as pd

df = pd.read_csv("./book_recommendation_ai/data.csv")
description = df['description']

# model embedding
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
embedding = model.encode(description)

# encode the description
embedding_df = pd.DataFrame(embedding)
embedding_df.to_csv('./book_recommendation_ai/embedded_description.csv', index = False, encoding='utf-8') 


