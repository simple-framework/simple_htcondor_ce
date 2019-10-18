from helpers.generic_helpers import get_lightweight_component
from models.parameter_category import ParameterCategory


class ConfigFile:
    def __init__(self, output_file, augmented_site_level_config, execution_id):
        self.categories = []
        self.evaluated_lines = []
        self.output_file = output_file
        self.augmented_site_level_config = augmented_site_level_config
        self.lightweight_component = get_lightweight_component(augmented_site_level_config, execution_id)
        self.dns = None
        for dns_info in augmented_site_level_config['dns']:
            if dns_info['execution_id'] == int(execution_id):
                self.dns = dns_info
                break
        if self.dns is None:
            raise Exception("Cannot find DNS entry for current HTCondor-CE lightweight component")
        self.lightweight_component_queried_category = ParameterCategory("{name}_lightweight_component_queried".format(name=output_file),
                                                                        self.lightweight_component)
        self.global_queried_category = ParameterCategory("{name}_global_queried".format(name=output_file), augmented_site_level_config)
        self.static_category = ParameterCategory("{name}_static".format(name=output_file))
        self.advanced_category = ParameterCategory("{name}_static".format(name=output_file), augmented_site_level_config)

        self.categories.append(self.advanced_category)
        self.categories.append(self.global_queried_category)
        self.categories.append(self.lightweight_component_queried_category)
        self.categories.append(self.static_category)

        self.add_advanced_parameters()
        self.add_global_queried_parameters()
        self.add_lightweight_component_queried_parameters()
        self.add_static_parameters()

    def add_categories(self, categories):
        for category in categories:
            self.categories.append(category)

    def add_category(self, category):
        self.categories.append(category)

    def evaluate_categories(self):
        for category in self.categories:
            evaluated_results = category.get()
            for data_entry in evaluated_results:
                self.evaluated_lines.append(data_entry)

    def generate_output_file(self):
        output_file = open(self.output_file, 'w')
        self.evaluate_categories()
        for line in self.evaluated_lines:
            output_file.write(line)
        output_file.close()

    ### Default Categories ###
    def add_lightweight_component_queried_parameters(self):
        pass

    def add_global_queried_parameters(self):
        pass

    def add_static_parameters(self):
        pass

    def add_advanced_parameters(self):
        pass

    ## Utils ##
    def get_batch_execution_id(self):
        batch_execution_id = None
        for component in self.augmented_site_level_config['lightweight_components']:
            if component['type'] == "batch_system":
                if component['name'] == 'HTCondor-Batch':
                    batch_execution_id = component['execution_id']
                    break
        if batch_execution_id is None:
            raise Exception("Could not find HTCondor-Batch in the lightweight components section of the "
                            "site level configuration file. It is required to configure the HTCondor-CE's SCHEDD2 to "
                            "forward incoming jobs to the batch system. Please specify the repository "
                            "https://github.com/WLCG-Lightweight-Sites/simple_htcondor_batch"
                            "in the lightweight components section. Then rollback and re-run the framework. "
                            "Please note that the SIMPLE Grid Framework's HTCondorCE can only work with the SIMPLE "
                            "Grid Framework's HTCondor Batch system at present.")

        return batch_execution_id

    def get_batch_dns_info(self):
        batch_execution_id = self.get_batch_execution_id()
        dns_section = self.augmented_site_level_config['dns']
        dns = None
        for dns_info in dns_section:
            if dns_info['execution_id'] == batch_execution_id:
                dns = dns_info
                break

        if dns is None:
            raise Exception("Cannot find lightweight component for HTCondor-Batch in dns section of "
                            "augmented site level config file.")

        return dns
