from models.config_file import ConfigFile
from helpers.generic_helpers import get_all_linux_users_as_list


class SupportedVOUsers(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        supported_vos = " ".join(get_all_linux_users_as_list(self.augmented_site_level_config, self.lightweight_component))
        self.advanced_category.add_key_value('SUPPORTED_VO_USERS', supported_vos)
