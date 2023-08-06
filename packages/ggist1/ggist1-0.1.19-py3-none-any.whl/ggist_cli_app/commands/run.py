import click
from ggist_cli_app.settings import click_pass_settings
from ggist_cli_app.core.script_runner import ScriptRunner
import inquirer
from ggist_cli_app.utils.console import console, error_console

@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('name',  required=False)
@click_pass_settings
@click.pass_context
def run(ctx, settings, name: str):
    """
    Run something
    """

    available_scripts = settings.sources_manager.scripts

    if not name:
        questions = [
            inquirer.List(
                "script",
                message="What script to run?",
                choices=tuple(available_scripts.keys()),
            ),
        ]

        answers = inquirer.prompt(questions)
        name = answers['script']


    if name in available_scripts:
        script = available_scripts[name]    

        if not script.supports_os(settings.os):
            error_console.print('This script not supporting your os') 
            return

        script_args = ctx.args
        # print('args=', script_args)
        output = ScriptRunner.run(script, settings.os, script_args, settings)

        console.print("[blue] Script executed:")
        for line in output:
            console.print(f' - {line}')

        console.print(f"[bold green]Script {script.name} completed")
    else:
        error_console.print('I don\'t know this script')        
