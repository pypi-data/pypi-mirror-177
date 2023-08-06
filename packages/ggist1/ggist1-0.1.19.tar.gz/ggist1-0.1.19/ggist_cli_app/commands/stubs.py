import click
from ggist_cli_app.settings import click_pass_settings


@click.command()
@click_pass_settings
def profile_loader(settings):
    # apply it in bashrc with 
    # cd /workspaces/ggist/ && eval "$(python -m ggist_cli_app apply)"

    # apply aliases
    with open(settings.aliases_file, 'r') as fin:
        line = fin.read()
        print(line)

    for name in settings.sources_manager.scripts.keys():
        print(f'alias {name}="ggist run {name}"')


@click.command()
@click_pass_settings
def refresh(settings):
    settings.sources_manager.save()