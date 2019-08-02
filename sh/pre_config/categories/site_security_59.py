from models.config_file import ConfigFile


class SiteSecurity59(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()

    def add_lightweight_component_queried_parameters(self):
        super().add_lightweight_component_queried_parameters()
        self.lightweight_component_queried.add_key_value_query("uid_domain", "$.config.uid_domain")



