import os
import click
from ggist_cli_app.consts import Consts
from ggist_cli_app.utils.io import mkdir, touch
from ggist_cli_app.utils.sys import get_os
from ggist_cli_app.core.sources_manager import SourcesManager

class Settings:
    def __init__(self, home=None, terminal=None):
        self.home = os.path.abspath(home or Consts.HOME)
        self.terminal = terminal or Consts.DEFAULT_TERMINAL
        self.aliases_file = os.path.join(self.home, Consts.ALIASES_FILE)
        self.scripts_dir = os.path.join(self.home, Consts.SCRIPTS_DIR)
        self.config_file = os.path.join(self.home, Consts.CONFIG_FILE)
        self.sources_file = os.path.join(self.home, Consts.SOURCES_FILE)
        mkdir(self.home)
        touch(self.aliases_file)
        mkdir(self.scripts_dir)
        touch(self.sources_file)

        self.os = get_os()

        self.sources_manager = SourcesManager(self)

# from https://click.palletsprojects.com/en/8.1.x/complex/
click_pass_settings = click.make_pass_decorator(Settings, ensure=True)
