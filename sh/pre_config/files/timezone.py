from models.config_file import ConfigFile


class TimeZone(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        timezone = ""
        try:
            timezone = self.augmented_site_level_config['site']['timezone']
        except Exception:
            self.advanced_category.add("")
        self.advanced_category.add("{timezone}".format(timezone=timezone))
