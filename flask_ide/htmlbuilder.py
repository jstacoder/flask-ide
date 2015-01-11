# -*- coding: utf-8 -*-
"""
    flaskext.htmlbuilder
    ~~~~~~~~~~~~~~~~~~~~

    Flask-HTMLBuilder is a `Flask`_ extension that allows **flexible** and 
    **easy** Python-only generation of HTML snippets and full HTML documents
    using a robust syntax.  For more advanced usage it provides a lean template
    inheritance system that is intertwined with the Flask/Werkzeug endpoint
    mechanisms.

    :copyright: (c) 2010 by Zahari Petkov.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import

from keyword import kwlist

from flask import request, g


__all__ = [
    'init_htmlbuilder', 'html', 'render', 'render_template', 'root_block',
    'block', 'RootBlock', 'Block', 'Context', 'Attrs'
]


def init_htmlbuilder(app):
    """Initializes the extension so that the `g.blocks` and `g.attrs`
    dictionaries are created for each request.
    """
    @app.before_request
    def before_request():
        g.blocks = {}
        g.attrs = {}


class HTMLDispatcher(object):
    def __getattr__(self, attr):
        if attr in special_elements:
            return special_elements[attr]()
        return Element(attr)


html = HTMLDispatcher()
"""The :data:`html` instance is used as a factory for building HTML tree
structure. Example::

    headline = html.div(id='headline')(
        html.h1(class_='left')('Headline text')
    )

The tree structure can be directly rendered to HTML using `str` or `unicode`.
Example::
    
    >>> unicode(headline)
    u'<div id="headline"><h1 class="left">Headline text</h1></div>'

This is useful when combined with a template engine like Jinja 2.  An
alternative approach is to use the :func:`render` function when indentation is
needed.  Or another approach is to use the :func:`render_template` function in
this module that is a powerful standalone solution for full HTML document
rendering.

This extension provides a special HTML builder syntax accessed through
the :data:`html` instance.

Void HTML element::

    >>> str(html.br)
    '<br />'

Void element with attributes::

    >>> str(html.img(src='/img/logo.png', class_='centered'))
    '<img class="centered" src="/img/logo.png" />'

.. note::
    Since attribute names like `class` are reserved Python keywords those need
    to be escaped with an underscore "_" symbol at the end of the name.  The
    same holds true for HTML elements like `del`, which needs to be declared as
    `html.del_`.

Non-void element::

    >>> str(html.div())
    '<div></div>'

Element with children::
    
    >>> str(html.div(html.p('First'), html.p('Second')))
    '<div><p>First</p><p>Second</p></div>'

Element with attributes and children::

    >>> str(html.div(class_='centered')(html.p('First')))
    '<div class="centered"><p>First</p></div>'
    
.. note::
    Attribute definition is done in a different call from child elements
    definition as you can see in the above example.  This approach is taken
    because Python does not allow keyword arguments (the attributes in this
    case) to be placed before the list arguments (child elements).  `__call__`
    chaining allows the definition syntax to be closer to HTML.
"""

def render(element, level=0):
    """Renders the HTML builder `element` and it's children to a string. 
    Example::
    
        >>> print(
        ...     render(
        ...         html.form(action='/search', name='f')(
        ...             html.input(name='q'),
        ...             html.input(name='search_button', type='submit')
        ...         )
        ...     )
        ... )
        <form action="/search" name="f">
          <input name="q" />
          <input type="submit" name="search_button" />
        </form>

    The :func:`render` function accepts the following arguments:
    
    :param element: element created through the `html` builder instance, a list
                    of such elements, or just a string.
    :param level: indentation level of the rendered element with a step of two
                  spaces.  If `level` is `None`, the `element` will be rendered
                  without indentation and new line transferring, passing the 
                  same rule to the child elements.
    """
    if hasattr(element, 'render'):
        return element.render(level)
    elif hasattr(element, '__iter__'):
        return _render_iteratable(element, level)
    elif isinstance(element, basestring):
        return _render_string(element, level)
    elif element is None:
        return ''
    
    raise TypeError('Cannot render %r' % element)


class BaseElement(object):
    __slots__ = []
    
    def __str__(self):
        return str(self.render(None))
    
    def __unicode__(self):
        return unicode(self.render(None))
    
    def __html__(self):
        return self.__unicode__()
    
    def render(self, level):
        raise NotImplementedError('render() method has not been implemented')


class Element(BaseElement):
    __slots__ = ['_name', '_children', '_attributes']
    
    def __init__(self, name):
        self._name = _unmangle_element_name(name)
        
        # `None` indicates a void element or a list content for non-void
        # elements. 
        self._children = None
        
        # `None` indicates no attributes, or it is a list if there are any.
        self._attributes = None
        
    def __call__(self, *children, **attributes):
        # Consequent calling the instances of that class with keyword
        # or list arguments or without arguments populates the HTML element
        # with attribute and children data.
        
        if attributes:
            # Keyword arguments are used to indicate attribute definition.
            self._attributes = attributes
        elif children:
            # Child nodes are passed through the list arguments.
            self._children = children
        else:
            # Create an empty non-void HTML element.
            self._children = []
        
        return self
    
    def __repr__(self):
        result = '<' + type(self).__name__ + ' ' + self._name
        
        if self._attributes is not None:
            result += _serialize_attributes(self._attributes)
        
        if self._children:
            result += ' ...'
            
        result += '>'
        
        return result
    
    def render(self, level):
        # Keeping this method intentionally long for execution speed gain.
        result = _indent(level) + '<' + self._name
        
        if self._attributes is not None:
            result += _serialize_attributes(self._attributes)
        
        if self._children is None:
            result += ' />'
        else:
            result += '>'
            if self._children:
                if len(self._children) == 1 and isinstance(self._children[0], basestring) or self._children[0] is None:
                    result += escape(self._children[0])
                else:
                    result += _new_line(level)
                    
                    if level is not None:
                        level += 1
                    result += _render_iteratable(self._children, level)
                    if level is not None:
                        level -= 1
                    
                    result += _indent(level)
            
            result += '</' + self._name + '>'
        
        result += _new_line(level)
        return result


class Comment(BaseElement):
    """`html.comment` is used for rendering HTML comments.
    Example::
        
        >>> print(render([
        ...     html.comment('Target less enabled mobile browsers'),
        ...     html.link(rel='stylesheet', media='handheld',
        ...               href='css/handheld.css')
        ... ]))
        <!--Target less enabled mobile browsers-->
        <link media="handheld" href="css/handheld.css" rel="stylesheet" />
        
    """
    __slots__ = ['_comment']
    
    def __init__(self):
        self._comment = None
    
    def __call__(self, comment):
        self._comment = comment
        return self
    
    def render(self, level):
        result = _indent(level) + '<!--'
        if self._comment is not None:
            result += self._comment
        result += '-->' + _new_line(level)
        return result


class Doctype(BaseElement):
    """`html.doctype` is used for rendering HTML doctype definition at the
    beginning of the HTML document.  Example::
        
        >>> print(render([
        ...     html.doctype('html'),
        ...     html.html(
        ...         html.head('...'),
        ...         html.body('...')
        ...     )
        ... ]))
        <!doctype html>
        <html>
          <head>...</head>
          <body>...</body>
        </html>
        
    """
    __slots__ = ['_doctype']
    
    def __init__(self):
        self._doctype = None

    def __call__(self, doctype):
        self._doctype = doctype
        return self
    
    def render(self, level):
        return _indent(level) + '<!doctype ' + self._doctype + '>' + \
               _new_line(level)


class Safe(BaseElement):
    """`html.safe` renders HTML text content without escaping it. This is
    useful for insertion of prerendered HTML content.  Example::
        
        >>> print(render([
        ...     html.div(
        ...         html.safe('<strong>Hello, World!</strong>')
        ...     )
        ... ]))
        <div>
          <strong>Hello, World!</strong>
        </div>

    """
    __slots__ = ['_content']
    
    def __init__(self):
        self._content = None
    
    def __call__(self, content):
        self._content = content
        return self
    
    def render(self, level):
        return _indent(level) + self._content + _new_line(level)


class Join(BaseElement):
    """`html.join` is used for rendering a list of HTML builder elements
    without indenting them and transferring each of them to a new line.  This
    is necessary when rendering a paragraph content for example and all text
    and other elements need to stick together.  Example::
    
        >>> print(render([
        ...     html.p(
        ...         html.join(
        ...             'Read the ', html.a(href='/docs')('documentation'), '.'
        ...         )
        ...     )
        ... ]))
        <p>
          Read the <a href="/docs">documentation</a>.
        </p>
    """
    __slots__ = ['_children']
    
    def __init__(self):
        self._children = None
    
    def __call__(self, *children):
        self._children = children
        return self
    
    def render(self, level):
        return _indent(level) + _render_iteratable(self._children, None) + \
               _new_line(level)


class NewLine(BaseElement):
    """`html.newline` adds an empty new line in the content.  This is only
    needed for better readibility of the HTML source code.  Example::
    
        >>> print(render([
        ...     html.p('First'),
        ...     html.newline(),
        ...     html.p('Second')
        ... ]))
        <p>First</p>
        
        <p>Second</p>
    """
    __slots__ = []
        
    def __call__(self):
        return self
    
    def render(self, level):
        return _indent(level) + _new_line(level)


class BaseHasElement(BaseElement):
    __slots__ = ['_children', '_name']
    
    def __init__(self):
        self._children = None
        
        self._name = None
    
    def __call__(self, *arguments):
        if self._name is None:
            self._name = arguments[0]
        else:
            self._children = arguments
        return self


class HasBlock(BaseHasElement):
    """`html.has_block` checks whether a specified HTML block exists in the
    `g.blocks` dictionary and if so then it returns specified child elements.
    
    The following function::
    
        def container_main():
            if g.blocks.has_key('main_content'):
                return html.div(id='container_main')(
                    html.block('main_content')
                )
            else:
                return None
    
    Is equivalent to the following::
        
        def container_main():
            return html.has_block('main_content')(
                html.div(id='container_main')(
                    html.block('main_content')
                )
            )
    
    """
    def render(self, level):
        if g.blocks.has_key(self._name):
            return _render_iteratable(self._children, level)
        else:
            return ''


class BlockElement(BaseElement):
    """`html.block` is used for retreiving already populated blocks from the
    `g.blocks` dictionary.  It is a shortcut method for `g.blocks.get` with
    the small difference that it returns a block element on it's own like the
    other `html` instance methods.
    
    The following call::
    
        >>> html.p(
        ...     g.blocks.get('content')
        ... )
    
    Is equivalent to the following::

        >>> html.p(
        ...     html.block('content')
        ... )
    
    Additionally it has the ability to set block content if the block with the
    same name is not already defined.  This is useful for definition of default
    blocks.
    
    Setting block content is used that way::
    
        >>> html.block('content')(
        ...     html.join(
        ...         'Hello, ', html.a(href='/world')('World'), '!'
        ...     )
        ... )
    
    Which is equivalent to the following::
    
        >>> g.blocks['content'] = html.join(
        ...     'Hello, ', html.a(href='/world')('World'), '!'
        ... )
        
    An example of specifying a default block:
    
        html.head(
            html.title(
                html.block('title')(
                    'Default Title'
                )
            )
        )
    
    """
    __slots__ = ['_name']
    
    def __init__(self):
        self._name = None
    
    def __call__(self, *arguments):
        if self._name is None:
            self._name = arguments[0]
        elif not g.blocks.has_key(self._name):
            g.blocks[self._name] = arguments
        return self
    
    def render(self, level):
        return render(g.blocks.get(self._name, None), level)


class HasAttr(BaseHasElement):
    """`html.has_attr` checks whether a given key exists in the
    `g.attrs` dictionary and if so then it returns specified child elements.
    
    The following function::
        
        def meta_description():
            if g.attrs.has_key('description'):
                return html.meta(name='description', content=g.attrs['description'])
            else:
                return None
    
    Is equivalent to the following::
    
        def meta_description():
            return html.has_attr('description)(
                html.meta(name='description', content=Attr('description'))
            )
    
    It is used usually in conjunction with :class:`Attr`.
    """
    def render(self, level):
        if g.attrs.has_key(self._name):
            return _render_iteratable(self._children, level)
        else:
            return ''


special_elements = {
    'comment': Comment,
    'doctype': Doctype,
    'safe': Safe,
    'join': Join,
    'newline': NewLine,
    'has_block': HasBlock,
    'block': BlockElement,
    'has_attr': HasAttr,
}


def _indent(level):
    """Indent a line that will contain HTML data."""
    if level is None:
        return ''
    
    return ' ' * level * 2


def _new_line(level):
    if level is None:
        return ''
    else:
        return '\n'


def _render_string(string, level):
    """Renders HTML escaped text."""
    return _indent(level) + escape(string) + _new_line(level)


def _render_iteratable(iteratable, level):
    """Renders iteratable sequence of HTML elements."""
    return ''.join([render(element, level) for element in iteratable])


def _serialize_attributes(attributes):
    """Serializes HTML element attributes in a name="value" pair form."""
    result = ''
    for name, value in attributes.iteritems():
        if value is None or (hasattr(value, 'is_none') and value.is_none()):
            continue
        result += ' ' + _unmangle_attribute_name(name) + '="' \
               + escape(value, True) + '"'
    return result


_PYTHON_KEYWORD_MAP = dict((reserved + '_', reserved) for reserved in kwlist)

def _unmangle_element_name(name):
    """Unmangles element names so that correct Python method names are
    used for mapping element names."""
    
    # Python keywords cannot be used as method names, an underscore should
    # be appended at the end of each of them when defining attribute names.
    return _PYTHON_KEYWORD_MAP.get(name, name)


def _unmangle_attribute_name(name):
    """Unmangles attribute names so that correct Python variable names are
    used for mapping attribute names."""
    
    # Python keywords cannot be used as variable names, an underscore should
    # be appended at the end of each of them when defining attribute names.
    name = _PYTHON_KEYWORD_MAP.get(name, name)
    
    # Attribute names are mangled with double underscore, as colon cannot
    # be used as a variable character symbol in Python. Single underscore is
    # used for substituting dash.
    name = name.replace('__', ':').replace('_', '-')
    
    return name


def escape(string, quote=False):
    """Standard HTML text escaping, but protecting against the agressive
    behavior of Jinja 2 `Markup` and the like.
    """
    if string is None:
        return ''
    elif hasattr(string, '__html__'):
        return unicode(string)
    string = string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    if quote:
        string = string.replace('"', "&quot;")
    return string


DEFAULT_TEMPLATE_NAME = 'default'


def render_template(template_name=DEFAULT_TEMPLATE_NAME):
    """Renders the HTML document based on the template hierarchy taking into
    account internally which view function is processing the request.
    
    The :func:`render_template` function accepts the following arguments:
    
    :param template_name: The name of the block template hierarchy that is used
                          to render the HTML document.
    """
    return render(RootBlock.block_templates[template_name].html_block())


def root_block(template_name=DEFAULT_TEMPLATE_NAME):
    """A decorator that is used to define that the decorated block function
    will be at the root of the block template hierarchy.  In the usual case 
    this will be the HTML skeleton of the document, unless the template is used
    to serve partial HTML rendering for Ajax.
    
    The :func:`root_block` decorator accepts the following arguments:
    
    :param template_name: The name of the block template hierarchy which is
                          passed to the :func:`render_template` document
                          rendering function.  Different templates are useful
                          for rendering documents with differing layouts
                          (e.g. admin back-end vs. site front-end), or for
                          partial HTML rendering for Ajax.
    """
    def decorator(block_func):
        block = RootBlock(block_func, template_name)
        return block_func
    return decorator


def block(context_name, parent_block_func, view_func=None):
    """A decorator that is used for inserting the decorated block function in
    the block template hierarchy.
    
    The :func:`block` decorator accepts the following arguments:
    
    :param context_name: key in the `g.blocks` dictionary in which the result
                         of the decorated block function will be stored for
                         further processing by the parent block function
                         `parent_block_func`.
    :param parent_block_func: parent block function in the template hierarchy
                              which will use the stored result.
    :param view_func: the decorated block will take an effect only in the
                      execution context of the specified view function.  If the
                      default value of `None` is used, then the block will be
                      used as default for the specified `context_name`.
                      Internally this parameter is converted to a Werkzeug
                      endpoint in the same way Flask is doing that with the
                      `Flask.route` decorator.
    """
    def decorator(block_func):
        block = Block(block_func, view_func)
        parent_block = Block.block_mapping[parent_block_func]
        parent_block.append_context_block(context_name, block)
        return block_func
    return decorator


class Block(object):
    """In conjunction with :class:`Context` works exactly like the
    :func:`block` decorator, but as an alternative approach that is described
    in the documentation of :class:`RootBlock`.
    """
    __slots__ = ['endpoint', 'block_func', 'contexts']
    
    block_mapping = {}
    
    def __init__(self, block_func, view_func=None):
        Block.block_mapping[block_func] = self
        
        if hasattr(view_func, '__name__'):
            endpoint = view_func.__name__
        else:
            endpoint = view_func
        
        self.endpoint = endpoint
        self.block_func = block_func
        self.contexts = []
        
    def __call__(self, *contexts):
        self.contexts += contexts
        return self
        
    def __repr__(self):
        result = '<' + self.__class__.__name__ + ' ' + self.block_func.__name__
        if self.endpoint is not None:
            result += ' => ' + repr(self.endpoint)
        
        result += '>'
        return result
        
    def html_block(self):
        if self.contexts is not None:
            for html_context in self.contexts:
                html_context.attach()
        
        return self.block_func()
    
    def append_context_block(self, name, block):
        context = self._find_context(name)
        
        if context is None:
            context = Context(name)
            self.contexts.append(context)
        
        context.blocks.append(block)
        
    def _find_context(self, name):
        for context in self.contexts:
            if context.name == name:
                return context
        return None


class RootBlock(Block):
    """Works exactly like the :func:`root_block` decorator, but is used for the
    alternative approach to defining template block inheritance.
    
    Basically for the following view functions::
        
        @app.route('/sidebar/first')
        def sidebar_first_view():
            return render_template('sidebar')
        
        @app.route('/sidebar/second')
        def sidebar_second_view():
            return render_template('sidebar')
    
    
    This example of template block inheritance definition::
    
        @root_block('sidebar')
        def sidebar_base():
            return html.div(id='sidebar')(
                html.block('sidebar_content')
            )
        
        @block('sidebar_content', sidebar_base, sidebar_first_view)
        def sidebar_first_content():
            return html.p('First')
        
        @block('sidebar_content', sidebar_base, sidebar_second_view)
        def sidebar_second_content():
            return html.p('Second')
    
    
    Is equivalent to the following::
        
        def sidebar_base():
            return html.div(id='sidebar')(
                html.block('sidebar_content')
            )
        
        def sidebar_first_content():
            return html.p('First')
        
        def sidebar_second_content():
            return html.p('Second')
        
        RootBlock(sidebar_base, 'sidebar')(
            Context('sidebar_content')(
                Block(sidebar_first_content, sidebar_first_view),
                Block(sidebar_second_content, sidebar_second_view)
            )
        )
    
    The mapping between both approaches is straightforward.  The most notable
    difference is that the first argument of the :func:`block` decorator is
    pulled out in a separate class :class:`Context`.
    
    The :class:`RootBlock`, :class:`Block` and :class:`Context` classes use the
    same `__call__` pattern used for building the HTML tree.
    """
    block_templates = {}
    def __init__(self, block_func, template_name=DEFAULT_TEMPLATE_NAME):
        super(RootBlock, self).__init__(block_func)
        RootBlock.block_templates[template_name] = self


class Context(object):
    """When used with :class:`Block` it plays the same role as the
    `context_name` parameter of the :func:`block` decorator. Check the
    documentation of :class:`RootBlock` for more information.
    """
    __slots__ = ['name', 'blocks']
    
    def __init__(self, name):
        self.name = name
        self.blocks = []
        
    def __repr__(self):
        return '<' + self.__class__.__name__ + ' ' + repr(self.name) + '>'
        
    def __call__(self, *blocks):
        self.blocks += blocks
        return self
        
    def attach(self):
        endpoint = request.url_rule.endpoint
        block = self._get_block(endpoint)
        
        if block is not None:
            g.blocks[self.name] = block.html_block()
        
    def _get_block(self, endpoint):
        exact_block = self._find_block(endpoint)
        if exact_block is not None:
            return exact_block
        
        return self._find_block(None)
        
    def _find_block(self, endpoint):
        for block in self.blocks:
            if block.endpoint == endpoint:
                return block
        return None


class Attr(object):
    """A shortcut class for accessing the `g.attrs` dictionary for populating
    HTML element attributes with data.
    
    The following two calls are equivalent::
        
        html.meta(name='description', content=Attr('description'))
        
        html.meta(name='description', content=g.attrs['description'])
    """
    __slots__ = ['_name']
    
    def __init__(self, name):
        self._name = name
    
    def __str__(self):
        return self._to_string(str)
    
    def __unicode__(self):
        return self._to_string(unicode)
    
    def replace(self, old, new):
        g.attrs[self._name].replace(old, new)
        return self
    
    def __add__(self, other):
        return unicode(self) + other
    
    def __radd__(self, other):
        return other + unicode(self)
    
    def _to_string(self, string_class):
        return string_class(g.attrs[self._name])
    
    def is_none(self):
        return g.attrs[self._name] is None

