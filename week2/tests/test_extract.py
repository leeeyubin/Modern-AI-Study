import os
import pytest

from ..app.services.extract import extract_action_items
from unittest.mock import patch, MagicMock
from ..app.services.extract import extract_action_items_llm

def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items

def make_mock_response(content: str):
    mock = MagicMock()
    mock.message.content = content
    return mock

def test_llm_bullet_list():
    """일반적인 액션 아이템 리스트"""
    with patch("week2.app.services.extract.chat") as mock_chat:
        mock_chat.return_value = make_mock_response(
            '["Fix the bug", "Write tests", "Update docs"]'
        )
        result = extract_action_items_llm("- Fix the bug\n- Write tests\n- Update docs")
        assert "Fix the bug" in result
        assert "Write tests" in result
        assert "Update docs" in result

def test_llm_empty_input():
    """빈 입력이면 ollama 호출 없이 바로 빈 리스트 반환"""
    with patch("week2.app.services.extract.chat") as mock_chat:
        result = extract_action_items_llm("")
        mock_chat.assert_not_called()
        assert result == []

def test_llm_keyword_prefixed():
    """Todo:, Action: 같은 키워드 앞에 붙은 경우"""
    with patch("week2.app.services.extract.chat") as mock_chat:
        mock_chat.return_value = make_mock_response(
            '["Set up CI", "Deploy to staging"]'
        )
        result = extract_action_items_llm("Todo: Set up CI\nAction: Deploy to staging")
        assert len(result) == 2

def test_llm_dict_response():
    """모델이 {"items": [...]} 형태로 줄 때도 처리"""
    with patch("week2.app.services.extract.chat") as mock_chat:
        mock_chat.return_value = make_mock_response(
            '{"items": ["Review PR", "Merge branch"]}'
        )
        result = extract_action_items_llm("Review PR\nMerge branch")
        assert "Review PR" in result

def test_llm_invalid_json():
    """모델이 이상한 걸 뱉으면 빈 리스트 반환"""
    with patch("week2.app.services.extract.chat") as mock_chat:
        mock_chat.return_value = make_mock_response("I cannot help with that.")
        result = extract_action_items_llm("some notes")
        assert result == []
