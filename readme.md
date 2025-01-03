# LLM Security Classification

This project analyzes the accuracy of Large Language Models (LLMs) in identifying security-related requirements. Follow the steps below to replicate the results.

## Model configuration
The following models are used in this project. The models and their specification are accessible through the provided links:
- **Llama 3:** https://ollama.com/library/llama3:8b
- **Llama 3.1:** https://ollama.com/library/llama3.1
- **Llama 3.2 - Vision:** https://ollama.com/library/llama3.2-vision
- **Mistral:** https://ollama.com/library/mistral
- **Mistral-Nemo:** https://ollama.com/library/mistral-nemo
- **Mistral-Small:** https://ollama.com/library/mistral-small
- **Gemma:** https://ollama.com/library/gemma
- **Gemma 2:** https://ollama.com/library/gemma2:27b
- **GPT-4o Mini:** https://platform.openai.com/docs/models


## Steps to Replicate

1. **Set Up the Environment**  
   - Create a virtual environment and install the packages listed in `requirements.txt`.

2. **Install Ollama**  
   - Install Ollama and start the Ollama server.

3. **Create a Consolidated Dataset**  
   - Run `source/create_consolidated_dataset.py` to generate the consolidated dataset.

4. **Generate Model Predictions**  
   - Run `source/main` to generate predictions from the models.
     - The `main` script contains a list of models. To evaluate new models:
       - Add the model name to the list. 
       - Ensure the model meets one of the following criteria:
         - It is from OpenAI (its name must include "gpt" as it stands).
         - It is available in the Ollama library. Missing models defined for evaluation should be automatically pulled by the Ollama provider.

5. **Generate Metrics for Analysis**  
   - Run `source/results_metrics.py` to create the evaluation metrics used for analysis.
     - This script also contains a model list. Update it to specify which models you want to include in the metrics generation.
     - The generated DataFrames are passed to functions in the `source/data_analysis.py` file. Each function corresponds to one of the tables displayed in the results section.

## Prompt Design
Prompts are generated in `source/prompt.py`. The factory injects each requirement into the specified strategy template and returns it as a user message.  

To add new prompts:
1. Add the template to the prompt factory in `source/prompt.py`.
2. Update the `strategies` list at the end of the file.

---

If you have any questions, feel free to reach out at **murilodsmartin@gmail.com**.
