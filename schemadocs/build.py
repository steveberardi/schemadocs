import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("schemadocs/templates"),
    autoescape=select_autoescape()
)

def render_doc(object_schema):
    template = env.get_template("object.html")

    context = {
        "data_object": object_schema,
        "data_objects": []
    }

    return template.render(**context)