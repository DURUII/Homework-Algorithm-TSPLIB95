from typing import List, Dict
import os
import numpy as np
import math

from matplotlib import pyplot as plt
import scienceplots

plt.style.use(["science"])


class TSPParser:
    """
    将.tsp文件解析为python-dict，
    记录状态（邻接矩阵、最优解等）

    静态调用：
    TSPParser(filename=file_name, plot_tsp=True)
    print(TSPParser.tsp_cities_dict)
    """

    name: str = None
    dimension: int = 0
    should_plot: bool = False
    # .tsp
    tsp_cities_dict: Dict = {}
    tsp_distance_matrix: np.array = None
    my_cities_tour: List = None
    my_tour_length: int = 0
    # .opt
    opt_cities_tour: List = None
    opt_tour_length: int = 0

    @classmethod
    def __init__(cls, name: str, plot_tsp: bool = True) -> None:
        # 静态成员
        cls.name = name
        cls.dimension = 0
        cls.should_plot = plot_tsp
        cls.tsp_cities_dict = {}
        cls.tsp_distance_matrix: np.array = None
        cls.opt_cities_tour = []
        cls.opt_tour_length: int = 0

        # 读取.tsp文件，维护邻接矩阵
        cls.load_tsp_file()
        # 读取.opt.tour文件，计算最优解
        cls.load_opt_file()
        # 数据可视化
        cls.plot()

    @classmethod
    def load_tsp_file(cls):
        # .tsp
        tsp_filename = f"tsplib_benchmark/{cls.name}.tsp"
        assert os.path.exists(tsp_filename)
        # print(tsp_filename)

        # 逐行读取
        with open(tsp_filename) as fin:
            tsp_file_contents = [line.strip() for line in fin.readlines()]

        # DIMENSION 城市数量
        for record in tsp_file_contents:
            if record.startswith("DIMENSION"):
                parts = record.split(":")
                cls.dimension = int(parts[1])
                break
        cls.tsp_distance_matrix = np.zeros((cls.dimension + 1, cls.dimension + 1))

        # NODE_COORD_SECTION 城市坐标
        zero_index = tsp_file_contents.index("NODE_COORD_SECTION") + 1
        for index in range(zero_index, zero_index + cls.dimension):
            # 编号、横坐标、纵坐标
            # city_coords_parts = re.findall(r"[+-]?\d+(?:\.\d+)?", tsp_file_contents[index].strip())
            city_coords_parts = tsp_file_contents[index].strip().split()

            # tsp_cities_dict[__index__] = (x, y)
            cls.tsp_cities_dict[int(city_coords_parts[0])] = (
                float(city_coords_parts[1]),
                float(city_coords_parts[2])
            )

        # DISTANCE MATRIX 邻接矩阵
        for i in range(1, cls.dimension + 1):
            for j in range(1, i + 1):
                x1, y1 = cls.tsp_cities_dict[i]
                x2, y2 = cls.tsp_cities_dict[j]
                # EUC_2D: 用勾股定理算出两点（城市）间距离后，四舍五入取整
                cls.tsp_distance_matrix[i][j] = round(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))
                cls.tsp_distance_matrix[j][i] = cls.tsp_distance_matrix[i][j]

    @classmethod
    def load_opt_file(cls):
        # .opt
        opt_filename = f"tsplib_benchmark/{cls.name}.opt.tour"
        if os.path.exists(opt_filename):

            # 逐行读取
            with open(opt_filename) as fin:
                opt_file_contents = [line.strip() for line in fin.readlines()]

                # TOUR_SECTION 最优解路径
                zero_index = opt_file_contents.index("TOUR_SECTION") + 1

                counter = 0
                journey = 0
                for index in range(zero_index, len(opt_file_contents)):
                    # rd100.opt.tour
                    if counter >= cls.dimension:
                        break

                    for city in opt_file_contents[index].strip().split():
                        # 编号
                        cls.opt_cities_tour.append(int(city))
                        counter += 1
                        if counter > 1:
                            journey += cls.tsp_distance_matrix[cls.opt_cities_tour[counter - 1]][
                                cls.opt_cities_tour[counter - 2]]

                journey += cls.tsp_distance_matrix[cls.opt_cities_tour[-1]][cls.opt_cities_tour[0]]
                cls.opt_tour_length = journey
                # print(f"{cls.name} -> {cls.opt_tour_length}")

    @classmethod
    def set_a_tour(cls, tour: List[int], cost: int):
        cls.my_cities_tour = tour
        cls.my_tour_length = cost

    @classmethod
    def plot(cls):
        if cls.should_plot:
            plt.clf()
            nums_of_axes = (1 if cls.opt_cities_tour else 0) + (1 if cls.my_cities_tour else 0)

            if nums_of_axes == 0:
                fig, ax = plt.subplots(layout='constrained', dpi=500)
                plt.scatter(*zip(*cls.tsp_cities_dict.values()), s=2.5, zorder=1)
                ax.set_title(f"{cls.name}")
                # plt.savefig(f"tsplib_benchmark/{cls.name}.pdf")

            elif nums_of_axes == 1:
                fig, ax = plt.subplots(layout='constrained', dpi=500)
                if cls.opt_cities_tour:
                    x_data, y_data = [], []
                    for i in range(cls.dimension):
                        x, y = cls.tsp_cities_dict[cls.opt_cities_tour[i]]
                        x_data.append(x)
                        y_data.append(y)
                    x_data.append(x_data[0])
                    y_data.append(y_data[0])
                    ax.plot(x_data, y_data, marker='o', linestyle='--', linewidth=0.75, markersize=2)
                    ax.set_title(f"{cls.name}'s optimal tour")
                else:
                    x_data, y_data = [], []
                    for i in range(cls.dimension):
                        x, y = cls.tsp_cities_dict[cls.my_cities_tour[i]]
                        x_data.append(x)
                        y_data.append(y)

                    x_data.append(x_data[0])
                    y_data.append(y_data[0])
                    ax.plot(x_data, y_data, color="red", marker='o', linestyle=':', linewidth=0.75, markersize=2)
                    # ax.set_title(f"{cls.name}'s optimal tour")
                    # plt.savefig(f"tsplib_benchmark/{cls.name}.opt.tour.pdf")

            else:
                fig, axes = plt.subplots(2, 1, figsize=(7.5, 12), layout='constrained', dpi=500)
                ax = axes[0]
                x_data, y_data = [], []
                for i in range(cls.dimension):
                    x, y = cls.tsp_cities_dict[cls.opt_cities_tour[i]]
                    x_data.append(x)
                    y_data.append(y)
                x_data.append(x_data[0])
                y_data.append(y_data[0])
                ax.plot(x_data, y_data, color="C1", marker='o', linestyle='--', linewidth=1.5, markersize=4)
                ax.set_title(f"{cls.name}'s optimal tour - {cls.opt_tour_length}")

                ax = axes[1]
                x_data, y_data = [], []
                for i in range(cls.dimension):
                    x, y = cls.tsp_cities_dict[cls.my_cities_tour[i]]
                    x_data.append(x)
                    y_data.append(y)

                x_data.append(x_data[0])
                y_data.append(y_data[0])
                ax.plot(x_data, y_data, color="C2", marker='o', linestyle='--', linewidth=1.5, markersize=4)
                ax.set_title(f"{cls.name}'s approximate tour - {cls.my_tour_length}")
                plt.savefig(f"{cls.name}-contrast.pdf")

            plt.show()
