from models.config_file import ConfigFile


class VOMSConfig(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id, server_data):
        self.server = server_data
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        self.advanced_category.add(f"{self.server['dn']}\n")
        self.advanced_category.add(f"{self.server['ca_dn']}\n")
