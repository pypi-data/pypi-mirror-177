"""
Actions to compose TOML file.

Conditor builtin actions for Python 3 packaging to compose toml file.
"""

import os
import subprocess
import pathlib

import conditor.action

__CONDITOR_ACTIONS__ = ['ListAuthors']


class ListAuthors (conditor.action.Action) :
    """Composesa a list of project authors for the TOML file."""

    DEFAULT_NAME = 'conditor.py3pkg.toml.list_authors'

    def __init__(self, *args, **kwargs) :
        super().__init__(*args, **kwargs)
        return

    def run(self, script=None) :

        # Compose authors string.
        als = 'authors = ['
        for author in self.project.config['project.authors'] :
            author_tag = author[0]
            author_name = author[1]
            author_email = author[2]
            als += f'    {{ name = \'{author_name}\', email =\'{author_email}\' }}'
            pass
        als += ']'

        return als

    pass

