import settings
from gigachat import GigaChat
from pydantic import BaseModel
import json
import pprint


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def giga_chat(giga, message):
    response = giga.chat(message)
    l_json = response.choices[0].message.content.split(":**")
    js = json.loads(l_json[-1])
    pprint.pprint(js, indent=2)


if __name__ == "__main__":
    with GigaChat(credentials=settings.GIGACHAT_API_KEY, ca_bundle_file="russian_trusted_root_ca_pem.crt") as giga:
        instruction = f"""Отвечай только в формате JSON, соответствующем следующей модели Pydantic:
            {CalendarEvent.model_json_schema()}, но саму модель не включай в ответ."""
        mes = {
        "messages": [
            {"role": "system", "content": "Extract the event information and follow this instruction: " + instruction},
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday",
                }
        ],
        "temperature": 0.5
    }
        giga_chat(giga, mes)