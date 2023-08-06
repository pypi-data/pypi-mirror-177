from graphviz import Digraph
import os
from .consts import *

class FormatToPdf(object):
    name = 'pdf'

    def __init__(self, modelfile: "ModelFile"):
        self.modelfile = modelfile
        self.store_dir = ''
        self.pdf_path = ''

    def clear_old(self):
        dir_path = os.path.dirname(self.modelfile.model_filepath)
        target_dir = os.path.join(dir_path, f'target_{FormatToPdf.name}')
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        self.store_dir = target_dir
        self.pdf_path = os.path.join(self.store_dir, "models.dart")
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)

    def class_view(self, classwrapper):
        lines = []
        lines.append(f"{classwrapper.class_name}[{classwrapper.comment}]")
        lines.append("------------------------------------")
        for fieldwrapper in classwrapper.fields:
            lines.append(f"{fieldwrapper.name}\t:\t{fieldwrapper.field_type}\t\t{fieldwrapper.comment}")
        return "\r\n".join(lines)

    def table_view(self, classwrapper):
        rows = []
        for fieldwrapper in classwrapper.fields:
            rows.append([fieldwrapper.name, fieldwrapper.field_type, fieldwrapper.comment])
        rows.insert(0, ["模型:", classwrapper.class_name, classwrapper.comment])
        return "<<table>%s</table>>" % "".join(["<tr>%s</tr>" % "".join(["<td>%s</td>" % c for c in r]) for r in rows])

    def format(self):
        self.clear_old()
        dot = Digraph(name="models", comment=self.modelfile.model_filepath, format="pdf")
        for classwrapper in self.modelfile.classes:
            # height=f"{0.4*len(classwrapper.fields)}"
            dot.node(classwrapper.class_name, label=self.table_view(classwrapper), shape="box", fontsize="6")

        for class_name, relations in self.modelfile.relations.targets.items():
            for referenceItem in relations:
                if referenceItem.relation_type == RelationType.POINTTO:
                    dot.edge(class_name, referenceItem.item_type, label=f"{referenceItem.field.name}->{referenceItem.item_type} n->1", fontsize="6")

        for class_name, f1, f2 in self.modelfile.relations.findN2NRelation():
            dot.edge(f1.classwrapper.class_name, f2.classwrapper.class_name, label="n<->n", dir="both", fontsize="6")

        dot.render(filename=self.modelfile.mode_name, directory=self.store_dir, view=True)


