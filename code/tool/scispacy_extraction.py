import os
import json
import csv
import spacy
from scispacy.abbreviation import AbbreviationDetector
from tqdm import tqdm
from datetime import datetime

# 加载SciSpacy模型
nlp = spacy.load("en_core_sci_sm")
nlp.add_pipe("abbreviation_detector")

# 定义使用SciSpacy进行实体提取的函数
def extract_entities_with_scispacy(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            'text': ent.text,
            'label': ent.label_
        })
    return entities

# 确保输出目录存在
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 输入文件路径
input_file_path = '/ihome/hdaqing/abg96/llm/EHR_notes_hpi_annotation_updated_1.28.json'
output_directory = '/ihome/hdaqing/jul230/program/result/tools'

# 确保输出目录存在
ensure_directory_exists(output_directory)

# 定义工具名称和输出标签
tool = "scispacy"
labels = ['Onset', 'Region', 'Quality', 'Severity', 'Time of symptom', 'Provocation']

for label in labels:
    output_file_path = f'{output_directory}/{tool}_extracted_results_{label}.csv'

    with open(input_file_path, 'r') as json_file:
        data = json.load(json_file)

    # 初始化必要参数
    column_names = ['text', 'true', 'pred', 'extraction reasoning']

    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)

        for i in tqdm(data):
            hpi = i['hpi']
            annotations = i['annotation']['HPI']
            entity_texts = []

            # 遍历所有注释，找到所有匹配的注释
            for annotation in annotations:
                if label.lower() in (lbl.lower() for lbl in annotation['labels']):  # 匹配指定的原始标签
                    entity_texts.append(annotation['text'])

            # 处理找到的所有匹配的注释
            for entity_text in entity_texts:
                try:
                    results = extract_entities_with_scispacy(hpi)
                    pred_entities = [res['text'] for res in results]

                    pred_sentence = ', '.join(pred_entities)  # 将实体列表转换为完整的句子

                    if pred_sentence:
                        writer.writerow([hpi, entity_text, pred_sentence, f'SciSpacy extracted these entities ({label})'])
                    else:
                        writer.writerow([hpi, entity_text, '', 'No relevant entities extracted'])
                except Exception as e:
                    writer.writerow([hpi, entity_text, '', f'Error: {str(e)}'])
