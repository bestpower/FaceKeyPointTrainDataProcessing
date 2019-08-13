from numpy import *
from PIL import Image
import matplotlib.pyplot as plt
import os, glob

# 绘制关键点
def drawPoints(img_path, x, y, out_path):
    """
    在指定图片上画散点图
    :param img_path: 待画点图片路径
    :param x: 所有点的x坐标数组
    :param y: 所有点的y坐标数组
    :return: 显示绘制的散点图
    """
    im = Image.open(img_path)
    plt.imshow(im)
    fig = plt.gcf()
    plt.scatter(x, y, color='g', marker='.', s=2)

    plt.xticks([])  # 去掉横坐标值
    plt.yticks([])  # 去掉纵坐标值
    plt.axis('off')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)

    # plt.show()
    fig.savefig(out_path)
    plt.close()

def drawFacePoit(img_path, index_path, out_path):
    """
    根据标签文件中的坐标在人脸图片上绘制关键点
    :param img_path:
    :param index_path:
    :return:
    """

    x = []
    y = []
    num_of_line = 1
    with open(index_path, 'r') as f:
        while True:
            line = f.readline()
            # print(line)
            # if num_of_line < 2:
            if num_of_line < 5:
                # print("非坐标行")
                pass
            # elif num_of_line > 1 and num_of_line < 70:
            elif num_of_line >= 5 and num_of_line <= 72:
                num = list(map(float, line.strip().split()))
                # 坐标变换
                # x.append(num.__getitem__(0)*112)
                x.append(num.__getitem__(0))
                # y.append(num.__getitem__(1)*112)
                y.append(num.__getitem__(1))
            else:
                break
            num_of_line = num_of_line + 1
    # print("x = " + str(x) + "y = " + str(y))
    drawPoints(img_path, x, y, out_path)

def batch_drawFacePoit(root_path, out_root_path):
    """
    批量绘制关键点
    :param root_path: 待绘制图片路径
    :param out_root_path: 绘制后存储路径
    :return:
    """
    if os.path.exists(out_root_path):
        print("文件夹：" + out_root_path + "已存在")
    else:
        os.mkdir(out_root_path)

    img_num = 1
    # png格式图片处理
    for fi in glob.glob(os.path.join(root_path, "*.png")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.png':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                fitxt = root_path + fileName + ".pts"
                drawFacePoit(fi, fitxt, out_root_path + fileName +"_lm.png")
                print("第" + str(img_num) + "张图：" + fi + "绘制完毕")
                img_num = img_num + 1

    # jpg格式图片处理
    for fi in glob.glob(os.path.join(root_path, "*.jpg")):
        if fi is not None:
            if os.path.splitext(os.path.basename(fi))[1] == '.jpg':
                fileName = os.path.splitext(os.path.basename(fi))[0]
                fitxt = root_path + fileName + ".pts"
                drawFacePoit(fi, fitxt, out_root_path + fileName + "_lm.jpg")
                print("第" + str(img_num) + "张图：" + fi + "绘制完毕")
                img_num = img_num + 1

if __name__ == "__main__":
    # batch_drawFacePoit("lfpw/trainset/", "lfpw/trainset_lm/")
    # batch_drawFacePoit("afw/trainset/", "afw/trainset_lm/")
    # batch_drawFacePoit("helen/trainset/", "helen/trainset_lm/")
    # batch_drawFacePoit("300w/01_Indoor/", "300w/trainset_lm/")
    # batch_drawFacePoit("300w/02_Outdoor/", "300w/trainset_lm/")
    batch_drawFacePoit("WFLW/trainset/", "WFLW/trainset_lm/")
