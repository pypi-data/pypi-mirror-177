import sys
import os
import time

import click
import jinja2
import requests
from .draw_formattor import FormatToPdf

from .filters import db_type
from .transform import ModelFile


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    pass


@cli.command()
@click.argument('model_filepath')
@click.argument('output')
def trans(model_filepath, output):
    model_fp = os.path.abspath(model_filepath)
    if not os.path.exists(model_fp):
        click.echo('Model File:%s not exists' % model_filepath)
        sys.exit(1)

    target_fp = os.path.abspath(output)
    if output.endswith('.pdf'):
        modelfile = ModelFile(model_fp)
        modelfile.process()
        modelfile.analyze()
        fmt = FormatToPdf(modelfile)
        fmt.format()
        return

    if output.startswith('/') or output.startswith("./") or output.startswith('~/') or output.startswith('../'):
        if not os.path.exists(target_fp):
            click.echo('Format File:%s not exists' % target_fp)
            sys.exit(1)
    else:
        uri = 'https://raw.githubusercontent.com/ipconfiger/ModelTransfer/main/templates/%s.tmp?v=%s' % (output, time.time())
        r = requests.get(uri)
        try:
            r.raise_for_status()
        except:
            click.echo('No such template:%s' % uri)
            sys.exit(1)
        target_dir_path = os.path.expanduser('~/.model_templates')
        if not os.path.exists(target_dir_path):
            os.mkdir(target_dir_path)
        target_file_path = os.path.join(target_dir_path, "%s.tmp" % output)
        # print('local path:%s' % target_file_path)
        with open(target_file_path, 'w') as f:
            f.write(r.text)
        target_fp = target_file_path
    modelfile = ModelFile(model_fp)
    modelfile.process()
    modelfile.analyze()

    loader = jinja2.FileSystemLoader(os.path.dirname(target_fp))
    env = jinja2.Environment(autoescape=True, loader=loader)
    env.filters['db_type'] = db_type
    template = env.get_template(target_fp.split(os.sep)[-1])
    print(template.render(mod=modelfile))


def main():
    cli()


if __name__ == '__main__':
    main()


