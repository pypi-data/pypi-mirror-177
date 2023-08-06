import click
from ggist_cli_app.settings import click_pass_settings
from ggist_cli_app.commands.groups import remove
from ggist_cli_app.core.source import Source



@remove.command(name="source")
@click.argument('source')
@click_pass_settings
def remove_source(settings, source: str):
    """
    remove a source
    """
    source = Source(source, settings)
    settings.sources_manager.remove_source(source)
