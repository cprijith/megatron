import csv
class IOManager:
    def __init__(self, input, output, output_fieldnames, input_method='r', output_method='w'):
        self.input_reader = csv.DictReader(open(input, input_method), dialect="excel")
        self.output_writer = csv.DictWriter(open(output, output_method), fieldnames=output_fieldnames, encoding='utf-8',
                                            delimiter="\t", extrasaction='ignore',
                                            quotechar=None, quoting=csv.QUOTE_NONE, escapechar="\\")
        self.io_stat = {}

    def __iter__(self):
        self._reset_stats()
        return self

    def __next__(self):
        self.io_stat['LINES_READ'] += 1
        line = next(self.input_reader)
        self.io_stat['SIZE_READ'] += len(line)
        return line

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.input_reader:
            self.input_reader.close()
        if self.output_writer:
            self.output_writer.close()

    def _reset_stats(self):
        self.io_stat['LINES_READ'] = 0
        self.io_stat['SIZE_READ'] = 0

    def write(self, processed_row):
        self.output_writer.writerow(processed_row)