import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_anthropic_model(model_name: str = "claude-3-haiku-20240307"):
    """Initialize Anthropic chat model with API key from environment."""
    return init_chat_model(
        model=model_name,
        model_provider="anthropic",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
    )


anthropic_model = get_anthropic_model()
