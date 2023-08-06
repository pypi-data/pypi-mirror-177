
import pathlib
import subprocess
import os

import conditor.action
import conditor.build
import conditor.compose


__CONDITOR_RECIPES__ = ['HTML']


class HTML (conditor.build.Recipe) :
    """Builds Sphinx html documentation.

    Stores the resulting HTML in the output directory.
    """

    DEFAULT_NAME = 'conditor.sphinx.html'

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
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
        """Configure build process."""

        # Set build paths.
        build.paths['docs.source'] = build.path.joinpath('./docs_source')
        build.paths['docs.output'] = build.path.joinpath('./out')
        build.paths['ref.python_source'] = build.project.config['conditor.build.sphinx.python_source_tree_path']

        return

    @classmethod
    def deploy(cls, build) :
        """Create build process initial file tree."""

        # Create build file tree.
        build.paths['docs.source'].mkdir(parents=True, exist_ok=True)
        build.paths['docs.output'].mkdir(parents=True, exist_ok=True)

        return

    @classmethod
    def compose(cls, build) :
        """Copy documentation source file tree."""

        build.composer.compose_tree(
            src_root = build.project.config['path.docsrc'],
            dst_root = build.paths['docs.source'])

        return

    @classmethod
    def build(cls, build) :
        """Build the HTML documentation."""

        # Compose build command.
        p_cmd = ['sphinx-build', '-a',
            '-b', 'html', # Sphinx builder.
            '-c', build.paths['docs.source'], # Location of config containing directory.
            build.paths['docs.source'], # Source location.
            build.paths['docs.output'] # Build output.
        ]

        # Modify build environment.
        p_env = os.environ.copy()
        p_env['PYTHONPATH'] = build.paths['ref.python_source']

        # Execute build.
        p = subprocess.run(p_cmd,
            cwd = build.path,
            env = p_env
        )

        return

    @classmethod
    def distribute(cls, build) :
        """Copies build outut to distribute."""

        # Copy output files.
        conditor.compose.copy(build.paths['docs.output'], build.paths['distribute'])

        return

    @classmethod
    def clean(cls, build) :
        """Deletes build directory."""

        conditor.compose.rm_tree(build.path)

        return

    pass

