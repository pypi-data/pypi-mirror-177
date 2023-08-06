import os
from .consts import *

class FormatToJORM(object):
    name = 'jm'

    def __init__(self, modelfile: "ModelFile"):
        self.modelfile = modelfile
        self.store_dir = ''

    def clear_old(self):
        dir_path = os.path.dirname(self.modelfile.model_filepath)
        target_dir = os.path.join(dir_path, f'target_{FormatToJORM.name}')
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        self.store_dir = target_dir
        for classwrapper in self.modelfile.classes:
            file_path = os.path.join(self.store_dir, f"{classwrapper.class_name.lower()}.dart")
            if os.path.exists(file_path):
                os.remove(file_path)
            orm_path = os.path.join(self.store_dir, f"{classwrapper.class_name.lower()}.jorm.dart")
            if os.path.exists(orm_path):
                os.remove(orm_path)

    def type_map(self, fieldwrapper):
        mapper = {
            BUILIN_TYPE_STR: 'String',
            BUILIN_TYPE_INT: 'int',
            BUILIN_TYPE_FLOAT: 'double',
            BUILIN_TYPE_DOUBLE: 'double',
            BUILIN_TYPE_BOOL: 'bool'
        }
        if fieldwrapper.is_list:
            return f"List<{fieldwrapper.field_type}>"
        if fieldwrapper.is_complex:
            return fieldwrapper.field_type
        return mapper[fieldwrapper.field_type]

    def convert_type(self, fieldwrapper):
        mapper = {
            BUILIN_TYPE_STR: 'Str',
            BUILIN_TYPE_INT: 'Int',
            BUILIN_TYPE_FLOAT: 'Double',
            BUILIN_TYPE_DOUBLE: 'Double',
            BUILIN_TYPE_BOOL: 'Bool'
        }
        if fieldwrapper.is_complex:
            return "Str"
        return mapper[fieldwrapper.field_type]

    def format(self):
        self.clear_old()
        for classwrapper in self.modelfile.classes:
            file_path = os.path.join(self.store_dir, f"{classwrapper.class_name.lower()}.dart")
            type_def_lines = []
            type_def_lines.append("import 'dart:convert';")
            type_def_lines.append("import 'package:flutter/foundation.dart';")
            type_def_lines.append("import 'package:jaguar_orm/jaguar_orm.dart';")
            type_def_lines.append("import 'package:uuid/uuid.dart';")
            type_def_lines.append("")
            type_def_lines.append(f"part '{classwrapper.class_name.lower()}.jorm.dart';")
            type_def_lines.append("")
            type_def_lines.append("class %s {" % classwrapper.class_name)
            type_def_lines.append("      String uuid;")
            for fieldwrapper in classwrapper.fields:
                if not fieldwrapper.is_list:
                    if fieldwrapper.is_complex:
                        type_def_lines.append(f"    String {fieldwrapper.name}_id;")
                    else:
                        type_def_lines.append(f"    {self.type_map(fieldwrapper)} {fieldwrapper.name};")
            type_def_lines.append("      int createTs;")
            type_def_lines.append("      int updateTs;")
            type_def_lines.append("")
            type_def_lines.append(f"    {classwrapper.class_name}();")
            type_def_lines.append("")
            type_def_lines.append("    %s.make({" % classwrapper.class_name)
            type_def_lines.append("        this.uuid,")
            for fieldwrapper in classwrapper.fields:
                if not fieldwrapper.is_list:
                    if fieldwrapper.is_complex:
                        type_def_lines.append(f"        this.{fieldwrapper.name}_id,")
                    else:
                        type_def_lines.append(f"        this.{fieldwrapper.name},")
            type_def_lines.append("    }): this.uuid = this.uuid??Uuid().v1(),")
            type_def_lines.append("        this.createTs = DateTime.now().millisecondsSinceEpoch,")
            type_def_lines.append("        this.updateTs = DateTime.now().millisecondsSinceEpoch;")
            type_def_lines.append("")
            type_def_lines.append("}")
            type_def_lines.append("")
            type_def_lines.append("@GenBean()")
            type_def_lines.append(f"class {classwrapper.class_name}Bean extends Bean<{classwrapper.class_name}> with _{classwrapper.class_name}Bean " + "{")
            type_def_lines.append(f"    {classwrapper.class_name}Bean(Adapter adapter) : super(adapter);")
            type_def_lines.append("")
            type_def_lines.append("    @override")
            type_def_lines.append(f"    String get tableName => \"{classwrapper.class_name.lower()}\";")
            type_def_lines.append("")
            type_def_lines.append(f"    /// Select {classwrapper.class_name} by uuid")
            type_def_lines.append(f"    Future<{classwrapper.class_name}> getById(String uuid) async " + "{")
            type_def_lines.append(f"        return await findOne(finder.where(this.uuid.eq(uuid)));")
            type_def_lines.append("    }")
            type_def_lines.append("")
            type_def_lines.append("    Future deleteByUuid(String uuid) async {")
            type_def_lines.append("        return await removeWhere(this.uuid.eq(uuid));")
            type_def_lines.append("    }")
            type_def_lines.append("")
            type_def_lines.append(f"    Future<int> update{classwrapper.class_name}({classwrapper.class_name} mod) async " + "{")
            type_def_lines.append(f"        final upt = Update(tableName).where(this.uuid.eq(mod.uuid));")
            for fieldwrapper in classwrapper.fields:
                type_def_lines.append(f"        upt.set(this.{fieldwrapper.name}, mod.{fieldwrapper.name});")
            type_def_lines.append("        upt.set(this.updateTs, DateTime.now().millisecondsSinceEpoch);")
            type_def_lines.append("        return await adapter.update(upt);")
            type_def_lines.append("    }")
            type_def_lines.append("")
            type_def_lines.append(f"    Future<int> insertOrUpdate({classwrapper.class_name} mod) async " + "{")
            type_def_lines.append("        final ext = await this.getById(mod.uuid);")
            type_def_lines.append("        if (ext == null){")
            type_def_lines.append("            return await this.insert(mod);")
            type_def_lines.append("        }else{")
            type_def_lines.append("            return await this.updateTitle(uuid, title);")
            type_def_lines.append("        }")
            type_def_lines.append("")
            type_def_lines.append("    }")
            type_def_lines.append("")
            type_def_lines.append(f"    Future<List<{classwrapper.class_name}>> fetchList(Expression exps, String orderField, [bool ascending = false]) async " + "{")
            type_def_lines.append("        return await findMany(")
            type_def_lines.append("                finder.where(exps).orderBy(orderField, ascending));")
            type_def_lines.append("    }")
            type_def_lines.append("")
            type_def_lines.append("}")
            type_def_lines.append("")

            with open(file_path, 'w') as f:
                f.write("\n".join(type_def_lines))

            orm_path = os.path.join(self.store_dir, f"{classwrapper.class_name.lower()}.jorm.dart")
            orm_lines = []
            orm_lines.append("// GENERATED CODE - DO NOT MODIFY BY HAND")
            orm_lines.append("")
            orm_lines.append(f"part of '{classwrapper.class_name.lower()}.dart';")
            orm_lines.append("")
            orm_lines.append("// **************************************************************************")
            orm_lines.append("// BeanGenerator")
            orm_lines.append("// **************************************************************************")
            orm_lines.append("")
            orm_lines.append(f"abstract class _{classwrapper.class_name}Bean implements Bean<{classwrapper.class_name}> " + "{")
            orm_lines.append("    final uuid = StrField('uuid');")
            orm_lines.append("    final createTs = IntField('create_ts');")
            orm_lines.append("    final updateTs = IntField('update_ts');")
            for fieldwrapper in classwrapper.fields:
                fieldwrapper.field_type

                orm_lines.append(f"    final {fieldwrapper.name} = IntField('{fieldwrapper.name.lower()}');")
            orm_lines.append("    Map<String, Field> _fields;")
            orm_lines.append("")
            orm_lines.append("    Map<String, Field> get fields => _fields ??= {")
            orm_lines.append("        uuid.name: uuid,")
            orm_lines.append("        createTs.name: createTs,")
            orm_lines.append("        updateTs.name: updateTs,")
            for fieldwrapper in classwrapper.fields:
                orm_lines.append(f"        {fieldwrapper.name}.name: {fieldwrapper.name},")
            orm_lines.append("      };")
            orm_lines.append("")
            orm_lines.append(f"    {classwrapper.class_name} fromMap(Map map) " + "{")
            orm_lines.append(f"        {classwrapper.class_name} model = {classwrapper.class_name}();")
            orm_lines.append("        model.uuid = adapter.parseValue(map['uuid']);")
            orm_lines.append("        model.createTs = adapter.parseValue(map['create_ts']);")
            orm_lines.append("        model.updateTs = adapter.parseValue(map['update_ts']);")
            for fieldwrapper in classwrapper.fields:
                orm_lines.append(f"        model.{fieldwrapper.name} = adapter.parseValue(map['{fieldwrapper.name.lower()}']);")
            orm_lines.append("        return model;")
            orm_lines.append("    }")
            orm_lines.append("")
            orm_lines.append(f"    List<SetColumn> toSetColumns({classwrapper.class_name} model,")
            orm_lines.append("            {bool update = false, Set<String> only, bool onlyNonNull = false}) {")
            orm_lines.append("        List<SetColumn> ret = [];")
            orm_lines.append("")
            orm_lines.append("        if (only == null && !onlyNonNull) {")
            orm_lines.append("            ret.add(uuid.set(model.uuid));")
            orm_lines.append("            ret.add(createTs.set(model.createTs));")
            orm_lines.append("            ret.add(updateTs.set(model.updateTs));")
            for fieldwrapper in classwrapper.fields:
                orm_lines.append(f"            ret.add({fieldwrapper.name}.set(model.{fieldwrapper.name}));")
            orm_lines.append("        } else if (only != null) {")
            orm_lines.append("            if (only.contains(uuid.name)) ret.add(uuid.set(model.uuid));")
            orm_lines.append("            if (only.contains(createTs.name)) ret.add(createTs.set(model.createTs));")
            orm_lines.append("            if (only.contains(updateTs.name)) ret.add(updateTs.set(model.updateTs));")
            for fieldwrapper in classwrapper.fields:
                orm_lines.append(f"            if (only.contains({fieldwrapper.name}.name)) ret.add({fieldwrapper.name}.set(model.{fieldwrapper.name}));")
            orm_lines.append("        } else")
            orm_lines.append("        /* if (onlyNonNull) */ {")
            orm_lines.append("            if (model.uuid != null) {")
            orm_lines.append("                ret.add(uuid.set(model.uuid));")
            orm_lines.append("            }")
            orm_lines.append("            if (model.createTs != null) {")
            orm_lines.append("                ret.add(createTs.set(model.createTs));")
            orm_lines.append("            }")
            orm_lines.append("            if (model.updateTs != null) {")
            orm_lines.append("                ret.add(updateTs.set(model.updateTs));")
            orm_lines.append("            }")
            for fieldwrapper in classwrapper.fields:
                orm_lines.append(f"            if (model.{fieldwrapper.name} != null) " + "{")
                orm_lines.append(f"                ret.add({fieldwrapper.name}.set(model.{fieldwrapper.name}));")
                orm_lines.append("            }")
            orm_lines.append("        }")
            orm_lines.append("        return ret;")
            orm_lines.append("    }")
            orm_lines.append("")
            orm_lines.append("    Future<void> createTable({bool ifNotExists = false}) async {")
            orm_lines.append("        final st = Sql.create(tableName, ifNotExists: ifNotExists);")
            orm_lines.append("        st.addStr(uuid.name, isNullable: false);")
            orm_lines.append("        st.addInt(createTs.name, isNullable: false);")
            orm_lines.append("        st.addInt(updateTs.name, isNullable: false);")
            for fieldwrapper in classwrapper.fields:
                orm_lines.append(f"        st.add{self.convert_type(fieldwrapper)}({fieldwrapper.name}.name, isNullable: false);")
            orm_lines.append("        return adapter.createTable(st);")
            orm_lines.append("    }")
            orm_lines.append("")
            operation_codes = """    Future<dynamic> insert(%(cname)s model,
            {bool cascade = false,
            bool onlyNonNull = false,
            Set<String> only}) async {
        final Insert insert = inserter
                .setMany(toSetColumns(model, only: only, onlyNonNull: onlyNonNull));
        return adapter.insert(insert);
    }

    Future<void> insertMany(List<%(cname)s> models,
            {bool onlyNonNull = false, Set<String> only}) async {
        final List<List<SetColumn>> data = models
                .map((model) =>
                        toSetColumns(model, only: only, onlyNonNull: onlyNonNull))
                .toList();
        final InsertMany insert = inserters.addAll(data);
        await adapter.insertMany(insert);
        return;
    }

    Future<dynamic> upsert(%(cname)s model,
            {bool cascade = false,
            Set<String> only,
            bool onlyNonNull = false,
            isForeignKeyEnabled = false}) async {
        final Upsert upsert = upserter
                .setMany(toSetColumns(model, only: only, onlyNonNull: onlyNonNull));
        return adapter.upsert(upsert);
    }

    Future<void> upsertMany(List<%(cname)s> models,
            {bool onlyNonNull = false,
            Set<String> only,
            isForeignKeyEnabled = false}) async {
        final List<List<SetColumn>> data = [];
        for (var i = 0; i < models.length; ++i) {
            var model = models[i];
            data.add(
                    toSetColumns(model, only: only, onlyNonNull: onlyNonNull).toList());
        }
        final UpsertMany upsert = upserters.addAll(data);
        await adapter.upsertMany(upsert);
        return;
    }

    Future<void> updateMany(List<%(cname)s> models,
            {bool onlyNonNull = false, Set<String> only}) async {
        final List<List<SetColumn>> data = [];
        final List<Expression> where = [];
        for (var i = 0; i < models.length; ++i) {
            var model = models[i];
            data.add(
                    toSetColumns(model, only: only, onlyNonNull: onlyNonNull).toList());
            where.add(null);
        }
        final UpdateMany update = updaters.addAll(data, where);
        await adapter.updateMany(update);
        return;
    }
""" % dict(cname=classwrapper.class_name)
            orm_lines.append(operation_codes)
            orm_lines.append("}")
            orm_lines.append("")
            with open(orm_path, 'w') as f:
                f.write("\n".join(orm_lines))



