# -*- coding: ascii -*-
"""
web2ldap.app.monitor: Display (SSL) connection data

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import os
import time
import socket
import threading
import pwd

import web2ldapcnf

from ..__about__ import __version__
from ..utctime import strftimeiso8601
from ..log import EXC_TYPE_COUNTER
from ..ldapsession import LDAPSession
from .. import STARTUP_TIME
from .gui import (
    footer,
    simple_main_menu,
    top_section,
)
from .session import session_store
from .metrics import METRICS_AVAIL
from .stats import COMMAND_COUNT

MONITOR_TEMPLATE = """
<h1>Monitor</h1>

<h2>System information</h2>

{text_metricsurl}

<table summary="System information">
  <tr>
    <td>web2ldap version:</td>
    <td>{text_version}</td>
  </tr>
  <tr>
    <td>Hostname:</td>
    <td>{text_sysfqdn}</td>
  </tr>
  <tr>
    <td>PID / PPID:</td>
    <td>{int_pid:d} / {int_ppid:d}</td>
  </tr>
  <tr>
    <td>UID:</td>
    <td>{text_username} ({int_uid:d})</td>
  </tr>
</table>

<h3>Time information</h3>
<table summary="Time information">
  <tr>
    <td>Current time:</td>
    <td>{text_currenttime}</td>
  </tr>
  <tr>
    <td>Startup time:</td>
    <td>{text_startuptime}</td>
  </tr>
  <tr>
    <td>Uptime:</td>
    <td>{text_uptime}</td>
  </tr>
</table>

<h3>{int_numthreads:d} active threads:</h3>
<ul>
  {text_threadlist}
</ul>

<h2>Session counters</h2>
<table summary="Session counters">
  <tr>
    <td>Web sessions initialized:</td>
    <td>{int_sessioncounter:d}</td>
  </tr>
  <tr>
    <td>Max. concurrent sessions:</td>
    <td>{int_maxconcurrentsessions:d}</td>
  </tr>
  <tr>
    <td>Sessions removed after timeout:</td>
    <td>{int_removedsessions:d}</td>
  </tr>
  <tr>
    <td>Web session limit:</td>
    <td>{int_sessionlimit:d}</td>
  </tr>
  <tr>
    <td>Web session limit per remote IP:</td>
    <td>{int_sessionlimitperip:d}</td>
  </tr>
  <tr>
    <td>Session removal time:</td>
    <td>{int_sessionremoveperiod:d}</td>
  </tr>
  <tr>
    <td>Currently active remote IPs:</td>
    <td>{int_currentnumremoteipaddrs:d}</td>
  </tr>
</table>

<h3>{int_numremoteipaddrs:d} remote IPs seen:</h3>
<table>
  <tr><th>Remote IP</th><th>Count</th></tr>
  {text_remoteiphitlist}
</table>

<h3>Command URLs:</h3>
<table>
  <tr><th>URL</th><th>Count</th></tr>
  {text_cmd_counters}
</table>

<h3>Unhandled exceptions:</h3>
<table>
  <tr><th>Exception</th><th>Count</th></tr>
  {text_exc_counters}
</table>

<h2>Active sessions</h2>
"""

MONITOR_CONNECTIONS_TMPL = """
<h3>%d active LDAP connections:</h3>
<table summary="Active LDAP connections">
  <tr>
    <th>Remote IP</th>
    <th>Last access time</th>
    <th>Target URI</th>
    <th>Bound as</th>
  </tr>
  %s
</table>
"""

MONITOR_SESSIONS_JUST_CREATED_TMPL = """
<h3>%d sessions just created:</h3>
<table summary="Sessions not fully initialized">
  <tr>
    <th>Creation time</th>
  </tr>
  %s
</table>
"""


def get_uptime() -> float:
    """
    returns seconds since start
    """
    return time.time() - STARTUP_TIME


def get_user_info() -> tuple:
    """
    returns tuple of numeric POSIX-ID and accompanying user name (if found)
    """
    uid = os.getuid()
    try:
        username = pwd.getpwuid(uid).pw_name
    except KeyError:
        username = None
    return (uid, username)


def w2l_monitor(app):
    """
    List several general gateway stats
    """

    uptime = get_uptime()
    posix_uid, posix_username = get_user_info()
    _session_store = session_store()

    top_section(app, 'Monitor', simple_main_menu(app), [])

    monitor_tmpl_vars = dict(
        text_metricsurl=METRICS_AVAIL*app.anchor('metrics', 'Metrics endpoint', []),
        text_version=__version__,
        text_sysfqdn=socket.getfqdn(),
        int_pid=os.getpid(),
        int_ppid=os.getppid(),
        text_username=app.form.s2d(posix_username or '-/-'),
        int_uid=posix_uid,
        text_currenttime=strftimeiso8601(time.gmtime(time.time())),
        text_startuptime=strftimeiso8601(time.gmtime(STARTUP_TIME)),
        text_uptime='%02d:%02d' % (int(uptime//3600), int(uptime//60%60)),
        int_numthreads=threading.active_count(),
        text_threadlist='\n'.join(
            [
                '<li>%s</li>' % ''.join(
                    [
                        app.form.s2d(str(repr(t))),
                        ', alive'*t.is_alive(),
                        ', daemon'*t.daemon,
                    ]
                )
                for t in threading.enumerate()
            ]
        ),
        int_sessioncounter=_session_store.sessionCounter,
        int_maxconcurrentsessions=_session_store.max_concurrent_sessions,
        int_removedsessions=_session_store.expired_counter,
        int_sessionlimit=web2ldapcnf.session_limit,
        int_sessionlimitperip=web2ldapcnf.session_per_ip_limit,
        int_sessionremoveperiod=_session_store.session_ttl,
        int_currentnumremoteipaddrs=len(_session_store.remote_ip_sessions),
        int_numremoteipaddrs=len(_session_store.remote_ip_counter),
        text_remoteiphitlist='\n'.join(
            [
                '<tr><td>%s</td><td>%d</td></tr>' % (
                    app.form.s2d((ip or '-')),
                    count,
                )
                for ip, count in _session_store.remote_ip_counter.most_common()
            ]
        ),
        text_cmd_counters='\n'.join(
            [
                '<tr><td>%s</td><td>%d</td></tr>' % (
                    app.form.s2d(cmd),
                    ctr,
                )
                for cmd, ctr in sorted(COMMAND_COUNT.items())
            ]
        ),
        text_exc_counters='\n'.join(
            [
                '<tr><td>%s</td><td>%d</td></tr>' % (
                    app.form.s2d(str(exc_type)),
                    exc_ctr,
                )
                for exc_type, exc_ctr in EXC_TYPE_COUNTER.items()
            ]
        ),
    )
    app.outf.write(MONITOR_TEMPLATE.format(**monitor_tmpl_vars))

    if _session_store.sessiondict:

        real_ldap_sessions = []
        fresh_ldap_sessions = []
        for k, i in _session_store.sessiondict.items():
            if not k.startswith('__'):
                if isinstance(i[1], LDAPSession) and i[1].uri:
                    real_ldap_sessions.append((k, i))
                else:
                    fresh_ldap_sessions.append((k, i))

        if real_ldap_sessions:
            app.outf.write(
                MONITOR_CONNECTIONS_TMPL % (
                    len(real_ldap_sessions),
                    '\n'.join([
                        '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
                            app.form.s2d((i[1].on_behalf or '') or 'unknown'),
                            strftimeiso8601(time.gmtime(i[0])),
                            app.form.s2d(i[1].uri or 'no connection'),
                            app.form.s2d(i[1].who or 'anonymous'),
                        )
                        for k, i in real_ldap_sessions
                    ]),
                )
            )

        if fresh_ldap_sessions:
            app.outf.write(
                MONITOR_SESSIONS_JUST_CREATED_TMPL % (
                    len(fresh_ldap_sessions),
                    '\n'.join([
                        '<tr><td>{}</td></tr>'.format(strftimeiso8601(time.gmtime(i[0])))
                        for k, i in fresh_ldap_sessions
                    ]),
                )
            )

    else:
        app.outf.write('No active sessions.\n')

    footer(app)
