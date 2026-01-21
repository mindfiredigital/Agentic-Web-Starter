from typing import List

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.config.settings import settings
from src.constants.app_constants import LLM


def generate_answer(
    query: str,
    documents: List[Document],
    history_text: str,
) -> str:
    context = "\n\n".join(doc.page_content for doc in documents)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Use the context to answer. "
                "If the answer is not in the context, say you do not know.",
            ),
            ("system", "Conversation history:\n{history}"),
            ("human", "Question: {question}\n\nContext:\n{context}"),
        ]
    )
    llm = ChatOpenAI(
        model=LLM.CHAT_MODEL.value,
        temperature=LLM.TEMPERATURE.value,
        api_key=settings.OPENAI_API_KEY,
    )
    chain = prompt | llm
    result = chain.invoke({"question": query, "context": context, "history": history_text})
    return result.content
