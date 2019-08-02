import sys
import os
import glob
from PIL import Image
import re
import matplotlib.pyplot as plt
import logging
import logging.handlers

logging.FileHandler(filename='Face_data_mark.log', mode='a', encoding='utf-8')
logging.basicConfig(filename='Face_data_mark.log', filemode='a', level=logging.INFO)

def myInput(prompt):
    """
    终端输入内容
    :param prompt: 终端提示信息
    :return:
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return sys.stdin.readline()

def insertLine(txt_path, newLine):
    """
    指定行插入字符串
    :param txt_path: 插入文件路径
    :param newLine: 待插入文本
    :return:
    """
    lines = []
    with open(txt_path, 'r') as fr:
        linelist = fr.readlines()
        fr.close()
    for l in linelist:
        lines.append(l)
    lines.insert(1, newLine)  # 在第 2 行插入
    with open(txt_path, 'w') as fw:
        fw.writelines(lines)
        fw.close()

def imgShowAndMark(img_path, img_txt):
    """
    指定图片提示标记
    :param img_path: 待标记图片路径
    :param img_txt:  待标记图片标签路径
    :return:
    """

    # 显示待标记图片
    im = Image.open(img_path)
    plt.imshow(im)
    plt.xticks([])  # 去掉横坐标值
    plt.yticks([])  # 去掉纵坐标值
    plt.axis('off')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.show()
    # 自定义输入属性
    newLine = myInput("请输入当前图片六属性：")
    print("你输入的属性为，{}！".format(newLine).strip())
    # 插入对应标签文件指定行
    insertLine(img_txt, newLine)
    logging.info("已标记：" + str(img_path) + " 属性为：" + str(newLine).strip())
    plt.close()

def MarkTool(img_root_path):
    # png格式图片处理
    for fi in glob.glob(os.path.join(img_root_path, "*.png")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.png':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                # 消重
                f = open('Face_data_mark.log', 'rb')
                a = f.readlines()
                matchObj = re.search(fileName, "%s" % a, re.M | re.I)
                if matchObj:
                    print(img_root_path + fileName + " 已标记过")
                else:
                    fitxt = img_root_path + fileName + ".txt"
                    print("正在标记：" + str(fi))
                    imgShowAndMark(fi, fitxt)
    # jpg格式图片处理
    for fi in glob.glob(os.path.join(img_root_path, "*.jpg")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.jpg':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                # 消重
                f = open('Face_data_mark.log', 'rb')
                a = f.readlines()
                matchObj = re.search(fileName, "%s" % a, re.M | re.I)
                if matchObj:
                    print(img_root_path + fileName + " 已标记过")
                else:
                    fitxt = img_root_path + fileName + ".txt"
                    print("正在标记：" + str(fi))
                    imgShowAndMark(fi, fitxt)

if __name__ == "__main__":
    MarkTool("helen/trainfaceset/") # 属性标记自动化工具
    # MarkTool("lfpw/trainfaceset/") # 属性标记自动化工具
    # MarkTool("afw/trainfaceset/") # 属性标记自动化工具
    # MarkTool("300w/trainfaceset/") # 属性标记自动化工具