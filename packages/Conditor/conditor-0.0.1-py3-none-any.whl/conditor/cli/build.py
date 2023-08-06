
from .__init__ import *


class CMD_Build (Command) :
    CMD_NAME = 'build'
    CMD_SHORTDESC = 'Build action group.'
    CMD_DESCRIPTION = 'Build actions.'
    def load(self, parser) :
        self['list-recipes'] = CMD_ListRecipes
        self['stage-all'] = CMD_StageAll
        return
    def run(self, args, final) :
        return
    pass


class CMD_ListRecipes (Command) :
    CMD_NAME = 'list-recipes'
    CMD_SHORTDESC = 'List all available build recipes.'
    CMD_DESCRIPTION = 'Print a list of all available recipes loaded in this project.'
    def load(self, parser) :
        parser.add_argument('--delimiter',
            action = 'store',
            const = None,
            default = '\n',
            type = str,
            choices = None,
            required = False,
            help = 'Delimiter used to separate recipe names.',
            metavar = '<delimiter>',
            dest = self.argname('delimiter')
        )

        return
    def run(self, args, final) :
        if not final :
            return
        delimiter = self.get_arg(args, 'delimiter', '\n')
        names_str = delimiter.join(self.project.recipe_manager.names)
        self.output(names_str, '\n')
        return
    pass


class CMD_StageAll (Command) :
    CMD_NAME = 'stage-all'
    CMD_SHORTDESC = 'Stage all in recipe.'
    CMD_DESCRIPTION = 'Create new build and stage all stages in given recipe.'
    def load(self, parser) :
        parser.add_argument(
            action = 'store',
            const = None,
            type = str,
            choices = None,
            help = 'Name of build recipe.',
            metavar = '<recipe_name>',
            dest = self.argname('recipe')
        )
        parser.add_argument('--identity',
            action = 'store',
            const = None,
            default = None,
            type = str,
            choices = None,
            required = False,
            help = 'Custom identity for build.',
            metavar = '<build_identity>',
            dest = self.argname('identity')
        )
        return
    def run(self, args, final) :
        if not final :
            return
        build_identity = self.get_arg(args, 'identity')
        if build_identity is None :
            build_identity = self.project.strcfg['conditor.build.fallback_id']
            pass
        recipe_name = self.get_arg(args, 'recipe')
        recipe = self.project.recipe[recipe_name]
        build = recipe.new_build_process(
            identifier = build_identity)
        build.stage_all()
        return
    pass

