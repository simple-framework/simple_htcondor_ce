from models.config_file import ConfigFile
from helpers.generic_helpers import get_all_linux_users_as_list


class SupportedVOUsers(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        users = []
        super().add_advanced_parameters()
        if "user_accounts" in self.lightweight_component['config']:
            users.extend(self.lightweight_component['config']['user_accounts'])
        supported_vos = get_all_linux_users_as_list(self.augmented_site_level_config, self.lightweight_component)
        users.extend(supported_vos)
        self.advanced_category.add_key_value('SUPPORTED_VO_USERS', " ".join(users))
