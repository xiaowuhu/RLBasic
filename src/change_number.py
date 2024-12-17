# 改变每个 chx.md 中的图、表、式的序号，从 x.y.z -> x-y
# 为每一章单独做一个索引，并把结果放入一个字典中，供其它章节参考

import re
import pickle

figure_pattern = r'图 \d+.\d+.\d+'
formular_1_pattern = r"tag\{\d+.\d+.\d+\}"
formular_2_pattern = r"式（\d+.\d+.\d+）"
table_pattern = r"表 \d+.\d+.\d+"

def findall(line, pattern):
    r = re.findall(pattern, line)
    return r    

def open_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')
    return lines

def check_obj_key(key, target_obj="图"):
    if target_obj in ["图","表"]:
        # 第一个字是图
        if key[0] != target_obj:
            return False
        # 第二个字是空格
        if key[1] != ' ':
            return False
        # 包含两个 .
        if key.count('.') != 2:
            return False
        return True
    else:
        assert(target_obj == "式")
        if key[0:4] != "tag{":
            return False
        if key[-1] != "}":
            return False
        # 包含两个 .
        if key.count('.') != 2:
            return False
        return True        

# 是否引用了其它章的图号
def get_ch(key):
    first_point = key.index('.')
    if key.startswith("tag{"):
        ch_num = int(key[4:first_point])
    else:
        ch_num = int(key[2:first_point])
    return ch_num

def get_obj_number(ch, target_obj="图"):
    dict_obj = {}
    filename = str.format(f'../RLBasic_output/ch{ch}/ch{ch}.md', ch)
    lines = open_file(filename)
    for line in lines:
        if target_obj == "图":
            pattern = figure_pattern
        elif target_obj == "表":
            pattern = table_pattern
        else:
            pattern = formular_1_pattern
        results = findall(line, pattern)
        for result in results:
            #print(result)
            if result not in dict_obj:
                dict_obj[result] = result
    sorted_keys = sorted(dict_obj)
    print("按顺序的key:", sorted_keys)
    i = 1
    for key in sorted_keys:
        if check_obj_key(key, target_obj) == False:
            print("Error key:", key)
            raise Exception('Error')
        # elif get_ch(key) != ch:
        #     print("引用其它章", key)
        else:
            if target_obj in ["图","表"]:
                dict_obj[key] = str.format(f'{target_obj} {ch}.{i}')
            else: # 式
                dict_obj[key] = "tag{" + str(ch) + "." + str(i) + "}"
            i += 1  

    return dict_obj


def find_and_replace(ch_num, line, dict, pattern):
    results = findall(line, pattern)
    if len(results) > 0:
        for result in results:
            ch_num = get_ch(result)
            if dict[ch_num].__contains__(result):
                line = line.replace(result, dict[ch_num][result])
            else:
                print("没找到原始索引:", result)
                print(line)
                raise Exception('Error')
    return line

def change_obj_number(
        ch, 
        dict_figures, dict_tables, dict_formulars_tag, dict_formulars_shi,
        figure_pattern, table_pattern, formular_1_pattern, formular_2_pattern):
    filename = str.format(f'../RLBasic_output/ch{ch}/ch{ch}.md', ch)
    lines = open_file(filename)
    new_filename = str.format(f'../RLBasic_output/ch{ch}/new_ch{ch}.md', ch)
    with open(new_filename, 'w', encoding='utf-8') as f:
        print(ch, len(lines))
        for line in lines:
            line = find_and_replace(ch, line, dict_figures, figure_pattern)
            line = find_and_replace(ch, line, dict_tables, table_pattern)
            line = find_and_replace(ch, line, dict_formulars_tag, formular_1_pattern)
            line = find_and_replace(ch, line, dict_formulars_shi, formular_2_pattern)
            f.write(line + '\n')

def copy_tag_formular(dict_formular_tag):
    dict_formular_2 = {}
    for key, value in dict_formular_tag.items():
        number_in_key = key[4:-1]
        number_in_value = value[4:-1]
        new_key = "式（" + number_in_key + "）"
        new_value = "式（" + number_in_value + "）"
        dict_formular_2[new_key] = new_value
    return dict_formular_2

if __name__ == '__main__':
    chs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    dict_figures = [None]
    dict_tables = [None]
    dict_formulars_tag = [None]
    dict_formulars_shi = [None]
    for ch in chs:
        dict_figure = get_obj_number(ch, target_obj="图")
        dict_figures.append(dict_figure)
        dict_table = get_obj_number(ch, target_obj="表")
        dict_tables.append(dict_table)
        dict_formular_1 = get_obj_number(ch, target_obj="式")
        dict_formulars_tag.append(dict_formular_1)
        dict_formular_2 = copy_tag_formular(dict_formular_1)
        dict_formulars_shi.append(dict_formular_2)

    with open("../RLBasic_output/dict_figures.pkl", "wb")  as f:
        pickle.dump(dict_figures, f)

    with open("../RLBasic_output/dict_tables.pkl", "wb")  as f:
        pickle.dump(dict_tables, f)

    with open("../RLBasic_output/dict_formulars_tag.pkl", "wb")  as f:
        pickle.dump(dict_formulars_tag, f)

    with open("../RLBasic_output/dict_formulars_shi.pkl", "wb")  as f:
        pickle.dump(dict_formulars_shi, f)

    # with open("../output/dict_figures.pkl", "rb")  as f:
    #     dict_figures = pickle.load(f)
    #     print(dict_figures)
    # with open("../output/dict_tables.pkl", "rb")  as f:
    #     dict_tables = pickle.load(f)
    #     print(dict_tables)
    # with open("../output/dict_formulars_tag.pkl", "rb")  as f:
    #     dict_formulars_tag = pickle.load(f)
    #     print(dict_formulars_tag)
    # with open("../output/dict_formulars_shi.pkl", "rb")  as f:
    #     dict_formulars_shi = pickle.load(f)
    #     print(dict_formulars_shi)

    for ch in chs:
        change_obj_number(
            ch, 
            dict_figures, dict_tables, dict_formulars_tag, dict_formulars_shi,
            figure_pattern, table_pattern, formular_1_pattern, formular_2_pattern
        )
