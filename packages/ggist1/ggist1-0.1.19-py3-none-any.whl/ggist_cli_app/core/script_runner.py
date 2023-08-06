
from os import path
from typing import Sequence, Optional, List
import webbrowser
import inquirer
from ggist_cli_app.consts import Consts
from ggist_cli_app.core.models.script_model import ScriptModel, StepModel, StepRunnerType, StepRefModel, StepsModel
from rich.markdown import Markdown

from ggist_cli_app.core.os import OS
from ggist_cli_app.utils import io
import subprocess
from ggist_cli_app.utils.console import console, error_console
from collections import OrderedDict

class ScriptRunner:
    
    @staticmethod
    def run(script: ScriptModel, os: OS, script_args: Sequence[str], settings: 'Settings')->List[str]:

        def out(command, *script_args, runner: StepRunnerType):
            exec_file = path.join(io.get_tmp(), Consts.TMP_EXEC_FILE_NAME)
            io.file_write(exec_file, command)
            
            if runner==StepRunnerType.PYTHON:
                p = subprocess.run('python ' + exec_file + ' ' + ' '.join(script_args), shell=True)           
            else:
                io.chmod_x(exec_file)
                p = subprocess.run(exec_file + ' ' + ' '.join(script_args), shell=True)           
            return p

                
        console.print(script.title, style="frame white on blue")

        variations_for_os = script.get_variations_for_os(os)

        if len(variations_for_os) > 1:
            questions = [
                inquirer.List(
                    "variation",
                    message="What variations to run?",
                    choices=tuple(
                        variation.label
                        for variation in variations_for_os
                    ),
                ),
            ]

            answers = inquirer.prompt(questions)
            variation = answers['variation']
        else:
            variation = variations_for_os[0]

        

        steps_choices = OrderedDict()
        for ii, step in enumerate(ScriptRunner.iterate_steps(script, variation, settings)):
            steps_choices[f'{ii} - {step.title}'] = step

        # questions = [
        #     inquirer.Checkbox(
        #         "steps",
        #         message="Select what to execute: (all by default)",
        #         choices=steps_choices.keys(),
        #         default=steps_choices.keys(),
        #     ),
        # ]

        # answers = inquirer.prompt(questions)

        # chosen_steps = tuple(
        #     step
        #     for label, step in steps_choices.items()
        #     if label in answers['steps']
        # )
        chosen_steps = tuple(steps_choices.values())
        
        # console.print(f'Executing {len(chosen_steps)} steps:')

        output = []
        for ii, step in enumerate(chosen_steps):


            res = 'ok'
            if step.runner == StepRunnerType.SHELL:
                
                console.print(f'step {ii} - {step.title}', style="blue")
            
                questions = [
                    inquirer.Confirm("sure", message="Execute step?", default=True)]

                answers = inquirer.prompt(questions)
                
                
                if answers['sure']:
                    r = out('set -x\n' + step.content, *script_args, runner=step.runner)

                    if r.returncode:
                        error_console.print("failed to run step")
                        res = 'failed'
                else:
                    res = 'skipped'
            elif step.runner == StepRunnerType.PYTHON:
                console.print(f'step {ii} - {step.title}', style="blue")
            
                questions = [
                    inquirer.Confirm("sure", message="Execute step?", default=True)]

                answers = inquirer.prompt(questions)
                
                
                if answers['sure']:
                    r = out(step.content, *script_args, runner=step.runner)

                    if r.returncode:
                        error_console.print("failed to run step")
                        res = 'failed'
                else:
                    res = 'skipped'
            elif step.runner == StepRunnerType.MARKDOWN:
                markdown = Markdown(step.content)
                console.print(markdown)
            elif step.runner == StepRunnerType.LINK:
                console.print(f'step {ii} - {step.title} -> link to {step.content}', style="blue")
                questions = [
                    inquirer.Confirm("sure", message="Open Link?", default=True)]

                answers = inquirer.prompt(questions)
                
                
                if answers['sure']:
                    webbrowser.open(step.content, new=2)
                    console.print()
                else:
                    res = 'skipped'
                
            elif step.runner == StepRunnerType.GGIST_SCRIPT:
                nested_script = settings.sources_manager.scripts[step.content]
                output.extend(ScriptRunner.run(nested_script, os, [], settings))
            else:
                raise NotImplementedError()

            if step.runner != StepRunnerType.GGIST_SCRIPT:
                if res == 'skipped':
                    output.append(f'skipped [strike]"{step.title}"')
                elif res == 'failed':
                    output.append(f'[red] x "{step.title}"')
                else:
                    output.append(f'[green] ✓ "{step.title}"')
                
                
        
        return output

    @staticmethod
    def iterate_steps(script: ScriptModel, variation: StepsModel, settings: 'Settings'):
        for step in variation.steps:
            if isinstance(step, StepRefModel):
                
                try:
                    step = next(
                        global_step
                        for global_step in script.spec.globals
                        if global_step.id == step.ref
                    )
                except StopIteration:
                    # no results from globals                
                    try:
                        ref_script = settings.sources_manager.scripts[step.ref]
                        step = StepModel(
                            title=ref_script.title,
                            description=ref_script.description,
                            runner=StepRunnerType.GGIST_SCRIPT,
                            content=step.ref
                        )
                    except KeyError:
                        # can't find the script in ggist or script globals
                        raise ValueError(f"unable to find reference {step.ref}")

                
                
            yield step