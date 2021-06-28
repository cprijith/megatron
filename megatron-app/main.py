import argparse
import uuid
from commons.metadata_utils import MetadataUtils
from transformers.basic_transformers import InputDataTransformer


def get_tenants_configs(config_root):
    pass


def get_global_config():
    pass


def preserve_log():
    pass


def run(args):
    global_configs = get_global_config()
    tenant_configs = get_tenants_configs(args.config_root)
    metadata_utils = MetadataUtils()
    metadata_utils.create_db_backend(global_configs)

    for tenant_config in tenant_configs:
        tenant_transformer = InputDataTransformer(file_path=tenant_config.file_path,
                                                  file_format=tenant_config.file_format,
                                                  field_separator=tenant_config.field_separator,
                                                  output_path=tenant_config.output_path,
                                                  output_file_separator=global_configs.output_format,
                                                  validator=global_configs.validator,
                                                  logger_config=global_configs.logger,
                                                  meta_logger=global_configs.meta_logger)
        try:
            transformer_meta_id = uuid.uuid1()
            metadata_utils.log_metadata_to_db(transformer_meta_id,
                                              'PROCESSING',
                                              'file {}'.format(tenant_config.file_path)
                                              )
            tenant_transformer.transform()
            metadata_utils.log_metadata_to_db(transformer_meta_id,
                                              'PROCESSING COMPLETED',
                                              'file {}'.format(tenant_config.file_path)
                                              )
        finally:
            # upload log to a persistent storage
            metadata_utils.log_metadata_to_db(transformer_meta_id,
                                              'ARCHIVE LOGS',
                                              'file {}'.format(tenant_config.file_path)
                                              )
            preserve_log()
            # upload log to a persistent storage
            metadata_utils.log_metadata_to_db(transformer_meta_id,
                                              'ARCHIVE LOGS COMPLETED',
                                              'file {}'.format(tenant_config.file_path)
                                              )
            tenant_transformer.shutdown()
            metadata_utils.log_metadata_to_db(transformer_meta_id,
                                              'TRANSFORMER DONE',
                                              'file {}'.format(tenant_config.file_path)
                                              )


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--log_file_path', nargs='?', type=str, help='path to log file including name',
                            required=True)
    arg_parser.add_argument('--source_dir_root', nargs='?', type=str, help='path to source root', required=True)
    arg_parser.add_argument('--config_root', nargs='?', type=str, help='path to config root', required=True)
    arg_parser.add_argument('--output_file_path', nargs='?', type=str, help='full path of the output file',
                            required=True)
    return arg_parser.parse_args()


def main():
    args = parse_args()
    run(args)


if __name__ == '__main__':
    main()
