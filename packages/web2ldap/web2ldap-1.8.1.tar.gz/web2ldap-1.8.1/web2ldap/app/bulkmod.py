# -*- coding: ascii -*-
"""
web2ldap.app.bulkmod: modify several entries found by prior search

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import time

import ldap0
from ldap0.dn import DNObj

import web2ldapcnf

from ..ldaputil.oidreg import OID_REG
from ..ldapsession import LDAPLimitErrors

from . import ErrorExit
from .gui import attrtype_select_field, footer, main_menu, top_section
from .schema.syntaxes import syntax_registry, LDAPSyntaxValueError
from .modify import modlist_ldif


BULKMOD_FORM_TMPL = """
{form_begin}
{text_msg}
<fieldset>
  <legend>Search parameters</legend>
  <table>
    <tr>
      <td>Search base:</td><td>{field_hidden_dn}</td>
    </tr>
    <tr>
      <td>Search scope:</td><td>{field_hidden_scope}</td>
    </tr>
    <tr>
      <td>Search filter:</td>
      <td>
        {field_hidden_filterstr}
      </td>
    </tr>
  </table>
</fieldset>
<fieldset>
  <legend>Bulk modify input</legend>
  <p><input type="submit" name="bulkmod_submit" value="Next&gt;&gt;"></p>
  <table>
  <tr>
    <td colspan="2">Superior DN:</td><td colspan="3">{field_bulkmod_newsuperior}</td>
  </tr>
  <tr>
    <td colspan="2">Copy entries:</td><td colspan="3">{field_bulkmod_cp}</td>
  </tr>
  {input_fields}
  </table>
</fieldset>
<fieldset>
  <legend>Extended controls</legend>
  {field_bulkmod_ctrl}
</fieldset>
</form>
"""

BULKMOD_CONFIRMATION_FORM_TMPL = """
{form_begin}
<p class="WarningMessage">
  Apply changes to entries found with search?
</p>
<table>
  <tr>
    <td>Search base:</td><td>{field_hidden_dn}</td>
  </tr>
  <tr>
    <td>Search scope:</td><td>{field_hidden_scope}</td>
  </tr>
  <tr>
    <td>Search filter:</td>
    <td>
      {field_hidden_filterstr}
    </td>
  </tr>
  <tr>
    <td># affected entries / referrals:</td>
    <td>
      {num_entries} / {num_referrals}
    </td>
  </tr>
</table>
<dl>
  <dt>LDIF change record:</dt>
  <dd>
    {text_ldifchangerecord}
  </dd>
  <dt>
    <strong>{text_bulkmod_cp}</strong> all entries beneath this new superior DN:
  </dt>
  <dd><strong>{field_bulkmod_newsuperior}</strong></dd>
  <dt>Use extended controls:</dt>
  <dd><ul>{field_bulkmod_ctrl}<ul></dd>
</dl>
{hidden_fields}
<p class="WarningMessage">Are you sure?</p>
<input type="submit" name="bulkmod_submit" value="&lt;&lt;Back">
<input type="submit" name="bulkmod_submit" value="Apply">
<input type="submit" name="bulkmod_submit" value="Cancel">
'</form>
"""

BULKMOD_MESSAGE_TMPL = """
<p class="SuccessMessage">Modified entries.</p>
<table>
  <tr>
    <td>Modified entries:</td>
    <td>{num_modify_success_count:d}</td>
    <td>
      <meter
        min="0"
        max="{num_all_modify_count:d}"
        value="{num_modify_success_count:d}"
        optimum="{num_all_modify_count:d}"
        title="entries"
      >
        {num_modify_success_count:d}
      </meter>
    </td>
  </tr>
  <tr>
    <td>Modification errors:</td>
    <td>{num_modify_error_count:d}</td>
    <td>
      <meter
        min="0"
        max="{num_all_modify_count:d}"
        value="{num_modify_error_count:d}"
        optimum="0"
        title="entries"
      >
        {num_modify_error_count:d}
      </meter>
    </td>
  </tr>
  <tr>
    <td>Renamed/copied entries:</td>
    <td>{num_modrdn_success_count:d}</td>
    <td>
      <meter
        min="0"
        max="{num_all_modrdn_count:d}"
        value="{num_modrdn_success_count:d}"
        optimum="{num_all_modrdn_count:d}"
        title="entries"
      >
        {num_modrdn_success_count:d}
      </meter>
    </td>
  </tr>
  <tr>
    <td>Rename/copy errors:</td>
    <td>{num_modrdn_error_count:d}</td>
    <td>
      <meter
        min="0"
        max="{num_all_modrdn_count:d}"
        value="{num_modrdn_error_count:d}"
        optimum="0"
        title="entries"
      >
        {num_modrdn_error_count:d}
      </meter>
    </td>
  </tr>
  <tr><td>Search base:</td><td>{text_dn}</td></tr>
  <tr><td>Search scope:</td><td>{text_scope}</td></tr>
  <tr><td>Time elapsed:</td><td>{num_elapsed_time:0.2f} seconds</td></tr>
</table>
{text_form_begin}
{text_fields}
  <p><input type="submit" name="bulkmod_submit" value="&lt;&lt;Back"></p>
</form>
{text_errors}
{text_changes}
"""


def input_modlist(app, bulkmod_at, bulkmod_op, bulkmod_av):

    mod_dict = {}
    input_errors = set()

    for i in range(len(bulkmod_at)):

        mod_op_str = bulkmod_op[i]
        if not mod_op_str:
            continue
        mod_op = int(mod_op_str)
        mod_type = bulkmod_at[i]
        if not mod_type:
            continue

        attr_instance = syntax_registry.get_at(
            app, '', app.schema, mod_type, None, entry=None,
        )
        try:
            mod_val = attr_instance.sanitize((bulkmod_av[i] or '').encode(app.ls.charset))
        except LDAPSyntaxValueError:
            mod_val = ''
            input_errors.add(i)
        try:
            attr_instance.validate(mod_val)
        except LDAPSyntaxValueError:
            input_errors.add(i)

        if mod_op == ldap0.MOD_INCREMENT:
            mod_dict[(mod_op, mod_type)] = set([None])
        elif not mod_val and mod_op == ldap0.MOD_DELETE:
            mod_dict[(mod_op, mod_type)] = set([None])
        elif mod_val and mod_op in {ldap0.MOD_DELETE, ldap0.MOD_ADD, ldap0.MOD_REPLACE}:
            try:
                mod_dict[(mod_op, mod_type)].add(mod_val)
            except KeyError:
                mod_dict[(mod_op, mod_type)] = set([mod_val])

    mod_list = []
    if not input_errors:
        for mod_op, mod_type in mod_dict.keys():
            mod_vals = mod_dict[(mod_op, mod_type)]
            if mod_op == ldap0.MOD_DELETE and None in mod_vals:
                mod_vals = None
            mod_list.append((mod_op, mod_type.encode('ascii'), mod_vals))
        for i, m in enumerate(mod_list):
            if m[2] is not None:
                mod_list[i] = (m[0], m[1], list(m[2]))

    return mod_list, input_errors
    # end of input_modlist()


def bulkmod_input_form(
        app,
        bulkmod_submit,
        dn, scope, bulkmod_filter, bulkmod_newsuperior,
        bulkmod_at, bulkmod_op, bulkmod_av, bulkmod_cp,
        input_errors,
    ):
    # Extend the input lists to at least one empty input row
    bulkmod_at = bulkmod_at or ['']
    bulkmod_op = bulkmod_op or ['']
    bulkmod_av = bulkmod_av or ['']
    error_attrs = sorted({bulkmod_at[i] for i in input_errors})
    if error_attrs:
        error_msg = '<p class="ErrorMessage">Invalid input: %s</p>' % (
            ', '.join(map(app.form.s2d, error_attrs))
        )
    else:
        error_msg = '<p class="WarningMessage">Input bulk modify parameters here.</p>'
    if bulkmod_submit and bulkmod_submit.startswith('-'):
        del_row_num = int(bulkmod_submit[1:])
        if len(bulkmod_at) > 1:
            del bulkmod_at[del_row_num]
            del bulkmod_op[del_row_num]
            del bulkmod_av[del_row_num]
    elif bulkmod_submit and bulkmod_submit.startswith('+'):
        insert_row_num = int(bulkmod_submit[1:])
        if len(bulkmod_at) < web2ldapcnf.max_searchparams:
            bulkmod_at.insert(insert_row_num+1, bulkmod_at[insert_row_num])
            bulkmod_op.insert(insert_row_num+1, bulkmod_op[insert_row_num])
            bulkmod_av.insert(insert_row_num+1, '')
    # Generate a select field for the attribute type
    bulkmod_attr_select = attrtype_select_field(
        app,
        'bulkmod_at',
        'Attribute type',
        [], default_attr_options=None
    )
    # Output confirmation form
    top_section(app, 'Bulk modification input', main_menu(app))
    input_fields = '\n'.join([
        """
        <tr>
          <td><button type="submit" name="bulkmod_submit" value="+%d">+</button></td>
          <td><button type="submit" name="bulkmod_submit" value="-%d">-</button></td>
          <td>%s</td><td>%s</td><td>%s %s</td>
        </tr>
        """ % (
            i, i,
            bulkmod_attr_select.input_html(default=bulkmod_at[i]),
            app.form.field['bulkmod_op'].input_html(default=bulkmod_op[i]),
            app.form.field['bulkmod_av'].input_html(default=bulkmod_av[i]),
            (i in input_errors)*'&larr; Input error!'
        )
        for i in range(len(bulkmod_at))
    ])

    app.outf.write(
        BULKMOD_FORM_TMPL.format(
            text_msg=error_msg,
            form_begin=app.begin_form('bulkmod', 'POST'),
            field_bulkmod_ctrl=app.form.field['bulkmod_ctrl'].input_html(default=app.form.field['bulkmod_ctrl'].val),
            input_fields=input_fields,
            field_hidden_dn=app.form.hidden_field_html('dn', app.dn, app.dn),
            field_hidden_filterstr=app.form.hidden_field_html('filterstr', bulkmod_filter, bulkmod_filter),
            field_hidden_scope=app.form.hidden_field_html(
                'scope',
                str(scope),
                str(ldap0.ldapurl.SEARCH_SCOPE_STR[scope]),
            ),
            field_bulkmod_newsuperior=app.form.field['bulkmod_newsuperior'].input_html(
                default=bulkmod_newsuperior,
                title='New superior DN where all entries are moved beneath',
            ),
            field_bulkmod_cp=app.form.field['bulkmod_cp'].input_html(checked=bulkmod_cp),
        )
    )
    footer(app)
    # end of bulkmod_input_form()


def bulkmod_confirmation_form(
        app,
        dn, scope,
        bulkmod_filter, bulkmod_newsuperior, bulk_mod_list, bulkmod_cp,
    ):

    # first try to determine the number of affected entries
    try:
        num_entries, num_referrals = app.ls.count(app.dn, scope, bulkmod_filter, sizelimit=1000)
    except LDAPLimitErrors:
        num_entries, num_referrals = ('unknown', 'unknown')
    else:
        if num_entries is None:
            num_entries = 'unknown'
        else:
            num_entries = str(num_entries)
        if num_referrals is None:
            num_referrals = 'unknown'
        else:
            num_referrals = str(num_referrals)

    # generate an LDIF representation of the modifications
    if bulk_mod_list:
        bulk_mod_list_ldif = modlist_ldif(
            'cn=bulkmod-dummy',
            app.form,
            bulk_mod_list,
        )
    else:
        bulk_mod_list_ldif = '- none -'

    # Output confirmation form
    top_section(app, 'Modify entries?', main_menu(app), main_div_id='Input')
    app.outf.write(
        BULKMOD_CONFIRMATION_FORM_TMPL.format(
            form_begin=app.begin_form('bulkmod', 'POST'),
            field_bulkmod_ctrl='\n'.join([
                '<li>%s (%s)</li>' % (
                    app.form.s2d(OID_REG.get(ctrl_oid, (ctrl_oid,))[0]),
                    app.form.s2d(ctrl_oid),
                )
                for ctrl_oid in app.form.field['bulkmod_ctrl'].val or []
            ]) or '- none -',
            field_hidden_dn=app.form.hidden_field_html('dn', dn, dn),
            field_hidden_filterstr=app.form.hidden_field_html('filterstr', bulkmod_filter, bulkmod_filter),
            field_hidden_scope=app.form.hidden_field_html('scope', str(scope), str(ldap0.ldapurl.SEARCH_SCOPE_STR[scope])),
            field_bulkmod_newsuperior=app.form.hidden_field_html(
                'bulkmod_newsuperior',
                bulkmod_newsuperior,
                bulkmod_newsuperior
            ),
            text_bulkmod_cp={False:'Move', True:'Copy'}[bulkmod_cp],
            num_entries=num_entries,
            num_referrals=num_referrals,
            text_ldifchangerecord=bulk_mod_list_ldif,
            hidden_fields=app.form.hidden_input_html(ignored_fields=[
                'dn', 'scope', 'filterstr', 'bulkmod_submit', 'bulkmod_newsuperior',
            ]),
        )
    )
    footer(app)
    # end of bulkmod_confirmation_form()


def w2l_bulkmod(app):
    """
    Applies bulk modifications to multiple LDAP entries
    """

    bulkmod_submit = app.form.get_input_value('bulkmod_submit', [None])[0]

    bulkmod_at = app.form.get_input_value('bulkmod_at', [])
    bulkmod_op = app.form.get_input_value('bulkmod_op', [])
    bulkmod_av = app.form.get_input_value('bulkmod_av', [])

    bulkmod_cp = app.form.get_input_value('bulkmod_cp', [''])[0] == 'yes'

    scope = int(app.form.get_input_value('scope', [str(app.ldap_url.scope or ldap0.SCOPE_BASE)])[0])

    bulkmod_filter = app.form.get_input_value(
        'filterstr',
        [(app.ldap_url.filterstr or '')]
    )[0] or '(objectClass=*)'
    bulkmod_newsuperior = app.form.get_input_value('bulkmod_newsuperior', [''])[0]

    # Generate a list of requested LDAPv3 extended controls to be sent along
    # with the modify requests
    bulkmod_ctrl_oids = app.form.get_input_value('bulkmod_ctrl', [])

    if not len(bulkmod_at) == len(bulkmod_op) == len(bulkmod_av):
        raise ErrorExit('Invalid bulk modification input.')

    bulk_mod_list, input_errors = input_modlist(
        app,
        bulkmod_at, bulkmod_op, bulkmod_av,
    )

    if bulkmod_submit == 'Cancel':

        app.simple_message(
            'Canceled bulk modification.',
            '<p class="SuccessMessage">Canceled bulk modification.</p>',
            main_menu_list=main_menu(app),
        )

    elif not (bulk_mod_list or bulkmod_newsuperior) or \
         input_errors or \
         bulkmod_submit is None or \
         bulkmod_submit == '<<Back' or \
         bulkmod_submit.startswith('+') or \
         bulkmod_submit.startswith('-'):

        bulkmod_input_form(
            app,
            bulkmod_submit,
            app.dn, scope, bulkmod_filter,
            bulkmod_newsuperior,
            bulkmod_at, bulkmod_op, bulkmod_av, bulkmod_cp,
            input_errors
        )

    elif bulkmod_submit == 'Next>>':

        bulkmod_confirmation_form(
            app,
            app.dn, scope, bulkmod_filter,
            bulkmod_newsuperior, bulk_mod_list, bulkmod_cp,
        )

    elif bulkmod_submit == 'Apply':

        # now gather list of extended controls to be used with search request
        bulkmod_ctrl_oids = app.form.get_input_value('bulkmod_ctrl', [])
        conn_server_ctrls = {
            server_ctrl.controlType
            for server_ctrl in app.ls.l.req_ctrls['**all**']+app.ls.l.req_ctrls['**write**']+app.ls.l.req_ctrls['modify']
        }
        bulkmod_server_ctrls = list({
            ldap0.controls.LDAPControl(ctrl_oid, True, None)
            for ctrl_oid in bulkmod_ctrl_oids
            if ctrl_oid and ctrl_oid not in conn_server_ctrls
        }) or None

        ldap_error_html = []

        begin_time_stamp = time.time()
        modify_success_count = modrdn_success_count = 0
        modify_error_count = modrdn_error_count = 0

        # search the entries to be modified
        ldap_msgid = app.ls.l.search(
            app.dn,
            scope,
            bulkmod_filter,
            attrlist=['*'] if bulkmod_cp else ['1.1'],
        )

        result_ldif_html = []

        # not collect the DNs of the entries to be modified from search results
        for res in app.ls.l.results(ldap_msgid):

            # Real entry?
            if res.rtype == ldap0.RES_SEARCH_REFERENCE:
                # ignore search continuations
                continue

            for rdat in res.rdata:

                # Apply the modify request
                if bulk_mod_list:
                    try:
                        app.ls.l.modify_s(rdat.dn_s, bulk_mod_list, req_ctrls=bulkmod_server_ctrls)
                    except ldap0.LDAPError as err:
                        modify_error_count += 1
                        ldap_error_html.append(
                            '<dt>%s</dt><dd>%s</dd>' % (
                                app.form.s2d(rdat.dn_s),
                                app.ldap_error_msg(err),
                            )
                        )
                    else:
                        modify_success_count += 1
                        result_ldif_html.append(modlist_ldif(
                            rdat.dn_s, app.form, bulk_mod_list
                        ))

                # Apply the modrdn request
                if bulkmod_newsuperior:
                    old_rdn = str(DNObj.from_str(rdat.dn_s).rdn())
                    try:
                        if bulkmod_cp:
                            new_ldap_dn = ','.join((
                                old_rdn,
                                bulkmod_newsuperior,
                            ))
                            if not rdat.entry_b:
                                raise ldap0.NO_SUCH_OBJECT
                            app.ls.l.add_s(new_ldap_dn, rdat.entry_as)
                        else:
                            app.ls.rename(
                                rdat.dn_s,
                                old_rdn,
                                new_superior=bulkmod_newsuperior,
                                delold=app.cfg_param('bulkmod_delold', 0),
                            )
                    except ldap0.LDAPError as err:
                        modrdn_error_count += 1
                        ldap_error_html.append(
                            '<dt>%s</dt><dd>%s</dd>' % (
                                app.form.s2d(rdat.dn_s),
                                app.form.s2d(str(err)),
                            )
                        )
                    else:
                        modrdn_success_count += 1
                        result_ldif_html.append(
                            '<p>%s %s beneath %s</p>' % (
                                {False:'Moved', True:'Copied'}[bulkmod_cp],
                                app.form.s2d(rdat.dn_s),
                                app.form.s2d(bulkmod_newsuperior),
                            )
                        )

        end_time_stamp = time.time()

        error_messages = ''
        if ldap_error_html:
            error_messages = '<strong>Errors</strong><dl>%s</dl>' % (
                '\n'.join(ldap_error_html),
            )
        change_records = ''
        if result_ldif_html:
            change_records = '<strong>Successfully applied changes</strong><p>%s</p>' % (
                '\n'.join(result_ldif_html),
            )

        app.simple_message(
            'Modified entries',
            BULKMOD_MESSAGE_TMPL.format(
                # modify operations
                num_modify_success_count=modify_success_count,
                num_modify_error_count=modify_error_count,
                num_all_modify_count=modify_success_count+modify_error_count,
                # modrdn operations
                num_modrdn_success_count=modrdn_success_count,
                num_modrdn_error_count=modrdn_error_count,
                num_all_modrdn_count=modrdn_success_count+modrdn_error_count,
                # other stuff
                text_dn=app.display_dn(app.dn),
                text_scope=ldap0.ldapurl.SEARCH_SCOPE_STR[scope],
                num_elapsed_time=end_time_stamp-begin_time_stamp,
                text_form_begin=app.begin_form('bulkmod', 'POST'),
                text_fields=app.form.hidden_input_html(ignored_fields=['bulkmod_submit']),
                text_errors=error_messages,
                text_changes=change_records,
            ),
            main_menu_list=main_menu(app),
        )

    else:

        raise ErrorExit('Invalid bulk modification form data.')

    # end of w2l_bulkmod()
