"""
Python 3 package build recipes.

.. note::
    Requires :py:class:`conditor.actlib.py3pkg.toml.ListAuthors` action..

"""


from __future__ import annotations

import pathlib
import subprocess

import conditor.action
import conditor.build
import conditor.compose


__CONDITOR_RECIPES__ = ['Base', 'Install']


class Base (conditor.build.Recipe) :
    """Basic Python 3 package build recipe.

    Outputs a build and source distribution to the output directory.
    """

    DEFAULT_NAME = 'conditor.py3pkg'

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)

        # Define staging order.
        self.stages['create'] = type(self).create
        self.stage_order.append('create')
        self.stages['configure'] = type(self).configure
        self.stage_order.append('configure')
        self.stages['deploy'] = type(self).deploy
        self.stage_order.append('deploy')
        self.stages['compose'] = type(self).compose
        self.stage_order.append('compose')
        self.stages['build'] = type(self).build
        self.stage_order.append('build')
        self.stages['distribute'] = type(self).distribute
        self.stage_order.append('distribute')
        self.stages['clean'] = type(self).clean
        #self.stage_order.append('clean')

        return

    @classmethod
    def create(cls, build) :
        """Initial build creation."""
        return

    @classmethod
    def configure(cls, build) :
        """Configure build."""

        # Define build paths.
        build.paths['build.source'] = build.path.joinpath('./src')
        build.paths['build.output'] = build.path.joinpath('./out')

        return

    @classmethod
    def deploy(cls, build) :
        """Build package file tree."""

        # Create build file tree.
        build.paths['build.source'].mkdir(parents=True, exist_ok=True)
        build.paths['build.output'].mkdir(parents=True, exist_ok=True)

        return

    @classmethod
    def compose(cls, build) :
        """Copy and format source tree."""

        # Compose source tree.
        build.composer.compose_tree(
            src_root = build.project.config['conditor.build.py3pkg.python_source_tree_path'],
            dst_root = build.paths['build.source'])

        return

    @classmethod
    def build(cls, build) :
        """Build Python 3 package."""

        # Compose Python package build command.
        p_cmd = ['python3', '-m', 'build',
            '--outdir', build.paths['build.output'],
            build.paths['build.source']
        ]

        # Run python package build command.
        p = subprocess.run(p_cmd,
            cwd = build.path
        )

        # Get output files.
        for outfile in build.paths['build.output'].iterdir() :
            if outfile.match('*.whl') :
                build.paths['build.output.build_dist'] = outfile
                continue
            elif outfile.match('*.tar.gz') :
                build.paths['build.output.source_dist'] = outfile
                continue
            pass

        return

    @classmethod
    def distribute(cls, build) :
        """Output package."""

        # Create distribute directory.
        build.paths['distribute'].mkdir(parents=True, exist_ok=True)

        # Define output files.
        dist_build = build.paths['distribute'].joinpath(build.paths['build.output.build_dist'].name).resolve()
        dist_source = build.paths['distribute'].joinpath(build.paths['build.output.source_dist'].name).resolve()

        # Copy build output.
        conditor.compose.copy(build.paths['build.output.build_dist'], dist_build)
        conditor.compose.copy(build.paths['build.output.source_dist'], dist_source)

        return

    @classmethod
    def clean(cls, build) :

        # Delete build file tree.
        conditor.compose.rm_tree(build.path)

        return

    pass


class Install (Base) :
    """Installs the built Python 3 package instead of distributing."""

    DEFAULT_NAME = 'conditor.py3pkg.install'

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)

        # Change distribute for install.
        self.stages['distribute'] = type(self).distribute

        return

    @classmethod
    def distribute(cls, build) :
        """install built package."""

        # Compose Python pipy install command..
        p_cmd = ['python3', '-m', 'pip', 'install',
            '--force-reinstall',
            build.paths['build.output.build_dist']
        ]

        # Run install command.
        p = subprocess.run(p_cmd,
            cwd = build.path
        )

        return

    pass

