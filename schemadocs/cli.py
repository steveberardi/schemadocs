import json
import shutil

from pathlib import Path

import click

from schemadocs.build import render_doc, render_index


BASE_DIR = Path(__file__).parent.resolve()

@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', default=".")
@click.argument('destination', default=".")
def build(source, destination):
    click.secho("\N{hammer and wrench}  Building the docs...", bold=True)
    
    source_path = Path(source).resolve().glob("**/*.json")
    destination_path = Path(destination).resolve()
    
    for json_filename in source_path:
        with open(json_filename) as json_file:
            object_schema = json.loads(json_file.read())

            click.secho(f"Creating docs for: {object_schema['title']}", fg="blue")

            rendered_doc = render_doc(object_schema)
            output_filename = destination_path / f"{object_schema['title'].lower()}.html"
            
            with open(output_filename, "w") as outfile:
                outfile.write(rendered_doc)

    # create index page
    with open(destination_path / "index.html", "w") as index_file:
        index_file.write(render_index())

    # copy css style
    shutil.copytree(
        BASE_DIR / "templates" / "css", 
        destination_path / "css",
        dirs_exist_ok=True
    )

    click.secho('\N{rocket} Done!', fg='green')


if __name__ == '__main__':
    cli()