import click
import json
import requests
from pathlib import Path
from .helpers import write_to_file, append_to_file

@click.command()
@click.option('--template', '-t', type=str, help='name of the gitignore template to use')
@click.option('--force', '-f', is_flag=True, help='replace existing gitignore file if one exists')
@click.option('--append', '-a', is_flag=True, help='replace existing gitignore file if one exists')
def run(template, force, append):
    """Generates a .gitignore template from githubs repo"""
    url_template = f'https://raw.githubusercontent.com/github/gitignore/main/{template}.gitignore'
    req = requests.get(url_template)
    if req.status_code == 200:
        data = req.text
        fileexists = False
        
        if Path('./.gitignore').is_file():
            fileexists = True
        
        # If there is no .gitignore file just write the data
        # and be done
        if fileexists is False:
            write_to_file('./.gitignore', data)
        elif fileexists is True:

            # Append data to the file based on --append
            if append is True:
                print(f'Appending {template}.gitignore to .gitignore')
                append_to_file('./.gitignore', data)
                return

            # Write to the file based on --force
            if force is False:
                print(".gitignore already exists, goodbye!")
            elif force is True:
                print(f'Replacing .gitignore {template}.gitignore')
                write_to_file('./.gitignore', data)
                return
