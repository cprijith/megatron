from commons.coreutils import get_logger
import csv

from transformers.sample_client1 import *
import ioresource.spark_resource as spark_resource


class AbstractRowProcessor:
    def __init__(self):
        self.logger = get_logger(AbstractRowProcessor.__name__)

    def _process(self, row, validator):
        pre_validate_meta = validator.pre_validate(row)
        self.logger.debug(pre_validate_meta)
        if pre_validate_meta.is_good_to_process:
            processed_row = self.process_row(row)
            post_validate_meta = validator.post_validate(row, processed_row)
            self.logger.debug(post_validate_meta)
            return processed_row

    def process_row(self, row):
        pass


class AbstractRowValidator:
    def pre_validate(self, row):
        pass

    def post_validate(self, row, processed_row):
        pass


class AbstractDataValidator:
    def pre_validate(self, io_manager):
        pass

    def post_validate(self, io_manager):
        pass


class InputDataTransformer:
    """
    Transformer represents end to end process of reading, processing, format convertions and writing

    This class initiates several sub components that fulfills each of such processing stages, and
    orchestrates the execution of the components. Some of the tasks that are centralized or needed to be delegated
    to common utils may be handled through transformer.
    """

    def __init__(self, file_path, file_format, field_separator, output_path, output_field_separator, validator, tenant):
        self.input_file_path = file_path,
        self.input_file_format = file_format,
        self.input_field_separator = field_separator,
        self.output_path = output_path,
        self.output_field_separator = output_field_separator,
        self.row_validator = validator,
        self.logger = get_logger(InputDataTransformer.__name__)

        self._init_components(self, tenant)

    def _init_components(self, tenant):
        if tenant == 'client1':
            self.row_processor = Client1RowProcessor()
            self.row_validator = Client1RowValidator()
            self.data_validator = Client1DataValidator()
            self.io_manager = spark_resource.IOManager()


    def transform(self):
        with self.io_manager as io:
            processed = io.map(lambda line: self.row_processor.process(line, self.row_validator))
            io.write(processed)
            self.data_validator.post_validate(io)

    def shutdown(self):
        pass
