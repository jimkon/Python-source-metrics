import sys

from flask import Flask, render_template

from pystruct.objects.imports_data_objects import MostImportedPackages, UnusedModules, InvalidImports, \
    MostImportedProjectModules, MostImportedProjectPackages
from pystruct.objects.metric_tables import AllMetricsTable, AllMetricsStatsHTML
from pystruct.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj, InProjectImportModuleGraphObj, \
    PackagesImportModuleGraphObj

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', **globals())


@app.route('/obj/<obj_class>')
def obj(obj_class):
    cls = getattr(sys.modules[__name__], obj_class)
    html_object = cls().data()
    return render_template('objects.html', html_object=html_object)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
