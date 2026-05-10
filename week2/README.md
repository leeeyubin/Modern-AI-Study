# The Anatomy of Coding Agents

## Demo

<img width="700" src="https://github.com/user-attachments/assets/d587c8fb-b799-45c8-a337-750737ac8f09" />

## File Structure

```
week2/
├── app/
│   ├── main.py          # 앱 시작점
│   ├── db.py            # DB 관련 함수
│   ├── routers/
│   │   ├── action_items.py  # /action-items 관련 API 엔드포인트
│   │   └── notes.py         # /notes 관련 API 엔드포인트
│   └── services/
│       └── extract.py   # 실제 추출 로직
├── frontend/
│   └── index.html       # 브라우저 화면
└── tests/
    └── test_extract.py  # 테스트
```

## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### ✅ Exercise 1: Scaffold a New Feature
Prompt: 
```
Implement extract_action_items_llm() function in extract.py that uses Ollama to extract action items via LLM. It should return a JSON array of strings, handle empty input, and handle cases where the model returns a dict instead of a list.
``` 

Generated Code Snippets:
```
week2/app/services/extract.py — extract_action_items_llm() 함수 추가 (하단)
```

### ✅ Exercise 2: Add Unit Tests
Prompt: 
```
Write unit tests for extract_action_items_llm() covering: bullet list input, empty input, keyword-prefixed input, dict response from model, and invalid JSON response. Use unittest.mock to mock the ollama chat call.
``` 

Generated Code Snippets:
```
week2/tests/test_extract.py

test_llm_bullet_list()
test_llm_empty_input()
test_llm_keyword_prefixed()
test_llm_dict_response()
test_llm_invalid_json()
```

### ✅ Exercise 3: Refactor Existing Code for Clarity
Prompt:
```
Refactor the backend focusing on: well-defined API schemas using Pydantic, database layer cleanup, app lifecycle using lifespan instead of init_db() at module load, and improved error handling.
```

Generated/Modified Code Snippets:
```
week2/app/schemas.py — 새로 생성 (Pydantic request/response 모델)
week2/app/routers/action_items.py — Dict[str, Any] → Pydantic 스키마 적용
week2/app/routers/notes.py — Dict[str, Any] → Pydantic 스키마 적용, GET /notes 추가
week2/app/main.py — lifespan 방식으로 변경
```

### ✅ Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Add a new endpoint POST /action-items/extract-llm that uses extract_action_items_llm() for LLM-based extraction.
Add an "Extract LLM" button to the frontend that calls this new endpoint.
Add a GET /notes endpoint and a "List Notes" button to the frontend that fetches and displays all saved notes.
``` 

Generated Code Snippets:
```
week2/app/routers/action_items.py — /extract-llm 엔드포인트 추가
week2/frontend/index.html — Extract LLM 버튼, List Notes 버튼 추가
```

### ✅ Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze the entire codebase and generate a well-structured Cursor.md file that includes:

A brief overview of the project
How to set up and run the project
All API endpoints and their functionality
Instructions for running the test suite
Save it as README.md in the project root.
``` 

Generated Code Snippets:
```
week2/Cursor.md — 새로 생성
```
