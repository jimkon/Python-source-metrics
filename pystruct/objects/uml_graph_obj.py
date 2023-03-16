from itertools import chain

import networkx as nx

from pystruct.html_utils.html_pages import HTMLPage
from pystruct.objects.data_objects import AbstractObject
from pystruct.objects.imports_data_objects import InProjectImportModuleGraphDataframe, PackagesImportModuleGraphDataframe
from pystruct.objects.python_object import PObject
from pystruct.reports.uml_class import UMLClassBuilder, UMLClassRelationBuilder, ObjectRelationGraphBuilder
from pystruct.utils.file_strategies import HTMLFile
from pystruct.utils.plantuml_utils import PlantUMLService


class PlantUMLDiagramObj(AbstractObject):
    def __init__(self, multithread=False):
        super().__init__(HTMLFile(self))
        self._plant_uml = PlantUMLService(multithread)

    def build(self):
        docs = self.plantuml_docs()

        if isinstance(docs, str):
            docs = [docs]

        plantuml_diagram_html_images = self._plant_uml.convert_multiple_docs_to_html_images(docs)

        html_page = HTMLPage()
        [html_page.add_element(html_image) for html_image in plantuml_diagram_html_images]

        return html_page.html()

    def plantuml_docs(self):
        pass


class UMLClassDiagramObj(PlantUMLDiagramObj):
    def __init__(self):
        super().__init__(multithread=True)

    def plantuml_docs(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassBuilder()
        pobj.use_visitor(uml_builder)

        plantuml_doc_strings = uml_builder.result()

        return plantuml_doc_strings


class UMLClassRelationDiagramObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        pobj = PObject().python_source_object()

        uml_builder = UMLClassRelationBuilder()
        pobj.use_visitor(uml_builder)

        plantuml_doc_strings = uml_builder.result()

        plantuml_doc_strings = UMLClassRelationDiagramObj.split_documents(plantuml_doc_strings)
        return plantuml_doc_strings

    @staticmethod
    def split_documents(graph_doc):
        graph_doc_lines = graph_doc.split('\n')
        class_relations_lines = [line for line in graph_doc_lines if '<|--' in line]
        class_relations = [line.split(' <|-- ') for line in class_relations_lines]

        subgraphs = UMLClassRelationDiagramObj.split_subgraphs(class_relations)

        subgraph_docs = []
        for subgraph in subgraphs:
            subgraph_lines = [line for line in graph_doc_lines if any([_class in line for _class in subgraph])]
            subgraph_doc = '@startuml\nleft to right direction\n'+'\n'.join(subgraph_lines)+'\n@enduml'

            subgraph_docs.append(subgraph_doc)

        return subgraph_docs


    @staticmethod
    def split_subgraphs(relations):
        G = nx.Graph()
        G.add_nodes_from(set(chain.from_iterable(relations)))
        for a, b in relations:
            G.add_edge(a, b)

        subgraphs = [list(G.subgraph(c).nodes) for c in nx.connected_components(G)]

        return subgraphs



class InProjectImportModuleGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = InProjectImportModuleGraphDataframe().data()
        plantuml_doc_strings = ObjectRelationGraphBuilder(df.values.tolist()).result()
        return plantuml_doc_strings


class PackagesImportModuleGraphObj(PlantUMLDiagramObj):
    def plantuml_docs(self):
        df = PackagesImportModuleGraphDataframe().data()

        plantuml_doc_strings = []
        for package in df['import_root'].unique():
            doc = ObjectRelationGraphBuilder(df[df['import_root'] == package].values.tolist()).result()
            plantuml_doc_strings.append(doc)
        return plantuml_doc_strings


if __name__ == '__main__':
    # UMLClassDiagramObj().data()
    UMLClassRelationDiagramObj().data()
    # InProjectImportModuleGraphObj().data()
    # PackagesImportModuleGraphObj().data()
