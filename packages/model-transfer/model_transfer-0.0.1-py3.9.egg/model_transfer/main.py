import sys
import os

from .draw_formattor import FormatToPdf
from .transform import ModelFile
from .jorm_formmator import FormatToJORM
from .trans_formattor import FormatToTrans
from .db_formmator import FormatToDatabase

OUTPUT_TYPES = ['jm', 'tm', 'dm', 'pdf']

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


if __name__ == '__main__':
    main()


