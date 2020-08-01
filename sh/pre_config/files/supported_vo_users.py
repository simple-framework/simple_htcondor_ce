from models.config_file import ConfigFile
from helpers.generic_helpers import *


class SupportedVOUsers(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        users = []
        super().add_advanced_parameters()
        if "user_accounts" in self.lightweight_component['config']:
            users.extend(self.lightweight_component['config']['user_accounts'])
        supported_vos = get_supported_vos(self.augmented_site_level_config)
        fqans = [fqan['voms_fqan'] for vo in supported_vos for fqan in
                 get_fqan_for_vo(vo, self.augmented_site_level_config, self.lightweight_component)]

        for fqan in fqans:
            user = get_primary_user_for_fqan(fqan, self.augmented_site_level_config, self.lightweight_component)
            users.append(user)
        self.advanced_category.add_key_value('SUPPORTED_VO_USERS', " ".join(users))
