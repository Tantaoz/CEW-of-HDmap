import xml.etree.ElementTree as ET


def swap_widths_in_lanesections(xodr_file, output_file):
    # 解析Xodr文件
    tree = ET.parse(xodr_file)
    root = tree.getroot()

    # 找到包含laneSection信息的所有laneSection元素
    lanesection_elements = root.findall(".//laneSection")

    # 遍历laneSection元素
    for lanesection_element in lanesection_elements:
        # 找到laneSection下的left和right元素
        left_element = lanesection_element.find(".//left")
        right_element = lanesection_element.find(".//right")

        # 处理left元素的宽度信息
        if left_element is not None:
            process_widths(left_element)

        # 处理right元素的宽度信息
        if right_element is not None:
            process_widths(right_element)

    # 将修改后的XML树写入新的文件
    tree.write(output_file)


def process_widths(element):
    e = [[0, 1, 3, 2], [0, 2, 1, 3], [0, 2, 3, 1], [0, 3, 1, 2], [0, 3, 2, 1],
         [1, 0, 2, 3], [1, 0, 3, 2], [1, 2, 0, 3], [1, 2, 3, 0], [1, 3, 0, 2], [1, 3, 2, 0],
         [2, 0, 1, 3], [2, 0, 3, 1], [2, 1, 0, 3], [2, 1, 3, 0], [2, 3, 0, 1], [2, 3, 1, 0],
         [3, 0, 1, 2], [3, 0, 2, 1], [3, 1, 0, 2], [3, 1, 2, 0], [3, 2, 0, 1], [3, 2, 1, 0]]  # 碱基对互补编码
    # 找到element元素中的lane元素
    lane_elements = element.findall(".//lane")

    # 遍历lane元素
    for lane_element in lane_elements:
        # 找到lane元素中的width信息
        width_elements = lane_element.findall(".//width")

        # 创建一个新的一维列表
        S = []

        # 使用S的值替换width元素的属性a、b、c、d的值
        for width_element in width_elements:
            id = width_element.get("sOffset")
            a = width_element.get("a")
            b = width_element.get("b")
            c = width_element.get("c")
            d = width_element.get("d")
            S=[a,b,c,d]
            index = int(float(id) * 1e4) % 23
            X = e[index]
            Q = [S[i] for i in X]

            width_element.set("a", Q[0])
            width_element.set("b", Q[1])
            width_element.set("c", Q[2])
            width_element.set("d", Q[3])


if __name__ == "__main__":
    # 调用函数
    xodr_file = r"E:\High precision map\SanFrancisco.xodr"
    output_file = r"E:\EnMap\SanFranciscoA.xodr"
    swap_widths_in_lanesections(xodr_file, output_file)
    print('finish')
