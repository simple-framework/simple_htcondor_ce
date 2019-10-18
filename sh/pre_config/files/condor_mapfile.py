from models.config_file import ConfigFile


class CondorMapfile(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config_file, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config_file, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()
        self.static_category.add("GSI \"(/CN=[-.A-Za-z0-9/= ]+\" \\1@unmapped.htcondor.org\n"
                                 "GSI (.*) simple\n"
                                 "CLAIMTOBE .* anonymous@claimtobe\n"
                                 "FS (.*) \\1"
                                 )
