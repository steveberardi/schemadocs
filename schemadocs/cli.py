import json
import shutil

from pathlib import Path

import click

from schemadocs.build import build_index, render_object, render_index


BASE_DIR = Path(__file__).parent.resolve()

@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', default=".")
@click.argument('destination', default=".")
def build(source, destination):
    click.secho("\N{hammer and wrench}  Building the docs...", bold=True)
    
    schemas = []
    source_path = Path(source).resolve().glob("**/*.json")
    destination_path = Path(destination).resolve()
    
    for json_filename in source_path:
        with open(json_filename) as json_file:
            schema = json.loads(json_file.read())

            schemas.append(schema)

    index = build_index(schemas)

    for schema in schemas:
        click.secho(f"Creating docs for: {schema['title']}", fg="blue")

        rendered_doc = render_object(schema, index)
        output_filename = destination_path / f"{schema['title'].lower()}.html"
        
        with open(output_filename, "w") as outfile:
            outfile.write(rendered_doc)

    # create index page
    with open(destination_path / "index.html", "w") as index_file:
        index_file.write(render_index(index))

    # copy css style
    shutil.copytree(
        BASE_DIR / "templates" / "css", 
        destination_path / "css",
        dirs_exist_ok=True
    )

    click.secho('\N{rocket} Done!', fg='green')


if __name__ == '__main__':
    cli()