import click
from .project import Projects

@click.group()
def main():
    """Orby DevTools CLI."""
    pass

@main.command()
@click.argument("name", default="Orby app")
@click.argument("path", default="")
@click.option("--template", default="default", help="Project template.")
def new(name, path, template):
    """Create a new Orby project."""
    status, exception = Projects.new(name, path, template)
    if status:
        click.echo(f"Project '{name}' created!")
    else:
        raise Exception(f"Error when creating project: {exception}") from exception


@main.command()
@click.argument("path")
@click.argument("save_at", default="")
def build(path, save_at):
    """Create a new Orby project."""
    status, exception = Projects.build(path, save_at)
    if status:
        click.echo("Project builded!")
    else:
        raise Exception(f"Error when building project: {exception}") from exception


if __name__ == "__main__":
    main()