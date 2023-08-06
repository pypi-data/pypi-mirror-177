from .consts import BUILIN_TYPE_INT, BUILIN_TYPE_STR, BUILIN_TYPE_FLOAT, BUILIN_TYPE_DOUBLE, BUILIN_TYPE_BOOL


def db_type(fieldwrapper):
    mapper = {
        BUILIN_TYPE_STR: f'String({fieldwrapper.field_length})' if fieldwrapper.field_length else "Text",
        BUILIN_TYPE_INT: 'Integer',
        BUILIN_TYPE_FLOAT: 'Numeric(10, 2)',
        BUILIN_TYPE_DOUBLE: 'Numeric(10, 2)',
        BUILIN_TYPE_BOOL: 'Boolean'
    }
    return mapper[fieldwrapper.field_type]