
from .__init__ import *


class CMD_Action (Command) :
    CMD_NAME = 'action'
    CMD_SHORTDESC = 'Action commands group.'
    CMD_DESCRIPTION = 'Interact with project actions..'
    def load(self, parser) :
        self[CMD_ListNames.CMD_NAME] = CMD_ListNames
        self[CMD_Run.CMD_NAME] = CMD_Run
        return
    def run(self, args, final) :
        return
    pass


class CMD_ListNames (Command) :
    CMD_NAME = 'list-names'
    CMD_SHORTDESC = 'List all available action entry names.'
    CMD_DESCRIPTION = 'Print a list of all available action entry names.'
    def load(self, parser) :
        parser.add_argument('--delimiter',
            action = 'store',
            const = None,
            default = '\n',
            type = str,
            choices = None,
            required = False,
            help = 'Delimiter used to separate action names.',
            metavar = '<delimiter>',
            dest = self.argname('delimiter')
        )
        return
    def run(self, args, final) :
        if not final :
            return
        delimiter = self.get_arg(args, 'delimiter', '\n')
        names_str = delimiter.join(self.project.action_manager.names)
        self.output(names_str, '\n')
        return
    pass


class CMD_Run (Command) :
    CMD_NAME = 'run'
    CMD_SHORTDESC = 'Run action.'
    CMD_DESCRIPTION = 'Runs the given action in current context.'
    def load(self, parser) :
        parser.add_argument(
            action = 'store',
            const = None,
            type = str,
            choices = None,
            help = 'Name of action entry.',
            metavar = '<action_name>',
            dest = self.argname('name')
        )
        return
    def run(self, args, final) :
        if not final :
            return
        action_name = self.get_arg(args, 'name')
        action = self.project.action[action_name]
        action.setup_cli(self.parser)

        args_namespace, unknown_args = self.parser.parse_known_args(
            self.get_args_unknown(args),
            self.get_args_namespace(args))
        args = vars(args_namespace)
        args['__parse__.namespace'] = args_namespace
        args['__parse__.unknown'] = unknown_args

        action_return = action.run_cli(args)
        self.output(action_return, '\n')
        return
    pass

