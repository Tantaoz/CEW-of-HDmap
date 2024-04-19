import xml.etree.ElementTree as ET

def swap_elevation_profiles(xodr_file, output_file):
    # 解析Xodr文件
    tree = ET.parse(xodr_file)
    root = tree.getroot()

    # 找到包含elevationProfile信息的所有elevationProfile元素
    elevation_profile_elements1 = root.findall(".//elevationProfile")

    # 遍历elevationProfile元素
    for elevation_profile_element1 in elevation_profile_elements1:
        # 处理elevationProfile元素中的elevation信息
        process_elevations(elevation_profile_element1)

    # 找到包含lateralProfile信息的所有lateralProfile元素
    elevation_profile_elements2 = root.findall(".//lateralProfile")

    # 遍历lateralProfile元素
    for elevation_profile_element2 in elevation_profile_elements2:
         # 处理elevationProfile元素中的elevation信息
        process_superelevation(elevation_profile_element2)
    # 将修改后的XML树写入新的文件
    tree.write(output_file)


def process_elevations(element):
    e = [[0, 1, 3, 2], [0, 2, 1, 3], [0, 2, 3, 1], [0, 3, 1, 2], [0, 3, 2, 1],
         [1, 0, 2, 3], [1, 0, 3, 2], [1, 2, 0, 3], [1, 2, 3, 0], [1, 3, 0, 2], [1, 3, 2, 0],
         [2, 0, 1, 3], [2, 0, 3, 1], [2, 1, 0, 3], [2, 1, 3, 0], [2, 3, 0, 1], [2, 3, 1, 0],
         [3, 0, 1, 2], [3, 0, 2, 1], [3, 1, 0, 2], [3, 1, 2, 0], [3, 2, 0, 1], [3, 2, 1, 0]]  # 碱基对互补编码

    # 找到element元素中的elevation元素
    elevation_elements = element.findall(".//elevation")

    # 遍历elevation元素
    for elevation_element in elevation_elements:
        s = elevation_element.get("s")
        a = elevation_element.get("a")
        b = elevation_element.get("b")
        c = elevation_element.get("c")
        d = elevation_element.get("d")

        # 进行相同的操作，可以根据需求进行调整
        index = int(float(s) * 1e4) % 23
        X = e[index]
        S = [a, b, c, d]
        Q = [S[i] for i in X]

        elevation_element.set("a", Q[0])
        elevation_element.set("b", Q[1])
        elevation_element.set("c", Q[2])
        elevation_element.set("d", Q[3])

def process_superelevation(element):
    e = [[0, 1, 3, 2], [0, 2, 1, 3], [0, 2, 3, 1], [0, 3, 1, 2], [0, 3, 2, 1],
         [1, 0, 2, 3], [1, 0, 3, 2], [1, 2, 0, 3], [1, 2, 3, 0], [1, 3, 0, 2], [1, 3, 2, 0],
         [2, 0, 1, 3], [2, 0, 3, 1], [2, 1, 0, 3], [2, 1, 3, 0], [2, 3, 0, 1], [2, 3, 1, 0],
         [3, 0, 1, 2], [3, 0, 2, 1], [3, 1, 0, 2], [3, 1, 2, 0], [3, 2, 0, 1], [3, 2, 1, 0]]  # 碱基对互补编码

    # 找到element元素中的elevation元素
    elevation_elements = element.findall(".//superelevation")

    # 遍历elevation元素
    for elevation_element in elevation_elements:
        s = elevation_element.get("s")
        a = elevation_element.get("a")
        b = elevation_element.get("b")
        c = elevation_element.get("c")
        d = elevation_element.get("d")

        # 进行相同的操作，可以根据需求进行调整
        index = int(float(s) * 1e4) % 23
        X = e[index]
        S = [a, b, c, d]
        Q = [S[i] for i in X]

        elevation_element.set("a", Q[0])
        elevation_element.set("b", Q[1])
        elevation_element.set("c", Q[2])
        elevation_element.set("d", Q[3])



if __name__ == "__main__":
    # 调用函数
    xodr_file = r"E:\High precision map\SanFrancisco.xodr"
    output_file = r"E:\SanFrancisco-Downtown(61).xodr"
    swap_elevation_profiles(xodr_file, output_file)
    print('finish')
