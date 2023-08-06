import os
import glob
from typing import Sequence
from ggist_cli_app.consts import Consts
from ggist_cli_app.core.models.script_model import ScriptModel
from ggist_cli_app.core.models.source_config_model import SourceConfigModel
from ggist_cli_app.utils.io import YamlIO, exists, file_read_lines
from ggist_cli_app.utils import git
from functools import partial

class Source:

    def __init__(self, _location: str, settings: 'Settings'):
        self.settings = settings
        self._location = _location.lower()

        if _location.startswith('demo/'):
            from ggist_cli_app import resources
            self._location = os.path.join(os.path.dirname(resources.__file__), self._location)

        if exists(self._location):
            self._location = os.path.abspath(self._location)  # convert to abs path
            self._aliases = self.read_aliases(os.path.join(self._location, Consts.ALIASES_FILE))
            self._scripts = self.read_scripts(os.path.join(self._location, Consts.SCRIPTS_DIR))
            self._ggist_config = YamlIO.from_file(os.path.join(self._location, Consts.SOURCE_CONFIG_FILE), cls=SourceConfigModel)
        elif self._location.endswith('.git'):
            local_repo = os.path.join(settings.home, git.get_repo_name(self._location))
            if not exists(local_repo):
                git.clone(
                    self._location, 
                    local_repo
                )
            self._aliases = self.read_aliases(os.path.join(local_repo, Consts.ALIASES_FILE))
            self._scripts = self.read_scripts(os.path.join(local_repo, Consts.SCRIPTS_DIR))
            self._ggist_config = YamlIO.from_file(os.path.join(local_repo, Consts.SOURCE_CONFIG_FILE), cls=SourceConfigModel)
        else:

            raise RuntimeError(f'path {self._location} not exists. edit `~/.ggist/sources.txt` and remove it manually')
        
        

    @property
    def is_exists_locally(self):
        return False
    
    @property
    def aliases(self):
        return self._aliases

    @property
    def name(self):
        return self._ggist_config.name

    @property
    def scripts(self):
        return self._scripts

    @property
    def location(self):
        return self._location

            
    
    def __repr__(self):
        return str(self._location)

    def __str__(self):
        return str(self._location)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash((type(self), self._location))

    @staticmethod
    def read_aliases(file)->Sequence[str]:
        def _clean(s):
            s = s.strip()
            return s

        return tuple(filter(bool, map(_clean, file_read_lines(file))))

    
    @staticmethod
    def read_scripts(scripts_path)->Sequence[str]:
        
        files_it = glob.glob(os.path.join(scripts_path, "*.yaml"))
        return tuple(map(partial(YamlIO.from_file, cls=ScriptModel), files_it))