from src.html.pages.page import HTMLPage
from src.objects.data_objects import AbstractObject
from src.objects.imports_data_objects import InProjectImportModuleGraphDataframe, PackagesImportModuleGraphDataframe
from src.objects.python_object import PObject
from src.reports.uml_class import UMLClassBuilder, UMLClassRelationBuilder, ObjectRelationGraphBuilder
from src.utils.file_strategies import HTMLFile
from src.utils.plantuml_utils import produce_plantuml_diagrams_in_html_images_multithreading, \
    produce_plantuml_diagrams_in_html_images


class PlantUMLDiagramObj(AbstractObject):
    def __init__(self, multithread_prod=False):
        super().__init__(HTMLFile(self))
        self._prod_func = produce_plantuml_diagrams_in_html_images_multithreading if multithread_prod else produce_plantuml_diagrams_in_html_images

    def build(self):
        docs = self.plantuml_docs()

        if isinstance(docs, str):
            docs = [docs]

        plantuml_diagram_html_images = self._prod_func(docs)

        html_page = HTMLPage()
        [html_page.add(html_image) for html_image in plantuml_diagram_html_images]

        return html_page.html

    def plantuml_docs(self):
        pass


class UMLClassDiagramObj(PlantUMLDiagramObj):
    def __init__(self):
        super().__init__(multithread_prod=True)

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

        return plantuml_doc_strings


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
    UMLClassDiagramObj().data()
    UMLClassRelationDiagramObj().data()
    InProjectImportModuleGraphObj().data()
    PackagesImportModuleGraphObj().data()
