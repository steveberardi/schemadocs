import json
from pathlib import Path

import click

from build import render_doc

@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', default=".")
@click.argument('destination', default=".")
def build(source, destination):
    click.echo(click.style("\N{hammer and wrench}  Building the docs...", bold=True))
    
    source_path = Path(source).resolve().glob("**/*.json")
    
    for json_filename in source_path:
        
        with open(json_filename) as json_file:
            object_schema = json.loads(json_file.read())

            click.echo(click.style(f"Creating docs for: {object_schema['title']}", fg="blue"))

            rendered_doc = render_doc(object_schema)
            output_filename = Path(destination).resolve() / f"{object_schema['title'].lower()}.html"
            
            with open(output_filename, "w") as outfile:
                outfile.write(rendered_doc)

    click.echo(click.style('\N{rocket} Done!', fg='green'))


if __name__ == '__main__':
    cli()