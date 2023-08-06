import os
from .consts import *


class FormatToDatabase(object):
    name = 'dm'

    def __init__(self, modelfile: "ModelFile"):
        self.modelfile = modelfile
        self.store_dir = ''
        self.py_path = ''

    def clear_old(self):
        dir_path = os.path.dirname(self.modelfile.model_filepath)
        target_dir = os.path.join(dir_path, f'target_{FormatToDatabase.name}')
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        self.store_dir = target_dir
        self.py_path = os.path.join(self.store_dir, "models.dart")
        if os.path.exists(self.py_path):
            os.remove(self.py_path)

    def db_type(self, fieldwrapper):
        mapper = {
            BUILIN_TYPE_STR: f'String({fieldwrapper.field_length})' if fieldwrapper.field_length else "Text",
            BUILIN_TYPE_INT: 'Integer',
            BUILIN_TYPE_FLOAT: 'Numeric(10, 2)',
            BUILIN_TYPE_DOUBLE: 'Numeric(10, 2)',
            BUILIN_TYPE_BOOL: 'Boolean'
        }
        return mapper[fieldwrapper.field_type]

    def format(self):
        self.clear_old()
        py_lines = []
        py_lines.append("# coding=utf8")
        py_lines.append('__author__ = ""')
        py_lines.append('')
        py_lines.append('from sqlalchemy import Column, String, Integer, Index, Text, Boolean, BigInteger')
        py_lines.append('from sqlalchemy.ext.declarative import declarative_base, declared_attr')
        py_lines.append('from sqlalchemy.dialects.postgresql import UUID')
        py_lines.append('import uuid')
        py_lines.append('import time')
        py_lines.append('import re')
        py_lines.append('')
        py_lines.append('')
        py_lines.append('class ModelBase:')
        py_lines.append('    @declared_attr')
        py_lines.append('    def __tablename__(self):')
        py_lines.append('        return "_".join(re.findall("[A-Z][^A-Z]*", self.__name__)).lower()')
        py_lines.append('')
        py_lines.append('    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1, unique=True, nullable=False)')
        py_lines.append('    create_ts = Column(BigInteger, index=True, default=time.time_ns, nullable=False)')
        py_lines.append('    update_ts = Column(BigInteger, index=True, default=time.time_ns(), nullable=False)')
        py_lines.append('')
        py_lines.append('')
        py_lines.append('Base = declarative_base(cls=ModelBase)')
        py_lines.append('')
        py_lines.append('')
        for classwrapper in self.modelfile.classes:
            py_lines.append(f'class {classwrapper.class_name}(Base):')
            py_lines.append(f'    """{classwrapper.comment.strip()}"""')
            for fieldwrapper in classwrapper.fields:
                if fieldwrapper.is_list:
                    continue
                if fieldwrapper.is_complex:
                    py_lines.append(f'    {fieldwrapper.name}_id = Column(UUID(as_uuid=True), index=True, nullable=False), doc="{fieldwrapper.comment}"')
                else:
                    py_lines.append(f'    {fieldwrapper.name} = Column({self.db_type(fieldwrapper)}, doc="{fieldwrapper.comment}")')
            py_lines.append('')
            py_lines.append('')

        for className, field1, field2 in self.modelfile.relations.findN2NRelation():
            py_lines.append(f'class {className}(Base):')
            py_lines.append(f'    """{field1.comment.strip()}->{field2.comment.strip()}"""')
            py_lines.append(f'    {field1.name}_id = Column(UUID(as_uuid=True), index=True, nullable=False, doc="{field1.comment}")')
            py_lines.append(f'    {field2.name}_id = Column(UUID(as_uuid=True), index=True, nullable=False, doc="{field2.comment}")')
            py_lines.append('')
            py_lines.append('')

        with open(self.py_path, 'w') as f:
            f.write("\n".join(py_lines))
