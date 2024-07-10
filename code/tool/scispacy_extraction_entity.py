import os
import json
import csv
import spacy
import scispacy
from tqdm import tqdm
from scispacy.abbreviation import AbbreviationDetector

# 加载SciSpacy模型
nlp = spacy.load("en_ner_bc5cdr_md")
nlp.add_pipe("abbreviation_detector")

# 确保输出目录存在
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 定义实体提取函数并进行处理
def extract_entities(text, label):
    doc = nlp(text)
    entities = []

    if label == "Region" or label == "Radiation":
        entity_types = ["ANAT", "BODY_PART"]
    elif label == "Severity":
        entity_types = ["QUANT"]
    elif label == "Onset":
        entity_types = ["TEMP"]
    elif label == "Quality":
        entity_types = ["CLINICAL_ATTRIBUTE", "SYMPTOM"]
    elif label == "Provocation":
        entity_types = ["EVENT"]
    else:
        entity_types = []

    for ent in doc.ents:
        if ent.label_ in entity_types:
            entity = {
                'preferred_name': ent.text,
                'semantic_types': [ent.label_]
            }
            entities.append(entity)

    return entities

# 输入文件路径
input_file_path = '/ihome/hdaqing/abg96/llm/EHR_notes_hpi_annotation_updated_1.28.json'
output_directory = '/ihome/hdaqing/jul230/program/result/tools'

# 确保输出目录存在
ensure_directory_exists(output_directory)

# 读取JSON文件
with open(input_file_path, 'r') as json_file:
    data = json.load(json_file)

# 定义工具名称和输出标签
tool = "scispacy"
labels = ['Onset', 'Region', 'Radiation', 'Quality', 'Severity', 'Provocation']

for label in labels:
    output_file_path = f'{output_directory}/{tool}_extracted_results_{label}_entity.csv'

    # 初始化CSV文件
    column_names = ['text', 'true', 'pred', 'extraction reasoning']
    with open(output_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)

        for i in tqdm(data):
            hpi = i['hpi']
            annotations = i['annotation']['HPI']
            entity_texts = []

            print(f"Debug: Processing HPI - {hpi}")  # 调试信息

            # 遍历所有注释，找到所有匹配的注释
            for annotation in annotations:
                print(f"Debug: Annotation labels - {annotation['labels']}")  # 调试信息
                # 确保标签匹配时的严格性
                if any(label == lbl for lbl in annotation['labels']):
                    print(f"Debug: Matched label - {label}")  # 调试信息
                    entity_texts.append(annotation['text'])

            # 处理找到的所有匹配的注释
            for entity_text in entity_texts:
                print(f"Debug: Processing annotation - {entity_text}")  # 调试信息
                try:
                    results = extract_entities(hpi, label)
                    pred_entities = [entity['preferred_name'] for entity in results]  # 提取实体名称
                    pred_sentence = ', '.join(pred_entities)  # 将实体列表转换为完整的句子

                    if pred_sentence:
                        writer.writerow([hpi, entity_text, pred_sentence, f'SciSpacy extracted these entities ({label})'])
                    else:
                        writer.writerow([hpi, entity_text, '', 'No relevant entities extracted'])
                except Exception as e:
                    print(f"Error: {str(e)}")  # 调试信息
                    writer.writerow([hpi, entity_text, '', f'Error: {str(e)}'])

print(f'Results saved to {output_directory}')
