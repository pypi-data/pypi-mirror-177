
from __future__ import annotations

from typing import Any
import collections.abc
import pathlib
import importlib
import importlib.util

import conditor
import conditor.build
import conditor.util


class ActionManager :
    """Project action manager."""

    def __init__(self,project:conditor.Project) :

        self.project:conditor.Project = project
        """Reference to related project instance."""

        self._entries = {}
        """Project action entries."""

        self.default_map_interface:DefaultMapInterface = DefaultMapInterface(self)
        """Default interface as mutable mapping."""

        self.string_map_interface:StringMapInterface = StringMapInterface(self)
        """Interface as mapping returning run_str from actions."""

        return

    @property
    def names(self) -> list[str] :
        """Get list of all loaded action names."""
        action_names = []
        for action_name in self._entries :
            action_names.append(action_name)
            pass
        return action_names

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'ActionManager({str(self.project)})'

    def new(self, action_cls:type[Action], name:str|None=None, replace:bool=True) :
        """New action.

        Add new action to this action manager from given action class.

        Parameters:
            action_cls:
                Class of new action.
            name:
                Call name for new action.
                If `None`, default name in action class will be used.
            replace:
                If existing action should be replaced by this.
        """
        if name is None :
            name = action_cls.DEFAULT_NAME
            pass
        if name in self._entries and not replace :
            return
        self._entries[name] = action_cls(
            project = self.project,
            name = name)
        return

    def new_from_module_file(self, path:pathlib.Path|str, replace:bool=True) :
        """New actions from given module file.

        Parameters:
            path:
                Path of module to import.
            replace:
                If existing actions should be replaced by this.
        """

        # Import module if not loaded.
        module_name = f'{self.project.config["conditor.action.file_module_initials"]}{path}'
        module = conditor.util.import_module_path(module_name, path)

        # Create new action from given module file.
        for cls_name in getattr(module, '__CONDITOR_ACTIONS__') :
            action_cls = getattr(module, cls_name)
            self.new(action_cls, replace=replace)
            pass

        return

    def new_from_module_file_class(self, path:pathlib.Path|str, cls_name:str, name:str=None, replace:bool=True) :
        """New action from given module file path and class name.

        Parameters:
            path:
                Path of module to import.
            cls_name :
                Name of action class.
            name:
                Call name of new action.
                If `None`, default name from action class will be used.
            replace:
                If existing action should be replaced by this.
        """

        # Import module if not loaded.
        module_name = f'{self.project.config["conditor.action.file_module_initials"]}{path}'
        module = conditor.util.import_module_path(module_name, path)

        # Create new action from given module file.
        action_cls = getattr(module, cls_name)
        self.new(action_cls, name, replaace)

        return

    def new_from_module(self, module_name:str, replace:bool=True) :
        """New action from given module and class name.

        Parameters:
            module_name:
                Name of module to import.
            replace:
                If existing action should be replaced by this.
        """
        module = importlib.import_module(module_name)
        for cls_name in getattr(module, '__CONDITOR_ACTIONS__') :
            action_cls = getattr(module, cls_name)
            self.new(action_cls, replace=replace)
            pass

        return

    def new_from_module_class(self, module_name:str, cls_name:str, name:str=None, replace:bool=True) :
        """New action from given module and class name.

        Parameters:
            module_name:
                Name of module to import.
            cls_name:
                Name of action class.
            name:
                Call name of new action.
                If `None`, default name from action class will be used.
            replace:
                If existing action should be replaced by this.
        """
        module = importlib.import_module(module_name)
        action_cls = getattr(module, cls_name)
        self.new(action_cls, name, replace)
        return

    pass


class Action :
    """Conditor action superclass."""

    DEFAULT_NAME:str = '__ACTIONSUPERCLASS__'
    """Default action name, if none was given."""

    def __init__(self, project:conditor.Project, name:str) :

        self.project = project
        """Reference to related project."""

        self.name = name
        """Call name of this action."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'Action({self.name})'

    def setup_cli(self, parser) :
        """Setup for command line interface parser."""
        return

    def run(self, *args, **kwargs) -> Any :
        """Default run method."""
        return

    def run_cli(self, args:dict) -> None:
        """Invoke from command line interface.

        Parameters:
            args:
                Argument parser parsed arguments namespace.
        """
        self.run(args=args)
        return

    def run_str(self) -> str :
        """Ustally invoked for string formatting, expecting a string return."""
        return str(self.run())

    pass


class DefaultMapInterface (collections.abc.MutableMapping) :
    """Default mutable mapping actions interface."""

    def __init__(self, action_manager:ActionManager) :

        self.action_manager = action_manager
        """Reference to related configuration manager."""

        return

    def __str__(self) :
        return self.__repr__()
    def __repr__(self) :
        return f'DefaultMapInterface({str(self.action_manager)})'

    def __getitem__(self, name) :
        return self.action_manager._entries[name]

    def __setitem__(self, name, value) :
        return self.action_manager.new(value, name)

    def __delitem__(self, name) :
        return self.action_manager._entries.__delitem__(name)

    def __iter__(self) :
        return self.action_manager._entries.__iter__()

    def __len__(self) :
        return self.action_manager._entries.__len__()

    pass


class StringMapInterface (collections.abc.Mapping) :
    """String casting map actions interface."""

    def __init__(self, action_manager:ActionManager) :

        self.action_manager = action_manager
        """Reference to related configuration manager."""

        return

    def __str__(self) :
        return self.__repr__()
    def __repr__(self) :
        return f'StringMapInterface({str(self.action_manager)})'

    def __getitem__(self, name) :
        return self.action_manager._entries[name].run_str()

    def __delitem__(self, name) :
        return self.action_manager._entries.__delitem__(name)

    def __iter__(self) :
        return self.action_manager._entries.__iter__()

    def __len__(self) :
        return self.action_manager._entries.__len__()


