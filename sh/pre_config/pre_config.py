import argparse
import yaml

from sh.pre_config.models.config_file import ConfigFile
import sh.pre_config.categories.condor_mapfile as condor_mapfile_categories


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site_config', help="Compiled Site Level Configuration YAML file")
    parser.add_argument('--execution_id', help="ID of lightweight component")
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

    augmented_site_level_config = yaml.safe_load(augmented_site_level_config_file)

    condor_mapfile = ConfigFile("{output_dir}/condor_mapfile".format(output_dir=output_dir), augmented_site_level_config)
    condor_mapfile.add_categories(condor_mapfile_categories.get(augmented_site_level_config, execution_id))
    condor_mapfile.generate_output_file()