# copy all the .md files together into one file

import os
import shutil

def copy_img(src_dir, out_dir, idx):
    # 把图片copy到 img 子目录下
    img_dir = os.path.join(src_dir, "img")
    out_dir = os.path.join(out_dir, "ch" + str(idx), "img")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    # copy images into top folder
    images = os.listdir(img_dir)
    for image in images:
        image_filepath = os.path.join(img_dir, image)
        if os.path.isfile(image_filepath):
            new_image_path = os.path.join(out_dir, image)
            shutil.copy(image_filepath, new_image_path)    

# 处理每章的内容
def process_ch(src_dir, out_dir, idx):
    # 合并所有 .md 到一个 .md 文件中
    md_files = os.listdir(src_dir)
    tgt_md_file = os.path.join(out_dir, "ch" + str(idx), "ch" + str(idx) + ".md")
    print(tgt_md_file)
    with open(tgt_md_file, "w", encoding="utf8") as fw:
        for md_file in md_files:
            if md_file.endswith(".md"):
                print(md_file)
                md_file = os.path.join(src_dir, md_file)
                with open(md_file, "r", encoding="utf8") as fr:
                    lines = fr.readlines()
                    fw.writelines(lines)


def get_output_dir():
    current_path = os.path.abspath(__file__)
    root_path = os.path.dirname(current_path)
    root_path = os.path.dirname(root_path)
    root_path = os.path.dirname(root_path)
    # 创建 output 目录
    output_dir = os.path.join(root_path, "RLBasic_output")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return output_dir

def get_input_dir(folder_name):
    current_path = os.path.abspath(__file__)
    root_path = os.path.dirname(current_path)
    root_path = os.path.dirname(root_path)
    folder_path = os.path.join(root_path, folder_name)
    return folder_path

def main():
    folders = [
        "第0章-序",
        "第1章-蒙提霍尔问题",
        "第2章-租车还车问题",
        "第3章-醉汉回家问题",
        "第4章-安全驾驶问题",
        "第5章-开发流程问题",
        "第6章-射击气球问题",
        "第7章-穿越虫洞问题",
        "第8章-多臂强盗问题",
        "第9章-冰面滑行问题",
        "第10章-悬崖漫步问题",
        "第11章-多步时序差分",
        "第12章-表格学习问题",
    ]

    output_dir = get_output_dir()
    print(output_dir)
    
    for i in range(len(folders)):
        input_dir = get_input_dir(folders[i])
        print(input_dir)
        copy_img(input_dir, output_dir, i)
        process_ch(input_dir, output_dir, i)


if __name__=="__main__":
    # 运行之前先清空 all.md, img 文件夹
    main()
