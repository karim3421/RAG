from .LLMEnums import LLMEnum
from .provider import OpenAiProvider, HFProvider

class LLMProviderFactory:
    def __init__(self, config):
        self.config = config


    def create(self, provider: str):
        if provider == LLMEnum.OPEN_AI.value:
            return OpenAiProvider(
                api_key=self.config.OpenAI_API_KEY,
                api_url=self.config.OpenAI_API_URL,
                default_input_max_characters=self.config.DEFAULT_INPUT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.DEFAULT_GENERATION_MAX_OUTPUT_TOKENS,
                default_generation_temperature=self.config.DEFAULT_GENERATION_TEMPERATURE
            )


        if provider == LLMEnum.HUGGING_FACE.value:
            return HFProvider(
                api_key=self.config.HF_TOKEN,
                base_url="https://router.huggingface.co/cohere/compatibility/v1",
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE
            )
