from try1 import ChatBotWrapper, ChatBot
from langchain_core.tools import tool

chat = ChatBot()
model = ChatBotWrapper(chat)

print(chat.get_response("What is 10.6 mutilplied by 2?, dont add any text but the answer only"))

@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

