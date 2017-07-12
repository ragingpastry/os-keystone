def osclient(cmd,
             auth_url=None,
             auth_host=None,
             auth_host_scheme='http',
             username='admin',
             user_domain_name='Default',
             password='admin',
             project='admin',
             project_domain_name='Default',
             domain_name=None,
             api_version='3'):
    """
    Creates an openstack CLI command suitable for use with Command fixture
    :param cmd: sub command to pass to openstack's CLI
    :param auth_url: URL to pass to openstack's --os-auth-url CLI argument
    :param auth_host: host/IP to use in auth_url
    :param username: username to pass to openstack's --os-username CLI argument
    :param user_domain_name: passed to openstack --os-user-domain-name
    :param password: password to pass to openstack's --os-password CLI argument
    :param project: project name to pass to openstack's --os-project-name CLI argument
    :param project_domain_name: passed to openstack --os-project-domain-name
    :param domain_name: passed to openstack --os-domain-name for domain scoped token
    :param api_version: API version to pass to openstack's --os-identity-api-version CLI argument
    :returns: formatted CLI command
    """

    if auth_url is None and auth_host is None:
        auth_url = '{auth_host_scheme}://127.0.0.1:35357/v3'.format(**locals())

    if auth_url is None and auth_host:
        auth_url = '{auth_host_scheme}://{auth_host}:35357/v3'.format(
            **locals())

    if project is not None:
        scope = '--os-project-name {} --os-project-domain-name {} '.format(
            project, project_domain_name)
    elif domain_name is not None:
        scope = '--os-domain-name {}'.format(domain_name)
    else:
        scope = ''

    c = ('openstack '
         '--os-auth-url {} '
         '--os-username {} '
         '--os-user-domain-name {} '
         '--os-password {} '
         '{} '
         '--os-identity-api-version {} '
         '{}')

    return c.format(auth_url, username, user_domain_name, password, scope,
                    api_version, cmd)
