from helpers.generic_helpers import get_lightweight_component
from models.parameter_category import ParameterCategory


class SiteSecurityCategories:
    def __init__(self, name, augmented_site_level_config, execution_id):
        self.name = name
        self.lightweight_component = get_lightweight_component(augmented_site_level_config, execution_id)
        self.execution_id = execution_id
        self.augmented_site_level_config = augmented_site_level_config

        self.lightweight_component_queried = ParameterCategory("{name}_lightweight_component_queried".format(name=name), self.lightweight_component)
        self.global_queried = ParameterCategory("{name}_global_queried".format(name=name), augmented_site_level_config)
        self.static = ParameterCategory("{name}_static".format(name=name))
        self.advanced = ParameterCategory("{name}_static".format(name=name), augmented_site_level_config)

        self.add_advanced_categories()
        self.add_global_queried_categories()
        self.add_lightweight_component_queried_categories()
        self.add_static_categories()

    def add_lightweight_component_queried_categories(self):
        self.lightweight_component_queried.add_key_value_query("uid_domain", "$.config.uid_domain")

    def add_global_queried_categories(self):
        pass

    def add_static_categories(self):
        pass

    def add_advanced_categories(self):
        pass

    def get_categories(self):
        return [self.lightweight_component_queried, self.static, self.global_queried, self.advanced]

