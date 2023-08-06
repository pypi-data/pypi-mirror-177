
from .__init__ import *


class CMD_Config (Command) :
    CMD_NAME = 'config'
    CMD_SHORTDESC = 'Configuration command group.'
    CMD_DESCRIPTION = 'Read, write and manage project configuration.'
    def load(self, parser) :
        self['list-names'] = CMD_ListNames
        self['get'] = CMD_Get
        return
    def run(self, args, final) :
        return
    pass


class CMD_ListNames (Command) :
    CMD_NAME = 'list-names'
    CMD_SHORTDESC = 'List all available configuration entry names.'
    CMD_DESCRIPTION = 'Print a list of all available configuration entry names.'
    def load(self, parser) :
        parser.add_argument('--delimiter',
            action = 'store',
            const = None,
            default = '\n',
            type = str,
            choices = None,
            required = False,
            help = 'Delimiter used to separate configuration names.',
            metavar = '<delimiter>',
            dest = self.argname('delimiter')
        )

        return
    def run(self, args, final) :
        if not final :
            return
        delimiter = self.get_arg(args, 'delimiter', '\n')
        names_str = delimiter.join(self.project.config_manager.names)
        self.output(names_str, '\n')
        return
    pass


class CMD_Get (Command) :
    CMD_NAME = 'get'
    CMD_SHORTDESC = 'Get value from coniguration.'
    CMD_DESCRIPTION = 'Get value of given configuration entry.'
    def load(self, parser) :
        parser.add_argument(
            action = 'store',
            const = None,
            type = str,
            choices = None,
            help = 'Name of configuration entry.',
            metavar = '<config_name>',
            dest = self.argname('name')
        )

        return
    def run(self, args, final) :
        if not final :
            return
        config_name = self.get_arg(args, 'name', '\n')
        config_value = self.project.strcfg[config_name]
        self.output(config_value, '\n')
        return
    pass

