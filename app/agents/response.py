from langchain_community.chat_message_histories import RedisChatMessageHistory

from src.config.database import REDIS_URL
from src.tools.agent_tools import GenerateAnswerTool, RetrieveTool


class ResponseAgent:
    def __init__(self) -> None:
        self.retriever = RetrieveTool()
        self.generator = GenerateAnswerTool()

    def _get_history_text(self, thread_id: str) -> str:
        history = RedisChatMessageHistory(session_id=thread_id, url=REDIS_URL)
        if not history.messages:
            return ""
        return "\n".join(f"{m.type}: {m.content}" for m in history.messages)

    def _append_history(self, thread_id: str, user_msg: str, ai_msg: str) -> None:
        history = RedisChatMessageHistory(session_id=thread_id, url=REDIS_URL)
        history.add_user_message(user_msg)
        history.add_ai_message(ai_msg)

    def answer(self, thread_id: str, query: str) -> str:
        contexts = self.retriever.run(
            {"thread_id": thread_id, "query": query}
        )
        history_text = self._get_history_text(thread_id)
        answer = self.generator.run(
            {
                "thread_id": thread_id,
                "query": query,
                "contexts": contexts,
                "history": history_text,
            }
        )
        self._append_history(thread_id, query, answer)
        return answer
