# Module 2: Introduction to Cortex LLM Functions

This module demonstrates the native out-of-the-box LLM functions provided by Snowflake Cortex, including completion, translation, sentiment analysis, and classification.

## Contents
* `intro_to_LLM_functions.ipynb`: Introduction to using the SQL and Python APIs for Snowflake Cortex LLM functions.
* `using_LLM_functions.ipynb`: Deep-dive into prompt engineering, configuring model hyperparameters (like `temperature`, `top_p`, `max_tokens`), enabling guardrails, and managing multi-turn chat states.

## Snowflake Cortex Features Highlighted
1. `SNOWFLAKE.CORTEX.COMPLETE()`: Text generation using standard open-weights LLMs (Llama, Mistral).
2. `SNOWFLAKE.CORTEX.TRANSLATE()`: Managed translation service.
3. `SNOWFLAKE.CORTEX.SENTIMENT()`: Native sentiment parsing returning float polarity scores.
4. `SNOWFLAKE.CORTEX.CLASSIFY_TEXT()`: Few-shot or zero-shot text classification into custom category labels.
