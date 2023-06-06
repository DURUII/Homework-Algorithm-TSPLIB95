import re
from typing import List, Dict
import os

from matplotlib import pyplot as plt
import scienceplots

plt.style.use(["science"])


class TSPParser:
    """
    将.tsp文件解析为python-dict

    静态调用：
    TSPParser(filename=file_name, plot_tsp=True)
    print(TSPParser.tsp_cities_dict)
    """

    name: str = None
    dimension: int = 0
    should_plot: bool = False
    # .tsp
    tsp_cities_dict: Dict = {}
    # .opt
    opt_cities_tour: List = []

    @classmethod
    def __init__(cls, name: str, plot_tsp: bool = True) -> None:
        # 静态成员
        cls.name = name
        cls.dimension = 0
        cls.should_plot = plot_tsp
        cls.tsp_cities_dict = {}
        cls.opt_cities_tour = []

        # 读取.tsp文件
        cls.load_tsp_file()
        # 读取.opt.tour文件
        cls.load_opt_file()
        # 数据可视化
        cls.plot()

    @classmethod
    def load_tsp_file(cls):
        # .tsp
        tsp_filename = f"tsplib_benchmark/{cls.name}.tsp"
        assert os.path.exists(tsp_filename)
        print(tsp_filename)

        # 逐行读取
        with open(tsp_filename) as fin:
            tsp_file_contents = [line.strip() for line in fin.readlines()]

            # DIMENSION 城市数量
            for record in tsp_file_contents:
                if record.startswith("DIMENSION"):
                    parts = record.split(":")
                    cls.dimension = int(parts[1])
                    break

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
                for index in range(zero_index, len(opt_file_contents)):
                    # rd100.opt.tour
                    if counter >= cls.dimension:
                        break

                    for city in opt_file_contents[index].strip().split():
                        # 编号
                        cls.opt_cities_tour.append(int(city))
                        counter += 1

    @classmethod
    def plot(cls):
        if cls.should_plot:
            plt.clf()
            fig, ax = plt.subplots(layout='constrained', dpi=500)

            if cls.opt_cities_tour:
                x_data, y_data = [], []
                for i in range(cls.dimension):
                    x, y = cls.tsp_cities_dict[cls.opt_cities_tour[i]]
                    x_data.append(x)
                    y_data.append(y)
                x_data.append(x_data[0])
                y_data.append(y_data[0])
                ax.plot(x_data, y_data, marker='o', linestyle='--', linewidth=0.75, markersize=2.5)
                ax.set_title(f"{cls.name}'s optimal tour")
                plt.savefig(f"tsplib_benchmark/{cls.name}.opt.tour.pdf")
            else:
                plt.scatter(*zip(*cls.tsp_cities_dict.values()), s=2.5, zorder=1)
                ax.set_title(f"{cls.name}")
                plt.savefig(f"tsplib_benchmark/{cls.name}.pdf")

            plt.show()
