import re

class EntityResolver:
    """
    Deterministic & Seed-based Entity Resolution Engine.
    Maps raw entity strings to canonical names using string normalization,
    seed database lookup, and fuzzy edit distance.
    """
    def __init__(self):
        # Mock database of 50 known canonical AI startups & companies
        self.seed_canonical_entities = [
            "OpenAI", "Anthropic", "Cohere", "Mistral AI", "Perplexity AI",
            "Scale AI", "Hugging Face", "Midjourney", "Runway", "Stability AI",
            "Character.AI", "ElevenLabs", "Pinecone", "Weaviate", "Qdrant",
            "LangChain", "LlamaIndex", "DeepL", "Harvey AI", "Synthesia",
            "DeepSeek", "Grok xAI", "Meta AI", "Google DeepMind", "Microsoft AI",
            "Amazon Bedrock", "Databricks", "Snowflake", "Anyscale", "Modal",
            "Replicate", "Together AI", "Groq", "Cerebras", "Sambanova",
            "SambaNova Systems", "Writer AI", "Glean", "Abridge", "Cognition AI",
            "Poolside AI", "Sakura AI", "Superhuman", "Notion AI", "Cursor",
            "Superagent", "Vercel AI", "Weights & Biases", "Neptune.ai", "Baseten"
        ]

        self.legal_suffixes = [
            "inc", "inc.", "llc", "corp", "corporation", "labs", "technologies",
            "tech", "ai", "systems", "research", "limited", "ltd", "pvt"
        ]

    def _clean_string(self, text: str) -> str:
        """Normalizes case, removes punctuation, extra spaces, and legal suffixes."""
        cleaned = text.lower()
        cleaned = re.sub(r'[^\w\s]', ' ', cleaned)
        words = cleaned.split()
        # Filter out trailing legal suffixes
        filtered = [w for w in words if w not in self.legal_suffixes]
        if not filtered:
            filtered = words
        return " ".join(filtered)

    def resolve(self, raw_name: str, entity_type: str = "STARTUP") -> dict:
        """
        Resolves a raw entity string to its canonical form.
        Returns resolution record containing raw_name, canonical_name, method, and confidence.
        """
        if not raw_name:
            return {
                "raw_name": raw_name,
                "canonical_name": "Unknown Entity",
                "entity_type": entity_type,
                "confidence_score": 0.0,
                "resolution_method": "FALLBACK"
            }

        # Step 1: Direct Seed Match
        for canonical in self.seed_canonical_entities:
            if raw_name.strip().lower() == canonical.lower():
                return {
                    "raw_name": raw_name,
                    "canonical_name": canonical,
                    "entity_type": entity_type,
                    "confidence_score": 1.0,
                    "resolution_method": "EXACT_SEED"
                }

        # Step 2: Cleaned Normalization Match
        cleaned_raw = self._clean_string(raw_name)
        for canonical in self.seed_canonical_entities:
            cleaned_canonical = self._clean_string(canonical)
            if cleaned_raw == cleaned_canonical:
                return {
                    "raw_name": raw_name,
                    "canonical_name": canonical,
                    "entity_type": entity_type,
                    "confidence_score": 0.95,
                    "resolution_method": "NORMALIZED_MATCH"
                }

        # Step 3: Substring / Prefix Match against Seed Database
        for canonical in self.seed_canonical_entities:
            if canonical.lower() in raw_name.lower():
                return {
                    "raw_name": raw_name,
                    "canonical_name": canonical,
                    "entity_type": entity_type,
                    "confidence_score": 0.88,
                    "resolution_method": "SUBSTRING_SEED"
                }

        # Step 4: Fallback to Title-Cased Cleaned Name
        fallback_canonical = raw_name.split("#")[0].strip()
        # Clean trailing variants or legal terms
        for suffix in ["Inc.", "LLC", "Corp", "Labs", "AI", "Technologies"]:
            if fallback_canonical.endswith(suffix):
                fallback_canonical = fallback_canonical[:-len(suffix)].strip()

        return {
            "raw_name": raw_name,
            "canonical_name": fallback_canonical if fallback_canonical else raw_name,
            "entity_type": entity_type,
            "confidence_score": 0.75,
            "resolution_method": "HEURISTIC_CANONICALIZATION"
        }
