
from __future__ import annotations


INIT_CONFIG = {}
"""Initial project configuration.

Used to define fallback configuration and default properties for the project.
"""

# Conditor project module (CPM) file name
INIT_CONFIG['conditor.cpm.filename'] = '.project.py'

# CPM import name.
INIT_CONFIG['conditor.cpm.module_name'] = '_CPM'

# CPM project instance variable.
INIT_CONFIG['conditor.cpm.project_var_name'] = 'PROJECT'

# Module name initials for new action from import module file.
INIT_CONFIG['conditor.action.file_module_initials'] = 'conditor._loaded_action_module_file'

# Module name initials for new build recipe from import module file.
INIT_CONFIG['conditor.recipe.file_module_initials'] = 'conditor._loaded_recipe_module_file'

# File name for build data.
INIT_CONFIG['conditor.build.data_file_name'] = '.build.json'

# Fallback build id name.
INIT_CONFIG['conditor.build.fallback_id'] = 'FALLBACKID'

