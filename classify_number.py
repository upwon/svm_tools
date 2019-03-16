
import glob
import sys
import os
import cv2
from PIL import Image


dst_img_size_width=18          #resize 图像的宽度
dst_img_size_height=28         #resize 图像的高度


def main():
    if len(sys.argv) < 2:
        print(
            '输入参数不足，输入格式为：\n   python image_resize.py  [source folder name] [deststion folder name]')
        print("********结束程序*********\n")
        exit()
    else:
        # p=int(sys.argv[1])
        src = sys.argv[1] + '/'
        dst = sys.argv[2] + '/'
        if os.path.isdir(dst):  # path参数存在且是一个文件夹
            print("存在文件夹")
        elif not os.path.exists(dst):
            os.makedirs(dst)
            print("不存在文件夹，已创建")




main()
