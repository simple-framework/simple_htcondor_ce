import os
import argparse
import yaml
import os
from files.configured_attributes_60 import ConfiguredAttributes60
from files.site_security_59 import SiteSecurity59
from files.simple_98 import Simple98
from files.condor_mapfile import CondorMapfile
from files.pc_config_50 import PCConfig50
from files.simple_condor_98 import SimpleCondor98
from files.supported_vo_users import SupportedVOUsers
from files.supplemental_config import SupplementalConfig
from files.supported_vos import SupportedVOs
from files.timezone import TimeZone
from files.vomsconfig import VOMSConfig
from files.vomses import VOMSES

from helpers.generic_helpers import get_lightweight_component


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site_config', help="Compiled Site Level Configuration YAML file")
    parser.add_argument('--execution_id', help="Execution ID of lightweight component")
    parser.add_argument('--output_dir', help="Output directory")
    args = parser.parse_args()
    return {
        'augmented_site_level_config_file': args.site_config,
        'execution_id': args.execution_id,
        'output_dir': args.output_dir
    }


if __name__ == "__main__":
    args = parse_args()
    execution_id = args['execution_id']
    augmented_site_level_config_file = args['augmented_site_level_config_file']
    output_dir = args['output_dir']

    augmented_site_level_config = yaml.safe_load(open(augmented_site_level_config_file, 'r'))

    # Files present in container by default at /etc/condor-ce/config.d/: 01-ce-auth.conf  01-ce-router.conf
    # 01-common-auth.conf  02-ce-condor.conf  03-ce-shared-port.conf  03-managed-fork.conf

    # Custom config files /etc/condor-ce
    # site_security_59 = SiteSecurity59("{output_dir}/59_site_security.conf".format(output_dir=output_dir),
    #                                   augmented_site_level_config, execution_id)
    # site_security_59.generate_output_file()
    #
    # configured_attributes_60 = ConfiguredAttributes60("{output_dir}/60_configured_attributes.conf"
    #                                                   .format(output_dir=output_dir), augmented_site_level_config,
    #                                                   execution_id)
    # configured_attributes_60.generate_output_file()
    #
    # simple_98 = Simple98("{output_dir}/98_simple.conf".format(output_dir=output_dir),
    #                      augmented_site_level_config, execution_id)
    # simple_98.generate_output_file()
    #
    # condor_mapfile = CondorMapfile("{output_dir}/condor_mapfile".format(output_dir=output_dir),
    #                                augmented_site_level_config, execution_id)
    # condor_mapfile.generate_output_file()
    #
    # # Custom config files /etc/condor
    # pc_config_50 = PCConfig50("{output_dir}/50_PC.conf".format(output_dir=output_dir),
    #                           augmented_site_level_config, execution_id)
    # pc_config_50.generate_output_file()
    #
    # simple_condor_98 = SimpleCondor98("{output_dir}/98_simple_condor.conf".format(output_dir=output_dir),
    #                                   augmented_site_level_config, execution_id)
    # simple_condor_98.generate_output_file()
    #
    # timezone = TimeZone("{output_dir}/timezone".format(output_dir=output_dir), augmented_site_level_config, execution_id)
    # timezone.generate_output_file()
    #
    # supported_vo_users = SupportedVOUsers("{output_dir}/supported_vo_users.conf".format(output_dir=output_dir),
    #                                       augmented_site_level_config, execution_id)
    # supported_vo_users.generate_output_file()
    #
    # lc = get_lightweight_component(augmented_site_level_config, execution_id)
    #
    # if os.path.exists('{output_dir}/supplemental_mapfile'.format(output_dir=output_dir)):
    #     os.remove('{output_dir}/supplemental_mapfile'.format(output_dir=output_dir))
    # components = lc.get('supplemental_config', [])
    # if not (components is None or len(components) ==0):
    #     for component in components:
    #         supplemental_config = SupplementalConfig(output_dir, augmented_site_level_config, execution_id, component)
    #         supplemental_config.generate_output_file()

    if 'voms_config' in augmented_site_level_config:
        # vomsdir
        try:
            os.mkdir(f"{output_dir}/vomsdir")
        except OSError:
            pass

        # vomses
        try:
            os.mkdir(f"{output_dir}/vomses")
        except OSError:
            pass

        # subdirs
        vos = set()
        for voms_config in augmented_site_level_config['voms_config']:
            vos.add(voms_config['vo']['name'])

        for vo in vos:
            # vomsdir
            try:
                os.mkdir(f"{output_dir}/vomsdir/{vo}")
            except OSError:
                pass

        voms_config = augmented_site_level_config['voms_config']
        for voms in voms_config:
            vo_name = voms['vo']['name']
            servers = voms['vo']['servers']
            for server_data in servers:
                voms_config_file = VOMSConfig(f"{output_dir}/vomsdir/{vo_name}/{server_data['server']}.lsc",
                                              augmented_site_level_config,
                                              execution_id,
                                              server_data)

                vomses = VOMSES(f"{output_dir}/vomses/{vo_name}-{server_data['server']}",
                                augmented_site_level_config,
                                execution_id,
                                server_data,
                                vo_name)

                voms_config_file.generate_output_file()
                vomses.generate_output_file()
