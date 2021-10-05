from urllib.parse import urlparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("schemadocs/templates"),
    autoescape=select_autoescape()
)

REQUIRED_ATTRIBUTES = ["$id", "title"]

class SchemaValueError(Exception):
    pass


def validate_schema(schema):
    """
    Validates schema based on schemadocs-specific requirements:
    
    - Each schema must have the following attributes: $id, title
    """
    for attribute in REQUIRED_ATTRIBUTES:
        if not schema.get(attribute):
            raise SchemaValueError(f"Missing required attribute: {attribute}")


def build_index(schemas):
    index = {}
    for schema in schemas:
        schema_id = urlparse(schema["$id"]).path
        index[schema_id] = schema
    return index


def render_index(index):
    template = env.get_template("index.html")
    return template.render(index=index)


def render_object(object_schema, index=None):
    template = env.get_template("object.html")

    context = {
        "schema": object_schema,
        "index": index
    }

    return template.render(**context)