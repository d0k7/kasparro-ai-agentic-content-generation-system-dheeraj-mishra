from jinja2 import Template


def render_template(template_name: str, context: dict) -> str:
    # Load the HTML template
    with open(f"templates/{template_name}.html") as file:
        template = Template(file.read())
    # Render the template with the provided context
    return template.render(context)
