from helpers.generic_helpers import get_lightweight_component
from models.config_file import ConfigFile


class SupplementalConfig(ConfigFile):
    def __init__(self, output_dir, augmented_site_level_config, execution_id, component):
        self.component_props = get_lightweight_component(augmented_site_level_config, execution_id)['supplemental_config'][component]

        with open('{output_dir}/supplemental_mapfile'.format(output_dir=output_dir), 'a') as mapfile:
            if component == 'htcondor':
                output_file = '{output_dir}/99_problems_condor.conf'.format(output_dir=output_dir)
                print('99_problems_condor.conf' + ':/etc/condor/config.d/99_problems.conf', file=mapfile)
            elif component == 'htcondor-ce':
                output_file = '{output_dir}/99_problems_condor_ce.conf'.format(output_dir=output_dir)
                print('99_problems_condor_ce.conf' + ':/etc/condor-ce/config.d/99_problems.conf', file=mapfile)
            else:
                output_file = '{output_dir}/{component}'.format(output_dir=output_dir, component=component.replace('/', '_'))
                print(component.replace('/', '_') + ':' + component, file=mapfile)

        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()

        for prop in self.component_props:
            if type(prop) == dict:
                self.advanced_category.add_key_value(*list(prop.items())[0])
            else:
                self.advanced_category.add(prop + '\n')