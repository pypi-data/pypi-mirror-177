"""
Conditor Python3 development utility actions.
"""

import os
import subprocess
import pathlib

import conditor.action

__CONDITOR_ACTIONS__ = ['REPL']


class REPL (conditor.action.Action) :
    """Open REPL with access to imported source."""

    DEFAULT_NAME = 'conditor.dev.py3.repl'

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        return

    def run(self, script=None) :

        # Arguments for REPL execution.
        p_args = ['python3', '-i']

        # Requested script to run.
        if script is not None :
            script = script.resolve()
            p_args.append(script)
            pass

        # Execution environment.
        p_env = os.environ.copy()
        p_env['PYTHONPATH'] = self.project.config['path.source']

        # Run REPL with access ro source.
        p = subprocess.run(p_args,
            env = p_env
        )

        return

    def setup_cli(self, parser) :
        parser.add_argument('--script',
            action = 'store',
            #nargs = 1,
            const = None,
            default = None,
            type = pathlib.Path,
            choices = None,
            required = False,
            help = 'Execute given script before entering interactive mode.',
            metavar = '<script-path>',
            dest = 'run-script'
        )
        return

    def run_cli(self, args) :
        self.run(args['run-script'])
        return

    pass

