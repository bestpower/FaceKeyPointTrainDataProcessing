import os
import shutil

def get68FacePoit(index_path):
    """
    根据标签文件中的坐标在人脸图片上绘制关键点
    :param index_path:
    :return:
    """
    with open(index_path, 'r') as fr:
        linelist = fr.readlines()
        fr.close()
    for l in linelist:
        line = [str(n) for n in l.strip().split()]
        img_path = "WFLW/" + line[206]
        # 根据图片路径求得标签文件路径
        if os.path.splitext(img_path)[1] == '.jpg':
            write_68_pts(img_path, line, '.jpg')
        elif os.path.splitext(img_path)[1] == '.png':
            write_68_pts(img_path, line, '.png')

def write_68_pts(img_path, line, img_fmt):
    img_path_NoEx = os.path.splitext(img_path)[0]
    fileName = os.path.splitext(os.path.basename(img_path))[0]
    txt_path = img_path_NoEx + ".pts"
    # 判断标签文件后是否存在
    if not os.path.exists(txt_path):
        with open(txt_path, 'a') as fw:
            # 开头部分
            fw.write("version: 1" + "\n")
            fw.write("0 1 0 0 0 0" + "\n")
            fw.write("n_points: 68" + "\n")
            fw.write("{" + "\n")
            # 人脸轮廓部分关键点
            for i in range(0, 66, 4):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            # 人脸左眉毛部分关键点
            for i in range(66, 76, 2):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            # 人脸右眉毛部分关键点
            for i in range(84, 94, 2):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            # 人脸鼻子部分
            for i in range(102, 120, 2):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            # 人脸眼睛部分
            fw.write(line[120] + " " + line[121] + "\n")
            fw.write(line[122] + " " + line[123] + "\n")
            for i in range(126, 132, 2):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            for i in range(134, 140, 2):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            for i in range(142, 148, 2):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            fw.write(line[150] + " " + line[151] + "\n")
            # 嘴巴部分
            for i in range(152, 192, 2):
                fw.write(line[i] + " " + line[i + 1] + "\n")
            # 结尾部分
            fw.write("}")
            fw.close()
    # 拷贝
    shutil.copyfile(img_path, "WFLW/trainset/" + fileName + img_fmt)
    shutil.copyfile(txt_path, "WFLW/trainset/" + fileName + ".pts")
    os.remove(txt_path)

if __name__ == "__main__":
    get68FacePoit("WFLW/list_98pt_rect_attr_train.txt")