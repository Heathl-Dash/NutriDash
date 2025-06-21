import os
import json
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from app.schemas.askAliment import AskAliment
from openai import OpenAI
import logging
import re

load_dotenv()

router = APIRouter()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

@router.post("/nutrition-info-ai-request")
def ask_nutritional_info(data: AskAliment):
    system_prompt = (
        "Você é um especialista em nutrição. "
        "Responda apenas com informações nutricionais claras no formato JSON. "
        "Não forneça explicações. "
        "Exemplo de resposta: "
        '{"calories": "89 kcal", "glycemic_index": 36, "vitamins": ["A", "B"], '
        '"good_for": "Bom para diabéticos", "bad_for": "Ruim para quando está privado"}'
        "Todas as respostas contidas no JSON, devem ser em português, incluindo os minerais."
    )

    user_question = f"Me informe os dados nutricionais desse alimento: {data.aliment}"

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-small-3.2-24b-instruct:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question},
            ],
            temperature=0.2,
            extra_body={}
        )
        text_answer = response.choices[0].message.content
        cleaned_json = re.sub(
            r"```json\s*(.*?)```", r"\1",
            text_answer,
            flags=re.DOTALL 
        ).strip()
        try:
            return json.loads(cleaned_json)
        except json.JSONDecodeError:
            raise HTTPException(status_code=502, detail="Resposta do modelo não está em formato JSON válido")
    except Exception as e:
        logging.error(f"Erro ao chamar OpenAI: {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar o modelo de IA.")
