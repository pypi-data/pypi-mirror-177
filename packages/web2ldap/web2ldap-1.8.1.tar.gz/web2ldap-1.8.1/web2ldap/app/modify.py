# -*- coding: ascii -*-
"""
web2ldap.app.modify: modify an entry

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

from io import BytesIO

import ldap0
import ldap0.ldif
import ldap0.schema
from ldap0.schema.models import AttributeType
from ldap0.schema.util import modify_modlist

from . import ErrorExit
from .schema.syntaxes import syntax_registry
from .add import ADD_IGNORE_ATTR_TYPES
from .addmodifyform import (
    cfg_constant_attributes,
    w2l_modifyform,
    get_entry_input,
    read_old_entry,
)
from .gui import (
    context_menu_single_entry,
    invalid_syntax_message,
    extract_invalid_attr,
    main_menu,
)


def modlist_ldif(dn, form, modlist):
    """
    Return a string containing a HTML-formatted LDIF change record
    """
    lines = []
    lines.append('<pre>')
    bio = BytesIO()
    ldif_writer = ldap0.ldif.LDIFWriter(bio)
    ldif_writer.unparse(dn.encode('utf-8'), modlist)
    lines.append(form.s2d(bio.getvalue().decode('utf-8')).replace('\n', '<br>'))
    lines.append('</pre>')
    return ''.join(lines)


##############################################################################
# Modify existing entry
##############################################################################

def w2l_modify(app):

    in_assertion = app.form.get_input_value('in_assertion', ['(objectClass=*)'])[0]

    input_modrow = app.form.get_input_value('in_mr', ['.'])[0]

    if input_modrow[0] == '-':
        del_row_num = int(input_modrow[1:])
        in_at_len = len(app.form.field['in_at'].val)
        if in_at_len >= del_row_num+2 and \
           app.form.field['in_at'].val[del_row_num] == app.form.field['in_at'].val[del_row_num+1] \
           or \
           in_at_len >= 1 and \
           app.form.field['in_at'].val[del_row_num] == app.form.field['in_at'].val[del_row_num-1]:
            # more input fields for same attribute type => pop()
            app.form.field['in_at'].val.pop(del_row_num)
            app.form.field['in_av'].val.pop(del_row_num)
        else:
            # only delete attribute value
            app.form.field['in_av'].val[del_row_num] = ''
        app.form.field['in_avi'].val = map(str, range(0, len(app.form.field['in_av'].val)))
    elif input_modrow[0] == '+':
        insert_row_num = int(input_modrow[1:])
        app.form.field['in_at'].val.insert(
            insert_row_num+1, app.form.field['in_at'].val[insert_row_num]
        )
        app.form.field['in_av'].val.insert(insert_row_num+1, '')
        app.form.field['in_avi'].val = map(str, range(0, len(app.form.field['in_av'].val)))

    new_entry, invalid_attrs = get_entry_input(app)

    if invalid_attrs:
        error_msg = invalid_syntax_message(app, invalid_attrs)
    else:
        error_msg = ''

    # Check if the user just switched/modified input form
    if (
            not new_entry
            or invalid_attrs
            or 'in_ft' in app.form.input_field_names
            or 'in_oc' in app.form.input_field_names
            or 'in_mr' in app.form.input_field_names
        ):
        w2l_modifyform(
            app,
            new_entry,
            msg=error_msg,
            invalid_attrs=invalid_attrs,
        )
        return

    in_oldattrtypes = set(app.form.get_input_value('in_oldattrtypes', []))

    try:
        old_entry, dummy = read_old_entry(app, app.dn, app.schema, in_assertion)
    except ldap0.NO_SUCH_OBJECT:
        raise ErrorExit('Old entry was removed or modified in between! You have to edit it again.')

    # Filter out empty values
    for attr_type, attr_values in new_entry.items():
        new_entry[attr_type] = [av for av in attr_values if av]

    # Set up a dictionary of all attribute types to be ignored
    ignore_attr_types = ldap0.schema.models.SchemaElementOIDSet(
        app.schema,
        AttributeType,
        ADD_IGNORE_ATTR_TYPES,
    )

    if not app.ls.relax_rules:
        # In case Relax Rules control is not enabled
        # ignore all attributes which have NO-USER-MODIFICATION set
        ignore_attr_types.update(app.schema.no_user_mod_attr_oids)
        # Ignore attributes which are assumed to be constant (some operational attributes)
        ignore_attr_types.update(cfg_constant_attributes(app).values())

    # All attributes currently read which were not visible before
    # must be ignored to avoid problems with different access rights
    # after possible re-login
    ignore_attr_types.update([
        attr
        for attr in old_entry.keys()
        if attr not in in_oldattrtypes
    ])

    old_entry_structural_oc = old_entry.get_structural_oc()
    # Ignore binary attributes from old entry data in any case
    for attr_type in old_entry.keys():
        syntax_class = syntax_registry.get_syntax(app.schema, attr_type, old_entry_structural_oc)
        if not syntax_class.editable:
            ignore_attr_types.add(attr_type)

    ignore_attr_types.discard('2.5.4.0')
    ignore_attr_types.discard('objectClass')

    # Create modlist containing deltas
    modlist = modify_modlist(
        app.schema,
        old_entry, new_entry,
        ignore_attr_types=ignore_attr_types,
        ignore_oldexistent=False,
    )

    # Binary values are always replaced
    new_entry_structural_oc = new_entry.get_structural_oc()
    for attr_type in new_entry.keys():
        syntax_class = syntax_registry.get_syntax(app.schema, attr_type, new_entry_structural_oc)
        if (not syntax_class.editable) and \
           new_entry[attr_type] and \
           (not attr_type in old_entry or new_entry[attr_type] != old_entry[attr_type]):
            modlist.append((ldap0.MOD_REPLACE, attr_type.encode('ascii'), new_entry[attr_type]))

    if not modlist:
        # nothing to be changed
        app.simple_message(
            'Modify result',
            '<p class="SuccessMessage">No attributes modified of entry %s</p>' % (
                app.display_dn(app.dn, links=True),
            ),
            main_menu_list=main_menu(app),
            context_menu_list=context_menu_single_entry(app)
        )
        return


    # Send modify-list to host
    try:
        app.ls.modify(
            app.dn,
            modlist,
            assertion_filter=in_assertion,
        )
    except ldap0.ASSERTION_FAILED:
        raise ErrorExit(
            'Assertion failed '
            '=> Entry was removed or modified in between! '
            'You have to edit it again.'
        )
    except (
            ldap0.INVALID_SYNTAX,
            ldap0.OBJECT_CLASS_VIOLATION,
        ) as err:
        error_msg, invalid_attrs = extract_invalid_attr(app, err)
        # go back to input form so the user can correct something
        w2l_modifyform(app, new_entry, msg=error_msg, invalid_attrs=invalid_attrs)
        return
    except (
            ldap0.CONSTRAINT_VIOLATION,
            ldap0.INVALID_DN_SYNTAX,
            ldap0.NAMING_VIOLATION,
            ldap0.OBJECT_CLASS_VIOLATION,
            ldap0.OTHER,
            ldap0.TYPE_OR_VALUE_EXISTS,
            ldap0.UNDEFINED_TYPE,
            ldap0.UNWILLING_TO_PERFORM,
        ) as err:
        # go back to input form so the user can correct something
        w2l_modifyform(app, new_entry, msg=app.ldap_error_msg(err))
        return

    # Display success message
    app.simple_message(
        'Modify result',
        (
            '<p class="SuccessMessage">Modified entry %s</p>\n'
            '<dt>LDIF change record:</dt>\n'
            '<dd>%s</dd>\n'
        ) % (
            app.display_dn(app.dn, links=True),
            modlist_ldif(app.dn, app.form, modlist),
        ),
        main_menu_list=main_menu(app),
        context_menu_list=context_menu_single_entry(app)
    )
