"""Console script for leakcleaner."""
import sys
import click

@click.command()
@click.option('-d', '--data', 
              help='Input file or raw data.',
              type=click.File('r'),
              default=sys.stdin)
@click.option('-o', '--out', 
              help='Redirecting output to a file.',
              type=click.File('wb'),
              default='-')
def clean(data, out):
    with data:
        _data = data.read()
    out.write(_data.encode('utf-8'))

if __name__ == "__main__":
    sys.exit(clean())  # pragma: no cover
