from models.config_file import ConfigFile


class SiteSecurity59(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_static_parameters(self):
        super().add_static_parameters()
        self.static_category.add_key_value("FRIENDLY_DAEMONS",
                                           '$(FRIENDLY_DAEMONS), $(FULL_HOSTNAME)@$(UID_DOMAIN)/$(FULL_HOSTNAME), '
                                           '*@$(UID_DOMAIN), condor@$(UID_DOMAIN)/$(FULL_HOSTNAME), condor@child/$('
                                           'FULL_HOSTNAME)')
        self.static_category.add_key_value("USERS", "$(USERS), *@$(UID_DOMAIN)")
        self.static_category.add_key_value("ALLOW_DAEMON", "$(ALLOW_DAEMON), $(FRIENDLY_DAEMONS)")
        self.static_category.add_key_value("SCHEDD.ALLOW_WRITE",
                                           '$(SCHEDD.ALLOW_WRITE), $(FULL_HOSTNAME)@$(UID_DOMAIN)/$(FULL_HOSTNAME), '
                                           '*@$(UID_DOMAIN)')
        self.static_category.add_key_value("COLLECTOR.ALLOW_ADVERTISE_MASTER", "$(COLLECTOR.ALLOW_ADVERTISE_MASTER), "
                                                                               "$(FRIENDLY_DAEMONS), *@$(UID_DOMAIN)")
        self.static_category.add_key_value("COLLECTOR.ALLOW_ADVERTISE_SCHEDD", "$(COLLECTOR.ALLOW_ADVERTISE_SCHEDD), "
                                                                               "$(FRIENDLY_DAEMONS), *@$(UID_DOMAIN)")
        self.static_category.add_key_value("COLLECTOR.ALLOW_ADVERTISE_STARTD", "$(COLLECTOR.ALLOW_ADVERTISE_STARTD), "
                                                                               "$(UNMAPPED_USERS), $(FRIENDLY_DAEMONS), "
                                                                               "*@$(UID_DOMAIN)")
        self.static_category.add_key_value("SCHEDD.ALLOW_NEGOTIATOR", "$(SCHEDD.ALLOW_NEGOTIATOR), "
                                                                     "$(FULL_HOSTNAME)@$(UID_DOMAIN)/$(FULL_HOSTNAME), "
                                                                     "*@$(UID_DOMAIN)")
        self.static_category.add_key_value("ALLOW_ADMINISTRATOR", "$(ALLOW_ADMINISTRATOR), "
                                                                  "$(FULL_HOSTNAME)@$(UID_DOMAIN)/$(FULL_HOSTNAME)")

    def add_lightweight_component_queried_parameters(self):
        super().add_lightweight_component_queried_parameters()
        self.lightweight_component_queried_category.add_key_value_query("uid_domain", "$.config.uid_domain")



