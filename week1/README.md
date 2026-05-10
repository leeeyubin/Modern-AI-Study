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

## Prompting
- `zero-shot` : The prompt used to interact with the model won't contain examples or demonstrations.
- `few-shot` : The demonstrations serve as conditioning for subsequent examples where we would like the model to generate a response.
- `Chain-of-Thought` : CoT prompting enables complex reasoning capabilities through intermediate reasoning steps.
<img width="600" src="https://github.com/user-attachments/assets/1799dce2-8792-4a1e-9fbc-16c8e7cd9ec1" />

## LLM
- 🔗 [Practice multiple prompting techniques](https://github.com/leeeyubin/Modern-AI-Study/blob/main/week1/chain_of_thought.py)

- Step 1) Install locally on your machine called Ollama
```bash
# mac OS
brew install --cask ollama && ollama serve

# downlaod model
ollama run mistral-nemo:12b
ollama run llama3.1:8b
```

- Step 2) Fill the prompt
```python
YOUR_SYSTEM_PROMPT = """You are a mathematics expert. When solving modular arithmetic problems, use Euler's theorem and find repeating cycles.

Here are examples:

Problem: What is 2^100 (mod 10)?
Solution: Find the cycle of 2^n mod 10: 2,4,8,6,2,4,8,6... period=4. 100 mod 4 = 0, so use last in cycle = 6.
Answer: 6

Problem: What is 3^20 (mod 10)?
Solution: Cycle of 3^n mod 10: 3,9,7,1,3,9,7,1... period=4. 20 mod 4 = 0, so use last in cycle = 1.
Answer: 1

Problem: What is 7^50 (mod 100)?
Solution: Find cycle of 7^n mod 100. By Euler's theorem, phi(100)=40, so 7^40 ≡ 1 (mod 100). 50 = 40+10. 7^10 mod 100 = 49.
Answer: 49

Always end your response with the final answer on its own line as: Answer: <number>
"""
```

- Step 3) Check the result

<img width="650" src="https://github.com/user-attachments/assets/2a5ff8e0-fe59-4e4e-9b66-bae0aa1a77fc" />


## How can we handle?
```
 RAG Pipeline
1. Indexing (사전 작업)
   - 문서/데이터를 청킹
   - 임베딩 모델(BERT 등)로 벡터 변환
   - Qdrant 같은 Vector DB에 저장

2. Query (런타임)
   - 사용자 질문도 동일한 임베딩 모델로 벡터 변환
   - Vector DB에서 Top-K 유사 청크 검색
   - 질문 + 검색된 청크를 LLM에 컨텍스트로 전달
   - LLM이 컨텍스트 기반으로 답변 생성

 Prompting 선택 기준
 - 단순한 지시 → Zero-shot
 - 출력 포맷/스타일 통일 필요 → Few-shot
 - 수학, 논리처럼 단계적 추론 필요 → Chain-of-Thought
```
## 📝 Note
> You won't be replaced by AI. You'll be a competent engineer who knows how to use AI
