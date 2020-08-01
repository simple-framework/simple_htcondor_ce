import yaql

engine = yaql.YaqlFactory().create()


def get_lightweight_component(data, id):
    for component in data['lightweight_components']:
        if component['execution_id'] is int(id):
            return component


def get_dns_info(data, id):
    dns_section = data['dns']
    dns = None
    for dns_info in dns_section:
        if dns_info['execution_id'] == id:
            dns = dns_info
            break
    return dns


def get_supported_vos(augmented_site_level_config):
    return [vo['name'] for vo in augmented_site_level_config['supported_virtual_organizations']]


def get_fqan_for_vo(vo, augmented_site_level_config, lightweight_component):
    voms_config = get_voms_config(augmented_site_level_config, lightweight_component)
    return [fqan for fqan in voms_config if fqan['vo']['name'] == vo]


def generate_acct_group_for_fqan(vo, fqan):
    start_str = f"group_{vo}"
    if fqan.startswith('/'):
        fqan = fqan[1:]
    fqan = fqan.lower().split("role=")
    group_info = fqan[0]
    group_info = group_info.replace("/", ".")
    if len(fqan) == 1:
        return f"{start_str}.{group_info}"

    role_and_cap = fqan[1]
    role_and_cap = role_and_cap.split("capability=")
    role = role_and_cap[0]
    if len(role_and_cap) == 1:
        return f"{start_str}.{group_info}_{role}"

    cap = role_and_cap[1].replace(",", "_")
    return f"{start_str}.{group_info}_{role}_{cap}"


def get_primary_user_for_fqan(fqan, augmented_site_level_config, lightweight_component):
    voms_config = [x for x in get_voms_config(augmented_site_level_config, lightweight_component)
                   if x['voms_fqan'] == fqan
                   ]
    pool_accounts = list(
        {x['pool_accounts'][y]['base_name']: x['pool_accounts'][y] for x in voms_config
         for y in range(0, len(x['pool_accounts']))}.values())
    if len(pool_accounts) == 1:
        return pool_accounts[0]['base_name']
    else:
        return pool_accounts[len(pool_accounts) - 1]['base_name']


def get_users_for_fqan(fqan, augmented_site_level_config, lightweight_component):
    voms_config = [x for x in get_voms_config(augmented_site_level_config, lightweight_component)
                   if x['voms_fqan'] == fqan
                   ]
    pool_accounts = list(
        {x['pool_accounts'][y]['base_name']: x['pool_accounts'][y] for x in voms_config
         for y in range(0, len(x['pool_accounts']))}.values())
    users = []
    for pool_account in pool_accounts:
        users.extend(
            [pool_account['base_name'] + "{0:0=3d}".format(x) for x in range(1, pool_account['users_num'] + 1)])
    return users


def get_all_linux_users_as_list(augmented_site_level_config, lightweight_component):
    voms_config = get_voms_config(augmented_site_level_config, lightweight_component)
    pool_accounts = list(
        {x['pool_accounts'][y]['base_name']: x['pool_accounts'][y] for x in voms_config
         for y in range(0, len(x['pool_accounts']))}.values())
    users = []
    for pool_account in pool_accounts:
        users.extend(
            [pool_account['base_name'] + "{0:0=3d}".format(x) for x in range(1, pool_account['users_num'] + 1)])
    return users


def get_all_fqans(augmented_site_level_config, lightweight_component):
    voms_config = get_voms_config(augmented_site_level_config, lightweight_component)
    return list({x['voms_fqan']: x for x in voms_config}.values())


def analyze_fqan(fqan):
    if len(fqan) == 0:
        return ""


def evaluate(data, query):
    expression = engine(query)
    return expression.evaluate(data)


def get_voms_config(augmented_site_level_config, lightweight_component):
    default_voms_config = []
    try:
        supported_vos = lightweight_component['config']['vos']
    except KeyError:
        supported_vos = evaluate(augmented_site_level_config, "$.supported_virtual_organizations")
    try:
        voms_config = evaluate(augmented_site_level_config, "$.voms_config")
    except KeyError:
        for vo in supported_vos:
            default_pool_accounts = []
            default_pool_account_key = "default_pool_account_" + vo['name']
            default_pool_account__sgm_key = "default_pool_account_" + vo['name'] + "sgm"
            if default_pool_account_key in augmented_site_level_config:
                default_pool_accounts.append(augmented_site_level_config[default_pool_account_key])
                default_voms_config.append({
                    'voms_fqan': "/{vo_name}".format(vo_name=vo['name']),
                    'vo': vo,
                    'pool_accounts': default_pool_accounts
                })
            if default_pool_account__sgm_key in augmented_site_level_config:
                default_pool_accounts.append(augmented_site_level_config[default_pool_account__sgm_key])
                default_voms_config.append({
                    'voms_fqan': '/{vo_name}/ROLE=lcgadmin',
                    'vo': vo,
                    'pool_accounts': default_pool_accounts
                })
        voms_config = default_voms_config
    return voms_config
