from models.parameter_category import ParameterCategory
from helpers.generic_helpers import get_lightweight_component


class CondorMapfileStatic(ParameterCategory):
    def __init__(self, name, augmented_site_level_config, execution_id):
        ParameterCategory.__init__(self, name, augmented_site_level_config)
        self.add_key_value("test", "value")

def get(augmented_site_level_config, execution_id):
    static = CondorMapfileStatic("condor_mapfile_static", augmented_site_level_config, execution_id)
    lightweight_component = get_lightweight_component(augmented_site_level_config, execution_id)
    return static