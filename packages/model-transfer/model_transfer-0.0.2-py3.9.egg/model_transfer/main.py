import sys
import os

import click
import jinja2
import requests

from .filters import db_type
from .draw_formattor import FormatToPdf
from .transform import ModelFile
from .jorm_formmator import FormatToJORM
from .trans_formattor import FormatToTrans
from .db_formmator import FormatToDatabase

OUTPUT_TYPES = ['jm', 'tm', 'dm', 'pdf']

"""
def main():
    if len(sys.argv) < 2:
        print('Miss parameter model filepath')
        sys.exit(1)
    if len(sys.argv) < 3:
        print('Miss parameter output type (%s)' % ",".join(OUTPUT_TYPES))
        sys.exit(1)
    filepath = sys.argv[1]
    out_format = sys.argv[2]
    if out_format not in OUTPUT_TYPES:
        print('Parameter output type must in %s' % ",".join(OUTPUT_TYPES))
        sys.exit(1)
    modelfile = ModelFile(os.path.abspath(filepath))
    modelfile.process()
    modelfile.analyze()
    formatters = [FormatToJORM, FormatToTrans, FormatToDatabase, FormatToPdf]
    for formatter in formatters:
        if formatter.name == out_format:
            formatter(modelfile).format()
    print('format done!')
"""


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.argument('model_filepath')
@click.argument('output')
def trans(model_filepath, output):
    model_fp = os.path.abspath(model_filepath)
    if not os.path.exists(model_fp):
        click.echo('Model File:%s not exists' % model_filepath)
        sys.exit(1)
    target_fp = os.path.abspath(output)
    if output.startswith('/') or target_fp.startswith("./") or target_fp.startswith('~/') or target_fp.startswith('../'):
        if not os.path.exists(target_fp):
            click.echo('Format File:%s not exists' % target_fp)
            sys.exit(1)
    else:
        uri = 'https://raw.githubusercontent.com/ipconfiger/ModelTransfer/main/templates/%s.tmp' % output
        r = requests.get(uri)
        try:
            r.raise_for_status()
        except:
            click.echo('No such template:%s' % uri)
            sys.exit(1)
        target_dir_path = os.path.expanduser('~/.model_templates')
        if not os.path.exists(target_dir_path):
            os.mkdir(target_dir_path)
        target_file_path = os.path.join(target_dir_path, "%s.tmp" % target_fp)
        with open(target_file_path, 'w') as f:
            f.write(r.text)
        target_fp = target_file_path
    modelfile = ModelFile(model_fp)
    modelfile.process()
    modelfile.analyze()

    loader = jinja2.FileSystemLoader(os.path.dirname(model_fp))
    env = jinja2.Environment(autoescape=True, loader=loader)
    env.filters['db_type'] = db_type
    template = env.get_template(target_fp.split(os.sep)[-1])
    print(template.render(mod=modelfile))


def main():
    cli()


if __name__ == '__main__':
    main()


