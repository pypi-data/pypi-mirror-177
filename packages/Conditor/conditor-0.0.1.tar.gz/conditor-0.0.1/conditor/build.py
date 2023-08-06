
from __future__ import annotations

import json
import collections.abc
import pathlib
import importlib

import conditor
import conditor.util


class BuildProcess :
    """Represents a build process instance."""

    @classmethod
    def create(cls,
        project : conditor.Project,
        path : pathlib.Path | str,
        init_data : dict = {}
    ) -> BuildProcess :
        """Create build process

        Factory to create new build process instance.

        Parameters:
            project:
                Related conditor project instance.
            path:
                Path to new build directory.
            init_data:
                Initial data for this build.

        Returns:
            Instance of new created build.
        """
        process = cls(project, path)

        # Create build process file tree.
        process.path.mkdir(parents=True, exist_ok=True)
        process.data_path.touch(exist_ok=True)

        # Write initial process data.
        process.data_path.write_text(json.dumps(init_data))

        return process

    @classmethod
    def load(cls,
        project : conditor.Project,
        path : pathlib.Path | str,
        append_data : dict = {}
    ) -> BuildProcess :
        """Load build process

        Factory to load existing build process instance.

        Parameters:
            project:
                Related conditor project instance.
            path:
                Path to build directory to load.
            init_data:
                Data to append to loadedbuild instance

        Returns:
            Instance of loaded build.
        """

        # Initialize from file.
        process = cls(project, path)

        # Append process data.
        for data in append_data :
            process.data[data] = append_data[data]
            pass

        return process

    def __init__(self, project:conditor.Project, path:pathlib.Path) :
        """Build process initializer

        Danger:
            Use factory functions.
        """

        self.project:conditor.Project = project
        """Reference to related conditor project."""

        self.path:pathlib.Path = path
        """Path to build directory."""

        self.data:DefaultDataMapInterface = DefaultDataMapInterface(self)
        """Map interface for build data."""

        self.paths:PathDataInterface = PathDataMapInterface(self)
        """Map interface for paths."""

        self.composer = self.project.composer.new_context()
        """Composer context for this build process."""

        # Set build composer context data.
        self.composer.env['_b'] = self.data

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'BuildProcess({str(self.path)})'

    @property
    def data_path(self) -> pathlib.Path:
        """Path of build process data file."""
        return self.path.joinpath(f'./{self.project.config["conditor.build.data_file_name"]}').resolve()

    def _data_loads_dict(self) -> dict :
        """Loads dictionary of build data."""
        if self.data_path.exists() :
            return json.loads(self.data_path.read_text())
        return {}

    def _data_dumps_dict(self, data_dict:dict) :
        """Stores dictionary of build data."""
        self.data_path.write_text(json.dumps(data_dict))
        return

    @property
    def recipe(self) -> Recipe:
        """To this build related recipe instance."""
        return self.project.recipe[self.data['recipe.name']]

    def run_stage(self, name:str) :
        """Run stage by given name.

        Parameters:
            name:
                Name of stage to run.
        """
        self.data['recipe.current_stage'] = name
        return self.recipe.stages[name](self)

    def stage(self) -> int :
        """Run next recipe stage in stage order.

        Returns:
            Index of next stage.
            Is `-1` if complete.
        """

        # Get current stage index.
        stage_index = self.data['recipe.next_stage']
        if stage_index == -1 :
            return  -1
        stage_name = self.recipe.stage_order[stage_index]

        # Run stage.
        self.run_stage(stage_name)

        # Increment stage index.
        stage_index += 1
        if stage_index >= len(self.recipe.stage_order) :
            stage_index = -1
            pass
        self.data['recipe.next_stage'] = stage_index

        return stage_index

    def stage_all(self) :
        """Run all stages in stage order."""
        while self.stage() != -1 :
            pass
        return

    pass


class DefaultDataMapInterface (collections.abc.MutableMapping) :
    """Mutable map to interact with build data."""

    def __init__(self, build_process:BuildProcess) :

        self.build_process:BuildProcess = build_process
        """Reference to related build process instance."""

        return

    def __str__(self) -> str:
        return self.__repr__()
    def __repr__(self) -> str :
        return f'DefaultDataMapInterface({str(self.build_process)})'

    def __getitem__(self, name:str) -> Any :
        return self.build_process._data_loads_dict().__getitem__(name)

    def __setitem__(self, name:str, value:Any) :
        data_dict = self.build_process._data_loads_dict()
        data_dict.__setitem__(name, value)
        self.build_process._data_dumps_dict(data_dict)
        return

    def __delitem__(self, name:str) :
        data_dict = self.build_process._data_loads_dict()
        data_dict.__delitem__(name)
        self.build_process._data_dumps_dict(data_dict)
        return

    def __iter__(self) :
        return self.build_process._data_loads_dict().__iter__()

    def __len__(self) :
        return self.build_process._data_loads_dict().__len__()

    pass

class PathDataMapInterface (collections.abc.MutableMapping) :
    """Mutable map to interact with paths in build data."""

    def __init__(self, build_process:BuildProcess) :

        self.build_process:BuildProcess = build_process
        """Reference to related build process instance."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'PathDataMapInterface({str(self.build_process)})'

    def _compname(self, name:str) -> str:
        """Composed name of path data entry."""
        return f'path.{name}'

    def __getitem__(self, name:str) -> pathlib.Path :
        return pathlib.Path(self.build_process.data.__getitem__(self._compname(name)))

    def __setitem__(self, name:str, value:pathlib.Path|str) :
        value = pathlib.Path(value).resolve()
        return self.build_process.data.__setitem__(self._compname(name), str(value))

    def __delitem__(self, name:str) :
        return self.build_process.data.__delitem__(self._compname(name))

    def __iter__(self) :
        return self.build_process.data.__iter__()

    def __len__(self) :
        return self.build_process.data.__len__()

    pass



class Recipe :
    """Defines how a build is performed."""

    DEFAULT_NAME:str = '__UNDEFINED__'
    """Name of this recipe."""

    def __init__(self, project:conditor.Project, name:str) :

        self.project:conditor.Project = project
        """Reference to related project."""

        self.name:str = name
        """Defines index name of this recipe."""

        self.stages:dict = {}
        """Dictionary of recipe stages that can be performed. Defined as stage_name:stage_fn(build)"""

        self.stage_order:list[int] = []
        """List of stage names, in which this recipe is executed."""

        self.build_name_prefix:str = self.name
        """Prefix for build names."""

        return

    def __str__(self) -> str :
        return self.__repr__()
    def __repr__(self) -> str :
        return f'Recipe({self.name})'

    def new_build_process(self, identifier:str=None) -> BuildProcess :
        """Create a new build process.

        Parameters:
            identifier:
                Identifier for new build process.
                If `None`, config `conditor.build.fallback_id`.

        Returns:
            New created build process instance.
        """

        # Initial data for new build.
        build_data = {}
        build_data['build.identifier'] = identifier
        build_data['build.name'] = f'{self.build_name_prefix}-{identifier}'
        build_data['recipe.name'] = self.name
        build_data['recipe.current_stage'] = None
        build_data['recipe.next_stage'] = 0

        # Compose path of distribution location.
        build_data['path.distribute'] = str(self.project.config['path.distribute'].joinpath(f'./{build_data["build.name"]}').resolve())

        # Compose path for new build.
        build_path = self.project.config['path.build'].joinpath(f'./{build_data["build.name"]}').resolve()

        # Create new build process.
        process = BuildProcess.create(self.project, build_path, build_data)

        return process

    pass



class RecipeManager(dict) :
    """Stores loaded recipe instances."""
    def __init__(self, project:conditor.Project, *args, **kwargs) :
        super().__init__(*args, **kwargs)

        self.project = project
        """Reference to project instance."""

        return

    def __str__(self) :
        return self.__repr__()
    def __repr__(self) :
        return f'RecipeManager({self.project})'

    @property
    def names(self) -> list[str] :
        """List of all loaded recipe names."""
        names = []
        for name in self :
            names.append(name)
            pass
        return names

    def new(self, recipe_cls:type[Recipe], name:str=None, replace:bool=True) :
        """Add and initialize new recipe.

        Parameters:
            recipe_cls:
                Class of recipe to initialize.
            name:
                Call name for new recipe. Otherwise in class defined default will be used.
            replace:
                If existing recipe with same name sould be replaced by this.
        """
        if name is None :
            name = recipe_cls.DEFAULT_NAME
            pass
        self[name] = recipe_cls(self.project, name)
        return

    def new_from_module_file(self, path:str|pathlib.Path, replace:bool=True) :
        """New recipes from given module file.

        Parameters:
            path:
                Path of module containing recipes to add.
            replace:
                If existing recipe with same name sould be replaced by this.
        """

        # Import module if not loaded.
        module_name = f'{self.project.config["conditor.recipe.file_module_initials"]}{path}'
        module = conditor.util.import_module_path(module_name, path)

        # New recipes defined inmodule recipes constant.
        for cls_name in getattr(module, '__CONDITOR_RECIPES__') :
            recipe_cls = getattr(module, cls_name)
            self.new(recipe_cls, replace=replace)
            pass

        return

    def new_from_module_file_class(self, path:str|pathlib.Path, cls_name:str, name:str=None, replace:bool=True) :
        """New recipe from given module file and class name.

        Parameters:
            path:
                Path of module containing recipe to add.
            cls_name:
                String name of recipe class.
            name:
                Call name for new recipe. Otherwise in class defined default will be used.
            replace:
                If existing recipes with same name sould be replaced by this.
        """

        # Import module if not loaded.
        module_name = f'{self.project.config["conditor.recipe.file_module_initials"]}{path}'
        module = conditor.util.import_module_path(module_name, path)

        # Create new action from given module file.
        recipe_cls = getattr(module, cls_name)
        self.new(recipe_cls, name, replace)

        return

    def new_from_module(self, module_name:str, replace:bool=True) :
        """New recipes from given module.

        Parameters:
            module_name:
                String name of module containing recipes to add.
            replace:
                If existing recipes with same name sould be replaced by this.
        """

        # Import requested module.
        module = importlib.import_module(module_name)

        # New recipes defined inmodule recipes constant.
        for cls_name in getattr(module, '__CONDITOR_RECIPES__') :
            recipe_cls = getattr(module, cls_name)
            self.new(recipe_cls, replace=replace)
            pass

        return

    def new_from_module_class(self, module_name:str, cls_name:str, name:str=None, replace:bool=True) :
        """Import recipe from given module and class name.

        Parameters:
            module_name:
                String name of module containing recipe to add.
            cls_name:
                String name of recipe class.
            name:
                Call name for new recipe. Otherwise in class defined default will be used.
            replace:
                If existing recipe with same name sould be replaced by this.
        """

        # Import module.
        module = importlib.import_module(module_name)

        # New recipe from recipe class.
        build_cls = getattr(module, cls_name)
        self.new(build_cls, name, replace)

        return

    pass

