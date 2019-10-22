from config_file import ConfigFile
from generic_helpers import get_batch_dns_info


class PCConfig50(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        batch_dns = get_batch_dns_info(self.augmented_site_level_config)
        batch_ip = batch_dns['container_ip']
        allow_write = '.'.join((batch_ip.split('.')[0:-2] + ['*']))
        self.advanced_category.add("Use ROLE: submit\n")
        self.advanced_category.add_key_value("CONDOR_HOST", batch_ip)
        self.advanced_category.add_key_value("ALLOW_WRITE", allow_write)
