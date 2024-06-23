import json
from minsearch import Index
from groq import Groq
from dotenv import dotenv_values

config = dotenv_values("../.env")
client = Groq(
    api_key=config["GROQ_API_KEY"],
)


def get_documents() -> list:
    with open("documents.json", "rt") as f_in:
        docs_raw = json.load(f_in)
    documents = []
    for course_dict in docs_raw:
        for doc in course_dict["documents"]:
            doc["course"] = course_dict["course"]
            documents.append(doc)
    return documents


def build_prompt(query: str, search_results: list) -> str:
    context = ""

    for doc in search_results:
        context += f'section: {doc["section"]}\nquestion: {doc["question"]}\nanswer:: {doc["text"]}\n\n'

    prompt_template = """You're a course teaching assistant. You will answer QUESTION using information from CONTEXT only.

    QUESTION: {question}

    CONTEXT:
    {context}
    """
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt: str, model: str = "llama3-8b-8192") -> str | None:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )

    return chat_completion.choices[0].message.content
