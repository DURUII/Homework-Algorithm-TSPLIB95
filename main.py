from tsplib_parser.tsp_file_parser import TSPParser

if __name__ == '__main__':
    file_name = "tsplib_benchmark/a280.tsp"
    TSPParser(filename=file_name, plot_tsp=True)
