# chat.py   

from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.messages import HumanMessage, AIMessage
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from pydantic import PrivateAttr

class ChatBot:
    def __init__(self, model_name="microsoft/phi-4"):
        load_dotenv()
        self.api_key = os.getenv("MY_TOKEN")
        self.model = model_name
        self.client = InferenceClient(
            provider="nebius",
            api_key=self.api_key,
        )
    
    def get_response(self, message):

        system_prompt = SystemMessagePromptTemplate.from_template(
            "You are a highly knowledgeable and helpful medical assistant and your name is HealthMate. "
            "You are not a doctor, but you can provide general information based on established medical knowledge. "
            "You should encourage users to consult a healthcare provider for serious or personal health concerns."
        )

        human_prompt = HumanMessagePromptTemplate.from_template(
            "answer the following question in a helpful and informative manner.\n "
            "if the question is not related to health or medicine, provide a short general response that is not specific to any field and make sure it is short answer\n"
            "User's message:\n"
            "\"{user_message}\"\n\n"
            "Your response:"
        )

        chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
        messages = chat_prompt.format(user_message=message)
        print(messages)

        # prompt_template = (
        #     "You are a highly knowledgeable and helpful medical assistant. "
        #     "You are not a doctor, but you can provide general information based on established medical knowledge. "
        #     "You should encourage users to consult a healthcare provider for serious or personal health concerns.\n\n"
        #     "User's message:\n"
        #     "\"{user_message}\"\n\n"
        #     "Your response:"
        # )

        # prompt = prompt_template.format(user_message=message)

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": messages,
                }
            ],
        )
        return completion.choices[0].message.content
    
class ChatBotWrapper(BaseChatModel):
    _chatbot: ChatBot = PrivateAttr()

    def __init__(self, chatbot: ChatBot):
        super().__init__()
        self._chatbot = chatbot

    @property
    def _llm_type(self) -> str:
        return "custom-chatbot"

    def _generate(self, messages: List[HumanMessage], stop=None, run_manager=None, **kwargs) -> ChatResult:
        last_message = messages[-1].content
        response = self._chatbot.get_response(last_message)
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=response))]
        )
    

    

chat = ChatBot()
print(chat.model)