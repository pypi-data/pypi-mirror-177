
from __future__ import annotations

from typing import Any
import collections.abc

import conditor
import conditor.__config__


class ConfigManager :
    """Project configuration manager

    Stores and manages project configuration entries.
    """

    def __init__(self, project:conditor.Project) :
        """Initialize configuration manager.

        Parameters:
            project:
                Reference to related project instance.
        """

        self.project:conditor.Project = project
        """Reference to related project instance."""

        self._entries = {}
        """Dictionary of configuration entries."""

        self.default_map_interface:DefaultMapInterface = DefaultMapInterface(self)
        """Interface instance for configuration access as map."""

        self.string_map_interface:StringMapInterface = StringMapInterface(self)
        """Interface instance for configuration access as map casting strings."""

        # Load initial configuration.
        self._load_init_config()

        return

    def __str__(self) -> str:
        return self.__repr__()
    def __repr__(self) -> str:
        return f'ConfigManager({str(self.project)})'

    @property
    def names(self) -> list[str]:
        """Returns list of all config entry names."""
        names = []
        for entry in self._entries :
            names.append(entry)
            pass
        return names

    def _load_init_config(self) :
        """Loads initial project configuration."""

        # Load initial conditor entries.
        self._entries = {**self._entries, **conditor.__config__.INIT_CONFIG}
        _e = self._entries

        # Define default project paths.
        _e['path'] = self.project.path
        _e['path.cpm'] = _e['path'].joinpath(f'./{_e["conditor.cpm.filename"]}').resolve()
        _e['path.source'] = _e['path'].joinpath(f'./src').resolve()
        _e['path.docsrc'] = _e['path'].joinpath(f'./docs').resolve()
        _e['path.build'] = _e['path'].joinpath(f'./build').resolve()
        _e['path.distribute'] = _e['path'].joinpath(f'./dist').resolve()

        return

    def get(self, name:str) -> Any :
        """Get config entry.

        Get a configuration entry by name.

        Parameters:
            name:
                Name of configuration entry to return.

        Returns:
            Value of requested configuration entry.
        """
        return self._entries[name]

    def set(self, name:str, value:Any) :
        """Set config entry.

        Set a configuration entry value by name.

        Parameters:
            name:
                Name of the configuration entry to set.
            value:
                New value of configuration entry.
        """
        self._entries[name] = value
        return

    pass

class DefaultMapInterface (collections.abc.MutableMapping):
    """Default configuration manager map interface.

    Interface to access configuration entries as mutable map.
    """

    def __init__(self, config_manager:ConfigManager) :

        self.config_manager:ConfigManager = config_manager
        """Reference to related configuration manager."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'DefaultMapInterface({str(self.config_manager)})'

    def __getitem__(self, name:str) -> Any :
        return self.config_manager.get(name)

    def __setitem__(self, name:str, value:Any) :
        return self.config_manager.set(name, value)

    def __delitem__(self, name:str) :
        return self.config_manager._entries.__delitem__(name)

    def __iter__(self) :
        return self.config_manager._entries.__iter__()

    def __len__(self) :
        return self.config_manager._entries.__len__()

        return


class StringMapInterface (collections.abc.Mapping):
    """String configuration map interface
    
    Interface to access configuration entries, casting return values as strings.
    """

    def __init__(self, config_manager:ConfigManager) :

        self.config_manager:ConfigManager = config_manager
        """Reference to related configuration manager."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'StringMapInterface({str(self.config_manager)})'

    def __getitem__(self, name:str) -> Any :
        return str(self.config_manager.get(name))

    def __delitem__(self, name:str) :
        return self.config_manager._entries.__delitem__(name)

    def __iter__(self) :
        return self.config_manager._entries.__iter__()

    def __len__(self) :
        return self.config_manager._entries.__len__()

        return

    pass

