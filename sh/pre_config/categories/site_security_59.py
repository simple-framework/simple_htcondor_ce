from helpers.generic_helpers import get_lightweight_component
from models.parameter_category import ParameterCategory


class SiteSecutiryQueried(ParameterCategory):
    def __init__(self, name, augmented_site_level_config, execution_id):
        self.lightweight_component = get_lightweight_component(augmented_site_level_config, execution_id)
        ParameterCategory.__init__(self, name, self.lightweight_component)
        self.add_key_value_query("uid_domain", "$.config.uid_domain")
        self.add_key_value_query("uid_domain_adjadakj", "$.config.uid_domain")
        self.add("This Kob = Is very advanced, Got after 100 calculations\n")
        self.add_key_value("Key", "Value")

def get_categories(augmented_site_level_config, execution_id):
    queried = SiteSecutiryQueried("site_security_queried", augmented_site_level_config, execution_id)
    return queried
