from models.config_file import ConfigFile


class ConfiguredAttributes60(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config_file, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config_file, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()
        self.static_category.add_key_value("STATISTICS_TO_PUBLISH", "SCHEDD:2")
        self.static_category.add_key_value("SCHEDD_COLLECT_STATS_BY_VO", "x509userproxyvoname")

    def add_lightweight_component_queried_parameters(self):
        super().add_lightweight_component_queried_parameters()
        self.lightweight_component_queried_category.add_key_value_query("PER_JOB_HISTORY_DIR",
                                                                        "$.config.per_job_history_dir")
        self.lightweight_component_queried_category.add_key_value_query("GSS_ASSIST_GRIDMAP_CACHE_EXPIRATION",
                                                                        "$.config.gss_assist_gridmap_cache_expiration")

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        batch_execution_id = None
        for component in self.augmented_site_level_config['lightweight_components']:
            if component['name'] == "HTCondor-Batch":
                batch_execution_id = component['execution_id']
        if batch_execution_id is None:
            raise Exception("Could not find HTCondor-Batch in the lightweight components section of the "
                            "site level configuration file. It is required to configure the HTCondor-CE's SCHEDD2 to "
                            "forward incoming jobs to the batch system. Please specify the repository "
                            "https://github.com/WLCG-Lightweight-Sites/simple_htcondor_batch"
                            " in the lightweight components section. Merci Beaucoup!")
        dns_section = self.augmented_site_level_config['dns']
        dns = None
        for dns_info in dns_section:
            if dns_info['execution_id'] == batch_execution_id:
                dns = dns_info
                break

        if dns is None:
            raise Exception("Cannot find lightweight element for HTCondor-Batch in dns section of "
                            "augmented site level config file")
        fqdn = dns['container_fqdn']
        internal_ip = dns['container_ip']
        self.advanced_category.add_key_value("JOB_ROUTER_SCHEDD2_NAME", fqdn)
        self.advanced_category.add_key_value("JOB_ROUTER_SCHEDD2_POOL", "{internal_ip}:9618".format(
                                                                                internal_ip=internal_ip
                                                                            ))
