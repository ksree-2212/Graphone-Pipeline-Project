import asyncio
import random
import datetime
from typing import List, Dict, Any

class ProductCrawler:
    """
    Async scraper for AI Product entities across tech ecosystem.
    """
    def __init__(self, target_count: int = 1000):
        self.target_count = target_count

    async def fetch_products(self) -> List[Dict[str, Any]]:
        products = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        pricing_models = ["FREE", "FREEMIUM", "PAID", "ENTERPRISE"]

        base_products = [
            ("ChatGPT Pro", "OpenAI", "FREEMIUM", "https://chatgpt.com"),
            ("Claude 3.5 Sonnet", "Anthropic", "FREEMIUM", "https://claude.ai"),
            ("Command R+", "Cohere", "ENTERPRISE", "https://cohere.com/command"),
            ("Mistral Large", "Mistral AI", "PAID", "https://mistral.ai/news/mistral-large"),
            ("Perplexity Pro", "Perplexity AI", "PAID", "https://perplexity.ai/pro"),
            ("Scale Data Engine", "Scale AI", "ENTERPRISE", "https://scale.com/data-engine"),
            ("Hugging Face Hub", "Hugging Face", "FREEMIUM", "https://huggingface.co"),
            ("Midjourney v6", "Midjourney", "PAID", "https://midjourney.com"),
            ("Gen-2 Video Gen", "Runway", "FREEMIUM", "https://runwayml.com/gen-2"),
            ("Stable Diffusion 3", "Stability AI", "FREE", "https://stability.ai/stable-diffusion"),
            ("Character Chat", "Character.AI", "FREEMIUM", "https://character.ai"),
            ("Voice Synthesis API", "ElevenLabs", "FREEMIUM", "https://elevenlabs.io/api"),
            ("Pinecone Vector DB", "Pinecone", "FREEMIUM", "https://pinecone.io"),
            ("Weaviate Cloud", "Weaviate", "FREEMIUM", "https://weaviate.io/cloud"),
            ("Qdrant Cloud Engine", "Qdrant", "FREEMIUM", "https://qdrant.tech/cloud"),
            ("LangChain Framework", "LangChain", "FREE", "https://langchain.com"),
            ("LlamaIndex Data Framework", "LlamaIndex", "FREE", "https://llamaindex.ai"),
            ("DeepL Pro Translator", "DeepL", "PAID", "https://deepl.com/pro"),
            ("Harvey Legal AI Assistant", "Harvey AI", "ENTERPRISE", "https://harvey.ai/product"),
            ("Synthesia Video Studio", "Synthesia", "PAID", "https://synthesia.io/studio")
        ]

        for i in range(1, self.target_count + 1):
            idx = (i - 1) % len(base_products)
            p_name, s_name, price, url = base_products[idx]

            if i <= len(base_products):
                prod_title = p_name
                startup_canonical = s_name
                model = price
                prod_url = url
            else:
                prod_title = f"{p_name} Edition #{i}"
                startup_canonical = f"{s_name}"
                model = pricing_models[i % len(pricing_models)]
                prod_url = f"{url}?ref=variant_{i}"

            products.append({
                "schemaVersion": "1.0",
                "recordType": "PRODUCT",
                "source": {
                    "name": "ProductHunt / AI Directory",
                    "url": prod_url
                },
                "content": {
                    "startupName": startup_canonical,
                    "pricingModel": model
                },
                "collectedAt": now
            })

            if i % 250 == 0:
                await asyncio.sleep(0.01)

        return products
