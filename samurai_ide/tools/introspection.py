# -*- coding: utf-8 -*-
#
# This file is part of Samurai-IDE (https://samurai-ide.org).
#
# Samurai-IDE is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Samurai-IDE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Samurai-IDE; If not, see <http://www.gnu.org/licenses/>.
import ast

from samurai_ide.intellisensei.analyzer import model

from samurai_ide.tools.logger import NinjaLogger

logger_imports = NinjaLogger(
    'samurai_ide.tools.introspection.obtaining_imports')
logger_symbols = NinjaLogger(
    'samurai_ide.tools.introspection.obtaining_symbols')

_map_type = {
    ast.Tuple: 'tuple',
    ast.List: 'list',
    ast.Str: 'str',
    ast.Dict: 'dict',
    ast.Num: 'int',
    ast.Call: 'function()',
}


def _parse_assign(symbol):
    assigns = {}
    attributes = {}
    for var in symbol.targets:
        if isinstance(var, ast.Attribute):
            attributes[var.attr] = var.lineno
        elif isinstance(var, ast.Name):
            assigns[var.id] = var.lineno
    return (assigns, attributes)


def _parse_class(symbol, with_docstrings):
    docstring = {}
    attr = {}
    func = {}
    clazz = {}
    name = symbol.name + '('
    name += ', '.join([
        model.expand_attribute(base) for base in symbol.bases])
    name += ')'
    for sym in symbol.body:
        if isinstance(sym, ast.Assign):
            result = _parse_assign(sym)
            attr.update(result[0])
            attr.update(result[1])
        elif isinstance(sym, ast.FunctionDef):
            result = _parse_function(sym, with_docstrings)
            attr.update(result['attrs'])
            if with_docstrings:
                docstring.update(result['docstring'])
            func[result['name']] = {
                'lineno': result['lineno'],
                'functions': result['functions']
            }
        elif isinstance(sym, ast.ClassDef):
            result = _parse_class(sym, with_docstrings)
            clazz[result['name']] = {
                'lineno': result['lineno'],
                'members': {
                    'attributes': result['attributes'],
                    'functions': result['functions']
                }
            }
            docstring.update(result['docstring'])
    if with_docstrings:
        docstring[symbol.lineno] = ast.get_docstring(symbol, clean=True)

    lineno = symbol.lineno
    for decorator in symbol.decorator_list:
        lineno += 1

    return {
        'name': name,
        'attributes': attr,
        'functions': func,
        'lineno': lineno,
        'docstring': docstring,
        'classes': clazz
    }


def _parse_function(symbol, with_docstrings):
    docstring = {}
    attrs = {}
    func = {'functions': {}}

    func_name = symbol.name + '('
    # We store the arguments to compare with default backwards
    defaults = []
    for value in symbol.args.defaults:
        # TODO: In some cases we can have something like: a=os.path
        defaults.append(value)
    arguments = []
    for arg in reversed(symbol.args.args):
        if not isinstance(arg, ast.Name) or arg.id == "self":
            continue
        argument = arg.id
        if defaults:
            value = defaults.pop()
            arg_default = _map_type.get(value.__class__, None)
            if arg_default is None:
                if isinstance(value, ast.Attribute):
                    arg_default = model.expand_attribute(value)
                elif isinstance(value, ast.Name):
                    arg_default = value.id
                else:
                    arg_default = 'object'
            argument += '=' + arg_default
        arguments.append(argument)
    func_name += ', '.join(reversed(arguments))

    if symbol.args.vararg is not None:
        if not func_name.endswith('('):
            func_name += ', '
        func_name += '*'
        func_name += symbol.args.vararg.arg
    if symbol.args.kwarg is not None:
        if not func_name.endswith('('):
            func_name += ', '
        func_name += '**'
        func_name += symbol.args.kwarg.arg
    func_name += ')'

    for sym in symbol.body:
        if isinstance(sym, ast.Assign):
            result = _parse_assign(sym)
            attrs.update(result[1])
        elif isinstance(sym, ast.FunctionDef):
            result = _parse_function(sym, with_docstrings)
            if with_docstrings:
                docstring.update(result['docstring'])
            func['functions'][result['name']] = {
                'lineno': result['lineno'],
                'functions': result['functions']
            }

    if with_docstrings:
        docstring[symbol.lineno] = ast.get_docstring(symbol, clean=True)

    lineno = symbol.lineno
    for decorator in symbol.decorator_list:
        lineno += 1

    return {'name': func_name, 'lineno': lineno,
            'attrs': attrs, 'docstring': docstring, 'functions': func}


def obtain_symbols(source, with_docstrings=False, filename='',
                   simple=False, only_simple=False):
    """Parse a module source code to obtain: Classes, Functions and Assigns."""

    try:
        module = ast.parse(source)
    except SyntaxError:
        logger_symbols.debug("The file contains syntax errors: %s" % filename)
        if simple:
            return {}, {}
        else:
            return {}
    symbols = {}
    symbols_simplified = {}
    globalAttributes = {}
    globalFunctions = {}
    classes = {}
    docstrings = {}

    for symbol in module.body:
        if isinstance(symbol, ast.Assign) and not only_simple:
            result = _parse_assign(symbol)
            globalAttributes.update(result[0])
            globalAttributes.update(result[1])
        elif isinstance(symbol, ast.FunctionDef):
            if not only_simple:
                result = _parse_function(symbol, with_docstrings)
                if with_docstrings:
                    docstrings.update(result['docstring'])
                globalFunctions[result['name']] = {
                    'lineno': result['lineno'],
                    'functions': result['functions']}
            if simple:
                result_simple = _parse_function_simplified(symbol)
                symbols_simplified.update(result_simple)
        elif isinstance(symbol, ast.ClassDef):
            if not only_simple:
                result = _parse_class(symbol, with_docstrings)
                classes[result['name']] = {
                    'lineno': result['lineno'],
                    'members': {'attributes': result['attributes'],
                                'functions': result['functions'],
                                'classes': result['classes']}}
                docstrings.update(result['docstring'])
            if simple:
                result_simple = _parse_class_simplified(symbol)
                symbols_simplified.update(result_simple)
    if globalAttributes:
        symbols['attributes'] = globalAttributes
    if globalFunctions:
        symbols['functions'] = globalFunctions
    if classes:
        symbols['classes'] = classes
    if docstrings and with_docstrings:
        symbols['docstrings'] = docstrings

    if simple:
        return symbols, symbols_simplified
    else:
        return symbols


def obtain_imports(source='', body=None):
    if source:
        try:
            module = ast.parse(source)
            body = module.body
        except SyntaxError:
            logger_imports.debug("A file contains syntax errors.")
    # Imports{} = {name: asname}, for example = {sys: sysAlias}
    imports = {}
    # From Imports{} = {name: {module: fromPart, asname: nameAlias}}
    fromImports = {}
    if body is not None:
        for sym in body:
            if isinstance(sym, ast.Import):
                for item in sym.names:
                    imports[item.name] = {
                        'asname': item.asname,
                        'lineno': sym.lineno
                    }
            if isinstance(sym, ast.ImportFrom):
                for item in sym.names:
                    fromImports[item.name] = {
                        'module': sym.module,
                        'asname': item.asname,
                        'lineno': sym.lineno
                    }
    return {'imports': imports, 'fromImports': fromImports}


def _parse_class_simplified(symbol):
    results = {}
    name = symbol.name + '('
    name += ', '.join([
        model.expand_attribute(base) for base in symbol.bases])
    name += ')'
    for sym in symbol.body:
        if isinstance(sym, ast.FunctionDef):
            result = _parse_function_simplified(sym, symbol.name)
            results.update(result)
        elif isinstance(sym, ast.ClassDef):
            result = _parse_class_simplified(sym)
            results.update(result)

    lineno = symbol.lineno
    for decorator in symbol.decorator_list:
        lineno += 1

    results[lineno] = (name, 'c')
    return results


def _parse_function_simplified(symbol, member_of=""):
    results = {}
    inside_class = True if member_of != "" else False

    if member_of:
        func_name = member_of + " : " + symbol.name + '('
    else:
        func_name = symbol.name + '('
    # We store the arguments to compare with default backwards
    defaults = []
    for value in symbol.args.defaults:
        # TODO: In some cases we can have something like: a=os.path
        defaults.append(value)
    arguments = []
    for arg in reversed(symbol.args.args):
        if not isinstance(arg, ast.Name) or arg.id == "self":
            continue
        argument = arg.id
        if defaults:
            value = defaults.pop()
            arg_default = _map_type.get(value.__class__, None)
            if arg_default is None:
                if isinstance(value, ast.Attribute):
                    arg_default = model.expand_attribute(value)
                elif isinstance(value, ast.Name):
                    arg_default = value.id
                else:
                    arg_default = 'object'
            argument += '=' + arg_default
        arguments.append(argument)
    func_name += ', '.join(reversed(arguments))
    if symbol.args.vararg is not None:
        if not func_name.endswith('('):
            func_name += ', '
        func_name += '*'
        func_name += symbol.args.vararg.arg
    if symbol.args.kwarg is not None:
        if not func_name.endswith('('):
            func_name += ', '
        func_name += '**'
        func_name += symbol.args.kwarg.arg
    func_name += ')'

    for sym in symbol.body:
        if isinstance(sym, ast.FunctionDef):
            result = _parse_function_simplified(sym, symbol.name)
            results.update(result)

    lineno = symbol.lineno
    for decorator in symbol.decorator_list:
        lineno += 1

    results[lineno] = (func_name, 'f', inside_class)
    return results
