import os
import json
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from app.schemas.askAliment import AskAliment
import openai
import httpx

load_dotenv()

router = APIRouter()

client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    http_client=httpx.Client()
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
    )

    user_question = f"Me informe os dados nutricionais desse alimento: {data.aliment}"

    try:
        response = client.chat.completions.create(
            extra_body = {},
            model = "deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question},
            ],
            temperature=0.2,
        )
        text_answer = response.choices[0].message.content
        return json.loads(text_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
