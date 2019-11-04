from helpers.generic_helpers import get_lightweight_component
from models.config_file import ConfigFile

class SupplementalConfig(ConfigFile):
    def __init__(self, output_dir, augmented_site_level_config, execution_id):
        self.lc = get_lightweight_component(augmented_site_level_config, execution_id)

        if self.lc['name'] == 'HTCondor':
            output_file = '{output_dir}/99-problems-condor.conf'.format(output_dir=output_dir)
        elif self.lc['name'] == 'HTCondor-CE':
            output_file = '{output_dir}/99-problems-condor-ce.conf'.format(output_dir=output_dir)
        else:
            output_file = '{output_dir}/99-problems-{component}.conf'.format(output_dir=output_dir, component=self.lc['name'])

        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()

        for prop in self.lc['supplemental_config']:
            if type(prop) == dict:
                self.advanced_category.add_key_value(*list(prop.items())[0])
            else:
                self.advanced_category.add(prop + '\n')