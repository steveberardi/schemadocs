import json
import shutil

from pathlib import Path

import click
import jsonschema

from schemadocs.build import build_index, render_object, render_index


BASE_DIR = Path(__file__).parent.resolve()

def walk_schema_files(source):
    source_path = Path(source).resolve().glob("**/*.json")
    for json_filename in source_path:
        with open(json_filename) as json_file:
            yield json.loads(json_file.read())

@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', default=".")
def validate(source):
    click.secho("\U0001F50D  Validating schema...", bold=True)
    errors = False

    for schema in walk_schema_files(source):
        click.secho(f"Checking schema: {schema['title']}", fg="blue")
        try:
            jsonschema.Draft7Validator.check_schema(schema)
        except jsonschema.exceptions.SchemaError as e:
            errors = True
            click.secho(f'- {str(e)}', fg='red')

    if errors:
        raise click.ClickException("Schema validation failed")

    click.secho('\N{check mark} Schema looks good!', fg='green')


@cli.command()
@click.argument('source', default=".")
@click.argument('destination', default=".")
def build(source, destination):
    click.secho("\N{hammer and wrench}  Building the docs...", bold=True)
    
    destination_path = Path(destination).resolve()

    # read all schemas and build index
    schemas = [schema for schema in walk_schema_files(source)]
    index = build_index(schemas)

    # create doc page for each schema
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