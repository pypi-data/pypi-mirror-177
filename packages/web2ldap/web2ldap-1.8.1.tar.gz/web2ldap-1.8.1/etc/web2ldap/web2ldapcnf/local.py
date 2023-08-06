import ldap0

from .hosts import (
    ldap_uri_list,
    ldap_def,
    MSAD_CONFIG,
)

# Local MS AD VMs
ldap_def['ldaps://win-n2fcj0kh982.adt1.example.com'] = MSAD_CONFIG.clone(
    tls_options={
        ldap0.OPT_X_TLS_CACERTFILE: '/home/michael/Proj/ae-dir/ansible-example-site/files/my-ae-dir-testca-2021-03.pem',
    },
)

# Local AE-DIR test VMs
aedir_config_vnet1 = ldap_def['ldaps://demo.ae-dir.com/ou=ae-dir'].clone(
    tls_options={
        ldap0.OPT_X_TLS_CACERTFILE: '/home/michael/Proj/ae-dir/ansible-example-site/files/my-ae-dir-testca-2021-03.pem',
    },
)
for aedir_host in (
    'ae-dir-suse-p1.vnet1.local',
    'ae-dir-suse-p2.vnet1.local',
    'ae-dir-suse-c1.vnet1.local',
    'ae-dir-suse-c2.vnet1.local',
    'ae-dir-centos-p1.vnet1.local',
    'ae-dir-centos-p2.vnet1.local',
    'ae-dir-centos-c1.vnet1.local',
    'ae-dir-centos-c2.vnet1.local',
    'ae-dir-deb-p1.vnet1.local',
    'ae-dir-deb-p2.vnet1.local',
    'ae-dir-deb-c1.vnet1.local',
    'ae-dir-deb-c2.vnet1.local',
):
    ldap_def['ldap://{0}'.format(aedir_host)] = aedir_config_vnet1
    ldap_def['ldaps://{0}'.format(aedir_host)] = aedir_config_vnet1
    ldap_uri_list.append((
        'ldaps://{0}/ou=ae-dir????bindname=xkcd,X-BINDPW=Geheimer123456'.format(aedir_host),
        '{0} as \xC6 admin (xkcd)'.format(aedir_host),
    ))
# another cloned config for setting specific LDAPS parameters for internal server
ldap_def['ldaps://ldap.stroeder.local'] = ldap_def['ldap://ldap.stroeder.local'] = ldap_def['ldapi://%2Ftmp%2Fopenldap-socket/dc=stroeder,dc=de'].clone(
    tls_options={
        ldap0.OPT_X_TLS_CACERTFILE: '/etc/ssl/stroeder.com-rootca201907.crt',
    },
)

ldap_def['ldaps://sles-openldap-1.vnet1.local'] = ldap_def['ldap://sles-openldap-1.vnet1.local'] = ldap_def['ldaps://sles-openldap-2.vnet1.local'] = ldap_def['ldap://sles-openldap-2.vnet1.local'] = ldap_def['ldapi://%2Ftmp%2Fopenldap-socket/dc=stroeder,dc=de'].clone(
    tls_options={
        ldap0.OPT_X_TLS_CACERTFILE: '/home/michael/Bizness/Kunden/vhv.de/pki-scripts/rootca/rootca/ca.crt',
    },
)
