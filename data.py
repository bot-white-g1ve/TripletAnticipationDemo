import torch
import json

def d_print(str):
    print(str)

def read_file_txt(filepath):
    '''
    Read from txt file, convert into [T, C] one-hot format
    '''
    triplet = []
    with open(filepath, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            # Exclude the first value and convert the rest to integers
            triplet.append([int(x) for x in values[1:]])
    return triplet

def convert_format(onehot_list):
    '''
    convert one-hot format to id format
    [T, C] to [T, I]
    '''
    id_list = []
    for onehot in onehot_list:
        id = [index for index, value in enumerate(onehot) if value == 1]
        id_list.append(id)
    return id_list

mapping_file = "label_mapping.json"

def mapping_string(id_list, mapping_file, ivt):
    '''
    id format to string format
    [T, I] to [T, S]
    ivt chosen from "triplet", "instruction", "verb" and "target"
    '''
    with open(mapping_file, 'r') as f:
        mapping = json.load(f)
    id_to_string = mapping[ivt]

    string_list = []

    for ids in id_list:
        strings = []
        for id in ids:
            if str(id) in id_to_string:
                strings.append(id_to_string[str(id)].replace(',', ' '))
            else:
                d_print(f"Unknown id: {str(id)}")
        string_list.append(strings)

    return string_list

def read_txt_to_string_list(filepath, mapping_file, ivt):
    '''
    Combine read_file_txt, convert_format and mapping_string
    '''
    one_hot_list = read_file_txt(filepath)
    id_list = convert_format(one_hot_list)
    string_list = mapping_string(id_list, mapping_file, ivt)
    return string_list

def add_color_to_string_list(string_list):
    colored_string_list = []
    
    for sublist in string_list:
        colored_sublist = []
        for text in sublist:
            parts = text.split()
            # 确保分割出的部分至少有三个元素，否则可能会出错
            if len(parts) >= 3:
                # 对每个部分应用指定的颜色
                colored_text = (f'<span style="color:#FB000D;">{parts[0]}</span> '
                                f'<span style="color:#1729B0;">{parts[1]}</span> '
                                f'<span style="color:#A69800;">{parts[2]}</span>')
                # 如果有更多的词，可以继续以最后一种颜色添加
                if len(parts) > 3:
                    colored_text += ' ' + ' '.join(f'<span style="color:#A69800;">{part}</span>' for part in parts[3:])
            else:
                # 如果不足三个部分，则简单地将整个文本用第一种颜色显示
                colored_text = f'<span style="color:#FB000D;">{text}</span>'
            colored_sublist.append(colored_text)
        colored_string_list.append(colored_sublist)
    
    return colored_string_list

if __name__ == '__main__':
    # triplet = read_txt_to_string_list("VID01/triplet.txt", mapping_file, 'triplet')
    # print(triplet[:31])

    class_of_frame = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    id_of_frame = convert_format(class_of_frame)
    print(id_of_frame)
    string_of_frame = mapping_string(id_of_frame, mapping_file, 'triplet')
    print(string_of_frame)
    string_of_frame_colored = add_color_to_string_list(string_of_frame)
    print(string_of_frame_colored)