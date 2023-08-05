from ..ConexAPI import ConexAPI
from . import DebugParser


def _setup_remove_command(subparsers, conex_api: ConexAPI):
    parser = subparsers.add_parser("remove", help="Disable editable mode for a package")
    parser.add_argument("path", help="Path to the package folder in the user workspace")
    parser.set_defaults(command_func=lambda args: conex_api.editable.remove(args.path))


def _setup_add_command(subparsers, conex_api: ConexAPI):
    parser = subparsers.add_parser("add", help="Put a package in editable mode")
    parser.add_argument("path", help="Path to the package folder in the user workspace")
    parser.set_defaults(command_func=lambda args: conex_api.editable.add(args.path))


def setup_command(subparsers, conex_api: ConexAPI):
    parser = subparsers.add_parser("editable", help='''
        Manages editable packages (packages that reside in the user workspace, 
        but are consumed as if they were in the cache).''')

    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand")
    subparsers.required = True

    _setup_add_command(subparsers, conex_api)
    _setup_remove_command(subparsers, conex_api)

    DebugParser.setup(parser)
