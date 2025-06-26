from enum import Enum

class LLMEnum(Enum):
    OPEN_AI = "OPENAI"
    COHERE = "COHERE"
    HUGGING_FACE = "HUGGINGFACE"

class OpenAIEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"