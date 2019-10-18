from config_file import ConfigFile


class Simple98(ConfigFile):
    def __init__(self,output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_static_parameters(self):
        self.static_category.add_key_value("ALL_DEBUG", "D_FULLDEBUG")
        self.static_category.add_key_value("SEC_CLIENT_AUTHENTICATION_METHODS", "GSI, FS")

    def add_advanced_parameters(self):
        dns_section = self.augmented_site_level_config['dns']
        execution_id = self.lightweight_component['execution_id']
        dns = None
        for dns_info in dns_section:
            if dns_info['execution_id'] == execution_id:
                dns = dns_info
                break
        if dns is None:
            raise Exception("Could not find dns info for current lightweight component in the augmented site"
                            " level config file")
        fqdn = dns['container_fqdn']
        container_ip = dns['container_ip']
        host_ip = dns['host_ip']
        self.advanced_category.add_key_value("TCP_FORWARDING_HOST", host_ip)
        self.advanced_category.add_key_value("ALLOW_ADMINISTRATOR", "{container_ip}, {fqdn}".format(
            container_ip=container_ip, fqdn=fqdn)
        )