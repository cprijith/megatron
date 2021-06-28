class IOManager:
    def __init__(self, rdd, output_dir_path):
        self.input_rdd = rdd
        self.output_dir_path = output_dir_path
        self.io_stat = {}

    def __enter__(self):
        return self.input_rdd

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, output_rdd):
        output_rdd.saveAsTextFile(self.output_dir_path)
