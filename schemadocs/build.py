import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("schemadocs/templates"),
    autoescape=select_autoescape()
)

def build_index(schemas):
    index = {}
    for schema in schemas:
        index[schema["title"]] = schema
    return index

def render_index(index):
    template = env.get_template("index.html")

    context = {
        "index": index
    }

    return template.render(**context)

def render_object(object_schema, index=None):
    template = env.get_template("object.html")

    context = {
        "data_object": object_schema,
        "index": index
    }

    return template.render(**context)