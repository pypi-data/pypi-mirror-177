
from __future__ import annotations

import pathlib
import shutil
import os
import typing

import conditor
import conditor.build

PathLike = pathlib.Path|str
"""Path like type."""

def _format_fnc_support(source_string:str, format_map:dict={}) -> str :
    """Workaround to use function calls in string to format.

    Parameters:
        source_string:
            String to format.
        format_map:
            Map of items to format in given string.

    Returns:
        Formatted string.
    """
    return eval(f'f"""{source_string}"""', globals(), format_map)

def _rp(path:PathLike) -> pathlib.Path :
    """Wrapper to resolve unknown path.

    Parameters:
        path:
            Path to resolve.

    Returns:
        Resolved path.
    """
    return pathlib.Path(path).resolve()

# -----------------------------------------------------------------------------
# File interaction and handling
# -----------------------------------------------------------------------------

def mkfile(path:PathLike) -> pathlib.Path :
    """Creates file and missing parents.

    Parameters:
        path:
            Path of file to create.

    Returns:
        Path ofnewvreated file.
    """
    path = _rp(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    return path

def copy_file(src_path:PathLike, dst_path:PathLike) -> pathlib.Path:
    """Copies bytes content from source file to destination file.

    Parameters:
        src_path:
            Path of file to copy.
        dst_path:
            Path of file copy destination.

    Returns:
        Path of copied file in destination.
    """
    return mkfile(dst_path).write_bytes(_rp(src_path).read_bytes())

def copy(src_path:PathLike, dst_path:PathLike) -> list[pathlib.Path] :
    """Copy dictionary or file.

    Parameters:
        src_path:
            Copy source path.
        dst_path:
            Copy descination path.

    Returns:
        List of relative copied paths.
    """

    # Resolve paths.
    src_path = _rp(src_path)
    dst_path = _rp(dst_path)

    # Copyfile if file.
    if src_path.is_file() :
        copy_file(src_path, dst_path)
        return

    # New destination directory.
    if src_path.is_dir() :
        dst_path.mkdir(parents=True, exist_ok=True)

        # Copy child nodes.
        for node in src_path.iterdir() :
            copy(node, dst_path.joinpath(node.name))
            pass

        return

    return

def file_write_str(dst_path:PathLike, src_str:str) -> pathlib.Path:
    """Wrapper to write string to file.

    Parameters:
        dst_path:
            Path of file to write to (will be created if not existing).

    Returns:
        Path of written to file.
    """
    return mkfile(dst_path).write_text(src_str)

def file_read_str(src_path:PathLike, fallback_return:typing.Any='') -> str|typing.Any :
    """Wrapper to read string from file.

    Parameters:
        src_path:
            Path of file to read.
        fallback_return:
            Return value, if file cannot be read.

    Returns:
        String of file contents. If not readable (e.g. non existing) it returns the `fallback_return` attribute.
    """
    return _rp(src_path).read_text()

# -----------------------------------------------------------------------------
# File tree handling
# -----------------------------------------------------------------------------

def iter_tree(
        root : PathLike,
        fn_node : typing.Callable[[pathlib.Path], bool]
    ) -> list[pathlib.Path] :
    """Iterate file tree.

    Iterates tree and performs given function on each node in tree, except root itself.

    Parameters:
        root:
            Root pathof file tree to iterate.
        fn_node:
            Will be called on each node it's file path asattribute.

    Returns:
        List of all paths where fn_node returned true.
    """
    node_true = []
    for child in _rp(root).iterdir() :
        if (fn_node(child)) :
            node_tree.append(child)
            pass
        if child.is_dir() :
            iter_tree(child, fn_node)
            pass
        pass
    return node_true

def iter_tree_spec(
    root : PathLike,
    fn_dir : typing.Callable[[pathlib.Path], bool] = None,
    fn_file : typing.Callable[[pathlib.Path], bool] = None
    ) -> list[pathlib.Path] :
    """Iterate file tree specific functions

    Iterates the given file tree with specific function calls based on encuntered node type.

    Parameters:
        root:
            File tree root.
        fn_dir:
            Function to execute when directory was encountered.
            Will be ignored if `None`.
        fn_file:
            Function to execute when file was encountered.
            Will be ignored if `None`.

    Return:
        List of all paths, where functions returned `True`.
    """
    def fn_node(path:pathlib.Path) -> bool :
        if path.is_dir() :
            return fn_dir(path)
        elif path.is_file() :
            return fn_file(path)
        return
    return iter_tree(root, fn_node)

def rm_tree(path) :
    """Deletes a file tree."""
    path = _rp(path)
    if path.is_dir() :
        shutil.rmtree(path)
        return
    os.remove(path)
    return

def rm_tree_contents(path) :
    """Deletes the contents of a given file tree."""
    path = _rp(path)
    for node in path.iterdir() :
        rm_tree(node)
        pass
    return


class Context :
    """Provides a context environment to compose strings, files and file trees."""

    def __init__(self, parent_context:Context|None=None, init_env:dict={}) :
        """Initialize new context.

        Parameters:
            parent_context:
                Instance of parent context.
            init_env:
                Initial environment dictionary.

        Danger:
            Use new_context() factory function from Context or Composer.
        """

        self.parent:Context|None = parent_context
        """Instance of related composer."""

        self.env:dict = init_env
        """Additional format values environment."""

        return

    def new_context(self, init_env:dict={}) :
        """Creates a new coontext instance based on this context.

        Parameters:
            init_env:
                Initial environemnt of new context.

        Returns:
            New initialized context.
        """
        return Context(self, init_env)

    @property
    def project(self) -> conditor.Project :
        """Get related conditor project instance."""
        if self.parent is None :
            return self._project
        return self.parent.project

    @property
    def ctxmap(self) -> dict :
        """Complete map of current context."""
        if self.parent is None :
            return self.env
        return {**self.parent.ctxmap, **self.env}

    def compose_str_str(self, src_str:str) -> str:
        """Compose string.

        Formats a string in this conext.

        Parameters:
            src_str:
                String to compose.

        Returns:
            Composed string of source string.
        """
        return _format_fnc_support(src_str, self.ctxmap)
    
    def compose_file_str(self, src_path:PathLike) -> str :
        """Compose file to string.

        Composes a given file's content to returned string.

        Parameters:
            src_path:
                Path of file containing text which will be composed.

        Returns:
            Composed string of file contents.
        """
        src_str = file_read_str(src_path)
        return self.compose_str_str(src_str)
    
    def compose_str_file(self, src_str:str, dst_path:PathLike) -> None :
        """Compose string to file.

        Composes a given sring to file content.

        Parameters:
            src_str:
                Source string to compose.
            dst_path:
                Path of file to which composed string will be written.
        """
        dst_str = self.compose_str_str(src_str)
        file_write_str(_mkfile(dst_path), dst_str)
        return
    
    def compose_file_file(self, src_path:PathLike, dst_path:PathLike) -> None :
        """Compose file to file.

        Comoses a given file's content to content of another file.

        Parameters:
            src_path:
                Path of file containing text to compose.
            dst_path:
                Path of file to which composed content sould be written.
        """
        src_str = file_read_str(src_path)
        dst_str = self.compose_str_str(src_str)
        file_write_str(dst_path, dst_str)
        return
    
    def compose_files_files(self, files_list:list[tuple[PathLike, PathLike]]) -> None:
        """Compose files to files.

        Composes multiple files.

        Parameters:
            files_list:
                List of tuples containing file paths as `[(src_path, dst_path), ...]`.
        """
        for src_path, dst_path in files_list :
            self.compose_file_file(src_path, dst_path)
            pass
        return

    @property
    def _sfs_dict(self) :
        """Dictionary of special file siffix functions."""
        sfs = {}
        sfs['._copy_tpr_this_']  = self._sfs_copy_tpr_this
        sfs['._comp_this_this_'] = self._sfs_comp_this_this
        return sfs

    def _sfs_paths_from_file(self, path:PathLike) -> list[pathlib.Path] :
        """Get paths listed in a file.

        Parameters:
            path:
                Path of file to read path list from.

        Returns:
            List of paths defined in file of given path.
        """
        paths = []
        paths_str_list = path.read_text().split('\n')
        for path_str in paths_str_list :
            if not path_str :
                continue
            paths.append(pathlib.Path(path_str))
            pass
        return paths

    def _sfs_copy_tpr_this(self, rel_path, src_root, dst_root) :
        """Copy project root to this file.

        Copies a file relative to project root to this destination file.
        """
        src_path = src_root.joinpath(rel_path).resolve()
        dst_path = dst_root.joinpath(rel_path).resolve()
        # Compute sfs cmd paths.
        filepaths = self._sfs_paths_from_file(src_path)
        copy_src_path = self.project.path.joinpath(f'./{filepaths[0]}').resolve()
        copy_dst_path = dst_path.with_suffix('').resolve()
        copy(copy_src_path, copy_dst_path)
        return

    def _sfs_comp_this_this(self, rel_path, src_root, dst_root) :
        """Compose this file content to this file.

        Composes the contents of this source file to contents of this destination file."""
        src_path = src_root.joinpath(rel_path).resolve()
        dst_path = dst_root.joinpath(rel_path).with_suffix('').resolve()
        self.compose_file_file(src_path, dst_path)
        return

    def compose_tree(self,
        src_root:PathLike,
        dst_root:PathLike,
        fn_file_handle = copy
    ) :
        """Compose file tree.

        Composes a file tree from source root path to desitnation root path. SFS (Special file suffix) applies here.

        Parameters:
            src_root:
                Path to root of source file tree.
            dst_root:
                Path of destination file tree.
            fn_file_handle:
                Default function to handle files (e.g. copy or link).
        """

        # Itertree on file.
        def fn_file(src_path) :
            suffix = src_path.suffix
            rel_path = src_path.relative_to(src_root)
            dst_path = dst_root.joinpath(rel_path).resolve()
            # Handle cmd by suffix.
            if suffix in self._sfs_dict :
                self._sfs_dict[suffix](rel_path, src_root, dst_root)
                return
            fn_file_handle(src_path, dst_path)
            return

        # Itertree on directory.
        def fn_dir(src_path) :
            # copy dir only.
            rel_path = src_path.relative_to(src_root)
            dst_path = dst_root.joinpath(rel_path).resolve()
            dst_path.mkdir(parents=True, exist_ok=True)
            return

        # Iterate tree with specialized functions.
        iter_tree_spec(
            root = src_root,
            fn_file = fn_file,
            fn_dir = fn_dir)
        return



    pass


class Composer (Context) :
    """Main context for composing text."""

    def __init__(self, project:conditor.Project) :
        super().__init__()

        self._project:conditor.Project = project
        """Related instance of conditor project."""

        return

    @property
    def ctxmap(self) -> dict :
        """Base context map.."""
        context_map = {}
        context_map['_p']  = self.project
        context_map['_c']  = self.project.config
        context_map['_cs'] = self.project.strcfg
        context_map['_a']  = self.project.action
        context_map['_as'] = self.project.stract
        return context_map

    pass

