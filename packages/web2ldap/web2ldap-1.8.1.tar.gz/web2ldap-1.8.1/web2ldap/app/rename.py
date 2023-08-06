# -*- coding: ascii -*-
"""
web2ldap.app.rename: modify DN of an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

from typing import Dict

import ldap0
import ldap0.ldapurl
import ldap0.filter

from ..web import forms
from .schema.viewer import schema_anchors
from . import ErrorExit
from .form import DistinguishedNameInput
from .schema.syntaxes import DynamicDNSelectList
from .gui import context_menu_single_entry, footer, main_menu, top_section
from .gui import read_template, search_root_field


def new_superior_field(app, sup_search_url, old_superior_dn):
    """
    returns Select field for choosing a new superior entry
    """

    class NewSuperiorSelectList(DynamicDNSelectList):
        """
        plugin class for choosing a new superior entry
        """
        attr_value_dict: Dict[str, str] = {
            '': '- Root Naming Context -',
        }

        def __init__(self, app, dn, schema, attr_type, attr_value, ldap_url):
            self.ldap_url = ldap_url
            DynamicDNSelectList.__init__(self, app, dn, schema, attr_type, attr_value, entry=None)

    if not sup_search_url is None:
        attr_inst = NewSuperiorSelectList(
            app, app.dn,
            app.schema, 'rdn', old_superior_dn.encode(app.ls.charset), str(sup_search_url),
        )
        nssf = attr_inst.input_field()
        nssf.name = 'rename_newsuperior'
        nssf.text = 'New Superior DN'
    else:
        nssf = DistinguishedNameInput('rename_newsuperior', 'New Superior DN')
    nssf.charset = app.form.accept_charset
    nssf.set_default(old_superior_dn)
    return nssf # new_superior_field()


def w2l_rename(app):
    """
    rename an entry
    """

    rename_supsearchurl_cfg = app.cfg_param('rename_supsearchurl', {})

    if not app.dn:
        raise ErrorExit('Rename operation not possible at - World - or RootDSE.')

    rename_newrdn = app.form.get_input_value('rename_newrdn', [None])[0]
    rename_newsuperior = app.form.get_input_value('rename_newsuperior', [None])[0]
    rename_delold = app.form.get_input_value('rename_delold', ['no'])[0] == 'yes'

    if rename_newrdn:

        # ---------------------------------------
        # Rename the entry based on user's input
        # ---------------------------------------

        # Modify the RDN
        old_dn = app.dn
        app.dn, entry_uuid = app.ls.rename(
            app.dn,
            rename_newrdn,
            rename_newsuperior,
            delold=rename_delold
        )
        app.simple_message(
            'Renamed/moved entry',
            """<p class="SuccessMessage">Renamed/moved entry.</p>
            <dl><dt>Old name:</dt><dd>%s</dd>
            <dt>New name:</dt><dd>%s</dd></dl>""" % (
                app.display_dn(old_dn),
                app.display_dn(app.dn)
            ),
            main_menu_list=main_menu(app),
            context_menu_list=context_menu_single_entry(
                app, entry_uuid=entry_uuid
            ),
        )
        return

    # No input yet => output an input form
    #--------------------------------------

    old_rdn = str(app.dn_obj.rdn())
    old_superior = str(app.dn_obj.parent())

    app.form.field['rename_newrdn'].set_default(old_rdn)

    rename_template_str = read_template(app, 'rename_template', 'rename form')

    rename_supsearchurl = app.form.get_input_value('rename_supsearchurl', [None])[0]
    try:
        sup_search_url = ldap0.ldapurl.LDAPUrl(rename_supsearchurl_cfg[rename_supsearchurl])
    except KeyError:
        rename_newsupfilter = app.form.get_input_value('rename_newsupfilter', [None])[0]
        sup_search_url = ldap0.ldapurl.LDAPUrl()
        if rename_newsupfilter is not None:
            sup_search_url.urlscheme = 'ldap'
            sup_search_url.filterstr = (
                rename_newsupfilter or app.form.field['rename_newsupfilter'].default
            )
            sup_search_url.dn = app.form.get_input_value(
                'rename_searchroot',
                [''],
            )[0]
            sup_search_url.scope = int(
                app.form.get_input_value('scope', [str(ldap0.SCOPE_SUBTREE)])[0]
            )
        else:
            sup_search_url = None

    if not sup_search_url is None:
        if sup_search_url.dn in {'_', '..', '.'}:
            rename_searchroot_default = None
        else:
            rename_searchroot_default = sup_search_url.dn
        rename_newsupfilter_default = sup_search_url.filterstr
        scope_default = str(sup_search_url.scope)
    else:
        rename_searchroot_default = None
        rename_newsupfilter_default = app.form.field['rename_newsupfilter'].default
        scope_default = str(ldap0.SCOPE_SUBTREE)

    rename_search_root_field = search_root_field(app, name='rename_searchroot')
    rename_new_superior_field = new_superior_field(app, sup_search_url, old_superior)

    name_forms_text = ''
    dit_structure_rule_html = ''

    if app.schema.sed[ldap0.schema.models.NameForm]:
        # Determine if there are name forms defined for structural object class
        search_result = app.ls.l.read_s(
            app.dn,
            attrlist=['objectClass', 'structuralObjectClass', 'governingStructureRule'],
        )
        if not search_result:
            raise ErrorExit(
                'Empty search result when reading entry to be renamed.'
            )

        entry = ldap0.schema.models.Entry(app.schema, app.dn, search_result.entry_as)

        # Determine possible name forms for new RDN
        rdn_options = entry.get_rdn_templates()
        if rdn_options:
            name_forms_text = (
                '<p class="WarningMessage">Available name forms for RDN:<br>%s</p>'
            ) % (
                '<br>'.join(rdn_options)
            )
        # Determine LDAP search filter for building a select list for new superior DN
        # based on governing structure rule
        dit_structure_ruleids = entry.get_possible_dit_structure_rules(app.dn)
        for dit_structure_ruleid in dit_structure_ruleids:
            sup_structural_ruleids, sup_structural_oc = app.schema.get_superior_structural_oc_names(
                dit_structure_ruleid
            )
            if sup_structural_oc:
                rename_newsupfilter_default = '(|%s)' % (
                    ''.join([
                        '(objectClass=%s)' % (ldap0.filter.escape_str(oc))
                        for oc in sup_structural_oc
                    ])
                )
                dit_structure_rule_html = 'DIT structure rules:<br>%s' % (
                    '<br>'.join(
                        schema_anchors(
                            app,
                            sup_structural_ruleids,
                            ldap0.schema.models.DITStructureRule,
                        )
                    )
                )

    if rename_supsearchurl_cfg:
        rename_supsearchurl_field = forms.Select(
            'rename_supsearchurl',
            'LDAP URL for searching new superior entry',
            1,
            options=[],
        )
        rename_supsearchurl_field.set_options(rename_supsearchurl_cfg.keys())

    # Output empty input form for new RDN
    top_section(
        app,
        'Rename Entry',
        main_menu(app),
        context_menu_list=[],
    )

    app.outf.write(
        rename_template_str.format(
            form_begin=app.begin_form('rename', 'POST'),
            field_hidden_dn=app.form.hidden_field_html('dn', app.dn, ''),
            field_rename_newrdn=app.form.field['rename_newrdn'].input_html(),
            field_rename_new_superior=rename_new_superior_field.input_html(),
            text_name_forms=name_forms_text,
            field_rename_supsearchurl=rename_supsearchurl_field.input_html(),
            value_rename_newsupfilter=app.form.s2d(rename_newsupfilter_default),
            field_rename_search_root=rename_search_root_field.input_html(
                default=rename_searchroot_default,
            ),
            field_scope=app.form.field['scope'].input_html(default=scope_default),
            text_dit_structure_rule=dit_structure_rule_html,
        )
    )

    footer(app)
