import yaql


engine = yaql.YaqlFactory().create()


def get_lightweight_component(data, id):
    for component in data['lightweight_components']:
        if component['execution_id'] is int(id):
            return component


def evaluate(data, query):
    expression = engine(query)
    return expression.evaluate(data)


def get_voms_config(data, component_section):
    default_voms_config = []
    try:
        supported_vos = component_section['config']['vos']
    except KeyError:
        supported_vos = evaluate(data, "$.supported_virtual_organizations")
    try:
        voms_config = evaluate(data, "$.voms_config")
    except KeyError:
        for vo in supported_vos:
            default_pool_accounts = []
            default_pool_account_key = "default_pool_account_" + vo['name']
            default_pool_account__sgm_key = "default_pool_account_" + vo['name'] + "sgm"
            if default_pool_account_key in data:
                default_pool_accounts.append(data[default_pool_account_key])
                default_voms_config.append({
                    'voms_fqan': "/{vo_name}".format(vo_name=vo['name']),
                    'vo': vo,
                    'pool_accounts': default_pool_accounts
                })
            if default_pool_account__sgm_key in data:
                default_pool_accounts.append(data[default_pool_account__sgm_key])
                default_voms_config.append({
                    'voms_fqan': '/{vo_name}/ROLE=lcgadmin',
                    'vo': vo,
                    'pool_accounts': default_pool_accounts
                })
        voms_config = default_voms_config
    return voms_config


def get_batch_execution_id(augmented_site_level_config):
    batch_execution_id = None
    for component in augmented_site_level_config['lightweight_components']:
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


def get_batch_dns_info(augmented_site_level_config):
    batch_execution_id = get_batch_execution_id(augmented_site_level_config)
    dns_section = augmented_site_level_config['dns']
    dns = None
    for dns_info in dns_section:
        if dns_info['execution_id'] == batch_execution_id:
            dns = dns_info
            break

    if dns is None:
        raise Exception("Cannot find lightweight component for HTCondor-Batch in dns section of "
                        "augmented site level config file.")

    return dns

