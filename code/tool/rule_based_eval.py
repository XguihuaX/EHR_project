import pandas as pd
import re
import os

# 输入文件所在目录
input_dir = '/ihome/hdaqing/jul230/program/result/tools/'

# 定义工具名称和语义类型列表
tool = 'metamap'
semantic_types_list = ['tmco', 'spco', 'qlco', 'fndg', 'sosy', 'acty', 'phpr']

# 处理每个语义类型的文件
for entity in semantic_types_list:
    input_path = f'{input_dir}{tool}_extracted_results_{entity}.csv'
    output_file_path = f'{input_dir}{tool}_rule_annotations_extracted_{entity}.csv'

    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        continue

    # 读取输入文件
    df = pd.read_csv(input_path)
    df.columns = ['text', 'true', 'pred', 'extraction reasoning']
    true = list(df['true'])
    pred = list(df['pred'])
    n = len(true)
    rule_annotation = ['' for _ in range(n)]

    # 遍历每个样本，应用规则注释
    for i in range(n):
        if true[i] == ' ' or str(true[i]) == 'nan':
            true_compare = ''  # 替换为空或nan
        else:
            true_compare = str(true[i])

        if pred[i] == ' ' or str(pred[i]) == 'nan':
            pred_compare = ''
        else:
            pred_compare = str(pred[i])

        pattern = r"\b((n|N)o\s|(n|N)ot\s|(n|N)othing\b|N/A|n/a|(w|W)ithout\s|(d|D)enies\s|(n|N)on[\w-]*)\b"

        no_in_true = bool(re.search(pattern, true_compare))
        no_in_pred = bool(re.search(pattern, pred_compare))

        if no_in_true:
            true_compare = ''  # 如果字符串包含模式中的任何单词，替换为空字符串
        if no_in_pred:
            pred_compare = ''

        if true_compare == '' and pred_compare != '':
            rule_annotation[i] = 'Spurious'
        elif pred_compare == '' and true_compare != '':
            rule_annotation[i] = 'Missing'
        elif true_compare == '' and pred_compare == '':
            rule_annotation[i] = 'Similar'
        elif true_compare == pred_compare:
            rule_annotation[i] = 'Similar'
        else:
            rule_annotation[i] = 'to evaluate'  # 需要由LLM评估

    df['rule_annotation'] = rule_annotation
    ordered_columns = ['text', 'true', 'pred', 'rule_annotation', 'extraction reasoning']

    # 保存结果到输出文件
    df.to_csv(output_file_path, columns=ordered_columns, index=False)
