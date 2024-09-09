import click
import os
import validators

from .input_format import InputFormat
from .md import Md
from .web import Web

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
SUPPORTED_INPUT_FILE_FORMATS=[".json",".md"]
SUPPORTED_OUTPUT_FILE_FORMATS=[".epub"]

def check_input(value: str) -> str:
    if not os.path.isfile(value):
        raise click.BadParameter(f"Could not find file `{value}`.")
    
    extension = os.path.splitext(value)[-1]
    if not extension.lower() in SUPPORTED_INPUT_FILE_FORMATS:
        raise click.BadParameter(f"{extension} is not a supported file format. Supported formats are: "
                                 f"{', '.join(SUPPORTED_INPUT_FILE_FORMATS)}")
    return value

def check_output(value: str) -> str:
    extension = os.path.splitext(value)[-1]
    if not extension.lower() in SUPPORTED_OUTPUT_FILE_FORMATS:
        raise click.BadParameter(f"{extension} is not a supported file format for output. Supported formats are: "
                                 f"{', '.join(SUPPORTED_OUTPUT_FILE_FORMATS)}")
    return value

def make_input_converter(input_path: str) -> InputFormat:
    extension = os.path.splitext(input_path)[-1].lower()
    if extension == ".json":
        # Assume the json document is a list of urls
        return Web(input_path)
    elif extension == ".md":
        return Md(input_path)
    else:
        raise click.BadParameter(f"Couldn't find an input converter for `{input_path}`.")

@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.argument("input", type=check_input)
@click.argument("output", type=check_output)
def cli(input: str, output: str):
    """Convert various kinds of document into an ebook.

INPUT is a file path to a supported document type.

OUTPUT is a file path whose extension determines the output format."""
    output_extension = os.path.splitext(output)[-1].lower()

    converter = make_input_converter(input)
    if output_extension == ".epub":
        identifier = converter.to_epub(output)
        click.echo(f"Created {output} with identifier {identifier}")
    else:
        click.echo(f"Couldn't find an output converter for `{output_extension}`.")
