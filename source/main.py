import json
import ollama
from tqdm.auto import tqdm
from prompt import prompt_factory, strategys
client = ollama.Client(host='http://localhost:11434')
from openai import OpenAI

#Add OpenAI api key, ex:
#client_openAI = OpenAi(MyApiKey) 
client_openAI = None



def extract_label(response):
    if 'label' in response:
        return response['label']
    if 'result' in response and 'label' in response['result']:
        return response['result']['label']
    
    #for few shot strategy
    if "user_3" in response and 'label' in response['user_3']:
        return response['user_3']['label']

def classify_req_openAI(user_prompt, model, response_logs):
    completion = client_openAI.chat.completions.create(
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
                    },
                    "additionalProperties": False
                }
            }
        }
    }
    )
    response = json.loads(completion.choices[0].message.content)
    response_logs.append(response) 
    label = extract_label(response)
    return label
    
    
       
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
    models = ['gemma', 'gemma2_27b', 'gpt-4o-mini', 'llama3', 'llama3.1', 'llama3.2-vision', 'mistral', 'mistral-nemo', 'mistral-small']


    path = r'./ConsolidatedData/data.json'

    for model in models:
        response_logs = []
        response_logs_path = rf'./results/logs/response_logs_{model.replace(":","_")}.json'
        output_path = rf'./results/{model.replace(":","_")}.json'
        with open(path, 'r') as file:
            data = json.load(file)

        #change sample size for testing
        sample_size = 4
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



    

            
        