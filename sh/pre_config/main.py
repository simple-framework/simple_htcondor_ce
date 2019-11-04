import argparse
import yaml

from files.configured_attributes_60 import ConfiguredAttributes60
from files.site_security_59 import SiteSecurity59
from files.simple_98 import Simple98
from files.condor_mapfile import CondorMapfile
from files.pc_config_50 import PCConfig50
from files.simple_condor_98 import SimpleCondor98
from files.supported_vo_users import SupportedVOUsers
from files.supplemental_config import SupplementalConfig


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
    site_security_59 = SiteSecurity59("{output_dir}/59_site_security.conf".format(output_dir=output_dir),
                                      augmented_site_level_config, execution_id)
    site_security_59.generate_output_file()

    configured_attributes_60 = ConfiguredAttributes60("{output_dir}/60_configured_attributes.conf"
                                                      .format(output_dir=output_dir), augmented_site_level_config,
                                                      execution_id)
    configured_attributes_60.generate_output_file()

    simple_98 = Simple98("{output_dir}/98_simple.conf".format(output_dir=output_dir),
                         augmented_site_level_config, execution_id)
    simple_98.generate_output_file()

    condor_mapfile = CondorMapfile("{output_dir}/condor_mapfile".format(output_dir=output_dir),
                                   augmented_site_level_config, execution_id)
    condor_mapfile.generate_output_file()

    # Custom config files /etc/condor
    pc_config_50 = PCConfig50("{output_dir}/50_PC.conf".format(output_dir=output_dir),
                              augmented_site_level_config, execution_id)
    pc_config_50.generate_output_file()

    simple_condor_98 = SimpleCondor98("{output_dir}/98_simple_condor.conf".format(output_dir=output_dir),
                                      augmented_site_level_config, execution_id)
    simple_condor_98.generate_output_file()

    supported_vo_users = SupportedVOUsers("{output_dir}/supported_vo_users.conf".format(output_dir=output_dir),
                                          augmented_site_level_config, execution_id)
    supported_vo_users.generate_output_file()

    for lc in augmented_site_level_config['lightweight_components']:
        if 'supplemental_config' in lc:
            supplemental_config = SupplementalConfig(output_dir, augmented_site_level_config, lc['execution_id'])
            supplemental_config.generate_output_file()