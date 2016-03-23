
import os
from ConfigParser import SafeConfigParser

from charmhelpers.core.host import service_running
from charmhelpers.core.host import service_restart
from charmhelpers.core.host import service_reload


APP_DIR = '/etc/uwsgi/apps-enabled'
HEADER = '[uwsgi]\n'


def configure(site, dir, uid='www-data', gid='www-data', cfg=None,
              plugins=None):
    """ create or update a UWSGI config

    :param site: name of configuration
    :param chdir: directory of UWSGI app, same as chdir in UWSGI
    :param uid: user id/name to run with
    :param gid: group id/name to run with
    :param cfg: additional UWSGI configuration params
    :param plugins: list of plugins to use
    """

    cfg['uid'] = uid
    cfg['gid'] = gid
    cfg['chdir'] = dir

    if plugins and isinstance(plugins, list):
        cfg['plugins'] = plugins

    if 'socket' not in cfg and not cfg.get('socket'):
        cfg['socket'] = '/run/uwsgi/%s/socket' % site

    reload = True
    if not os.path.exists(cfg_path(site)):
        reload = False  # need to restart for new configuration

    with open(cfg_path(site), 'w') as f:
        wsgi_txt = '\n'.join(['%s = %s' % (k, d) for k, d in cfg.items()])
        f.write(HEADER + wsgi_txt)

    restart(reload)


def config(site):
    """ retrieve configuration for UWSGI site

    :param site: name of configuration to retrieve
    """

    c = SafeConfigParser()
    c.read(cfg_path(site))
    cfg = {s[0]: s[1] for s in c.items('uwsgi')}


def remove(site):
    """ remove a wsgi configured site

    :param site: name of configuration to delete
    """

    os.unlink(cfg_path(site))


def running():
    """ check if uwsgi is running """
    return service_running('uwsgi')


def restart(reload=False):
    """ restart or reload uwsgi

    :param reload: boolean to reload instead of restart
    """
    if reload:
        return service_reload('uwsgi', True)

    return service_restart('uwsgi')


def cfg_path(site):
    return os.path.join(APP_DIR, '%s.ini' % site)