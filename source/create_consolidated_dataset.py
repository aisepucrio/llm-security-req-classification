import chardet
import json

def get_file_encoding(file_path):
    '''
    Get the encoding of a file
    '''
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    return chardet.detect(raw_data)['encoding']

def treat_promise_exp(consolidated_data):
    path = r'./DataSets/Promise_exp/PROMISE_exp.arff'
    encoding = get_file_encoding(path)
    with open(path, 'r', encoding=encoding) as file:
        lines = file.readlines()
        data = False
        for line in lines:
            if data:
                output = line.split(',')
                label = 'sec' if output[2].strip() == 'SE' else 'nonsec'
                consolidated_data.append({'project_id': int(output[0]), 'requirement': output[1], 'label':label, 'source': 'promise_exp'})
            if '@DATA' in line:
                data = True
    return consolidated_data

def treat_sec_req(consolidated_data):
    path_cpn = r'./DataSets/SecReq/CPN.csv'
    path_ePurse = r'./DataSets/SecReq/ePurse.csv'
    path_gps = r'./DataSets/SecReq/GPS.csv'
    paths = [path_cpn, path_ePurse, path_gps]
    for i, path in enumerate(paths):
        encoding = get_file_encoding(path)
        with open(path, 'r', encoding=encoding) as file:
            lines = file.readlines()
            for line in lines:
                output = line.split(';')
                label = output[1].strip()
                if label == "xyz":
                    continue
                consolidated_data.append({'project_id': 50+i, 'requirement': output[0], 'label':label, 'source': 'SecReq'})

    return consolidated_data

def treat_dosspre(consolidated_data):
    path = r'./DataSets/DOSSPRE/DOSSPRE 2.0Binary.csv'
    encoding = get_file_encoding(path)
    with open(path, 'r', encoding=encoding) as file:
        lines = file.readlines()
        for line in lines[1:]:
            output = line.split(',')
            if len(output) < 3:
                continue
            project_id = int(output[0])
            label = "sec" if output[1] == "SR" else "nonsec"
            consolidated_data.append({'project_id': project_id, 'requirement': output[2].strip(), 'label': label, 'source': 'DOSSPRE'})

    return consolidated_data


def treat_promise_plus(consolidated_data):
    path = r'./DataSets/Promise+/PROMISE+.arff'
    encoding = get_file_encoding(path)
    with open(path, 'r', encoding=encoding) as file:
        lines = file.readlines()
        data = False
        for line in lines:
            if data:
                output = line.split("'")
                label = 'sec' if output[-1].strip().endswith('SE') else 'nonsec'
                consolidated_data.append({'project_id': 105 + int(output[0].strip(",")), 'requirement': output[1], 'label':label, 'source': 'promise_exp'})
            if '@DATA' in line:
                data = True
    return consolidated_data

if __name__ == '__main__':
    consolidated_data = []
    consolidated_data = treat_promise_exp(consolidated_data)
    consolidated_data = treat_sec_req(consolidated_data)
    output_path = r'./ConsolidatedData/data.json'
    with open(output_path, 'w') as file:
        json.dump(consolidated_data, file, indent=4)

    consolidated_data = []
    consolidated_data = treat_dosspre(consolidated_data)
    consolidated_data = treat_promise_plus(consolidated_data)
    output_path = r'./ConsolidatedData/data_extra_datasets.json'
    with open(output_path, 'w') as file:
        json.dump(consolidated_data, file, indent=4)
