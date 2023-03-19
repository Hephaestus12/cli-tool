import openai
import pandas as pd
import numpy as np
import os
from openai.embeddings_utils import distances_from_embeddings

openai.api_key = "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"

# Specify the folder containing your CSV files

embeddings_directory = '../embeddings'
embeddings_list = []

for file in os.listdir(embeddings_directory):
    if file.endswith('.csv'):
        filepath = os.path.join(embeddings_directory, file)
        with open(filepath, 'r') as f:
            _ = f.readline()  # Skip the index row
            embedding_row = f.readline()
        embedding_values = np.array([float(x) for x in embedding_row.strip().split(',')])
        embeddings_list.append(embedding_values)

embeddings_df = pd.DataFrame(embeddings_list, columns=[f'emb_{i}' for i in range(embeddings_list[0].shape[0])])
print(f"Embedding dimensions: {embeddings_df.shape[1]}")


# The rest of the code remains the same

# Define a function to create the context for a question
def create_context(question, df, max_len=1800):
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']
    print(f"Question embedding dimensions: {len(q_embeddings)}")
    df['distances'] = distances_from_embeddings(q_embeddings, df.values, distance_metric='cosine')
    returns = []
    cur_len = 0

    print('distances')
    print(df['distances'])
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])

    return "\n\n###\n\n".join(returns)

# Define a function to answer the question using the created context
def answer_question(df, model="text-davinci-003", question="Explain what the codebase is doing", max_len=1800, max_tokens=150, stop_sequence=None):
    context = create_context(question, df, max_len=max_len)

    try:
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""

# Ask your question
answer = answer_question(embeddings_df, question="Explain what the codebase is doing")
print(answer)