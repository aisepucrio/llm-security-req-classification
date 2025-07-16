import json
import ollama
from tqdm.auto import tqdm
from prompt import prompt_factory, strategys
client = ollama.Client(host='http://localhost:11434')
import openai
import time

# List of OpenAI API keys to rotate on rate limit
OPENAI_API_KEYS = [
    "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",  # Replace with your actual OpenAI API keys
]

key_index = 0
num_keys = len(OPENAI_API_KEYS)

def extract_label(response):
    if 'label' in response:
        return response['label']
    if 'result' in response and 'label' in response['result']:
        return response['result']['label']
    
    #for few shot strategy
    if "user_3" in response and 'label' in response['user_3']:
        return response['user_3']['label']

def classify_req_openAI(user_prompt, model, response_logs):
    global key_index
    global num_keys

    while True:
        try:
            client = openai.OpenAI(api_key=OPENAI_API_KEYS[key_index], timeout=10.0, max_retries=0)
            completion = client.chat.completions.create(
                model=model,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": f"{user_prompt}"
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "classify_req_openAI",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "label": {
                                    "description": "The predited label",
                                    "type": "string"
                                }
                            },
                            "additionalProperties": False
                        }
                    }
                }
            )
            response = json.loads(completion.choices[0].message.content)
            response_logs.append(response)
            label = extract_label(response)
            return label
        except Exception as err:
            # Handle timeouts, rate limits, and other errors by rotating keys
            if "timeout" in str(err).lower() or "timed out" in str(err).lower():
                print(f"Timeout with key {key_index+1}. Rotating to next key...")
            elif hasattr(err, 'status_code') and err.status_code == 429:
                print(f"Rate limit hit for key {key_index+1}. Rotating to next OpenAI API key...")
            elif "rate limit" in str(err).lower():
                print(f"Rate limit error for key {key_index+1}. Rotating to next OpenAI API key...")
            else:
                print(f"Error with key {key_index+1}: {err}. Rotating to next key...")

            # Rotate to the next key
            key_index = (key_index + 1) % num_keys
            print(f"Switching to OpenAI API key {key_index + 1} of {num_keys}...")

            # Add a small delay to avoid immediate retry
            time.sleep(1)

def classify_req(user_prompt, model, response_logs):
        if 'gpt' in model:
            return classify_req_openAI(user_prompt, model, response_logs)
        while True:
            try:
                model_output = ollama.generate(
                model=model,
                format="json",
                options={
                    "temperature": 0,
                },
                stream=False,
                prompt=f"""{user_prompt}"""
            )
            except:
                continue
            break
        response_logs.append(model_output)
        try:
            response = json.loads(str(model_output['response']))
            label = extract_label(response)
            if label == None:
                raise
            return label
        except:
            response_logs.append("^^^^^^^^^^ ERROR ^^^^^^^^^^")
            return None

if __name__ == '__main__':
    # define models to run
    models = ['gpt-4o-mini', 'gemma', 'gemma2_27b', 'gpt-4o-mini', 'llama3', 'llama3.1', 'llama3.2-vision', 'mistral', 'mistral-nemo', 'mistral-small', 'deepseek-r1:14b']

    path = r'./ConsolidatedData/data.json'
    path_extra_datasets = r'./ConsolidatedData/data_extra_datasets.json'

    for model in models:
        response_logs = []
        response_logs_path = rf'./results/logs/response_logs_{model.replace(":","_")}.json'
        output_path = rf'./results/{model.replace(":","_")}.json'
        with open(path, 'r') as file:
            data = json.load(file)

        #change sample size for testing
        sample_size = -1
        for i in tqdm(data[:sample_size]):
            req = i['requirement']
            for strategy in strategys:   
                user_prompt = prompt_factory(strategy=strategy, requirement=req)['user_msg']
                response = classify_req(user_prompt, model, response_logs)

                if 'response' not in i:
                    i['response'] = {}

                i['response'][strategy] = response
        
        with open(output_path, 'w+') as file:
            json.dump(data[:sample_size], file, indent=4)

        with open(response_logs_path, 'w+') as file:
            json.dump(response_logs, file, indent=4)

    for model in models:
        response_logs = []
        response_logs_path = rf'./results/logs_extra_datasets/response_logs_{model.replace(":", "_")}.json'
        output_path = rf'./results/{model.replace(":", "_")}_extra_datasets.json'
        with open(path_extra_datasets, 'r') as file:
            data = json.load(file)

        # change sample size for testing
        sample_size = -1
        for i in tqdm(data[:sample_size]):
            req = i['requirement']
            for strategy in strategys:
                user_prompt = prompt_factory(strategy=strategy, requirement=req)['user_msg']
                response = classify_req(user_prompt, model, response_logs)

                if 'response' not in i:
                    i['response'] = {}

                i['response'][strategy] = response

        with open(output_path, 'w+') as file:
            json.dump(data[:sample_size], file, indent=4)

        with open(response_logs_path, 'w+') as file:
            json.dump(response_logs, file, indent=4)

