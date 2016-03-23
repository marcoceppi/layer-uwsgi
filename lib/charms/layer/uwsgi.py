

import os
from configparser import SafeConfigParser

from charmhelpers.core.host import service_running
from charmhelpers.core.host import service_restart
from charmhelpers.core.host import service_reload
from charmhelpers.core.host import chownr


APP_DIR = '/etc/uwsgi/apps-enabled'
HEADER = '[uwsgi]\n'


def configure(site, dir, uid='www-data', gid='www-data', plugins=None,
              cfg=None):
    """ create or update a UWSGI config

    :param site: name of configuration
    :param chdir: directory of UWSGI app, same as chdir in UWSGI
    :param uid: user id/name to run with
    :param gid: group id/name to run with
    :param cfg: additional UWSGI configuration params
    :param plugins: plugin to use
    """

    if not cfg:
        cfg = {}

    cfg['uid'] = uid
    cfg['gid'] = gid
    cfg['chdir'] = dir

    if plugins:
        cfg['plugins'] = plugins

    if 'socket' not in cfg and not cfg.get('socket'):
        socket_dir = '/srv/run/uwsgi'
        if not os.path.exists(socket_dir):
            os.makedirs(socker_dir)
        chownr(socket_dir, uid, gid)

        cfg['socket'] = os.path.join(socket_dir, '%s.socket' % site)

    if 'master' not in cfg:
        cfg['master'] = 'true'

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
    return {s[0]: s[1] for s in c.items('uwsgi')}


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
