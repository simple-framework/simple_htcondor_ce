from models.config_file import ConfigFile
from helpers.generic_helpers import *


class CondorMapfile(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config_file, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config_file, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()
        self.static_category.add("GSI (.*) simple\n"
                                 "CLAIMTOBE .* anonymous@claimtobe\n"
                                 "FS (.*) \\1"
                                 )

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        supported_vos = get_supported_vos(self.augmented_site_level_config)
        fqans = [fqan['voms_fqan'] for vo in supported_vos for fqan in
                 get_fqan_for_vo(vo, self.augmented_site_level_config, self.lightweight_component)]
        for fqan in fqans:
            user = get_users_for_fqan(fqan, self.augmented_site_level_config, self.lightweight_component)[0]
            final_fqan = fqan.replace("/", "\\/")
            # GSI "<DISTINGUISHED NAME>,<VOMS FQAN 1>,<VOMS FQAN 2>,...,<VOMSFQAN N>" <USERNAME>@users.htcondor.org
            # GSI ".*,\/GLOW\/Role=htpc.*" glow@users.htcondor.org
            self.advanced_category.add(f"GSI \".*,{final_fqan}\\/.*\" {user}\n")
