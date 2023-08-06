# -*- coding: ascii -*-
"""
web2ldap.app.schema.viewer -  Display LDAPv3 schema

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import ldap0

from ldap0.schema.subentry import (
    SCHEMA_ATTRS,
    SCHEMA_ATTR_MAPPING,
    SCHEMA_CLASS_MAPPING,
)
from ldap0.schema.models import (
    LDAPSyntax,
    AttributeType,
    ObjectClass,
    MatchingRule,
    MatchingRuleUse,
    DITContentRule,
    DITStructureRule,
    NameForm,
    OBJECTCLASS_KIND_STR,
)

from .. import ErrorExit
from ..gui import (
    footer,
    main_menu,
    top_section,
)
from ..form import OIDInput
from ..searchform import SEARCH_OPT_ATTR_EXISTS, SEARCH_OPT_IS_EQUAL
from . import OBSOLETE_TEMPL, schema_link_text, schema_anchor
from .syntaxes import syntax_registry

SCHEMA_VIEWER_USAGE = """
<p>Hints:</p>
<ul>
  <li>You can search for schema elements by OID or name.</li>
  <li>Wildcard search with * is supported.</li>
  <li>For browsing choose from context menu on the right</li>
</ul>
"""

SCHEMA_ELEMENT_HEAD_TMPL = """
%s
<h1>%s <em>%s</em> (%s)</h1>
Try to look it up:
<a id="alvestrand_oid" href="%s?https://www.alvestrand.no/objectid/%s.html">[Alvestrand]</a>
<a id="oid-info_oid" href="%s?http://www.oid-info.com/get/%s">[oid-info.com]</a>
<dl>
<dt>Schema element string:</dt>
<dd><code>%s</code></dd>
%s
</dl>
"""


def schema_anchors(app, se_names, se_class):
    link_texts = []
    for se_nameoroid in se_names:
        try:
            se_obj = app.schema.get_obj(se_class, se_nameoroid, default=None, raise_keyerror=True)
        except KeyError:
            link_texts.append((se_nameoroid, se_nameoroid))
            continue
        ltxt = schema_link_text(se_obj)
        try:
            schema_id = se_obj.oid
        except AttributeError:
            schema_id = se_obj.ruleid
        anchor = app.anchor(
            'oid', ltxt,
            [
                ('dn', app.dn),
                ('oid', schema_id),
                ('oid_class', SCHEMA_ATTR_MAPPING[se_class]),
            ],
        )
        link_texts.append((ltxt, anchor))
    link_texts.sort(key=lambda x: x[0].lower())
    return [i[1] for i in link_texts]


def schema_tree_html(app, schema, se_class, se_tree, se_oid, level):
    """
    returns HTML for displaying a schema descriptions inheritance tree
    """
    app.outf.write('<dl>')
    se_obj = schema.get_obj(se_class, se_oid)
    if se_obj is not None:
        display_id = (se_obj.names or (se_oid,))[0]
        app.outf.write(schema_anchor(app, display_id, se_class, name_template='<dt>{anchor}</dt>'))
    if se_tree[se_oid]:
        app.outf.write('<dd>')
        for sub_se_oid in se_tree[se_oid]:
            schema_tree_html(app, schema, se_class, se_tree, sub_se_oid, level+1)
        app.outf.write('</dd>')
    else:
        app.outf.write('<dd></dd>')
    app.outf.write('</dl>')
    # end of schema_tree_html()


def schema_context_menu(app):
    """Build context menu with schema-related items"""
    context_menu_list = []
    sub_schema_dn = None
    try:
        sub_schema_dn = app.ls.l.search_subschemasubentry_s(app.dn)
    except ldap0.LDAPError:
        pass
    else:
        if sub_schema_dn is not None:
            form_param_list = [
                ('dn', sub_schema_dn),
                ('filterstr', '(objectClass=subschema)'),
            ]
            for schema_attr in SCHEMA_ATTRS+['objectClass', 'cn']:
                form_param_list.append(('read_attr', schema_attr))
            context_menu_list.append(
                app.anchor(
                    'read', 'Subschema Subentry',
                    form_param_list,
                    title='Directly read the subschema subentry'),
                )
        if app.schema:
            se_class_attrs = [
                SCHEMA_ATTR_MAPPING[se_class]
                for se_class in app.schema.sed.keys()
                if app.schema.sed[se_class]
            ]
            se_class_attrs.sort(key=str.lower)
            for se_class_attr in se_class_attrs:
                context_menu_list.append(
                    app.anchor(
                        'oid', se_class_attr,
                        [('dn', app.dn), ('oid_class', se_class_attr)],
                        title='Browse all %s' % (se_class_attr,),
                    )
                )
    return context_menu_list


class DisplaySchemaElement:
    type_desc = 'Abstract Schema Element'
    detail_attrs = ()

    def __init__(self, app, se_obj):
        self._app = app
        self._schema = app.schema
        self._se = se_obj
        try:
            schema_id = self._se.oid
        except AttributeError:
            schema_id = self._se.ruleid
        self._sei = app.schema.get_inheritedobj(self._se.__class__, schema_id, [])

    def disp_details(self):
        for text, class_attr, se_class in self.detail_attrs:
            class_attr_value = getattr(self._sei, class_attr, None)
            if class_attr_value is None:
                continue
            if isinstance(class_attr_value, (tuple, list)):
                class_attr_value_list = list(class_attr_value)
                class_attr_value_list.sort(key=str.lower)
            else:
                class_attr_value_list = [class_attr_value]
            if se_class is None:
                value_output = ', '.join([
                    self._app.form.s2d(v, sp_entity=' ', lf_entity='<br>')
                    for v in class_attr_value_list
                ])
            else:
                value_output = ', '.join(
                    schema_anchors(self._app, class_attr_value_list, se_class)
                )
            self._app.outf.write('<dt>%s</dt>\n<dd>\n%s\n</dd>\n' % (text, value_output))
        # end of disp_details()

    def display(self):
        ms_ad_schema_link = ''
        if 'schemaNamingContext' in self._app.ls.root_dse:
            try:
                result = self._app.ls.l.search_s(
                    self._app.ls.root_dse['schemaNamingContext'][0].decode(self._app.ls.charset),
                    ldap0.SCOPE_SUBTREE,
                    (
                        '(|'
                        '(&(objectClass=attributeSchema)(attributeID=%s))'
                        '(&(objectClass=classSchema)(governsID=%s))'
                        ')'
                    ) % (
                        self._se.oid,
                        self._se.oid,
                    ),
                    attrlist=['cn']
                )
            except ldap0.LDAPError:
                pass
            else:
                if result:
                    ad_schema_dn, ad_schema_entry = result[0].dn_s, result[0].entry_s
                    ms_ad_schema_link = (
                        '<dt>Schema Definition Entry (MS AD)</dt>\n'
                        '<dd>\n%s\n</dd>\n'
                    ) % (
                        self._app.anchor(
                            'read', ad_schema_entry['cn'][0],
                            [('dn', ad_schema_dn)],
                        )
                    )
        obsolete = getattr(self._se, 'obsolete', 0)
        top_section(
            self._app,
            '%s %s (%s)' % (
                self.type_desc,
                ', '.join(
                    getattr(self._se, 'names', (()))
                ),
                self._se.oid
            ),
            main_menu(self._app),
            context_menu_list=schema_context_menu(self._app)
        )
        self._app.outf.write(
            SCHEMA_ELEMENT_HEAD_TMPL % (
                oid_input_form(self._app, ''),
                self.type_desc,
                OBSOLETE_TEMPL[obsolete] % (
                    ', '.join(getattr(self._se, 'names', (()))),
                ),
                self._se.oid,
                self._app.form.action_url('urlredirect', self._app.sid), self._se.oid,
                self._app.form.action_url('urlredirect', self._app.sid), self._se.oid,
                self._app.form.s2d(str(self._se)),
                ms_ad_schema_link,
            )
        )
        self.disp_details()
        footer(self._app)


class DisplayObjectClass(DisplaySchemaElement):
    type_desc = 'Object class'
    detail_attrs = (
        ('Description', 'desc', None),
        ('Derived from', 'sup', ObjectClass),
    )

    def __init__(self, app, se):
        DisplaySchemaElement.__init__(self, app, se)
        self._sei = app.schema.get_inheritedobj(self._se.__class__, self._se.oid, ['kind'])

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        must, may = self._schema.attribute_types([self._se.oid], raise_keyerror=False)
        # Display all required and allowed attributes
        self._app.outf.write('<dt>Kind of object class:</dt><dd>\n%s&nbsp;</dd>\n' % (
            OBJECTCLASS_KIND_STR[self._sei.kind],
        ))
        # Display all required and allowed attributes
        self._app.outf.write('<dt>All required attributes:</dt><dd>\n%s&nbsp;</dd>\n' % (
            ', '.join(schema_anchors(self._app, must.keys(), AttributeType)),
        ))
        self._app.outf.write('<dt>All allowed attributes:</dt><dd>\n%s&nbsp;</dd>\n' % (
            ', '.join(schema_anchors(self._app, may.keys(), AttributeType)),
        ))
        # Display relationship to DIT content rule(s)
        # normally only in case of a STRUCTURAL object class)
        content_rule = self._schema.get_obj(DITContentRule, self._se.oid)
        if content_rule:
            self._app.outf.write(
                '<dt>Governed by DIT content rule:</dt><dd>\n%s&nbsp;</dd>\n' % (
                    schema_anchor(self._app, content_rule.oid, DITContentRule),
                )
            )
            self._app.outf.write(
                '<dt>Applicable auxiliary object classes:</dt><dd>\n%s&nbsp;</dd>\n' % (
                    ', '.join(schema_anchors(self._app, content_rule.aux, ObjectClass)),
                )
            )
        # normally only in case of a AUXILIARY object class
        dcr_list = []
        structural_oc_list = []
        for _, content_rule in self._schema.sed[DITContentRule].items():
            for aux_class_name in content_rule.aux:
                aux_class_oid = self._schema.get_oid(ObjectClass, aux_class_name)
                if aux_class_oid == self._se.oid:
                    dcr_list.append(content_rule.oid)
                    structural_oc_list.append(content_rule.oid)
        if dcr_list:
            self._app.outf.write(
                '<dt>Referring DIT content rules:</dt><dd>\n%s&nbsp;</dd>\n' % (
                    ', '.join(schema_anchors(self._app, dcr_list, DITContentRule)),
                )
            )
        if structural_oc_list:
            self._app.outf.write(
                '<dt>Allowed with structural object classes:</dt><dd>\n%s&nbsp;</dd>\n' % (
                    ', '.join(schema_anchors(self._app, structural_oc_list, ObjectClass)),
                )
            )
        # Display name forms which regulates naming for this object class
        oc_ref_list = []
        for nf_oid, name_form_se in self._schema.sed[NameForm].items():
            name_form_oc = name_form_se.oc.lower()
            se_names = {o.lower() for o in self._sei.names}
            if name_form_se.oc == self._sei.oid or name_form_oc in se_names:
                oc_ref_list.append(nf_oid)
        if oc_ref_list:
            self._app.outf.write(
                '<dt>Applicable name forms:</dt>\n<dd>\n%s\n</dd>\n' % (
                    ', '.join(schema_anchors(self._app, oc_ref_list, NameForm)),
                )
            )
        # Display tree of derived object classes
        self._app.outf.write('<dt>Object class tree:</dt>\n')
        self._app.outf.write('<dd>\n')
        try:
            oc_tree = self._schema.tree(ObjectClass)
        except KeyError as err:
            self._app.outf.write(
                '<strong>Missing schema elements referenced:<pre>%s</pre></strong>\n' % (
                    self._app.form.s2d(err),
                )
            )
        else:
            if self._se.oid in oc_tree and oc_tree[self._se.oid]:
                schema_tree_html(self._app, self._schema, ObjectClass, oc_tree, self._se.oid, 0)
        self._app.outf.write('&nbsp;</dd>\n')
        # Display a link for searching entries by object class
        self._app.outf.write(
            '<dt>Search entries</dt>\n<dd>\n%s\n</dd>\n' % (
                self._app.anchor(
                    'searchform',
                    '(objectClass=%s)' % (
                        self._app.form.s2d((self._se.names or [self._se.oid])[0]),
                    ),
                    [
                        ('dn', self._app.dn),
                        ('searchform_mode', 'adv'),
                        ('search_attr', 'objectClass'),
                        ('search_option', SEARCH_OPT_IS_EQUAL),
                        ('search_string', (self._se.names or [self._se.oid])[0]),
                    ],
                    title='Search entries by object class',
                ),
            )
        )
        # end of disp_details()


class DisplayAttributeType(DisplaySchemaElement):
    type_desc = 'Attribute type'
    detail_attrs = (
        ('Description', 'desc', None),
        ('Syntax', 'syntax', LDAPSyntax),
        ('Derived from', 'sup', AttributeType),
        ('Equality matching rule', 'equality', MatchingRule),
        ('Sub-string matching rule', 'substr', MatchingRule),
        ('Ordering matching rule', 'ordering', MatchingRule),
    )

    def __init__(self, app, se):
        DisplaySchemaElement.__init__(self, app, se)
        try:
            self._sei = app.schema.get_inheritedobj(
                self._se.__class__, self._se.oid,
                ('syntax', 'equality', 'substr', 'ordering'),
            )
        except KeyError:
            # If the schema element referenced by SUP is not present
            self._sei = app.schema.get_obj(self._se.__class__, self._se.oid)

    def disp_details(self):

        DisplaySchemaElement.disp_details(self)

        at_oid = self._se.oid
        syntax_oid = self._sei.syntax

        self._app.outf.write('<dt>Usage:</dt>\n<dd>\n%s\n</dd>\n' % (
            {
                0: 'userApplications',
                1: 'directoryOperation',
                2: 'distributedOperation',
                3: 'dSAOperation',
            }[self._se.usage],
        ))

        if syntax_oid is not None:

            # Display applicable matching rules
            #---------------------------------------------------------------
            mr_use_se = self._schema.get_obj(MatchingRuleUse, syntax_oid)
            applies_dict = {}
            for mr_oid, mr_use_se in self._schema.sed[MatchingRuleUse].items():
                applies_dict[mr_oid] = {}
                mr_use_se = self._schema.get_obj(MatchingRuleUse, mr_oid)
                for at_nameoroid in mr_use_se.applies:
                    applies_dict[mr_oid][self._schema.get_oid(AttributeType, at_nameoroid)] = None
            # Display list of attribute types for which this matching rule is applicable
            mr_applicable_for = [
                mr_oid
                for mr_oid in self._schema.sed[MatchingRule].keys()
                if mr_oid in applies_dict and at_oid in applies_dict[mr_oid]
            ]
            if mr_applicable_for:
                self._app.outf.write('<dt>Applicable matching rules:</dt>\n<dd>\n%s\n</dd>\n' % (
                    ', '.join(
                        schema_anchors(self._app, mr_applicable_for, MatchingRule)
                    ),
                ))

        # Display DIT content rules which reference attributes of this type
        #-------------------------------------------------------------------
        attr_type_ref_list = []
        for oc_oid, object_class_se in self._schema.sed[ObjectClass].items():
            object_class_se = self._schema.get_obj(ObjectClass, oc_oid)
            for dcr_at in object_class_se.must+object_class_se.may:
                if dcr_at == at_oid or dcr_at in self._sei.names:
                    attr_type_ref_list.append(oc_oid)
        if attr_type_ref_list:
            self._app.outf.write(
                '<dt>Directly referencing object classes:</dt>\n<dd>\n%s\n</dd>\n' % (
                    ', '.join(schema_anchors(self._app, attr_type_ref_list, ObjectClass)),
                )
            )

        # Display object classes which may contain attributes of this type
        #-------------------------------------------------------------------
        all_object_classes = self._schema.sed[ObjectClass].keys()
        attr_type_ref_list = []
        for oc_oid in all_object_classes:
            must, may = self._schema.attribute_types([oc_oid], raise_keyerror=False)
            if at_oid in must or at_oid in may:
                attr_type_ref_list.append(oc_oid)
        if attr_type_ref_list:
            self._app.outf.write(
                '<dt>Usable in these object classes:</dt>\n<dd>\n%s\n</dd>\n' % (
                    ', '.join(schema_anchors(self._app, attr_type_ref_list, ObjectClass)),
                )
            )

        # Display DIT content rules which reference attributes of this type
        #-------------------------------------------------------------------
        attr_type_ref_list = []
        for dcr_oid, dit_content_rule_se in self._schema.sed[DITContentRule].items():
            dit_content_rule_se = self._schema.get_obj(DITContentRule, dcr_oid)
            for dcr_at in dit_content_rule_se.must+dit_content_rule_se.may+dit_content_rule_se.nots:
                if dcr_at == at_oid or dcr_at in self._sei.names:
                    attr_type_ref_list.append(dcr_oid)
        if attr_type_ref_list:
            self._app.outf.write('<dt>Referencing DIT content rules:</dt>\n<dd>\n%s\n</dd>\n' % (
                ', '.join(schema_anchors(self._app, attr_type_ref_list, DITContentRule)),
            ))

        # Display name forms which uses this attribute type for naming an entry
        #-----------------------------------------------------------------------
        attr_type_ref_list = []
        for nf_oid, name_form_se in self._schema.sed[NameForm].items():
            name_form_se = self._schema.get_obj(NameForm, nf_oid)
            for nf_at in name_form_se.must+name_form_se.may:
                if nf_at == at_oid or nf_at in self._sei.names:
                    attr_type_ref_list.append(nf_oid)
        if attr_type_ref_list:
            self._app.outf.write('<dt>Referencing name forms:</dt>\n<dd>\n%s\n</dd>\n' % (
                ', '.join(schema_anchors(self._app, attr_type_ref_list, NameForm)),
            ))

        #########################################
        # Output attribute type inheritance tree
        #########################################
        self._app.outf.write('<dt>Attribute type tree:</dt>\n<dd>\n')
        # Display tree of derived attribute types
        try:
            at_tree = self._schema.tree(AttributeType)
        except KeyError as err:
            self._app.outf.write(
                '<strong>Missing schema elements referenced:<pre>%s</pre></strong>\n' % (
                    self._app.form.s2d(err),
                )
            )
        else:
            if at_oid in at_tree and at_tree[at_oid]:
                schema_tree_html(self._app, self._schema, AttributeType, at_tree, at_oid, 0)
        # Display a link for searching entries by attribute presence
        self._app.outf.write(
            '</dd>\n<dt>Search entries</dt>\n<dd>\n%s\n</dd>\n' % (
                self._app.anchor(
                    'searchform',
                    '(%s=*)' % (
                        self._app.form.s2d((self._se.names or [self._se.oid])[0]),
                    ),
                    [
                        ('dn', self._app.dn),
                        ('searchform_mode', 'adv'),
                        ('search_attr', (self._se.names or [self._se.oid])[0]),
                        ('search_option', SEARCH_OPT_ATTR_EXISTS),
                        ('search_string', ''),
                    ],
                    title='Search entries by attribute presence',
                ),
            )
        )

        #########################################
        # Output registered plugin class name
        #########################################
        self._app.outf.write("""
          <dt>Associated plugin class(es):</dt>
          <dd>
            <table>
              <tr><th>Structural<br>object class</th><th>Plugin class</th>""")
        for structural_oc in (syntax_registry.at2syntax[at_oid].keys() or [None]):
            syntax_class = syntax_registry.get_syntax(
                self._schema,
                at_oid,
                structural_oc,
            )
            if structural_oc:
                oc_text = schema_anchor(self._app, structural_oc, ObjectClass)
            else:
                oc_text = '-any-'
            self._app.outf.write('<tr><td>%s</td><td>%s.%s</td></th>\n' % (
                oc_text,
                self._app.form.s2d(syntax_class.__module__),
                self._app.form.s2d(syntax_class.__name__),
            ))
        self._app.outf.write('</table>\n</dd>\n')
        # end of disp_details()


class DisplayLDAPSyntax(DisplaySchemaElement):
    type_desc = 'LDAP Syntax'
    detail_attrs = (
        ('Description', 'desc', None),
    )

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        # Display list of attribute types which directly reference this syntax
        syntax_using_at_list = [
            at_oid
            for at_oid in self._schema.sed[AttributeType].keys()
            if self._schema.get_syntax(at_oid) == self._se.oid
        ]
        if syntax_using_at_list:
            self._app.outf.write('<dt>Referencing attribute types:</dt>\n<dd>\n%s\n</dd>\n' % (
                ', '.join(schema_anchors(self._app, syntax_using_at_list, AttributeType))
            ))
        syntax_ref_mr_list = self._schema.listall(MatchingRule, [('syntax', self._se.oid)])
        if syntax_ref_mr_list:
            self._app.outf.write('<dt>Referencing matching rules:</dt>\n<dd>\n%s\n</dd>\n' % (
                ', '.join(schema_anchors(self._app, syntax_ref_mr_list, MatchingRule))
            ))
        try:
            x_subst = self._se.x_subst
        except AttributeError:
            pass
        else:
            if x_subst:
                self._app.outf.write('<dt>Substituted by:</dt>\n<dd>\n%s\n</dd>\n' % (
                    schema_anchor(self._app, x_subst, LDAPSyntax)
                ))
        #########################################
        # Output registered plugin class name
        #########################################
        syntax_class = syntax_registry.oid2syntax.get(self._se.oid, LDAPSyntax)
        self._app.outf.write('<dt>Associated syntax class</dt>\n<dd>\n%s\n</dd>\n' % (
            '.'.join((syntax_class.__module__, syntax_class.__name__))
        ))
        # end of disp_details()


class DisplayMatchingRule(DisplaySchemaElement):
    type_desc = 'Matching Rule'
    detail_attrs = (
        ('Description', 'desc', None),
        ('LDAP syntax', 'syntax', LDAPSyntax),
    )

    def disp_details(self):
        DisplaySchemaElement.disp_details(self)
        mr_use_se = self._schema.get_obj(MatchingRuleUse, self._se.oid)
        if mr_use_se:
            applies_dict = {}
            for at_nameoroid in mr_use_se.applies:
                applies_dict[self._schema.get_oid(AttributeType, at_nameoroid)] = None
            # Display list of attribute types for which this matching rule is applicable
            mr_applicable_for = [
                at_oid
                for at_oid in self._schema.sed[AttributeType].keys()
                if at_oid in applies_dict
            ]
            if mr_applicable_for:
                self._app.outf.write(
                    (
                        '<dt>Applicable for attribute types per matching rule use:</dt>\n'
                        '<dd>\n%s\n</dd>\n'
                    ) % (
                        ', '.join(schema_anchors(self._app, mr_applicable_for, AttributeType)),
                    )
                )
        mr_used_by = []
        mr_names = set(self._se.names)
        for at_oid in self._schema.sed[AttributeType]:
            try:
                at_se = self._schema.get_inheritedobj(
                    AttributeType,
                    at_oid,
                    ('equality', 'substr', 'ordering'),
                )
            except KeyError:
                continue
            if at_se is None:
                continue
            at_mr_set = {at_se.equality, at_se.substr, at_se.ordering}
            if (
                    at_se.equality in mr_names or
                    at_se.substr in mr_names or
                    at_se.ordering in mr_names or
                    self._se.oid in at_mr_set
                ):
                mr_used_by.append(at_se.oid)
        if mr_used_by:
            self._app.outf.write('<dt>Referencing attribute types:</dt>\n<dd>\n%s\n</dd>\n' % (
                ', '.join(schema_anchors(self._app, mr_used_by, AttributeType))
            ))
        # end of disp_details()


class DisplayMatchingRuleUse(DisplaySchemaElement):
    type_desc = 'Matching Rule Use'
    detail_attrs = (
        ('Names', 'names', None),
        ('Matching Rule', 'oid', MatchingRule),
        ('Applies to', 'applies', AttributeType),
    )


class DisplayDITContentRule(DisplaySchemaElement):
    type_desc = 'DIT content rule'
    detail_attrs = (
        ('Names', 'names', None),
        ('Governs structural object class', 'oid', ObjectClass),
        ('Auxiliary classes', 'aux', ObjectClass),
        ('Must have', 'must', AttributeType),
        ('May have', 'may', AttributeType),
        ('Must not have', 'nots', AttributeType),
    )


class DisplayDITStructureRule(DisplaySchemaElement):
    type_desc = 'DIT structure rule'
    detail_attrs = (
        ('Description', 'desc', None),
        ('Associated name form', 'form', NameForm),
        ('Superior structure rules', 'sup', DITStructureRule),
    )

    def display(self):
        top_section(
            self._app,
            '%s %s (%s)' % (
                self.type_desc,
                ', '.join(
                    getattr(self._se, 'names', (()))
                ),
                self._se.ruleid
            ),
            main_menu(self._app),
            context_menu_list=schema_context_menu(self._app)
        )
        self._app.outf.write(
            """
            %s
            <h1>%s <em>%s</em> (%s)</h1>
            <dl>
            <dt>Schema element string:</dt>
            <dd><code>%s</code></dd>
            </dl>
            """ % (
                oid_input_form(self._app, ''),
                self.type_desc,
                ", ".join(
                    getattr(self._se, 'names', (()))
                ),
                self._se.ruleid,
                self._app.form.s2d(str(self._se)),
            )
        )
        self.disp_details()
        footer(self._app)

    def disp_details(self):
        """
        Display subordinate DIT structure rule(s)
        """
        DisplaySchemaElement.disp_details(self)
        ditsr_rules_ref_list = []
        for ditsr_id, ditsr_se in self._schema.sed[DITStructureRule].items():
            if self._sei.ruleid in ditsr_se.sup:
                ditsr_rules_ref_list.append(ditsr_id)
        if ditsr_rules_ref_list:
            self._app.outf.write('<dt>Subordinate DIT structure rules:</dt>\n<dd>\n%s\n</dd>\n' % (
                ', '.join(schema_anchors(self._app, ditsr_rules_ref_list, DITStructureRule))
            ))
        # end of disp_details()


class DisplayNameForm(DisplaySchemaElement):
    type_desc = 'Name form'
    detail_attrs = (
        ('Description', 'desc', None),
        ('Structural object class this rule applies to', 'oc', ObjectClass),
        ('Mandantory naming attributes', 'must', AttributeType),
        ('Allowed naming attributes', 'may', AttributeType),
    )

    def disp_details(self):
        """
        Display referencing DIT structure rule(s)
        """
        DisplaySchemaElement.disp_details(self)
        ditsr_rules_ref_list = []
        for ditsr_id, ditsr_se in self._schema.sed[DITStructureRule].items():
            if ditsr_se.form == self._sei.oid or ditsr_se.form in self._sei.names:
                ditsr_rules_ref_list.append(ditsr_id)
        if ditsr_rules_ref_list:
            self._app.outf.write('<dt>Referencing DIT structure rule:</dt>\n<dd>\n%s\n</dd>\n' % (
                ', '.join(schema_anchors(self._app, ditsr_rules_ref_list, DITStructureRule))
            ))
        # end of disp_details()


SCHEMA_VIEWER_CLASS = {
    ObjectClass: DisplayObjectClass,
    AttributeType: DisplayAttributeType,
    LDAPSyntax: DisplayLDAPSyntax,
    MatchingRule: DisplayMatchingRule,
    MatchingRuleUse: DisplayMatchingRuleUse,
    DITContentRule: DisplayDITContentRule,
    DITStructureRule: DisplayDITStructureRule,
    NameForm: DisplayNameForm,
}


def oid_input_form(app, oid=None):
    oid_input_field_html = OIDInput(
        'oid',
        'OID or descriptive name of schema element',
        default=oid
    ).input_html(oid)
    oid_class_select_html = app.form.field['oid_class'].input_html('')
    return app.form_html(
        'oid', 'Search', 'GET',
        [('dn', app.dn)],
        extrastr='\n'.join((oid_input_field_html, oid_class_select_html)),
    )


def display_schema_elements(app, se_classes, se_list):
    se_list = se_list or []
    se_classes = tuple(filter(None, se_classes or []) or SCHEMA_CLASS_MAPPING.values())

    top_section(
        app,
        'Schema elements',
        main_menu(app),
        context_menu_list=schema_context_menu(app)
    )

    if app.schema is None:
        raise ErrorExit('No sub schema available!')

    oid_dict = {}
    if se_list:
        for schema_class in se_classes:
            oid_dict[schema_class] = []
        for se_obj in se_list:
            try:
                se_id = se_obj.oid
            except AttributeError:
                se_id = se_obj.ruleid
            try:
                oid_dict[se_obj.__class__].append(se_id)
            except KeyError:
                oid_dict[se_obj.__class__] = [se_id]
    else:
        for schema_class in se_classes:
            oid_dict[schema_class] = app.schema.sed[schema_class].keys()
    app.outf.write(oid_input_form(app, ''))

    if oid_dict:
        for schema_class, schema_elements in oid_dict.items():
            if not schema_elements:
                continue
            app.outf.write('<h2>%s</h2>\n<p>found %d</p>\n%s\n' % (
                SCHEMA_VIEWER_CLASS[schema_class].type_desc,
                len(schema_elements),
                ',\n '.join(schema_anchors(app, schema_elements, schema_class)),
            ))
    else:
        app.outf.write(SCHEMA_VIEWER_USAGE)
    footer(app)
    # end of display_schema_elements()


def w2l_schema_viewer(app):

    def contains_oid(val, oid):
        return val.__contains__(oid)

    def startswith_oid(val, oid):
        return val.startswith(oid)

    def endswith_oid(val, oid):
        return val.endswith(oid)

    # Get input parameter from form input
    oid = app.form.get_input_value('oid', [None])[0]
    se_classes = [
        SCHEMA_CLASS_MAPPING[se_name]
        for se_name in app.form.get_input_value('oid_class', [])
        if se_name
    ]

    if not oid:
        # Display entry page of schema browser
        display_schema_elements(app, se_classes, None)
        return

    # Sanitize oid
    oid = oid.strip()
    if oid.lower().endswith(';binary'):
        oid = oid[:-7]

    # Determine the matching method, e.g. for wildcard search
    if oid.startswith('*') and oid.endswith('*'):
        oid_mv = oid[1:-1].lower()
        cmp_method = contains_oid
    elif oid.startswith('*'):
        oid_mv = oid[1:].lower()
        cmp_method = endswith_oid
    elif oid.endswith('*'):
        oid_mv = oid[:-1].lower()
        cmp_method = startswith_oid
    else:
        cmp_method = None

    if len(se_classes) == 1 and cmp_method is None:
        # Display a single schema element referenced by OID and class
        se_list = []
        se_obj = app.schema.get_obj(se_classes[0], oid, None)
        if se_obj is not None:
            se_list.append(se_obj)
    else:
        # Search schema element by OID
        se_list = []
        if cmp_method is None:
            # No wildcard search => just try to look up directly via name or OID
            for schema_element_type in se_classes or SCHEMA_VIEWER_CLASS.keys():
                try:
                    se_obj = app.schema.get_obj(schema_element_type, oid, None, raise_keyerror=True)
                except KeyError:
                    pass
                else:
                    se_list.append(se_obj)
        else:
            # Do a wildcard search
            for schema_element_type in se_classes or SCHEMA_VIEWER_CLASS.keys():
                for se_obj in app.schema.sed[schema_element_type].values():
                    try:
                        se_id = se_obj.oid
                    except AttributeError:
                        se_id = se_obj.ruleid
                    if cmp_method(se_id.lower(), oid_mv):
                        # OID matched
                        se_list.append(se_obj)
                    else:
                        # Look whether a value of NAMEs match
                        try:
                            se_names = se_obj.names
                        except AttributeError:
                            continue
                        for se_name in se_names or []:
                            if cmp_method(se_name.lower(), oid_mv):
                                se_list.append(se_obj)
                                break

    if not se_list:
        # Display error message with input form
        app.simple_message(
            title='',
            message=(
                '<h1>Schema elements</h1><p class="ErrorMessage">'
                'Name or OID not found in schema!</p><p>%s</p>'
            ) % (
                oid_input_form(app, oid),
            ),
            main_div_id='Message',
            main_menu_list=main_menu(app),
            context_menu_list=schema_context_menu(app)
        )
        return
    if len(se_list) > 1:
        # Display a list of schema elements to choose from
        display_schema_elements(app, None, se_list)
        return

    # Directly display a single schema element
    se_obj = se_list[0]
    if se_obj.__class__ not in SCHEMA_VIEWER_CLASS:
        raise ErrorExit('No viewer for this type of schema element!')
    schema_viewer = SCHEMA_VIEWER_CLASS[se_obj.__class__](app, se_obj)
    schema_viewer.display()
