from models.config_file import ConfigFile


class SupportedVOUsers(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()

        supported_vos = ','.join(['user_' + vo['name'] for vo in self.augmented_site_level_config['supported_virtual_organizations']])
        self.advanced_category.add_key_value('SUPPORTED_VO_USERS', supported_vos)