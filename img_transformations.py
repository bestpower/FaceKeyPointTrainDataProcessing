
import os, glob
from numpy import *
import math
import matplotlib.pyplot as plt
import logging
from PIL import Image, ImageDraw
import operator
import shutil

logging.basicConfig(filename='Face_data_enrichment.log', filemode="w", level=logging.INFO)

def rotateimg(inputimg, outimg, rotate):
    """
    将图像按中心旋转指定角度
    :param inputimg: 输入图片路径
    :param outimg: 输出图片路径
    :param rotate: 旋转角度（角度数）
    :return:
    """
    im = Image.open(inputimg)
    # 旋转图片
    # 左旋转rotate度，当rotate为负时则为反向旋转
    im = im.rotate(rotate)
    im.save(outimg)

def batch_rotateimg(inputimg, outputimg):
    """
    批量旋转图片
    :param inputimg:
    :param outputimg:
    :return:
    """
    if os.path.exists(outputimg):
        print("文件夹：" + outputimg + "已存在")
    else:
        os.mkdir(outputimg)
    # 针对png格式处理
    for fi in glob.glob(os.path.join(inputimg, "*.png")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.png':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                # 以图片中心为旋转中心从-30到+30度，每5度为步长旋转
                for k in range(-30, 31, 5):
                    if k != 0:
                        print("正在处理：" + outputimg + fileName + "_" + str(k) + ".png")
                        rotateimg(fi, outputimg + fileName + "_" + str(k) + ".png", k)
                        logging.info("已处理：" + outputimg + fileName + "_" + str(k) + ".png")
    # 针对jpg格式处理
    for fi in glob.glob(os.path.join(inputimg, "*.jpg")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.jpg':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                # 以图片中心为旋转中心从-30到+30度，每5度为步长旋转
                for k in range(-30, 31, 5):
                    if k != 0:
                        print("正在处理：" + outputimg + fileName + "_" + str(k) + ".jpg")
                        rotateimg(fi, outputimg + fileName + "_" + str(k) + ".jpg", k)
                        logging.info("已处理：" + outputimg + fileName + "_" + str(k) + ".jpg")

def rotateCoordinate(x, y, w, h, rotate):
    """
    图片按中心旋转前后坐标变换
    :param x: 原横坐标
    :param y: 原纵坐标
    :param w: 图片像素点宽度
    :param h: 图片像素点高度
    :param rotate: 图片旋转角度（角度数）
    :return: 变换后的x,y坐标数组
    """
    c = []
    x1 = (x - w/2) * math.cos(math.radians(rotate)) + (y - h/2) * math.sin(math.radians(rotate)) + w/2
    c.append(x1)
    y1 = (w/2 - x) * math.sin(math.radians(rotate)) + (y - h/2) * math.cos(math.radians(rotate)) + h/2
    c.append(y1)
    return c

def batch_rotateCoordinate(inputtxt, outputtxt):
    """
    批量计算旋转图片人脸关键点坐标
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
            if os.path.exists(inputtxt + fileName + ".png"):
                im = Image.open(inputtxt + fileName + ".png")
            elif os.path.exists(inputtxt + fileName + ".jpg"):
                im = Image.open(inputtxt + fileName + ".jpg")
            # 图片的宽度和高度
            img_size = im.size
            w = img_size[0]
            h = img_size[1]
            for k in range(-30, 31, 5):
                if k != 0:
                    output_txt_file = outputtxt + fileName + "_" + str(k) + ".txt"
                    print("正在处理：" + output_txt_file)
                    num_of_line = 1
                    with open(fi, 'r') as f:
                        while True:
                            line = f.readline()
                            print(line)
                            if num_of_line == 1:
                                write_txt(output_txt_file, outputtxt + fileName + "_" + str(k) + ".png")
                                write_txt(output_txt_file, '\n')
                            elif num_of_line > 3 and num_of_line < 72:
                                num = list(map(float, line.strip().split()))
                                # 坐标变换
                                c = rotateCoordinate(num.__getitem__(0), num.__getitem__(1), w, h, k)
                                write_txt(output_txt_file, str(c.__getitem__(0)) + " " + str(c.__getitem__(1)))
                                write_txt(output_txt_file, '\n')
                            elif num_of_line >= 72:
                                break
                            num_of_line = num_of_line + 1
                        logging.info("已处理：" + output_txt_file)

def write_txt(output_file, line):
    with open(output_file, 'a') as f:
        f.write(line)

def getFaceArea(input_txt):
    """
    根据标签数据估计人脸范围
    :param input_txt: 人脸标签文件路径
    :return: 人脸坐标范围数组
    """
    x_num = []
    y_num = []
    fa = []
    num_of_line = 1
    with open(input_txt, 'r') as f:
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
    fa.append(x_min_number)
    x_max_index, x_max_number = max(enumerate(x_num), key=operator.itemgetter(1))  # 找出人脸关键点最大横坐标
    fa.append(x_max_number)
    y_min_index, y_min_number = min(enumerate(y_num), key=operator.itemgetter(1))  # 找出人脸关键点最小纵坐标
    fa.append(y_min_number)
    y_max_index, y_max_number = max(enumerate(y_num), key=operator.itemgetter(1))  # 找出人脸关键点最大纵坐标
    fa.append(y_max_number)

    return fa

def occlusionImg(input_img, output_img):
    """
    人脸区域随机矩形遮挡（10%-50%范围）
    :param input_img:
    :param output_img:
    :return:
    """
    impath = input_img
    img2 = Image.open(impath)
    img_size = img2.size
    print("image size = " + str(img2.size))
    draw = ImageDraw.Draw(img2)
    # 估计人脸范围
    if os.path.splitext(input_img)[1] == '.png':
        txtfilepath = os.path.splitext(input_img)[0]
        output_txt_file = txtfilepath + ".txt"
    elif os.path.splitext(input_img)[1] == '.jpg':
        txtfilepath = os.path.splitext(input_img)[0]
        output_txt_file = txtfilepath + ".txt"
    print("正在处理：" + output_txt_file)
    # 获取人脸区域范围数组
    fa = getFaceArea(output_txt_file)
    # 获取人脸区域最值坐标
    x_min_number = fa[0]
    x_max_number = fa[1]
    y_min_number = fa[2]
    y_max_number = fa[3]
    # 绘制遮挡方框
    slectXY = []
    isTrueOc = False
    # 最小遮挡占比10%
    min_percent_area = (int(x_max_number) - int(x_min_number)) * (int(y_max_number) - int(y_min_number)) / 10.0
    # 最大遮挡占比50%
    max_percent_area = (int(x_max_number) - int(x_min_number)) * (int(y_max_number) - int(y_min_number)) / 2.0
    # 随机取最小横坐标值
    x_mi = random.randint(int(x_min_number), int(x_max_number)-2)
    slectXY.append(x_mi)
    # 随机取最小纵坐标值
    y_mi = random.randint(int(y_min_number), int(y_max_number)-2)
    slectXY.append(y_mi)
    # 随机取最大横坐标值
    x_ma = random.randint(x_mi+1, int(x_max_number))
    slectXY.append(x_ma)
    # 随机取最大纵坐标值
    y_ma = random.randint(y_mi+1, int(y_max_number))
    slectXY.append(y_ma)
    # 在允许的遮挡占比范围内绘制矩形遮挡框
    if (x_ma - x_mi) * (y_ma - y_mi) <= max_percent_area:
        if (x_ma - x_mi) * (y_ma - y_mi) >= min_percent_area:
            try:
                # 绘制黑色遮挡
                draw.rectangle(slectXY, fill=(0, 0, 0))
            except:
                draw.rectangle(slectXY, fill=0)
            isTrueOc = True

    if isTrueOc:
        plt.imshow(img2)
        fig = plt.gcf()
        plt.xticks([])  # 去掉横坐标值
        plt.yticks([])  # 去掉纵坐标值
        plt.axis('off')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        fig.savefig(output_img)
        plt.close()
        # 同时复制对应坐标文件
        txtfilepath = os.path.splitext(input_img)[0]
        outtxtfilepath = os.path.splitext(output_img)[0]
        shutil.copyfile(txtfilepath + ".txt", outtxtfilepath + ".txt")
    else:
        print(output_img + "：选取框不符合遮挡要求")

# 批量遮挡
def batch_occlusionImg(inputimg, outputimg):
    """
    批量遮挡图片
    :param inputimg:
    :param outputimg:
    :return:
    """
    if os.path.exists(outputimg):
        print("文件夹：" + outputimg + "已存在")
    else:
        os.mkdir(outputimg)

    # 针对png格式处理
    for fi in glob.glob(os.path.join(inputimg, "*.png")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.png':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                print("正在处理：" + outputimg + fileName + "_oc" + ".png")
                # 随机黑色矩形遮挡
                # occlusionImg(fi, outputimg + fileName + "_oc" + ".png")
                # 随机方形、正三角形、圆形不同颜色遮挡
                drawOcclusionImg(fi, outputimg + fileName + "_oc" + ".png")
                logging.info("已处理：" + outputimg + fileName + "_oc" + ".png")
    # 针对jpg格式处理
    for fi in glob.glob(os.path.join(inputimg, "*.jpg")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.jpg':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                print("正在处理：" + outputimg + fileName + "_oc" + ".jpg")
                # 随机黑色矩形遮挡
                # occlusionImg(fi, outputimg + fileName + "_oc" + ".png")
                # 随机方形、正三角形、圆形不同颜色遮挡
                drawOcclusionImg(fi, outputimg + fileName + "_oc" + ".jpg")
                logging.info("已处理：" + outputimg + fileName + "_oc" + ".jpg")

def drawOcclusionImg(img_path, output_img):
    """
    在指定图片上绘制并保存有遮挡的图
    :param img_path:
    :param output_img:
    :return:
    """
    im = Image.open(img_path)
    plt.imshow(im)
    fig = plt.gcf()

    # 颜色选项
    c = ['b', 'c', 'g', 'k', 'm', 'r', 'w', 'y']
    # 形状选项
    m = ['^', 'v', '<', '>', 's', 'o']
    # 提取标签文件
    if os.path.splitext(img_path)[1] == '.png':
        txtfilepath = os.path.splitext(img_path)[0]
        output_txt_file = txtfilepath + ".txt"
        print("正在处理：" + output_txt_file)
        fa = getFaceArea(output_txt_file)
    elif os.path.splitext(img_path)[1] == '.jpg':
        txtfilepath = os.path.splitext(img_path)[0]
        output_txt_file = txtfilepath + ".txt"
        print("正在处理：" + output_txt_file)
        fa = getFaceArea(output_txt_file)

    # 坐标范围（保证不超过人脸尺寸边缘）
    xmin = float((fa[1] - fa[0])/2 * sqrt(5))
    xmax = float(fa[1] - xmin)
    ymin = float((fa[3] - fa[2]) / 2 * sqrt(5))
    ymax = float(fa[3] - ymin)
    # 遮挡面积20%人脸区域
    so = 112*112*9/5.0
    # 绘制遮挡（随机位置、随机颜色、随机形状）
    plt.scatter(random.uniform(xmin, xmax), random.uniform(ymin, ymax),
                color=random.choice(c), marker=random.choice(m), s=so)

    plt.xticks([])  # 去掉横坐标值
    plt.yticks([])  # 去掉纵坐标值
    plt.axis('off')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    fig.savefig(output_img)
    plt.close()
    # 同时复制对应坐标文件
    txtfilepath = os.path.splitext(img_path)[0]
    outtxtfilepath = os.path.splitext(output_img)[0]
    shutil.copyfile(txtfilepath + ".txt", outtxtfilepath + ".txt")

if __name__ == "__main__":

    # 批量旋转
    batch_rotateimg("300w/01_Indoor/", "300w/01_Indoor_Rt/")
    batch_rotateCoordinate("300w/01_Indoor/", "300w/01_Indoor_Rt/")
    batch_rotateimg("300w/02_Outdoor/", "300w/02_Outdoor_Rt/")
    batch_rotateCoordinate("300w/02_Outdoor/", "300w/02_Outdoor_Rt/")
    batch_rotateimg("lfpw/trainset/", "lfpw/trainset_Rt/")
    batch_rotateCoordinate("lfpw/trainset/", "lfpw/trainset_Rt/")
    batch_rotateimg("afw/trainset/", "afw/trainset_Rt/")
    batch_rotateCoordinate("afw/trainset/", "afw/trainset_Rt/")
    batch_rotateimg("helen/trainset/", "helen/trainset_Rt/")
    batch_rotateCoordinate("helen/trainset/", "helen/trainset_Rt/")
    # 批量图片遮挡
    batch_occlusionImg("300w/01_Indoor/", "300w/01_Indoor_Oc/")
    batch_occlusionImg("300w/02_Outdoor/", "300w/02_Outdoor_Oc/")
    batch_occlusionImg("300w/01_Indoor_Rt/", "300w/01_Indoor_Rt_Oc/")
    batch_occlusionImg("300w/02_Outdoor_Rt/", "300w/02_Outdoor_Rt_Oc/")
    batch_occlusionImg("lfpw/trainset/", "lfpw/trainfaceset_Oc/")
    batch_occlusionImg("afw/trainset/", "afw/trainset_Oc/")
    batch_occlusionImg("helen/trainset/", "helen/trainset_Oc/")
    batch_occlusionImg("lfpw/trainset_Rt/", "lfpw/trainset_Rt_Oc/")
    batch_occlusionImg("afw/trainset_Rt/", "afw/trainset_Rt_Oc/")
    batch_occlusionImg("helen/trainset_Rt/", "helen/trainset_Rt_Oc/")


