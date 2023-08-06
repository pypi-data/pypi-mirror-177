from .consts import *
import os


class SyntaxException(Exception):
    def __init__(self, message):
        super(SyntaxException, self).__init__(message)


def between(line: str, s: str, e: str, explicit=False):
    start_idx = line.index(s)
    try:
        end_idx = line.rindex(e)
    except ValueError as ex:
        if explicit:
            raise ex
        end_idx = len(line)
    return line[start_idx+1: end_idx].strip()


def before(line: str, e: str):
    end_idx = line.rindex(e)
    return line[0: end_idx]


class ReferenceItem(object):
    def __init__(self, container_type, item_type, field, relation_type):
        self.container_type = container_type
        self.item_type = item_type
        self.field = field
        self.relation_type = relation_type

    def __repr__(self):
        return f"{self.container_type} -> {self.item_type} in {self.field} type:{self.relation_type}"


class ReferenceHolder(object):
    def __init__(self):
        self.targets = {}

    def add_relation(self, a, b, f, ft):
        if a in self.targets:
            self.targets[a].append(ReferenceItem(a, b, f, ft))
        else:
            self.targets[a] = [ReferenceItem(a, b, f, ft), ]

    def findN2NRelation(self):
        mapper = []
        for cn, r_ls in self.targets.items():
            for referenceItem in r_ls:
                if referenceItem.relation_type == RelationType.CONTAINS:
                    mapper.append((referenceItem.container_type, referenceItem.item_type, referenceItem.field))

        keys = {}

        for a, b, fn1 in mapper:
            for f, t, fn2 in mapper:
                if a == t and f == b:
                    if a + b not in keys and b + a not in keys:
                        keys[a + b] = True
                        yield f"{a}Of{b}", fn1, fn2
                    else:
                        continue

    def __repr__(self):
        return str(self.targets)


class FieldWrapper(object):
    def __init__(self, name, field_type, comment, c: "ClassWrapper", g: "ModelFile"):
        self.name = name
        self.field_type = field_type
        self.comment = comment
        self.is_complex = False
        self.is_list = False
        self.field_length = 0
        self.required = False
        self.global_env = g
        self.classwrapper = c
        self.process()

    def process(self):
        if self.field_type.endswith("*"):
            self.required = True
            self.field_type = self.field_type.replace("*", '')
        try:
            type_length = between(self.field_type, '(', ')')
            self.field_length = int(type_length)
            self.field_type = before(self.field_type, '(')
        except ValueError:
            pass
        self.is_complex = self.field_type.lower() not in BUILIN_TYPES
        self.is_list = self.field_type.startswith("List[")
        if self.is_list:
            try:
                self.field_type = between(self.field_type, "[", "]", explicit=True)
            except ValueError:
                raise SyntaxException('List type must specify an item type in []')

    def analyze(self):
        if self.is_complex:
            if not self.global_env.class_exists(self.field_type):
                if self.field_type not in ['str', 'int', 'float', 'dict']:
                    raise SyntaxException(f'Sub type {self.field_type} not exist')
            self.global_env.relations.add_relation(self.classwrapper.class_name, self.field_type, self,
                                               RelationType.CONTAINS if self.is_list else RelationType.POINTTO)

    def __repr__(self):
        return f"{self.name}:{self.field_type} l:{self.field_length} c:{self.is_complex}"


class ClassWrapper(object):
    def __init__(self, lines, g: "ModelFile"):
        self.class_lines = lines
        self.class_name = ''
        self.fields = []
        self.comment = ''
        self.global_env = g
        self.process()

    def process(self):
        self.class_name = self.class_lines[0].split(":")[0]
        self.comment = self.class_lines[0].split("#")[-1]
        for line in self.class_lines[1:]:
            try:
                field_name = between(line, '-', ':')
            except ValueError:
                raise SyntaxException('Field starts with -, but not found')
            try:
                field_type = between(line, ':', '#')
            except ValueError:
                raise SyntaxException('Field type starts with :, but not found')
            try:
                comment = between(line, "#", "!")
            except ValueError:
                comment = field_name
            self.fields.append(FieldWrapper(
                field_name,
                field_type,
                comment,
                self,
                self.global_env
            ))

    def analyze(self):
        for field in self.fields:
            field.analyze()

    def __repr__(self):
        return f"{self.class_name} : {self.comment}"


class ModelFile(object):
    def __init__(self, path):
        self.model_filepath = path
        with open(path, 'r') as f:
            self.file_lines = f.readlines()
        self.classes = []
        self.relations = ReferenceHolder()
        self.mode_name = path.split(os.sep)[-1].split(".")[0]

    def find_class(self, name):
        for classwrapper in self.classes:
            if classwrapper.class_name == name:
                return classwrapper

    def class_exists(self, name):
        if self.find_class(name):
            return True
        return False

    def process(self):
        temp_lines = []
        for line in self.file_lines:
            if not line.strip():
                if temp_lines:
                    self.classes.append(ClassWrapper(temp_lines, self))
                temp_lines = []
                continue
            temp_lines.append(line)
        else:
            if temp_lines:
                self.classes.append(ClassWrapper(temp_lines, self))

    def analyze(self):
        for c in self.classes:
            c.analyze()




