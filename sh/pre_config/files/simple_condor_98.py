from models.config_file import ConfigFile


class SimpleCondor98(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config_file, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config_file, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()
        self.static_category.add_key_value("CONDOR_DEBUG", "D_FULLDEBUG, D_SECURITY:2")
        self.static_category.add_key_value("CCB_HEARTBEAT_INTERVAL", "0")
        # self.static_category.add_key_value("DAEMON_LIST", "MASTER, SHARED_PORT, COLLECTOR, NEGOTIATOR, SCHEDD")
        self.static_category.add_key_value("QUEUE_SUPER_USER_MAY_IMPERSONATE", ".*")
