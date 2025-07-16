import json

def merge_json_files(file1_path, file2_path, output_path, sources_to_exclude_file_1=None, sources_to_exclude_file_2=None):
    if sources_to_exclude_file_1 is None:
        sources_to_exclude_file_1 = []

    if sources_to_exclude_file_2 is None:
        sources_to_exclude_file_2 = []

    # Load data from both files
    with open(file1_path, 'r', encoding='utf-8') as f1:
        data1 = json.load(f1)
    with open(file2_path, 'r', encoding='utf-8') as f2:
        data2 = json.load(f2)

    # Exclude sources from data1 only
    filtered_data1 = [entry for entry in data1 if entry.get('source') not in sources_to_exclude_file_1]

    # Exclude sources from data1 only
    filtered_data2 = [entry for entry in data2 if entry.get('source') not in sources_to_exclude_file_2]

    # Merge filtered data1 and data2
    merged = filtered_data1 + filtered_data2

    # Reassign project_ids sequentially, preserving grouping
    # Map old project_id to new project_id
    old_to_new_id = {}
    next_id = 1
    for entry in merged:
        old_id = entry['project_id']
        if old_id not in old_to_new_id:
            old_to_new_id[old_id] = str(next_id)
            next_id += 1
        entry['project_id'] = old_to_new_id[old_id]

    # Write output
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(merged, out, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    models = ['deepseek-r1_14b', 'gemma', 'gemma2_27b', 'llama3', 'llama3.1', 'llama3.2-vision', 'mistral', 'mistral-nemo', 'mistral-small', 'gpt-4o-mini']
    for model in models:
        file1_path = f'./results/{model}.json'
        file2_path = f'./results/{model}_extra_datasets.json'
        output_path = f'./results/{model}_consolidated.json'

        merge_json_files(file1_path, file2_path, output_path, sources_to_exclude_file_1=['promise_exp'], sources_to_exclude_file_2=[])