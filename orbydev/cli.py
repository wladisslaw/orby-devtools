import click
from .project import create_project
from .compiler import build_project

@click.group()
def main():
    """Orby DevTools CLI."""
    pass

@main.command()
@click.argument("name")
@click.option("--template", default="default", help="Project template.")
def new(name, template):
    """Create a new Orby project."""
    create_project(name, template)
    click.echo(f"Project '{name}' created!")

@main.command()
@click.argument("path")
def build(path):
    """Build .orby from a project."""
    build_project(path)
    click.echo(f"Project at '{path}' compiled!")

if __name__ == "__main__":
    main()