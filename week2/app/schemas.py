from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

# ── Request Model ──────────────────────────

class ExtractRequest(BaseModel):
    text: str           # 필수 - 노트 텍스트
    save_note: bool = False  # 선택 - DB에 저장할지 여부

class NoteCreateRequest(BaseModel):
    content: str        # 필수 - 노트 내용

class MarkDoneRequest(BaseModel):
    done: bool = True   # 선택 - 완료 여부

# ── Response Model ─────────────────────────

class ActionItemResponse(BaseModel):
    id: int
    text: str

class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: list[ActionItemResponse]

class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str

class ActionItemDetailResponse(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str
