import os, glob


def make_txt(txt_root_path, output_txt_file):
    """
    遍历人脸数据根目录下标签文件
    :param txt_root_path: 原标签文件根目录
    :param output_txt_file: 输出标签文件路径
    :return:
    """
    for fi in glob.glob(os.path.join(txt_root_path, "*.txt")):
        make_one_line(fi, output_txt_file)


def make_one_line(input_path, output_txt_file):
    """
    将人脸数据标签文件中的68个关键点数据转为一行数据：
    第1列为图片路径，第2到137列为关键点x,y坐标，每列以空格间隔
    :param input_path: 原标签文件路径
    :param output_txt_file: 输出标签文件路径
    :return:
    """
    print('input_path:', input_path)
    num_of_line = 1
    a = ''
    with open(input_path) as file:
        while True:
            line = file.readline()  # 读取每一行
            if num_of_line == 1:
                # 第1行写入图片路径
                if os.path.splitext(input_path)[1] == '.txt':
                    imgFileName = os.path.splitext(input_path)[0]
                    imgFileName = imgFileName.replace("\\", "/")
                    if os.path.exists(imgFileName + '.png'):
                        imgFilePath = imgFileName + '.png'
                    elif os.path.exists(imgFileName + '.jpg'):
                        imgFilePath = imgFileName + '.jpg'
                a = imgFilePath + ' '
            elif num_of_line > 3 and num_of_line < 72:
                # 第4到71行为关键点坐标
                a += line.strip() + ' '
            elif num_of_line >= 72:
                break
            num_of_line = num_of_line + 1
    # 写入属性标签
    # num_of_line = 1
    # with open(input_path) as file:
    #     while True:
    #         line = file.readline()  # 读取每一行
    #         if num_of_line == 2:
    #             a += line.strip() + ' '
    #         elif num_of_line == 71:
    #             a += line.strip()
    #         elif num_of_line > 71:
    #             break
    #         num_of_line = num_of_line + 1
    print(a)
    write_txt(a, output_txt_file)
    write_txt('\n', output_txt_file)

def write_txt(line, output_txt_file):
    """
    按行写入
    :param line: 待写入行
    :param output_txt_file: 输出标签文件路径
    :return:
    """
    with open(output_txt_file, 'a') as f:
        f.write(line)

# 指定行插入方法
# def insertLine(txt_path, newLine):
#
#     lines = []
#     with open(txt_path, 'r') as fr:
#         linelist = fr.readlines()
#         fr.close()
#     for l in linelist:
#         lines.append(l)
#
#     lines.insert(2, newLine)  # 在第 3 行插入
#     with open(txt_path, 'w') as fw:
#         fw.writelines(lines)
#         fw.close()


if __name__ == '__main__':
    make_txt("300w/01_Indoor", "300w_indoor_one_line.txt")  # 300张室内图片
    make_txt("300w/02_Outdoor", "300w_outdoor_one_line.txt")  # 300张室外图片
    make_txt("afw/trainset", "afw_one_line.txt")  # 337张图片
    make_txt("helen/trainset", "helen_one_line.txt")  # 2000张图片
    make_txt("lfpw/trainset", "lfpw_one_line.txt")  # 811张图片
