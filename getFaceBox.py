from numpy import *
from PIL import Image
import operator
import logging
import logging.handlers
import os, glob


# 估计人脸位置
def estimateFaceBox(output_txt_file):
    # 估计人脸范围
    fb = []  # 人脸参数数组
    x_num = []
    y_num = []
    num_of_line = 1
    with open(output_txt_file, 'r') as f:
        while True:
            line = f.readline()
            if num_of_line <= 3:
                print(line)
            elif num_of_line > 3 and num_of_line < 72:
                num = list(map(float, line.strip().split()))
                x_num.append(num.__getitem__(0))
                y_num.append(num.__getitem__(1))
            elif num_of_line >= 72:
                break
            num_of_line = num_of_line + 1
    x_min_index, x_min_number = min(enumerate(x_num), key=operator.itemgetter(1))  # 找出人脸关键点最小横坐标
    x_max_index, x_max_number = max(enumerate(x_num), key=operator.itemgetter(1))  # 找出人脸关键点最大横坐标
    y_min_index, y_min_number = min(enumerate(y_num), key=operator.itemgetter(1))  # 找出人脸关键点最小纵坐标
    y_max_index, y_max_number = max(enumerate(y_num), key=operator.itemgetter(1))  # 找出人脸关键点最大纵坐标

    # 截取图片，取横纵坐标最大差值为基准
    padding = max(x_max_number - x_min_number, y_max_number - y_min_number)
    x = x_min_number - padding * 0.10
    y = y_min_number - padding * 0.15
    w = padding * 1.20
    h = padding * 1.20

    fb.append(w)
    fb.append(h)
    fb.append(x)
    fb.append(y)

    return fb

# 人脸图片裁剪放缩
def cropFaceImg(inputimg, tmpimg, outimg):
    """
    人脸裁剪放缩
    :param inputimg: 待处理图片路径
    :param tmpimg: 中间图片路径
    :param outimg: 输出图片路径
    :return:
    """
    im = Image.open(inputimg)
    # 图片的宽度和高度
    img_size = im.size
    print("图片宽度和高度分别是{}".format(img_size))
    '''
    裁剪：传入一个元组作为参数
    元组里的元素分别是：（距离图片左边界距离x， 距离图片上边界距离y，距离图片左边界距离+裁剪框宽度x+w，距离图片上边界距离+裁剪框高度y+h）
    '''
    if os.path.splitext(inputimg)[1] == '.png':
        txtfilepath = os.path.splitext(inputimg)[0]
        output_txt_file = txtfilepath + ".txt"
        print("正在处理：" + output_txt_file)
    elif os.path.splitext(inputimg)[1] == '.jpg':
        txtfilepath = os.path.splitext(inputimg)[0]
        output_txt_file = txtfilepath + ".txt"
        print("正在处理：" + output_txt_file)

    fb = estimateFaceBox(output_txt_file)
    x = fb.__getitem__(2)
    y = fb.__getitem__(3)
    w = fb.__getitem__(0)
    h = fb.__getitem__(1)
    # 裁剪出人脸框图片
    region = im.crop((x, y, x + w, y + h))
    region.save(outimg)
    # 图片尺寸放缩（根据具体训练要求来定）
    # region.save(tmpimg)
    # resizeimg(tmpimg, outimg)
    # os.remove(tmpimg)

# 批量裁剪人脸框内图片
def batch_cropFaceImg(inputimg, outputimg):
    """
    批量裁剪人脸框内图片
    :param inputimg: 待裁剪图片根路径
    :param outputimg: 裁剪后图片输出路径
    :return:
    """
    if os.path.exists(outputimg):
        print("文件夹：" + outputimg + "已存在")
    else:
        os.mkdir(outputimg)
    # 针对png格式图片的处理
    for fi in glob.glob(os.path.join(inputimg, "*.png")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.png':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                print("正在处理：" + outputimg + fileName + "_fb" + ".png")
                cropFaceImg(fi, outputimg + fileName + "_tmp" + ".png", outputimg + fileName + "_fb" + ".png")
                logging.info("已处理：" + outputimg + fileName + "_fb" + ".png")
    # 针对jpg格式图片的处理
    for fi in glob.glob(os.path.join(inputimg, "*.jpg")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.jpg':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                print("正在处理：" + outputimg + fileName + "_fb" + ".jpg")
                cropFaceImg(fi, outputimg + fileName + "_tmp" + ".jpg", outputimg + fileName + "_fb" + ".jpg")
                logging.info("已处理：" + outputimg + fileName + "_fb" + ".jpg")

def cropCoordinate(x, y, w, h, xfl, yft):
    """
    图片裁剪放缩前后坐标变换
    :param x: 原横坐标
    :param y: 原纵坐标
    :param w: 图片像素点宽度
    :param h: 图片像素点高度
    :param xfl: 人脸框左边框横坐标
    :param yft: 人脸框上边框纵坐标
    :return: 变换后的x,y坐标数组
    """
    c = []
    # x1 = float('%.6f' % float((x - xfl) / w)) # 归一化
    x1 = float('%.6f' % float(x - xfl))   # 原图尺寸
    c.append(x1)
    # y1 = float('%.6f' % float((y - yft) / h)) # 归一化
    y1 = float('%.6f' % float(y - yft))  # 原图尺寸
    c.append(y1)
    return c

def batch_cropCoordinate(inputtxt, outputtxt):
    """
    批量计算裁剪图片人脸关键点坐标
    :param inputtxt: 原图片人脸关键点坐标路径
    :param outputtxt: 旋转后图片人脸关键点坐标路径
    :return:
    """
    if os.path.exists(outputtxt):
        print("文件夹：" + outputtxt + "已存在")
    else:
        os.mkdir(outputtxt)

    for fi in glob.glob(os.path.join(inputtxt, "*.txt")):
        if os.path.splitext(os.path.basename(fi))[1] == '.txt':
            fileName = os.path.splitext(os.path.basename(fi))[0]
            imgPngFilePath = inputtxt + fileName + ".png"
            imgJpgFilePath = inputtxt + fileName + ".jpg"
            # 获取人脸框位置信息
            fb = estimateFaceBox(inputtxt + fileName + ".txt")
            output_txt_file = outputtxt + fileName + "_fb" + ".txt"
            print("正在处理：" + output_txt_file)
            num_of_line = 1
            with open(fi, 'r') as f:
                while True:
                    line = f.readline()
                    print(line)
                    if num_of_line == 1:
                        if os.path.exists(imgPngFilePath):
                            write_txt(output_txt_file, outputtxt + fileName + "_fb" + ".png")
                        elif os.path.exists(imgJpgFilePath):
                            write_txt(output_txt_file, outputtxt + fileName + "_fb" + ".jpg")
                        write_txt(output_txt_file, '\n')
                    elif num_of_line > 3 and num_of_line < 72:
                        num = list(map(float, line.strip().split()))
                        # 坐标变换
                        c = cropCoordinate(num.__getitem__(0), num.__getitem__(1), fb.__getitem__(0),
                                           fb.__getitem__(1), fb.__getitem__(2), fb.__getitem__(3))
                        write_txt(output_txt_file, str(c.__getitem__(0)) + " " + str(c.__getitem__(1)))
                        write_txt(output_txt_file, '\n')
                    elif num_of_line >= 72:
                        break
                    num_of_line = num_of_line + 1
                logging.info("已处理：" + output_txt_file)

def write_txt(output_file, line):
    with open(output_file, 'a') as f:
        f.write(line)


# 放缩图片
def resizeimg(inputimg,outimg):
    img1 = Image.open(inputimg)
    out = img1.resize((112, 112), Image.ANTIALIAS)
    print("图片宽度和高度分别是{}".format(out.size))
    out.save(outimg)

if __name__ == "__main__":
    batch_cropFaceImg("lfpw/trainset/", "lfpw/trainfaceset/")
    batch_cropCoordinate("lfpw/trainset/", "lfpw/trainfaceset/")
    batch_cropFaceImg("afw/trainset/", "afw/trainfaceset/")
    batch_cropCoordinate("afw/trainset/", "afw/trainfaceset/")
    batch_cropFaceImg("helen/trainset/", "helen/trainfaceset/")
    batch_cropCoordinate("helen/trainset/", "helen/trainfaceset/")
    batch_cropFaceImg("300w/01_Indoor/", "300w/trainfaceset/")
    batch_cropCoordinate("300w/01_Indoor/", "300w/trainfaceset/")
    batch_cropFaceImg("300w/02_Outdoor/", "300w/trainfaceset/")
    batch_cropCoordinate("300w/02_Outdoor/", "300w/trainfaceset/")