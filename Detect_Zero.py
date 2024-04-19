from Zero_HM import *
import numpy as np
from matplotlib import pyplot as plt

'''反置乱水印'''


def Arnold_Decrypt(image):
    shuffle_times, a, b = 10, 1, 1
    decode_image = np.zeros(shape=image.shape)
    h, w = image.shape[0], image.shape[1]
    N = h
    for time in range(shuffle_times):
        for ori_x in range(h):
            for ori_y in range(w):
                # 按照公式坐标变换
                new_x = ((a * b + 1) * ori_x + (-b) * ori_y) % N
                new_y = ((-a) * ori_x + ori_y) % N
                decode_image[new_x, new_y] = image[ori_x, ori_y]
    return decode_image


def Construction(XLst, feature_num, List_Zero):
    List_Fea = len(List_Zero) * [0]
    # 投票机制构造特征矩阵
    for i in range(0, feature_num):
        for j in range(i + 1, feature_num):
            Ni = len(XLst[i])
            Nj = len(XLst[j])
            ni = Ni % 2
            nj = Nj % 2
            index = (Ni * Nj) % len(List_Zero)  # 水印同步
            if ni == nj:
                List_Fea[index] += 1
            else:
                List_Fea[index] += -1
    for p in range(0, len(List_Fea)):
        if List_Fea[p] > 0:
            List_Fea[p] = 255
        else:
            List_Fea[p] = 0
    return List_Fea


def XOR2(List_Fea, List_Zero):
    Lst_WaterMark = len(List_Zero) * [0]
    for m in range(0, len(List_Zero)):
        if List_Fea[m] == List_Zero[m]:
            Lst_WaterMark[m] = 0
        else:
            Lst_WaterMark[m] = 255
    return Lst_WaterMark


# NC值
def NC(ori_img, decode_img):
    h, w = ori_img.shape
    S = 0
    for i in range(0, h):
        for j in range(0, w):
            if ori_img[i][j] == decode_img[i][j]:
                S += 1
            else:
                S += 0
    nc = S / (h * w)
    return nc


if __name__ == '__main__':
    # 调用函数
    xodr_file =  r"E:\High precision map\Gomentum.xodr"
    all_soffset_lists = swap_widths_in_lanesections(xodr_file)
    road_num = len(all_soffset_lists)
    img = cv2.imread(r"E:\Data_AA.jpg", 0)  # 读取零水印图像
    img_0 = cv2.imread(r"E:\watermark.png", 0)  # 读取水印图像
    img_deal = Watermark_deal(img)  # 水印图像处理（0，255）
    img_or = Watermark_deal(img_0)  # 水印图像处理（0，255）（原始版权信息）
    List_Zero = img_deal.flatten()  # 降维
    List_Fea = Construction(all_soffset_lists, road_num, List_Zero)
    Lst_WaterMark = XOR2(List_Fea, List_Zero)
    Re_mark = np.array(Lst_WaterMark).reshape(int(math.sqrt(len(List_Zero))), int(math.sqrt(len(List_Zero))))
    Decode_image = Arnold_Decrypt(Re_mark)  # 反置乱后水印
    # 控制次数
    # for i in range(0, 9):
    #     Decode_image = Arnold_Decrypt(Decode_image)  # arnold_img置乱后水印
    nc = NC(img_or,  Decode_image)
    print(nc)
    # 显示反置乱水印
    plt.subplot(222)
    plt.imshow(Decode_image, 'gray')
    plt.title("Decode_image")
    cv2.imwrite("Decode_image.jpg", Decode_image)

    plt.subplot(221)
    plt.imshow(img_or, 'gray')
    plt.title("ori_or")
    plt.show()
