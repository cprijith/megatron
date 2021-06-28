
class MetadataUtils:
    def create_db_backend(self, config):
        if 'type' in config and config['type'] == 'mysql':
            import mysql.connector
            self.backend = mysql.connector.connect(
                host=config['mysql_host'],
                user=config['mysql_user'],
                password=config['mysql_password'],
                db=config['mysql_db'],
                port=config['mysql_port'])
        else:
            raise NotImplemented('unknown db type: "{}"'.format(config['type'] if 'type' in config else ''))

    def log_metadata_to_db(self, transformer_id, transformer_state, message):
        """insert_sql = ' insert into <table> ... ';
        self.backend.cursor().execute()
        self.backend.commit()"""
        pass





