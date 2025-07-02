from ..LLMinterface import LLMInterface
import os
from ..LLMEnums import OpenAIEnum, HFEnum
from openai import OpenAI
from dotenv import load_dotenv
import logging
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)
load_dotenv()

class HFProvider(LLMInterface):
    def __init__(self, api_key: str, base_url: str = None,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):

        self.api_key = api_key
        self.base_url = base_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        # Initialize the OpenAI client for generation

        self.generation_client = OpenAI(
            base_url="https://router.huggingface.co/cohere/compatibility/v1",
            api_key=os.getenv("HF_TOKEN"),
        )

        # Initialize the Hugging Face client for embeddings

        self.embedding_client = InferenceClient(
            provider="hf-inference",
            api_key=os.getenv("HF_TOKEN"),
        )
        self.enums = HFEnum


    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int = None):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list = [], max_output_tokens: int = None, temperature: float = None):

        if not self.generation_client:
            logger.error("Hugging Face client is not initialized.")
            return None
        
        if not self.generation_model_id:
            logger.error("Generation model ID was not set.")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt, role=OpenAIEnum.USER.value)
        )

        response = self.generation_client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            logger.error("Failed to get response from OpenAI API.")
            return None
        
        return response.choices[0].message.content
    

    def embed_text(self, text, document_type = None):

        if not self.embedding_client:
            logger.error("Hugging Face client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            logger.error("Embedding model ID was not set.")
            return None
        
        embedding = self.embedding_client.feature_extraction(
            model=self.embedding_model_id,
            text=text
        )
        
        return embedding



    def construct_prompt(self, query: str, role: str):
        return {
            "role": role,
            "content": self.process_text(query)
        }



    