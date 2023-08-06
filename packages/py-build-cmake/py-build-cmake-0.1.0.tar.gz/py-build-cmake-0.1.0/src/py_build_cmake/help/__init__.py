import html
import itertools
import shutil
import textwrap

from ..config_options import ConfigOption, PathConfigOption, RequiredValue, pth2str


def _print_wrapped(text, indent, width=None):
    """Print the given string with the given indentation, wrapping it to the
    desired width, preserving line endings. If `width` is None, use the width 
    of the terminal, or 80 columns as a fallback."""
    if width is None:
        width = shutil.get_terminal_size((80, 24)).columns
    wrapper = textwrap.TextWrapper(width=width,
                                   initial_indent=indent,
                                   subsequent_indent=indent)
    wrapped = [wrapper.wrap(i) for i in text.split('\n')]
    for line in itertools.chain.from_iterable(wrapped):
        print(line)


def get_default_str(opt: ConfigOption):
    """Get a string representation of the default value for the given option."""
    return opt.default.get_name()


def help_print_md(pbc_opts: ConfigOption):
    """
    Prints the top-level options in `pbc_opts` as MarkDown tables.
    """
    print("# py-build-cmake configuration options\n")
    print("These options go in the `[tool.py-build-cmake]` section of "
          "the `pyproject.toml` configuration file.\n")
    for k, v in pbc_opts.sub.items():
        print('##', k)
        print(_get_full_description(v), '\n')
        print('| Option | Description | Type | Default |')
        print('|--------|-------------|------|---------|')
        for kk, vv in v.sub.items() or {}:
            print('|', f'`{kk}`', '|', _get_full_description(vv), '|',
                  vv.get_typename() or '', '|', f'`{get_default_str(vv)}`',
                  '|')
        print()
    print("# Local overrides\n")
    print("Additionally, two extra configuration files can be placed in "
          "the same directory as `pyproject.toml` to override some "
          "options for your specific use case:\n\n"
          "- `py-build-cmake.local.toml`: the options in this file "
          "override the values in the `tool.py-build-cmake` section of "
          "`pyproject.toml`.<br/>This is useful if you need specific "
          "arguments or CMake options to compile the package on your "
          "system.\n"
          "- `py-build-cmake.cross.toml`: the options in this file "
          "override the values in the `tool.py-build-cmake.cross` section "
          "of `pyproject.toml`.<br/>Useful for cross-compiling the "
          "package without having to edit the main configuration file.\n")
    print("# Command line overrides\n")
    print("Instead of using the `py-build-cmake.local.toml` and "
          "`py-build-cmake.cross.toml` files, you can also include "
          "additional config files using command line options:\n\n"
          "- `--local`: specifies a toml file that overrides the "
          "`tool.py-build-cmake` section of `pyproject.toml`, "
          "similar to `py-build-cmake.local.toml`\n"
          "- `--cross`: specifies a toml file that overrides the "
          "`tool.py-build-cmake.cross` section of `pyproject.toml`, "
          "similar to `py-build-cmake.cross.toml`\n\n"
          "These command line overrides are applied after the "
          "`py-build-cmake.local.toml` and `py-build-cmake.cross.toml` "
          "files in the project folder (if any).\n\n"
          "When using PyPA build, these flags can be specified using "
          "the `-C` or `--config-setting` flag: \n"
          "```sh\n"
          "python -m build . -C--cross=/path/to/my-cross-config.toml\n"
          "```\n"
          "The same flag may appear multiple times, for example: \n"
          "```sh\n"
          "python -m build . -C--local=conf-A.toml -C--local=conf-B.toml\n"
          "```\n"
          "For PyPA pip, you can use the `--config-settings` flag "
          "instead.")


def _get_full_description(vv: ConfigOption):
    descr = _md_escape(vv.description)
    if isinstance(vv, PathConfigOption):
        descr += '<br/>' + _describe_path_option(vv).capitalize() + '.'
    if vv.inherit_from:
        descr += '<br/>Inherits from: `/' + pth2str(vv.inherit_from) + '`'
    if vv.example:
        descr += '<br/>For example: `' + vv.example + '`'
    return descr


def _md_escape(descr):
    descr = html.escape(descr)
    descr = descr.replace('\n', '<br/>')
    descr = descr.replace('*', '\\*')
    descr = descr.replace('_', '\\_')
    return descr


def recursive_help_print(opt: ConfigOption, level=0):
    """Recursively prints the help messages for the options in `opt`."""
    for k, v in opt.sub.items():
        if k == 'project':
            continue
        indent = 4 * level * ' '
        header = '\n' + k
        if v.sub:
            header += ':'
            print(textwrap.indent(header, indent))
            if v.description:
                _print_wrapped(v.description, indent + '  ')
            recursive_help_print(v, level + 1)
        else:
            headerfields = []
            typename = v.get_typename()
            if typename is not None:
                headerfields += [typename]
            if isinstance(v, PathConfigOption):
                headerfields += [_describe_path_option(v)]
            is_required = isinstance(v.default, RequiredValue)
            if is_required:
                headerfields += ['required']
            if v.inherit_from:
                headerfields += ['inherits from /' + pth2str(v.inherit_from)]
            if headerfields:
                header += ' (' + ', '.join(headerfields) + ')'
            print(textwrap.indent(header + ':', indent))
            _print_wrapped(v.description, indent + '  ')
            if v.example:
                _print_wrapped('For example: ' + v.example, indent + '  ')
            default = v.default.get_name()
            if default is not None and not is_required:
                print(textwrap.indent('Default: ' + default, indent + '  '))


def _describe_path_option(v: PathConfigOption):
    t = 'absolute or relative' if v.allow_abs else 'relative'
    if v.base_path is not None:
        t += ' to ' + v.base_path.description
    return t


def help_print(pbc_opts: ConfigOption):
    print("List of py-build-cmake pyproject.toml options:")
    recursive_help_print(pbc_opts)
    print()
