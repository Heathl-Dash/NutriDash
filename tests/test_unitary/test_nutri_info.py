import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.api.routers import nutrition_info_ai_request
from app.schemas.askAliment import AskAliment


# ---------- CASO DE SUCESSO COM JSON VÁLIDO ----------
@patch("app.api.routers.nutrition_info_ai_request.client")
def test_ask_nutritional_info_success(mock_client):
    # simula resposta JSON válida do modelo
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content=json.dumps(
                    {
                        "calories": "89 kcal",
                        "carbohydrates": "22,8 g",
                        "proteins": "1,1 g",
                        "fats": "0,3 g",
                        "sugar": "12 g",
                        "fiber": "3,5 g",
                        "glycemic_index": 36,
                        "vitamins": ["A", "C", "B6"],
                        "minerals": ["Potássio", "Magnésio"],
                        "good_for": "Bom para diabéticos",
                        "bad_for": "Ruim para quem tem problemas renais",
                    }
                )
            )
        )
    ]
    mock_client.chat.completions.create.return_value = mock_response

    data = AskAliment(aliment="banana")
    result = nutrition_info_ai_request.ask_nutritional_info(data)

    mock_client.chat.completions.create.assert_called_once()
    assert result["calories"] == "89 kcal"
    assert isinstance(result["vitamins"], list)
    assert "good_for" in result


# ---------- CASO DE RESPOSTA INVÁLIDA (NÃO JSON) ----------
@patch("app.api.routers.nutrition_info_ai_request.client")
def test_ask_nutritional_info_invalid_json(mock_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Texto não JSON"))]
    mock_client.chat.completions.create.return_value = mock_response

    data = AskAliment(aliment="banana")

    with pytest.raises(HTTPException) as exc:
        nutrition_info_ai_request.ask_nutritional_info(data)

    assert exc.value.status_code == 502
    assert "JSON válido" in exc.value.detail


# ---------- CASO DE EXCEÇÃO NA CHAMADA DO CLIENTE ----------
@patch("app.api.routers.nutrition_info_ai_request.client")
def test_ask_nutritional_info_openai_error(mock_client):
    mock_client.chat.completions.create.side_effect = Exception("Falha na API")

    data = AskAliment(aliment="banana")

    with pytest.raises(HTTPException) as exc:
        nutrition_info_ai_request.ask_nutritional_info(data)

    assert exc.value.status_code == 502
    assert "Erro ao consultar o modelo de IA" in exc.value.detail
