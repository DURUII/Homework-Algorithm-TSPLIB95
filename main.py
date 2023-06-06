from tsplib_parser.tsp_file_parser import TSPParser
from rich import print

if __name__ == '__main__':
    # EUC_2D: 用勾股定理算出两点（城市）间距离后，四舍五入取整
    with open("tsplib_benchmark/euc_2d", "r") as fin:
        names = [line.strip() for line in fin.readlines()]
        for name in names:
            TSPParser(name)
    # print(TSPParser.tsp_cities_dict)
