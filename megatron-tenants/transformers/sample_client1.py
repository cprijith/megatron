
from commons.coreutils import get_logger
from transformers.basic_transformers import *


class Client1RowProcessor(AbstractRowProcessor):
    def __init__(self):
        super(self)
        self.logger = get_logger(Client1RowProcessor.__name__)

    def process_row(self, row):
        return row


class Client1RowValidator(AbstractRowValidator):
    def pre_validate(self, row):
        return len(row) > 0

    def post_validate(self, row):
        pass


class Client1DataValidator(AbstractDataValidator):
    def pre_validate(self, io_manager):
        pass

    def post_validate(self, io_manager):
        pass