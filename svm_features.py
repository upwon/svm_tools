"""
将图片的像素信息，利用特征工程，降维 为 特征列表文件
"""
import os
from os.path import join
import glob
import sys
from PIL import Image

#全局变量 源路径（） 目标路径（） txt文件名  dig 待提取特征的数字
src=""
dst=""
filename_txt=""
dig=0

def get_feature(img):
    """
    获取指定图片的特征值,
    1. 按照每排的像素点,高度为10,然后宽度为6,总共16个维度
    2. 计算每个维度（行 或者 列）上有效像素点的和

    :type img: Image
    :return:一个维度为16的列表
    """

    width, height = img.size

    pixel_cnt_list = []
    height = 10
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

def get_svm_test_txt():
    """
    获取 测试集 的像素特征文件
    :return:
    """

    #img_folder = "D:\\pic_test\\svm_classfiy\\8"
    #test_file = open('D:\\pic_test\\svm_classfiy\\8\\特征文件\\last_test_pix_xy_8.txt','w')
    img_folder = src

    test_file = open(dst+"/"+filename_txt,'w')
    #"w" 以写方式打开，只能写文件， 如果文件不存在，创建该文件如果文件已存在，先清空，再打开文件
    #test_file = open('D:\\pic_test\\svm_classfiy\\destination_png\\0\\last_test_pix_xy_0.txt', 'w')
    dig_int=int(dig)
    convert_imgs_to_feature_file(dig_int, test_file, img_folder)  # todo 先用0代替
    test_file.close()


def convert_imgs_to_feature_file(dig, svm_feature_file, img_folder):
    """
    将某个目录下二进制图片文件，转换成特征文件
    :param dig:检查的数字
    :param svm_feature_file: svm的特征文件完整路径
    :type dig:int
    :return:
    """
    dig=dig
    file_list = os.listdir(img_folder)
    imgType_list={'.png','.jpg','.bmp'}
    # sample_cnt = 0
    # right_cnt = 0
    for file in file_list:
        file_suffix=os.path.splitext(file)[-1]
        if os.path.splitext(file)[-1]  not in imgType_list: #!= '.png': #or '.jpg' or '.bmp':    #这里有bug
            continue
        img = Image.open(img_folder + '/' + file)
        dif_list = get_feature(img)
        # sample_cnt += 1
        line = convert_values_to_str(dig, dif_list)
        svm_feature_file.write(line)
        svm_feature_file.write('\n')


def convert_values_to_str(dig, dif_list):
    """
    将特征值串转化为标准的svm输入向量:

    9 1:4 2:2 3:2 4:2 5:3 6:4 7:1 8:1 9:1 10:3 11:5 12:3 13:3 14:3 15:3 16:6

    最前面的是 标记值，后续是特征值
    :param dif_list:
    :type dif_list: list[int]
    :return:
    """
    dig=dig
    index = 1
    line = '%d' % dig

    for item in dif_list:
        fmt = ' %d:%d' % (index, item)
        line += fmt
        index += 1

    # print(line)
    return line


def convert_feature_to_vector(feature_list):
    """

    :param feature_list:
    :return:
    """
    index = 1
    xt_vector = []
    feature_dict = {}
    for item in feature_list:
        feature_dict[index] = item
        index += 1
    xt_vector.append(feature_dict)
    return xt_vector


def main():
    if len(sys.argv) < 5:
        print(
            '输入参数不足，输入格式为：\n   python svm_features.py  [source folder name] [deststion file name] [file name] [dig]')
        print("\n例如： python svm_features.py D:\img D:\\img 1.txt 1  注意中间用空格分开\n")
        print("********结束程序*********\n")
        exit()
    else:
        # p=int(sys.argv[1])
        global src
        src = sys.argv[1] + '/'
        global  dst
        dst = sys.argv[2] + '/'
        global filename_txt
        filename_txt = sys.argv[3]+'/'
        global dig
        dig=sys.argv[4]
        if os.path.isdir(dst):  # path参数存在且是一个文件夹
            print("存在文件夹")
        elif not os.path.exists(dst):
            os.makedirs(dst)
            print("不存在文件夹，已创建")
        get_svm_test_txt()
        print("*******************************")
        print("操作完毕\n")
        exit()
main()