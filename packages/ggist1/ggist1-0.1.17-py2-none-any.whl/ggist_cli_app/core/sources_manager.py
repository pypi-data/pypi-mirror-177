from typing import Sequence
from ggist_cli_app.utils.io import exists, file_read_lines, file_write_lines
from ggist_cli_app.utils import git
from ggist_cli_app.core.source import Source
from ggist_cli_app.core.aliases import Aliases

class SourcesManager:

    def __init__(self, settings: 'Settings'):
        self.settings = settings
        self.sources_file = settings.sources_file
        self.sources = self.load_sources(self.sources_file, settings)

    def remove_source(self, source: Source):
        self.sources.remove(source)
        self.save()

    def add_source(self, source: Source):
        self.sources.add(source)
        self.save()


    def save(self):
        self.save_sources(self.sources_file, self.sources)
        # update aliases file
        Aliases.recreate_aliases(self.settings.aliases_file, self.sources)

    @staticmethod
    def load_sources(sources_file, settings):
        return set(map(lambda s: Source(s, settings), file_read_lines(sources_file)))

    @staticmethod
    def save_sources(sources_file, sources: Sequence[Source]):
        file_write_lines(sources_file, tuple(map(str, sources)))

    @property
    def scripts(self):
        scripts = {}
        for source in self.sources:
            for script in source.scripts:
                scripts[f'{source.name}.{script.name}'] = script
        return scripts