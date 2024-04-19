import xml.etree.ElementTree as ET
import numpy as np
import math
import cv2
import matplotlib.pyplot as plt

'''水印处理'''


def Watermark_deal(img_deal):
    h, w = img_deal.shape
    for i in range(0, h):
        for j in range(0, w):
            if img_deal[i][j] < 100:
                img_deal[i][j] = 0
            else:
                img_deal[i][j] = 255
    return img_deal


'''二值化图像'''


def Erzhi_watermark(Arnold_img):
    Erzhi_list = [y for x in Arnold_img for y in x]
    # Erzhi_list=Arnold_img.flatten()
    for i in range(0, len(Erzhi_list)):
        if Erzhi_list[i] == 255:
            Erzhi_list[i] = 1
        else:
            Erzhi_list[i] = 0
    return Erzhi_list


'''置乱水印'''


def Arnold_Encrypt(image):
    shuffle_times, a, b = 10, 1, 1
    arnold_image = np.zeros(shape=image.shape)
    h, w = image.shape
    N = h  # 或N=w
    # 3：遍历像素坐标变换
    for time in range(shuffle_times):
        for ori_x in range(h):
            for ori_y in range(w):
                # 按照公式坐标变换
                new_x = (1 * ori_x + b * ori_y) % N
                new_y = (a * ori_x + (a * b + 1) * ori_y) % N
                arnold_image[new_x, new_y] = image[ori_x, ori_y]
    return arnold_image


def swap_widths_in_lanesections(xodr_file):
    # 解析Xodr文件
    tree = ET.parse(xodr_file)
    root = tree.getroot()

    # 创建一个新的一维列表用于存储所有sOffset值的列表
    all_soffset_lists = []

    # 处理elevationProfile元素
    elevation_profile_elements = root.findall(".//elevationProfile")
    for elevation_profile_element in elevation_profile_elements:
        # 找到elevationProfile元素下的elevation信息
        elevation_elements = elevation_profile_element.findall(".//elevation")

        # 创建一个新的一维列表用于存储elevationProfile元素中的s值
        s_list = []

        # 遍历elevation信息并将s值添加到列表
        for elevation_element in elevation_elements:
            s_value = elevation_element.get("s")
            if s_value is not None:
                s_list.append(float(s_value))

        # 将elevationProfile元素中的s值列表添加到all_soffset_lists
        if s_list:
            all_soffset_lists.append(s_list)

    # 处理lateralProfile元素
    lateral_profile_elements = root.findall(".//lateralProfile")
    for lateral_profile_element in lateral_profile_elements:
        # 找到lateralProfile元素下的superelevation信息
        superelevation_elements = lateral_profile_element.findall(".//superelevation")

        # 创建一个新的一维列表用于存储lateralProfile元素中的s值
        s_list = []

        # 遍历superelevation信息并将s值添加到列表
        for superelevation_element in superelevation_elements:
            s_value = superelevation_element.get("s")
            if s_value is not None:
                s_list.append(float(s_value))

        # 将lateralProfile元素中的s值列表添加到all_soffset_lists
        if s_list:
            all_soffset_lists.append(s_list)

    # 找到包含laneSection信息的所有laneSection元素
    lanesection_elements = root.findall(".//laneSection")

    # 遍历laneSection元素
    for lanesection_element in lanesection_elements:
        # 找到laneSection下的left和right元素
        left_element = lanesection_element.find(".//left")
        right_element = lanesection_element.find(".//right")

        # 处理left元素的宽度信息
        if left_element is not None:
            # 找到left元素中的lane元素
            left_lane_elements = left_element.findall(".//lane")

            # 创建一个新的一维列表用于存储left元素中的sOffset值
            left_soffset_list = []

            for lane_element in left_lane_elements:
                # 找到lane元素中的width信息
                left_width_elements = lane_element.findall(".//width")

                # 遍历width信息并将sOffset值添加到列表
                for left_width_element in left_width_elements:
                    s_offset = left_width_element.get("sOffset")
                    if s_offset is not None:
                        left_soffset_list.append(float(s_offset))

            # 将left元素中的sOffset值列表添加到all_soffset_lists
            if left_soffset_list:
                all_soffset_lists.append(left_soffset_list)

        # 处理right元素的宽度信息
        if right_element is not None:
            # 找到right元素中的lane元素
            right_lane_elements = right_element.findall(".//lane")

            # 创建一个新的一维列表用于存储right元素中的sOffset值
            right_soffset_list = []

            for lane_element in right_lane_elements:
                # 找到lane元素中的width信息
                right_width_elements = lane_element.findall(".//width")

                # 遍历width信息并将sOffset值添加到列表
                for right_width_element in right_width_elements:
                    s_offset = right_width_element.get("sOffset")
                    if s_offset is not None:
                        right_soffset_list.append(float(s_offset))

            # 将right元素中的sOffset值列表添加到all_soffset_lists
            if right_soffset_list:
                all_soffset_lists.append(right_soffset_list)

    # 输出所有sOffset值的列表
    return all_soffset_lists


def Construction(Xlist, feature_num, Lst_WaterMark):
    List_Fea = len(Lst_WaterMark) * [0]
    # 投票机制构造
    for i in range(0, feature_num):
        for j in range(i + 1, feature_num):
            Ni = len(Xlist[i])
            Nj = len(Xlist[j])
            ni = Ni % 2
            nj = Nj % 2
            index = (Ni * Nj) % len(Lst_WaterMark)  # 水印同步
            if ni == nj:
                List_Fea[index] += 1
            else:
                List_Fea[index] += -1
    for p in range(0, len(List_Fea)):  # 二值化
        if List_Fea[p] > 0:
            List_Fea[p] = 255
        else:
            List_Fea[p] = 0
    return List_Fea


"""构造零水印图像"""


def XOR(List_Fea, Lst_WaterMark):
    List_Zero = len(Lst_WaterMark) * [0]
    for m in range(0, len(List_Zero)):
        if List_Fea[m] == Lst_WaterMark[m]:
            List_Zero[m] = 0
        else:
            List_Zero[m] = 255
    return List_Zero


if __name__ == "__main__":
    # 调用函数
    xodr_file = r"E:\High precision map\SanFrancisco.xodr"
    all_soffset_lists = swap_widths_in_lanesections(xodr_file)
    road_num=len(all_soffset_lists)
    print(all_soffset_lists[0])
    print(road_num)
    img = cv2.imread(r"E:\4096.png", 0)  # 读取水印图像
    img_deal = Watermark_deal(img)  # 水印图像处理（0，255）
    Arnold_img = Arnold_Encrypt(img_deal)  # 置乱图像
    # 控制次数
    for i in range(0, 11):
        Arnold_img = Arnold_Encrypt(Arnold_img)  # arnold_img置乱后水印
    Lst_WaterMark = Arnold_img.flatten()  # 降维
    List_Fea = Construction(all_soffset_lists, road_num, Lst_WaterMark)
    List_Zero = XOR(List_Fea, Lst_WaterMark)
    Array_Z = np.array(List_Zero).reshape(int(math.sqrt(len(List_Zero))), int(math.sqrt(len(List_Zero))))
    # 存储零水印图像
    plt.subplot()
    plt.imshow(Array_Z, 'gray')
    plt.title("zero_image")
    plt.show()
    cv2.imwrite(r"E:\Data_D1.jpg", Array_Z)
    print('finish')


