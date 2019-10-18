from config_file import ConfigFile


class PCConfig50(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        batch_dns = self.get_batch_dns_info()
        batch_ip = batch_dns['container_ip']
        batch_subnet = '.'.join((batch_ip.split('.')[0:-2] + ['0', '0']))
        self.advanced_category.add("Use ROLE: Submit\n")
        self.advanced_category.add_key_value("CONDOR_HOST", batch_ip)
        self.advanced_category.add_key_value("ALLOW_WRITE", batch_subnet)
