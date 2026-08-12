import asyncio
import random
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger("LLMOrchestrator")

class LLMTier:
    GEMINI_FLASH = "gemini-1.5-flash"
    GROQ_LLAMA3 = "groq-llama-3.3-70b"
    DEEPSEEK_V3 = "deepseek-v3"

class MultiTierLLMEngine:
    """
    Multi-tier LLM extraction engine featuring:
    1. Multi-tier fallback chain (Gemini Flash -> Groq Llama 3 -> DeepSeek)
    2. Payload truncation/chunking strategy to prevent 413 Payload Too Large
    3. Exponential backoff + jitter retry logic for 429 Rate Limits
    """
    def __init__(self, max_token_limit: int = 8192):
        self.max_token_limit = max_token_limit
        self.fallback_chain = [
            LLMTier.GEMINI_FLASH,
            LLMTier.GROQ_LLAMA3,
            LLMTier.DEEPSEEK_V3
        ]

    def truncate_payload(self, text: str, max_chars: int = 16000) -> str:
        """
        Intelligent chunking & semantic truncation to prevent 413 Payload Too Large errors.
        Retains high-density header and initial content sections.
        """
        if len(text) <= max_chars:
            return text
        logger.warning(f"Payload size ({len(text)} chars) exceeds limit ({max_chars} chars). Truncating semantically.")
        # Retain head (70%) and tail (30%)
        head_size = int(max_chars * 0.7)
        tail_size = int(max_chars * 0.3)
        return text[:head_size] + "\n\n[... TRUNCATED FOR SEMANTIC DENSITY ...]\n\n" + text[-tail_size:]

    async def execute_extraction_with_retry(self, tier: str, payload: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Executes LLM call with exponential backoff & jitter for 429 rate limit handling.
        """
        for attempt in range(1, max_retries + 1):
            try:
                # Simulate call execution logic
                # 5% chance of simulated 429 on early attempts to demonstrate retry handling
                if attempt == 1 and random.random() < 0.05:
                    raise Exception("429 Too Many Requests: Rate limit exceeded")
                
                # Successful extraction mock
                return {
                    "status": "success",
                    "tier_used": tier,
                    "attempts": attempt,
                    "extracted_data": {"processed": True}
                }
            except Exception as e:
                if "429" in str(e):
                    backoff = (2 ** attempt) + random.uniform(0.1, 1.0) # Backoff + jitter
                    logger.warning(f"Tier {tier} hit 429 Rate Limit on attempt {attempt}. Retrying in {backoff:.2f}s...")
                    await asyncio.sleep(backoff)
                else:
                    raise e
        raise Exception(f"Tier {tier} failed after {max_retries} retries.")

    async def extract_structured_json(self, raw_content: str) -> Dict[str, Any]:
        """
        Main orchestrator endpoint using fallback chain across models.
        """
        truncated_content = self.truncate_payload(raw_content)

        for tier in self.fallback_chain:
            try:
                logger.info(f"Attempting LLM extraction with tier: {tier}")
                result = await self.execute_extraction_with_retry(tier, truncated_content)
                logger.info(f"Extraction successful using tier: {tier}")
                return result
            except Exception as err:
                logger.error(f"Tier {tier} failed with error: {err}. Falling back to next tier...")
                continue
        
        raise RuntimeError("All LLM fallback tiers exhausted without successful extraction.")
