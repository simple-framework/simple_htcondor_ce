from generic_helpers import get_dns_info
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
        batch_execution_id  = self.lightweight_component['config']['condor_host_execution_id']
        batch_dns = get_dns_info(self.augmented_site_level_config, batch_execution_id)
        dns = get_dns_info(self.augmented_site_level_config, self.lightweight_component['execution_id'])
        fqdn = dns['container_fqdn']
        internal_ip = batch_dns['container_ip']
        self.advanced_category.add_key_value("JOB_ROUTER_SCHEDD2_NAME", fqdn)
        self.advanced_category.add_key_value("JOB_ROUTER_SCHEDD2_POOL", "{internal_ip}:9618".format(
                                                                                internal_ip=internal_ip
                                                                            ))
