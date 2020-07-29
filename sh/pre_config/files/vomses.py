from models.config_file import ConfigFile


class VOMSES(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id, server_data, vo_name):
        self.server = server_data
        self.vo = vo_name
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        self.advanced_category.add(
            f"\"{self.vo}\" \"{self.server['server']}\" \"{self.server['port']}\" \"{self.server['dn']}\" \"{self.vo}\" \"24\"\n")
