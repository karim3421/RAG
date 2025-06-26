from ..LLMinterface import LLMInterface
from openai import OpenAI
import logging
from ..LLMEnums import OpenAIEnum


class OpenAiProvider(LLMInterface):

    def __init__(self, api_key: str, api_url: str = None,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):
        
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(api_key=self.api_key, api_base=self.api_url)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id, embedding_size=None):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[: self.default_input_max_characters]

    def generate_text(self, prompt, chat_history: list = [], max_output_tokens = None,
                       temperature = None):

        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None        

        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature
        
        chat_history.append(
            self.construct_prompt(prompt = prompt, role = OpenAIEnum.USER.value)
        )

        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages= chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].messages:
            self.logger.error("Failed to get response from OpenAI API.")
            return None
        
        return response.choices[0].messages["content"]

    def embed_text(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None
        
        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input = text
        )        

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Failed to get embedding from OpenAI API.")
            return None
        
        return response.data[0].embedding
        

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }

