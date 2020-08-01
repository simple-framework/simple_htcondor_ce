from models.config_file import ConfigFile
from helpers.generic_helpers import *


class JobRouter(ConfigFile):
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        self.job_router_config_begin = "JOB_ROUTER_ENTRIES @=jre"
        self.job_router_config_end = "@jre"
        self.job_route_template = "[\n" \
                                  "  TargetUniverse = 5;\n" \
                                  "  name = {name};\n" \
                                  "  requirements = {req};\n" \
                                  "  set_AcctSubGroup = ifThenElse(NumberCpus > 1 ,\"_mcore\",\"_score\");" \
                                  "  eval_set_AccountingGroup = strcat({acct_group}, LivAcctSubGroup);\n" \
                                  "]\n"
        ConfigFile.__init__(self, output_file, augmented_site_level_config, execution_id)

    def add_advanced_parameters(self):
        super().add_advanced_parameters()
        routes = []
        voms_config = get_voms_config(self.augmented_site_level_config, self.lightweight_component)
        for voms_info in voms_config:
            fqan = voms_info['voms_fqan']
            user = get_primary_user_for_fqan(fqan, self.augmented_site_level_config, self.lightweight_component)
            name = f"Filtering by mapped job owner {user}"
            requirements_classad = f"(Owner =?= \"{user}\")"
            vo_name = voms_info['vo']['name']
            acct_group = generate_acct_group_for_fqan(vo_name, fqan)

            routes.append(self.job_route_template.format(
                name=name,
                req=requirements_classad,
                acct_group=acct_group
            ))
        generated_routes = "".join(routes)
        job_routes = f"{self.job_router_config_begin}\n{generated_routes}\n{self.job_router_config_end}"
        return job_routes
