"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Model Json."""


if __name__ == "__main__":
    main(prog_name="model-json")  # pragma: no cover
