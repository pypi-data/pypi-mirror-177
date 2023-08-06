
from __future__ import annotations

import argparse
import pathlib
import collections.abc

import conditor


EPILOG = 'Conditor (https://gitlab.com/srhuerzeler/conditor)'
"""Conditor default epilog."""


class Command (collections.abc.MutableMapping) :
    """Superclass for cli commands."""

    CMD_NAME = 'CMD_NAME'
    """Command call name."""

    CMD_SHORTDESC = 'SHORT DESCRIPTION'
    """Single line command description."""

    CMD_DESCRIPTION = 'LONG DESCRIPTION'
    """Extensive command descripton."""

    def __init__(self, name:str, parent:Command|None=None) :
        """Initialize command.

        Parameters:
            name:
                call name of this command.
            parent:
                instance of related parent command.
        """

        self.name = name
        """Call name of this command."""

        self.commands = {}
        """Dictionary of sub-commands."""

        self.parent = parent
        """Reference to parent command."""

        self._parser = None
        """Stores argparse parser instance if loaded."""

        return

    def __getitem__(self, name:str) -> Command :
        return self.commands[name]
    def __setitem__(self, name:str, value:type[Command]) :
        self.commands[name] = value(name, self)
        return
    def __delitem__(self, name:str) :
        self.commands.__delitem__(name)
        return
    def __iter__(self) :
        return self.commands.__iter__()
    def __len__(self) -> int :
        return self.commands.__len__()

    def output(self, *print_obj) :
        print(*print_obj, end = '')
        return

    @property
    def short_description(self) :
        return type(self).CMD_SHORTDESC

    @property
    def description(self) :
        return type(self).CMD_DESCRIPTION

    @property
    def chain_list(self) -> list[str] :
        """Names of root command to this command."""
        if self.parent is None :
            return [self.name]
        return [*self.parent.chain_list, self.name]

    @property
    def chain(self) -> str :
        """Dot character delimited command chain list."""
        return '.'.join(self.chain_list)

    @property
    def parser(self) -> argparse.Parser :
        """Instance of related argparse parser."""
        if self._parser is not None :
            return self._parser
        self._load()
        return self._parser

    @property
    def root_command(self) -> Command :
        """Get instance of root command."""
        if self.parent is None :
            return self
        return self.parent.root_command

    @property
    def project(self) -> conditor.Project|None :
        """Related project instance."""
        return self.root_command._project

    def argname(self, name:str) -> str :
        """Compose name for argument related to this command.

        Uses the chain and adds given name to build unique name for argument destination value.

        Parameters:
            name:
                Name of argument to build argument name.

        Returns:
            To this command related argument name.
        """
        return f'{self.chain}.{name}'

    def load(self, parser:argparse.Parse) :
        """Can be used to define custom arguments for this command.

        Parameters:
            parser:
                argparse.Parser to which arguments can be added.
        """
        return

    def _load(self) :
        """Load this command.

        Invokes loading of this command andalso handles sub-commands.
        """

        # Command parser.
        self._parser = argparse.ArgumentParser(
            prog = ' '.join(self.chain_list),
            description = self.description,
            epilog = EPILOG,
            allow_abbrev = False,
            add_help = False,
            formatter_class = argparse.RawTextHelpFormatter,
            exit_on_error = False
        )

        # Custom error handling.
        def _parsererror(msg) :
            #print('PARSER ERROR:', msg)
            return
        self._parser.error = _parsererror

        # Invoke custom load.
        self.load(self._parser)

        # Return if no sub-commands.
        if len(self.commands) == 0 :
            return

        # Compose sub-commands choices.
        cmd_choice = []
        for command in self.commands :
            cmd_choice.append(command)
            pass

        # Compose help text.
        help_str = 'Possible commands:\n'
        for command in self.commands :
            help_str += f'{command} => {self.commands[command].short_description}\n'
            pass

        # Add argument to argparse parser.
        self._parser.add_argument(
            dest = self.argname('command'),
            action = 'store',
            metavar = 'COMAND',
            help = help_str,
            default = None,
            nargs = '?',
            choices = cmd_choice,
        )
        return

    def get_command_name(self, args:dict) -> str :
        """Get name of selected sub-command from arguments dict.
        Parameters:
            args:
                Dictionary of arguments from parsing.
        Returns:
            Name of selected cub-command.
            `None` if not in args.
        """
        argname = self.argname('command')
        if argname in args :
            return args[argname]
        return None

    def get_arg(self, args:dict, name:str, fallback=None) :
        """Get argument by name."""
        argname = self.argname(name)
        if argname in args :
            return args[argname]
        return fallback

    def get_command(self, args:dict) -> Command :
        """Get command instance from arguments dict.
        Parameters:
            args:
                Dictionary of arguments from parsing.
        Returns:
            Instance of selected sub-command
        """
        return self[self.get_command_name(args)]

    def _add_help_argument(self) :
        """Adds a help argument to this command's parser. Invoked when this is a final command."""
        self.parser.add_argument('--help',
            action='store_true',
            dest = 'help',
        )
        return

    def parse(self, argv:list[str]=None, args_namespace:argparse.Namespace=None) -> dict :
        """Parse this command.

        Parameters:
            argv:
                List of arguments given to this command.
            args_namespace:
                Already existing namespace parsed before this command.

        Returns:
            Dictionary of parsed commands.
        """

        # process parser arguments.
        args_namespace, unknown_args = self.parser.parse_known_args(argv, args_namespace)
        args = vars(args_namespace)
        args['__parse__.namespace'] = args_namespace
        args['__parse__.unknown'] = unknown_args

        # If this is a final comand.
        final = self.get_command_name(vars(args_namespace)) is None

        # Return current args if final.
        if final :
            self._add_help_argument()
            args_namespace, unknown_args = self.parser.parse_known_args(argv, args_namespace)
            args = vars(args_namespace)
            args['__parse__.namespace'] = args_namespace
            args['__parse__.unknown'] = unknown_args
            return args

        return self.get_command(args).parse(unknown_args, args_namespace)

    def get_args_unknown(self, args) :
        return args['__parse__.unknown']

    def get_args_namespace(self, args) :
        return args['__parse__.namespace']

    def run(self, args:dict, final:bool) :
        """Can be used to define custom run functions for commands.

        Parameters:
            args:
                Dictionary of parsed arguments.
            final:
                If this is the final requested command.
        """
        print('RUN', args, 'RUN')
        return

    def _run(self, args:dict) :
        """Runs this command.

        Handles invokingof run or printing help.

        Parameters:
            args:
                Dictionary of parsed arguments.
        """

        # If this is the final requested command.
        final = self.get_command_name(args) is None

        # If help requested.
        if args['help'] :
            if final :
                return self.get_help()
            self.get_command(args)._run(args)
            return

        # Invoke custom run and exit if final.
        self.run(args, final)
        if final :
            return

        # Run sub command.
        self.get_command(args)._run(args)

        return

    def get_help(self) :
        """Returns string to print as help message."""
        self.parser.print_help()
        return

    pass


class CMD_Conditor (Command) :
    """Conditor root CLI command."""
    CMD_NAME = 'conditor'
    CMD_SHORTDESC = 'Conditor CLI.'
    CMD_DESCRIPTION = 'Conditor command line interface.'
    def __init__(self, name='conditor') :
        super().__init__(name)

        self._project = None
        """Stores project instance if loaded."""

        return
    def load(self, parser=None) :
        parser = self.parser
        from . import config
        from . import action
        from . import build
        self[config.CMD_Config.CMD_NAME] = config.CMD_Config
        self[action.CMD_Action.CMD_NAME] = action.CMD_Action
        self[build.CMD_Build.CMD_NAME] = build.CMD_Build
        parser.add_argument('--project-path',
            action = 'store',
            nargs = 1,
            const = None,
            default = './',
            type = pathlib.Path,
            choices = None,
            required = False,
            help = 'Any path within project root.',
            metavar = '<project_path>',
            dest = self.argname('project-path')
        )
        return
    def run(self, args, final=False) :
        project_path = self.get_arg(args, 'project-path')
        self._project = conditor.Project.get(project_path)
        return
    def parse(self, argv=None) :
        namespace = argparse.Namespace()
        namespace.help = False
        args = super().parse(argv, namespace)
        return args
    def exec(self, argv=None) :
        args = self.parse(argv)
        self._run(args)
        return 0

    pass

