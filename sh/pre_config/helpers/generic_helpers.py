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