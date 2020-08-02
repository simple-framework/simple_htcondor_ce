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
        output = []
        if "condor_mapfile_entries" in self.lightweight_component['config']:
            self.advanced_category.add("\n".join(self.lightweight_component['config']['condor_mapfile_entries']))
            self.advanced_category.add("\n")
        supported_vos = get_supported_vos(self.augmented_site_level_config)
        fqans = [fqan['voms_fqan'] for vo in supported_vos for fqan in
                 get_fqan_for_vo(vo, self.augmented_site_level_config, self.lightweight_component)]
        for fqan in fqans:
            user = get_primary_user_for_fqan(fqan, self.augmented_site_level_config, self.lightweight_component)
            # GSI "<DISTINGUISHED NAME>,<VOMS FQAN 1>,<VOMS FQAN 2>,...,<VOMSFQAN N>" <USERNAME>@users.htcondor.org
            # GSI ".*,/GLOW/Role=htpc.*" glow@users.htcondor.org
            # https://www-auth.cs.wisc.edu/lists/htcondor-users/2020-July/msg00013.shtml
            output.append(f"GSI \".*,{fqan}/.*\" {user}\n")
        output = sorted(output, key=lambda x: len(x), reverse=True)
        self.advanced_category.add("".join(output))
