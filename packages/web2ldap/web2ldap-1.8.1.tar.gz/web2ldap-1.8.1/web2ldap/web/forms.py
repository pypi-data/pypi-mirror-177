# -*- coding: ascii -*-
"""
web2ldap.web.forms - class library for handling <FORM> input

(C) 1998-2022 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""

import cgi
import sys
import re
import urllib.parse
import uuid
from typing import List

from . import escape_html
from .helper import AcceptCharsetDict, AcceptHeaderDict

class Field:
    """
    Base class for all kind of single input fields.

    In most cases this class is not used directly
    since derivate classes for most types of input fields exist.
    """
    __slots__ = (
        'accesskey',
        'charset',
        'default',
        'maxLen',
        'maxValues',
        'name',
        '_re',
        'required',
        'text',
        'val',
    )

    def __init__(
            self,
            name,
            text,
            maxLen,
            maxValues,
            pattern,
            required=False,
            default=None,
            accesskey='',
        ):
        """
        name
            Field name used in <input name="..">
        text
            User-friendly text describing this field
        maxLen
            maximum length of a single input value [Bytes]
        maxValues
            maximum amount of input values
        default
            default value to be used in method inputfield()
        required
            flag which marks field as mandantory input field
        accesskey
            key for accessing this field to be displayed by method input_html()
        pattern
            regex pattern of valid values either as string
            or tuple (pattern,options)
        """
        self.val = []
        self.name = name
        self.text = text
        self.maxLen = maxLen
        self.maxValues = maxValues
        self.required = required
        self.accesskey = accesskey
        # Charset is the preferred character set of the browser.
        # This is set by Form.add() to something meaningful.
        self.charset = 'utf-8'
        self.set_default(default)
        self.set_regex(pattern)

    def _accesskey_attr(self):
        if not self.accesskey:
            return ''
        return 'accesskey="%s" ' % (self.accesskey)

    @staticmethod
    def id_attr(id_value):
        """
        return id attribute if id_value is non-empty, else returns empty string
        """
        if id_value is None:
            return ''
        return 'id="%s" ' % (id_value)

    def set_default(self, default):
        """
        Set the default of a field.

        Mainly this is used by the application if self.default shall
        be changed after initializing the field object.
        """
        if isinstance(default, list):
            self.default = [i for i in default if i is not None]
        self.default = default or ''

    @staticmethod
    def _regex_with_options(pattern):
        """
        The result is a tuple (pattern string, pattern options).

        pattern
            Either a string containing a regex pattern,
            a tuple (pattern string, pattern options) or None.
        """
        if pattern is None:
            return None, 0
        if isinstance(pattern, tuple):
            return pattern
        if isinstance(pattern, str):
            return pattern, 0
        raise TypeError('Expected pattern to be None, str or tuple, got %r' % (pattern,))

    def set_regex(self, pattern: str):
        """
        Set the regex pattern for validating this field.

        Mainly this is used if self._re shall be changed after
        the field object was initialized.

        pattern
            Either a string containing a regex pattern,
            a tuple (pattern string, pattern options) or None.
            If None regex checking in _validate_format is switched off
            (not recommended).
        """
        patternstring, patternoptions = self._regex_with_options(pattern)
        if patternstring is None:
            # Regex checking is completely switched off
            self._re = None
        else:
            # This is a Unicode input field
            patternoptions = patternoptions | re.U
            self._re = re.compile('%s$' % patternstring, patternoptions)

    def _validate_len(self, value):
        """Check length of the user's value for this field."""
        if len(value) > self.maxLen:
            raise InvalidValueLen(self.name, self.text, len(value), self.maxLen)

    def _validate_format(self, value):
        """
        Check format of the user's value for this field.

        Empty input (zero-length string) are valid in any case.
        You might override this method to change this behaviour.
        """
        if (not self._re is None) and value:
            rm = self._re.match(value)
            if rm is None:
                raise InvalidValueFormat(self.name, self.text, value)

    def _validate_val_count(self):

        if len(self.val) >= self.maxValues:
            raise TooManyValues(self.name, self.text, len(self.val), self.maxValues)

    def _decode_val(self, value):
        """
        Return str to be stored in self.val
        """
        try:
            value = value.decode(self.charset)
        except UnicodeError:
            # Work around buggy browsers...
            value = value.decode('iso-8859-1')
        return value

    def set_value(self, value):
        """
        Store the user's value into the field object.

        This method can be used to modify the user's value
        before storing it into self.val.
        """
        assert isinstance(value, (str, bytes)), TypeError(
            'Expected value to be str or bytes, was %r' % (value,)
        )
        if isinstance(value, bytes):
            value = self._decode_val(value)
        # Length valid?
        self._validate_len(value)
        # Format valid?
        self._validate_format(value)
        self._validate_val_count()
        self.val.append(value)

    def _default_val(self, default):
        """returns default value"""
        return default or getattr(self, 'default', '')

    def title_attr(self, title):
        """HTML output of default."""
        return escape_html(title or self.text)

    def _default_html(self, default):
        """HTML output of default."""
        return escape_html(self._default_val(default))


class Textarea(Field):
    """
    Multi-line input field:
    <textarea>
    """

    def __init__(
            self,
            name,
            text,
            maxLen,
            maxValues,
            pattern,
            required=False,
            default=None,
            accesskey='',
            rows=10,
            cols=60,
        ):
        self.rows = rows
        self.cols = cols
        Field.__init__(self, name, text, maxLen, maxValues, None, required, default, accesskey)

    def set_regex(self, pattern: str):
        """
        Like Field.set_regex() but pattern options re.S and re.M are
        automatically added.
        """
        patternstring, patternoptions = self._regex_with_options(pattern)
        # This is a Unicode input field
        patternoptions = patternoptions | re.M | re.S
        Field.set_regex(self, (patternstring, patternoptions))

    def input_html(self, default=None, id_value=None, title=None):
        """Returns string with HTML input field."""
        return '<textarea %stitle="%s" name="%s" %s rows="%d" cols="%d">%s</textarea>' % (
            self.id_attr(id_value),
            self.title_attr(title),
            self.name,
            self._accesskey_attr(),
            self.rows,
            self.cols,
            self._default_html(default),
        )


class Input(Field):
    """
    Normal one-line input field:
    <input>
    """
    input_type = None

    def __init__(
            self,
            name,
            text,
            maxLen,
            maxValues,
            pattern,
            required=False,
            default=None,
            accesskey='',
            size=None
        ):
        self.size = size or maxLen
        Field.__init__(self, name, text, maxLen, maxValues, pattern, required, default, accesskey)

    def input_html(self, default=None, id_value=None, title=None):
        if self.input_type is not None:
            type_attr = ' type="%s"' % (escape_html(self.input_type))
        else:
            type_attr = ''
        if self._re is not None:
            pattern_attr = ' pattern="%s"' % (escape_html(self._re.pattern))
        else:
            pattern_attr = ''
        return '<input %stitle="%s" name="%s" %s maxlength="%d" size="%d"%s%s value="%s">' % (
            self.id_attr(id_value),
            self.title_attr(title),
            self.name,
            self._accesskey_attr(),
            self.maxLen,
            self.size,
            type_attr,
            pattern_attr,
            self._default_html(default),
        )


class HiddenInput(Input):
    """
    Hidden input field:
    <input type="hidden">
    """
    input_type = 'hidden'


class BytesInput(Input):

    def set_regex(self, pattern: str):
        """
        Set the bytes regex pattern for validating this field.
        """
        patternstring, patternoptions = self._regex_with_options(pattern)
        if patternstring is None:
            # Regex checking is completely switched off
            self._re = None
        else:
            # This is a binary input field
            patternoptions = patternoptions
            self._re = re.compile(
                '%s$' % patternstring.encode('iso-8859-1'), # this encoding is a 1:1 byte mapping
                patternoptions,
            )

    def _decode_val(self, value):
        return value


class File(Input):
    """
    File upload field
    <input type="file">
    """
    mimeType = 'application/octet-stream'

    def _validate_format(self, value):
        """Binary data is assumed to be valid all the time"""
        return

    def _decode_val(self, value):
        """
        Return bytes to be stored in self.val
        """
        return value

    def input_html(self, default=None, id_value=None, title=None, mimeType=None):
        return '<input type="file" %stitle="%s" name="%s" %s accept="%s">' % (
            self.id_attr(id_value),
            self.title_attr(title),
            self.name,
            self._accesskey_attr(),
            mimeType or self.mimeType
        )


class Password(Input):
    """
    Password input field:
    <input type="password">
    """
    input_type = 'password'


class Radio(Field):
    """
    Radio buttons:
    <input type="radio">
    """

    def __init__(
            self,
            name,
            text,
            maxValues=1,
            required=False,
            default=None,
            accesskey='',
            options=None
        ):
        """
        pattern and maxLen are determined from __init__ params
        Additional parameters:
        options
          List of options. Either just a list of strings
          ['value1','value2',..] for simple options
          or a list of tuples of string pairs
          [('value1','description1),('value2','description2),..]
          for options with different option value and description.
        """
        self.set_options(options)
        self.set_default(default)
        Field.__init__(self, name, text, self.maxLen, maxValues, '', required, default, accesskey)

    def _validate_format(self, value):
        """
        Check format of the user's value for this field.

        Empty input (zero-length string) are valid in any case.
        You might override this method to change this behaviour.
        """
        if value and (not value in self.optionValues):
            raise InvalidValueFormat(self.name, self.text, value)

    def set_options(self, options):
        self.optionValues = {}
        self.maxLen = 0
        if options:
            for i in options:
                if isinstance(i, tuple):
                    optionValue = i[0]
                else:
                    optionValue = i
                self.optionValues[optionValue] = None
            self.maxLen = max(map(len, self.optionValues.keys()))
        self.options = list(options)

    def input_html(self, default=None, id_value=None, title=None):
        s = []
        default_value = self._default_val(default)
        for i in self.options:
            if isinstance(i, tuple):
                optionValue, optionText = i
            else:
                optionValue = optionText = i
            s.append(
                """
                <input
                  type="radio"
                  %s
                  title="%s"
                  name="%s"
                  %s
                  value="%s"
                  %s
                >%s<br>
                """ % (
                    self.id_attr(id_value),
                    self.title_attr(title),
                    self.name.encode(self.charset),
                    self._accesskey_attr(),
                    optionValue.encode(self.charset),
                    ' checked'*(optionValue == default_value),
                    optionText.encode(self.charset)
                )
            )
        return '\n'.join(s)

    def set_default(self, default):
        """
        Set the default of a default field.

        Mainly this is used if self.default shall be changed after
        initializing the field object.
        """
        # generate a set of existing option values
        option_vals = set()
        for i in self.options:
            if isinstance(i, tuple):
                option_vals.add(i[0])
            else:
                option_vals.add(i)
        if isinstance(default, str):
            if default not in option_vals:
                # Append option to list of options
                self.options.append(default)
        elif isinstance(default, list):
            # Extend list of options with items in default which are not in options
            self.options.extend([
                v
                for v in default
                if v not in option_vals
            ])
        elif default is not None:
            raise TypeError('Expected None, str or list for argument default, got %r' % (default,))
        self.default = default


class Select(Radio):
    """
    Select field:
    <select multiple>
      <option value="value">description</option>
    </select>
    """

    def __init__(
            self,
            name,
            text,
            maxValues,
            required=False,
            default=None,
            accesskey='',
            options=None,
            size=1,
            ignoreCase=0,
            multiSelect=0,
            auto_add_option=False,
        ):
        """
        Additional parameters:
        size
          Integer for the size of displayed select field.
        ignorecase
          Integer flag. If non-zero the case of input strings is ignored
          when checking input values.
        multiSelect
          Integer flag. If non-zero the select field has HTML attribute
          "multiple" set.
        """
        self.size = size
        self.multiSelect = multiSelect
        self.ignoreCase = ignoreCase
        self.auto_add_option = auto_add_option
        Radio.__init__(self, name, text, maxValues, required, default, accesskey, options)

    def _default_val(self, default):
        """returns default value"""
        if default:
            return default
        if self.multiSelect:
            return self.default or set()
        return self.default

    @property
    def option_value_set(self):
        res = set()
        for i in self.options:
            if isinstance(i, tuple):
                try:
                    optionValue, _, _ = i
                except ValueError:
                    optionValue, _ = i
            else:
                optionValue = i
            res.add(optionValue)
        return res

    def input_html(self, default=None, id_value=None, title=None):
        res = ['<select %stitle="%s" name="%s" %s  size="%d" %s>' % (
            self.id_attr(id_value),
            self.title_attr(title),
            self.name,
            self._accesskey_attr(),
            self.size,
            " multiple"*(self.multiSelect > 0)
        )]
        default_value = self._default_val(default)
        if (
                self.auto_add_option
                and default_value is not None
                and default_value not in self.option_value_set
            ):
            self.options.insert(0, default_value)
        for i in self.options:
            if isinstance(i, tuple):
                try:
                    optionValue, optionText, optionTitle = i
                except ValueError:
                    optionTitle = None
                    optionValue, optionText = i
            else:
                optionTitle = None
                optionValue = optionText = i
            if self.multiSelect:
                option_selected = optionValue in default_value
            else:
                option_selected = (
                    optionValue == default_value or
                    (self.ignoreCase and optionValue.lower() == default_value.lower())
                )
            if optionTitle:
                optionTitle_attr = ' title="%s"' % escape_html(optionTitle)
            else:
                optionTitle_attr = ''
            res.append(
                '<option value="%s"%s%s>%s</option>' % (
                    escape_html(optionValue),
                    optionTitle_attr,
                    ' selected'*(option_selected),
                    escape_html(optionText),
                )
            )
        res.append('</select>')
        return '\n'.join(res)


class DataList(Input, Select):
    """
    Input field combined with HTML5 <datalist>
    """

    def __init__(
            self,
            name,
            text,
            maxLen=100,
            maxValues=1,
            pattern=None,
            required=False,
            default=None,
            accesskey='',
            options=None,
            size=None,
            ignoreCase=0,
        ):
        Input.__init__(self, name, text, maxLen, maxValues, pattern, required, default, accesskey)
        if size is None:
            size = max([
                len(option) for option, _ in options or []
            ])
        self.size = size or 20
        self.multiSelect = 0
        self.ignoreCase = ignoreCase
        self.set_options(options)
        self.set_default(default)

    def input_html(self, default=None, id_value=None, title=None):
        datalist_id = str(uuid.uuid4())
        s = [
            '<input %stitle="%s" name="%s" %s maxlength="%d" size="%d" value="%s" list="%s">' % (
                self.id_attr(id_value),
                self.title_attr(title),
                self.name,
                self._accesskey_attr(),
                self.maxLen,
                self.size,
                self._default_html(default),
                datalist_id,
            )
        ]
        s.append(
            Select.input_html(
                self,
                default=default,
                id_value=datalist_id,
                title=title
            ).replace('<select ', '<datalist ').replace('</select>', '</datalist>')
        )
        return '\n'.join(s)


class Checkbox(Field):
    """
    Check boxes:
    <input type="checkbox">
    """

    def __init__(
            self,
            name,
            text,
            maxValues=1,
            required=False,
            accesskey='',
            default=None,
            checked=0,
        ):
        """
        pattern and maxLen are determined by default
        """
        pattern = default
        maxLen = len(default or '')
        self.checked = checked
        Field.__init__(self, name, text, maxLen, maxValues, pattern, required, default, accesskey)

    def input_html(self, default=None, id_value=None, title=None, checked=None):
        if checked is None:
            checked = self.checked
        return '<input type="checkbox" %stitle="%s" name="%s" %s value="%s"%s>' % (
            self.id_attr(id_value),
            self.title_attr(title),
            self.name,
            self._accesskey_attr(),
            self._default_html(default),
            ' checked'*(checked),
        )


class FormException(Exception):
    """
    Base exception class to indicate form processing errors.
    """


class InvalidFormEncoding(FormException):
    """
    The form data is malformed.

    Attributes:
    param         name/value causing the exception
    """

    def __init__(self, param):
        FormException.__init__(self)
        self.param = param

    def __str__(self):
        return 'The form data is malformed.'


class ContentLengthExceeded(FormException):
    """
    Overall length of input data too large.

    Attributes:
    content_length         received content length
    maxContentLength      maximum valid content length
    """

    def __init__(self, content_length: int, max_length: int):
        FormException.__init__(self)
        self.content_length = content_length
        self.max_length = max_length

    def __str__(self):
        return 'Input length of %d bytes exceeded the maximum of %d bytes.' % (
            self.content_length,
            self.max_length
        )


class InvalidFieldName(FormException):
    """
    Parameter with undeclared name attribute received.

    Attributes:
    name          name of undeclared field
    """

    def __init__(self, name: str):
        FormException.__init__(self)
        self.name = name

    def __str__(self):
        return 'Unknown parameter %s.' % (self.name)


class ParamsMissing(FormException):
    """
    Required parameters are missing.

    Attributes:
    missingParamNames     list of strings containing all names of missing
                          input fields.
    """
    def __init__(self, missingParamNames: List[str]):
        FormException.__init__(self)
        self.missingParamNames = missingParamNames

    def __str__(self):
        return 'Required fields missing: %s' % (
            ', '.join(
                map(
                    lambda i: '%s (%s)' % (i[1], i[0]),
                    self.missingParamNames
                )
            )
        )


class InvalidValueFormat(FormException):
    """
    The user's input does not match the required format.

    Attributes:
    name          name of input field (Field.name)
    text          textual description of input field (Field.text)
    value         input value received
    """

    def __init__(self, name: str, text: str, value):
        FormException.__init__(self)
        self.name = name
        self.text = text
        self.value = value

    def __str__(self):
        return 'Invalid input value %r for field %s (%s)' % (
            self.value, self.name, self.text
        )


class InvalidValueLen(FormException):
    """
    Length of user input value invalid.

    Attributes:
    name          name of input field (Field.name)
    text          textual description of input field (Field.text)
    valueLen      integer number of received value length
    maxValueLen   integer number of maximum value length
    """

    def __init__(self, name: str, text: str, valueLen: int, maxValueLen: int):
        FormException.__init__(self)
        self.name = name
        self.text = text
        self.valueLen = valueLen
        self.maxValueLen = maxValueLen

    def __str__(self):
        return 'Content too long. Field %s (%s) has %d characters but is limited to %d.' % (
            self.text,
            self.name,
            self.valueLen,
            self.maxValueLen,
        )


class TooManyValues(FormException):
    """
    User's input contained too many values for same parameter.

    Attributes:
    name                  name of input field (Field.name)
    text                  textual description of input field (Field.text)
    valueCount            integer number of values counted with name
    maxValueCount         integer number of maximum values with name allowed
    """

    def __init__(self, name: str, text: str, valueCount: int, maxValueCount: int):
        FormException.__init__(self)
        self.name = name
        self.text = text
        self.valueCount = valueCount
        self.maxValueCount = maxValueCount

    def __str__(self):
        return '%d values for field %s (%s). Limited to %d input values.' % (
            self.valueCount,
            self.text,
            self.name,
            self.maxValueCount,
        )


class Form:
    """
    Class for declaring and processing a whole <form>
    """
    __slots__ = (
        'accept_charset',
        'accept_language',
        'env',
        'field',
        'http_accept_charset',
        'http_accept_encoding',
        'http_accept_language',
        'inf',
        'input_field_names',
        'query_string',
        'request_method',
        'script_name',
    )

    def __init__(self, inf, env):
        """
        Initialize a Form
        inf                 Read from this file object if method is POST.
        env                 Dictionary holding the environment vars.
        """
        # Dictionary of Field objects
        self.field = {}
        # set of parameters names received with input
        self.input_field_names = set()
        # Save the environment vars
        self.env = env
        # input file object
        self.inf = inf or sys.stdin
        # Save request method
        self.request_method = env['REQUEST_METHOD']
        self.script_name = env['SCRIPT_NAME']
        # Initialize the AcceptHeaderDict objects
        self.http_accept_charset = AcceptCharsetDict('HTTP_ACCEPT_CHARSET', env)
        self.accept_charset = self.http_accept_charset.preferred()
        self.http_accept_language = AcceptHeaderDict('HTTP_ACCEPT_LANGUAGE', env)
        self.accept_language = self.http_accept_language.keys()
        self.http_accept_encoding = AcceptHeaderDict('HTTP_ACCEPT_ENCODING', env)
        # Determine query string
        self.query_string = env.get('QUERY_STRING', '')
        # add Field instances
        for field in self.fields():
            self.add_field(field)
        # end of Form.__init__()

    def fields(self):
        """
        Return a list of Field instances to be added to this Form instance.
        """
        return []

    def add_field(self, field):
        """
        Add a input field object f to the form.
        """
        field.charset = self.accept_charset
        self.field[field.name] = field
        # end of Form.add_field()

    def get_input_value(self, name, default=None):
        """
        Return input value of a field defined by name if presented
        in form input. Return default else.
        """
        if name in self.input_field_names:
            return self.field[name].val
        if name in self.field:
            return default
        raise KeyError('Invalid field name %r requested for %s' % (name, self.__class__.__name__))

    def list_fields(self, fields=None, ignore_fields=None):
        """
        Return list with all former input parameters.

        ignore_fields
            Names of parameters to be excluded.
        """
        ignore_fields = set(ignore_fields or [])
        result = list(fields) or []
        for f in [
                self.field[p]
                for p in self.input_field_names-ignore_fields
            ]:
            for val in f.val:
                result.append((f.name, val))
        return result

    def hidden_fields(self, outf=sys.stdout, ignore_fields=None):
        """
        Output all parameters as hidden fields.

        outf
            File object for output.
        ignore_fields
            Names of parameters to be excluded.
        """
        ignore_fields = ignore_fields or []
        for field in [
                self.field[p]
                for p in self.input_field_names-ignore_fields
            ]:
            for val in field.val:
                outf.write(
                    '<input type="hidden" name="%s" value="%s">\n\r' % (
                        field.name,
                        escape_html(val),
                    )
                )
        # end of Form.hidden_fields()

    def _add_fields(self):
        """
        can be overwritten to add Field instances to the form
        """

    @property
    def max_content_length(self) -> int:
        """
        calculate maximum acceptable content length
        """
        res = 0
        for field in self.field.values():
            res += field.maxValues * field.maxLen
        return res

    def _parse_url_encoded(self):
        if self.request_method == 'POST':
            query_string = self.inf.read(int(self.env['CONTENT_LENGTH'])).decode(self.accept_charset)
        elif self.request_method == 'GET':
            query_string = self.env.get('QUERY_STRING', '')
        if not query_string:
            return
        content_length = 0
        for name, value in urllib.parse.parse_qsl(
                query_string,
                keep_blank_values=True,
                strict_parsing=True,
                encoding=self.accept_charset,
                errors='strict',
                max_num_fields=None
            ):
            if name not in self.field:
                raise InvalidFieldName(name)
            content_length += len(value)
            # Overall length of input data still valid?
            max_content_length = self.max_content_length
            if content_length > max_content_length:
                raise ContentLengthExceeded(content_length, max_content_length)
            # Input is stored in field instance
            self.field[name].set_value(value)
            # Add name of field to set of input keys
            self.input_field_names.add(name)
        # end of _parse_url_encoded()

    def _parse_mime_multipart(self):
        _, pdict = cgi.parse_header(self.env['CONTENT_TYPE'])
        pdict['boundary'] = pdict['boundary'].encode('ascii')
        pdict['CONTENT-LENGTH'] = self.env['CONTENT_LENGTH'].encode('ascii')
        parts = cgi.parse_multipart(self.inf, pdict)
        content_length = 0
        max_content_length = self.max_content_length
        for name in parts.keys():
            if name not in self.field:
                raise InvalidFieldName(name)
            for value in parts[name]:
                content_length += len(value)
                # sum of all received input still valid?
                if content_length > max_content_length:
                    raise ContentLengthExceeded(content_length, max_content_length)
                # Input is stored in field instance
                self.field[name].set_value(value)
                # Add name of field to set of input keys
                self.input_field_names.add(name)
        # end of _parse_mime_multipart()

    def get_input_fields(self):
        """
        Process user's <form> input and store the values in each
        field instance's content attribute.

        When a processing error occurs FormException (or derivatives)
        are raised.
        """
        content_type = self.env.get('CONTENT_TYPE', '').lower()
        if self.request_method == 'POST' and content_type.startswith('multipart/form-data'):
            self._parse_mime_multipart()
        else:
            self._parse_url_encoded()
        # Are all required parameters present?
        missing_params = []
        for _, field in self.field.items():
            if field.required and field.name not in self.input_field_names:
                missing_params.append((field.name, field.text))
        if missing_params:
            raise ParamsMissing(missing_params)
        # end of Form.get_input_fields()
