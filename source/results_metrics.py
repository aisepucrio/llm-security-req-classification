from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from prompt import strategys
from data_analysis import rq1_eda, rq2_eda, rq2_best_improvement, rq2_improvement_by_strategy, rq3_individual,rq3_consolidated



def get_data(models):
    consolidated_df = pd.DataFrame()
    for model in models:
        path = rf'./results/{model}.json'
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['model'] = model
        consolidated_df = pd.concat([consolidated_df, df], ignore_index=True)

    for strategy in strategys:
        consolidated_df[strategy] = consolidated_df['response'].apply(lambda x: x[strategy] if strategy in x else 'undefined')
    consolidated_df.drop('response', axis=1, inplace=True)
    consolidated_df.to_csv(rf'./results/consolidated.csv')
    return consolidated_df

def filter_by_model(model, df):
    return df[df['model'] == model]

def filter_by_project_id(id, df):
    if type(id) == list:
        return df[df['project_id'].isin(id)]
    return df[df['project_id'] == id]

def filter_out_projects(ids, df):
    filtered_rows = []  
    for _, row in df.iterrows():
        if row['project_id'] not in ids:
            filtered_rows.append(row)
    
    return pd.DataFrame(filtered_rows)

def get_df_from_report(report):
    report_data = []
    lines = report.split('\n')
    for line in lines[2:4]:
        row = {}
        row_data = line.split(' ') 
        row_data = list(filter(None, row_data))
        row['class'] = row_data[0]
        row['precision'] = float(row_data[1])
        row['recall'] = float(row_data[2])
        row['f1_score'] = float(row_data[3])
        row['support'] = int(row_data[4])
        report_data.append(row)

    return pd.DataFrame.from_dict(report_data)

def get_rq1_consolidated_result(labels, models ):
    df = get_data(models)
    report_text = ''
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy != 'zero_shot'):
            continue
        for model in models:
            df_temp = filter_by_model(model, df).copy() 
            df_temp['predicted_label'] = df_temp[strategy]
            df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
            df_temp = df_temp.drop(columns=strategys)
            cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
            report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
            df_aux = get_df_from_report(report)    
            df_aux['model'] = model       
            consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)
            report_text += f"Confusion Matrix for {model} - {strategy}:\n"
            report_text += f"{cm}\n"
            report_text += f"Classification Report for {model} - {strategy}:\n"
            report_text += f"{report}\n"


    with open(rf'.\results\report_rq1_consolidated.txt', "w+") as file:
        file.write(report_text)
    return consolidated_results_df

def get_rq2_consolidated_result(labels, models ):
    df = get_data(models)
    report_text = ''
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy == 'zero_shot'):
            continue
        for model in models:
            df_temp = filter_by_model(model, df).copy() 
            df_temp['predicted_label'] = df_temp[strategy]
            df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
            df_temp = df_temp.drop(columns=strategys)
            cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
            report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
            df_aux = get_df_from_report(report)    
            df_aux['model'] = model 
            df_aux['strategy'] = strategy     
            consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)
            report_text += f"Confusion Matrix for {model} - {strategy}:\n"
            report_text += f"{cm}\n"
            report_text += f"Classification Report for {model} - {strategy}:\n"
            report_text += f"{report}\n"
            

    with open(rf'.\results\report_rq2_consolidated.txt', "w+") as file:
        file.write(report_text)
    return consolidated_results_df

def get_rq3_individual_secreq_result(labels, models ):
    project_dict = {
        50: "CPN",
        51: "ePurse",
        52: "GPS"
    }
    df = get_data(models)
    report_text = ''
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy == 'zero_shot'):
            continue
        for model in models:
            for projectId in [50,51,52]:
                df_temp = filter_by_model(model, df).copy() 
                df_temp = filter_by_project_id(projectId, df_temp).copy()
                df_temp['predicted_label'] = df_temp[strategy]
                df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
                df_temp = df_temp.drop(columns=strategys)
                cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
                report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
                df_aux = get_df_from_report(report)    
                df_aux['model'] = model 
                df_aux['strategy'] = strategy     
                df_aux['project'] = project_dict[projectId]
                df_aux['project_id'] = projectId
                consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)
                report_text += f"Confusion Matrix for {model} - {strategy} - {project_dict[projectId]}:\n"
                report_text += f"{cm}\n"
                report_text += f"Classification Report for {model} - {strategy} - {project_dict[projectId]}:\n"
                report_text += f"{report}\n"
                

    with open(rf'.\results\report_rq3_secreq.txt', "w+") as file:
        file.write(report_text)
    return consolidated_results_df

def get_rq3_consolidated_secreq_result(labels, models ):
    df = get_data(models)
    report_text = ''
    consolidated_results_df = pd.DataFrame()
    for strategy in strategys:
        if (strategy == 'zero_shot'):
            continue
        for model in models:
            df_temp = filter_by_model(model, df).copy() 
            df_temp = filter_by_project_id([50,51,52], df_temp).copy()
            df_temp['predicted_label'] = df_temp[strategy]
            df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
            df_temp = df_temp.drop(columns=strategys)
            cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
            report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
            df_aux = get_df_from_report(report)    
            df_aux['model'] = model 
            df_aux['strategy'] = strategy     
            consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)
            report_text += f"Confusion Matrix for {model} - {strategy} :\n"
            report_text += f"{cm}\n"
            report_text += f"Classification Report for {model} - {strategy} :\n"
            report_text += f"{report}\n"
            

    with open(rf'.\results\report_rq3_secreq.txt', "w+") as file:
        file.write(report_text)
    return consolidated_results_df

def get_rq3_promise_result(labels, models ):

    df = get_data(models)
    report_text = ''
    consolidated_results_df = pd.DataFrame()
    model = "mistral"
    strategy = "raw_inst"
    
    df_temp = filter_by_model(model, df).copy() 
    df_temp = filter_out_projects([50,51,52], df_temp).copy()
    df_temp['predicted_label'] = df_temp[strategy]
    df_temp = df_temp[df_temp['predicted_label'].isin(labels)]
    df_temp = df_temp.drop(columns=strategys)
    cm = confusion_matrix(df_temp['label'], df_temp['predicted_label'], labels=labels)
    report = classification_report(df_temp['label'], df_temp['predicted_label'], labels=labels)
    df_aux = get_df_from_report(report)    
    df_aux['model'] = model 
    df_aux['strategy'] = strategy     
    consolidated_results_df = pd.concat([consolidated_results_df, df_aux], ignore_index=True)
    report_text += f"Confusion Matrix for {model} - {strategy} - 'Promise':\n"
    report_text += f"{cm}\n"
    report_text += f"Classification Report for {model} - {strategy} - 'Promise':\n"
    report_text += f"{report}\n"
    

    with open(rf'.\results\report_rq3_promise.txt', "w+") as file:
        file.write(report_text)
    return consolidated_results_df

def main():
    labels = ['sec', 'nonsec']
    models = ['gemma', 'gemma2_27b', 'gpt-4o-mini', 'llama3', 'llama3.1', 'llama3.2-vision', 'mistral', 'mistral-nemo', 'mistral-small']

    df_rq1 = get_rq1_consolidated_result(labels, models)
    print("Head of df_rq1:")
    print(df_rq1.head(10))

    df_rq2 = get_rq2_consolidated_result(labels, models)
    print("\nHead of df_rq2:")
    print(df_rq2.head(10))

    df_rq3_individual_sec_req = get_rq3_individual_secreq_result(labels, models)
    print("\nHead of df_rq3_individual_sec_req:")
    print(df_rq3_individual_sec_req.head(10))

    df_rq3_consolidated_sec_req = get_rq3_consolidated_secreq_result(labels, models)
    print("\nHead of df_rq3_consolidated_sec_req:")
    print(df_rq3_consolidated_sec_req.head(10))
    #rq1_eda(df_rq1)
    #df_rq3_promise = get_rq3_promise_result(labels, models)
    #rq2_eda(df_rq2)
    #rq2_best_improvement(df_rq1,df_rq2)
    #rq2_improvement_by_strategy(df_rq1,df_rq2)
    #rq3_individual(df_rq3_individual_sec_req)
    #rq3_consolidated(df_rq3_consolidated_sec_req)
    #rq3_individual(df_rq3_individual_sec_req)

if __name__ == "__main__":
    main()