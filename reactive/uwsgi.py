
from charms.reactive import hook
from charms.reactive import when
from charms.reactive import when_not
from charms.reactive import set_state
from charms.reactive import remove_state

from charms.layer import uwsgi


@when_not('uwsgi.running')
def start_uwsgi():
    uwsgi.restart()
    fresh_check()


@hook('update-status')
def fresh_check():
    if uwsgi.running():
        return remove_state('uwsgi.running')

    set_state('uwsgi.running')
