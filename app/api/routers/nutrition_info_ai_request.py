import os
import json
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from app.schemas.askAliment import AskAliment
from openai import OpenAI
from app.utils.system_prompt import SYTEM_PROMPT
import logging

load_dotenv()

router = APIRouter()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

@router.post("/nutrition-info-ai-request")
def ask_nutritional_info(data: AskAliment):
    system_prompt = (SYTEM_PROMPT)

    user_question = f"Me informe os dados nutricionais desse alimento: {data.aliment}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question},
            ],
            temperature=0.2,
            extra_body={}
        )
        text_answer = response.choices[0].message.content
        try:
            return json.loads(text_answer)
        except json.JSONDecodeError:
            raise HTTPException(status_code=502, detail="Resposta do modelo não está em formato JSON válido")
    except Exception as e:
        logging.error(f"Erro ao chamar OpenAI: {e}")
        raise HTTPException(status_code=500, detail="Erro ao consultar o modelo de IA.")