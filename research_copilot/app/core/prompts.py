"""Prompt templates for the research copilot."""

RESEARCH_SYNTHESIS_PROMPT = """You are a research assistant. Synthesize the following sources \
into a clear, well-structured answer to the user's question. Use inline citations like [1], \
[2], etc. to reference the sources provided below.

Question: {question}

Sources:
{sources}

Instructions:
- Provide a comprehensive yet concise answer.
- Cite sources inline using [N] notation.
- If sources conflict, note the disagreement.
- If sources are insufficient, say so clearly.
"""

CONFIDENCE_ASSESSMENT_PROMPT = """Rate your confidence in the following answer on a scale of \
0.0 to 1.0 based on the quality and quantity of supporting sources.

Answer: {answer}
Number of sources: {source_count}
"""
