import glob
import sys
import os
import cv2
from PIL import Image


dst_img_size_width=18          #resize 图像的宽度
dst_img_size_height=28         #resize 图像的高度
dst=""

def main():
    if len(sys.argv) < 2:
        print(
            '输入参数不足，输入格式为：\n   python image_resize.py  [source folder name] [deststion folder name]')
        print("********结束程序*********\n")
        exit()
    else:
        # p=int(sys.argv[1])
        src = sys.argv[1] + '/'
        global  dst
        dst = sys.argv[2] + '/'
        if os.path.isdir(dst):  # path参数存在且是一个文件夹
            print("存在文件夹")
        elif not os.path.exists(dst):
            os.makedirs(dst)
            print("不存在文件夹，已创建")

        img_path = get_img_file_name(src)  # 获取src路径下的图像文件的路径
        for i in img_path:
            print(i)
            flag=resize_img(i)
            print("\n\n")
            # 获取xml文件的前缀  比如1234.xml  获取前缀为1234
           # filename_qianzhui = jwkj_get_filePath_fileName_fileExt(i)
            # 将该xml文件解析为符合YOLO标准的txt文件
          #  convert_annotation(image_path_xml=i, dst=dst, filename_qianzhui=filename_qianzhui)
    print("***************************\n")
    print("操作完毕！\n")



def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table


# resize图像 并二值化 存储
def resize_img(img_path):
   # for filename in os.listdir("ima_path"):
    #    print (filename)
    image=Image.open(img_path)
    #image=cv2.imread(img_path)

    if image is None:                       #图片为空
        print("本图像为空:\r"+img_path+"\n")
        os.remove(img_path)                 #删除内容为空的图片
        return
    # INTER_CUBIC - 基于4x4像素邻域的3次插值法  宽×高
    #res=cv2.resize(image,(dst_img_size_width,dst_img_size_height),interpolation=cv2.INTER_CUBIC)
    res_image=image.resize((dst_img_size_width,dst_img_size_height))
   # retval,res_binary=cv2.threshold(res,50,255,cv2.THRESH_BINARY)
    res_image_L=res_image.convert('L')      #转换为灰度图
    #res_image_1=res_image_L.convert('1')    #转换为二值化图
   #  setup a converting table with constant threshold

    table=get_bin_table()                               #获取灰度转二值的映射table
    res_image_1=res_image_L.point(table,'1')            # 变成二值图片:0表示黑色,1表示白色
    bin_clear_img = get_clear_bin_image(res_image_1)    # 处理获得去噪的二值图


    dst_name = os.path.basename(img_path)     #获取文件名 比如text.bmp
    dst_name_full=dst+"\\"+dst_name

    portion = os.path.splitext(dst_name_full)                # 获取除后缀以外的路径
    newname = portion[0] + ".png"                       #更改后缀为png

    bin_clear_img.save(newname)                         #存储二值化图像


#根据噪点的位置信息，消除二值图片的黑点噪声
def remove_noise_pixel(img, noise_point_list):
    """
    根据噪点的位置信息，消除二值图片的黑点噪声
    :type img:Image
    :param img:
    :param noise_point_list:
    :return:
    """
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)

#9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
    :param img: Image
    :param x:
    :param y:
    :return:
    """
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum


# 图像去燥
def get_clear_bin_image(image):
    out=image
    noise_point_list = []  # 通过算法找出噪声点,第一步比较严格,可能会有些误删除的噪点
    for x in range(out.width):
        for y in range(out.height):
            res_9 = sum_9_region(out, x, y)
            if (0 < res_9 < 3) and out.getpixel((x, y)) == 0:  # 找到孤立点
                pos = (x, y)  #
                noise_point_list.append(pos)
    remove_noise_pixel(out, noise_point_list)
    return out

# 遍历file_dir路径下的 所有 图像
def get_img_file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg' or '.png' or '.bmp':
                L.append(os.path.join(root, file))
    return L


main()
