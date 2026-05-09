# LLM Prompting Playground

## Concepts Before Getting Started
- `Chunking`: In the context of building LLM-related applications, chunking is the process of breaking down large text into smaller segements called chunks.
- `Embeddings` : Embeddings convert complex, high-dimensional data(고차원 데이터) into low-dimensional vectors(저차원 벡터). This transformation allows machines to process and analyze data efficeintly.

<img width="500" src="https://github.com/user-attachments/assets/fc19dd2c-093f-4b86-9b41-b90b45c037d5" />

- `BERT` : Bidirectional Encoder Representations from Transformers. Generate contextual embeddings where the same word can have different embeddings based on its context.
- `Vector Database` : A database to store, index, and search embeddings vectors efficiently.
  - step 1) Convert the data into vectors via embeddings
   ```
   "I love cats" → [0.2, 0.8, 0.5, 0.1, ...]
   ```
  - step 2) store those vectors in the Vector DB
  - step 3) the query also gets converted to a vector
   ```
   "I like kittens" → [0.21, 0.79, 0.51, 0.09, ...]
   ``` 
  - step 4) DB finds vectors that are closest to the query vector
   ```
   "I love cats" → most similar
   ```
- `VPS` : A remote computer user rent from a hosting provider. 
- `Qdrant`: A database built specifically for vectors.
- `Orchestration` : Managing when, in what order, and how a series of tasks should run - including what happens if something fails.
- `Fine-Tuning` : Taking a pre-trained model(like GPT, BERT) and continuing to train it on your own specific data so it gets better at your particular task.
- `RAG` : Retrieval Augmented Generation. Instead of baking knowledge into the model, fetching relevant information at query time and hand it to the LLM as context.

## Prompt

## LLM

## RAG

## How can we handle?

