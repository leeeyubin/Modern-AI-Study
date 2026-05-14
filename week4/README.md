# Coding Agent Patterns

Building automations with Claude Code to enhance a developer workflow using custom slash commands, CLAUDE.md guidance files, and role-specialized SubAgents.

## Prerequisites

```bash
# 클로드 설치
npm install -g @anthropic-ai/claude-code
```
```bash
# 실행하기 
cd modern-software-dev-assignments/week4
make run
claude
```

## Demo
 
<img width="709" height="195" alt="image" src="https://github.com/user-attachments/assets/d6c494cd-1153-4395-bce0-2af09cb614b6" />

## Structure
 
<img width="700" src="https://github.com/user-attachments/assets/6dc0e18f-959e-46c6-a6d1-9505cd5b0b80" />

```
week4/
├── .claude/
│   ├── commands/
│   │   ├── tests.md        # /tests slash command
│   │   └── docs-sync.md    # /docs-sync slash command
│   └── agents/
│       ├── test-agent.md   # writes and verifies tests
│       └── code-agent.md   # implements code to pass tests
├── CLAUDE.md               # project guidance for Claude Code
├── backend/                # FastAPI app
├── frontend/               # static UI
├── docs/
│   └── API.md              # auto-generated API reference
└── data/                   # SQLite DB + seed
```


## Automations
 
### ✅ CLAUDE.md
 
 Claude Code가 시작할 때 자동으로 읽는 프로젝트 설명서, 프로젝트 구조, 앱 실행 방법, 라우터/테스트 위치, 코드 스타일 규칙을 담고 있어서 매번 따로 설명하지 않아도 Claude가 올바른 컨텍스트를 가지고 시작할 수 있다.
 
두 개의 파일 만들기
- `/CLAUDE.md` — 레포 전체 컨텍스트 (환경 설정, 주차별 개요, 공통 아키텍처)
- `week4/CLAUDE.md` — week4 전용 컨텍스트

### ✅ 슬래시 커맨드
 
 `.claude/commands/`에 저장된 재사용 가능한 워크플로우. Claude Code 안에서 `/`로 호출
 
1️⃣ `/tests`
 
테스트 전체를 실행하고 실패가 있으면 자동으로 처리
 
1. `PYTHONPATH=. pytest -q backend/tests` 실행
2. 전부 통과하면 결과를 출력하고 종료
3. 실패가 있으면 트레이스백을 인용하고, 원인을 파악해 수정 방법을 제안하고, 명확하면 직접 수정 후 재실행
4. 전체 테스트를 다시 돌려 최종 결과 리포트
결과: **3/3 통과**

<img width="600" src="https://github.com/user-attachments/assets/46d3e900-c80f-46d9-a2d5-da5dcee12191" />


</br>

 
2️⃣ `/docs-sync`
 
실행 중인 서버의 OpenAPI 스펙을 읽어 `docs/API.md`를 최신 상태로 자동 업데이트
 
1. 서버에서 `/openapi.json` 가져오기
2. 기존 `docs/API.md`와 비교
3. 현재 스펙 기준으로 파일 전체 재작성
결과: `notes`, `action_items` 2개 태그, **엔드포인트 7개 문서화**
 
### ✅ SubAgents
 
테스트 주도 워크플로우를 위해 협력하는 두 개의 역할 분리 에이전트
 
- **`test-agent`** — 새 기능에 대한 실패 테스트를 먼저 작성하고, 구현 완료 후 통과 여부를 검증
 
- **`code-agent`** — `test-agent`가 작성한 테스트를 읽고 통과하는 코드를 구현
 
ex. 사용 예시
```
Use the test-agent and code-agent subagents to add POST /notes/{note_id}/tags
```
 
 
## Test
 
```bash
make test
# 또는 Claude Code 안에서
/tests
```
 
