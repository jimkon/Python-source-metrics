import os
import sys

from flask import Flask, render_template, send_file, request, url_for, redirect

from pystruct.objects.grab_code import grab_code

from pystruct.objects.imports_data_objects import MostImportedPackages, UnusedModules, InvalidImports, \
    MostImportedProjectModules, MostImportedProjectPackages, ImportsStatsHTML
from pystruct.objects.metric_tables import AllMetricsTable, AllMetricsStatsHTML
from pystruct.objects.uml_graph_obj import UMLClassDiagramObj, UMLClassRelationDiagramObj, InProjectImportModuleGraphObj, \
    PackagesImportModuleGraphObj

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'

@app.route('/')
def main():
    return render_template('index.html', **globals())


@app.route('/obj/<obj_class>')
def obj(obj_class):
    cls = getattr(sys.modules[__name__], obj_class)
    html_object = cls().data()
    return render_template('objects.html', **locals())


@app.route('/download/<obj_class>')
def download_obj(obj_class):
    filepath = os.path.join(app.root_path, 'report_files/objs/', obj_class)
    app.logger.info(f"{filepath}")
    return send_file(filepath, as_attachment=True)


@app.route('/load/', methods=['GET', 'POST'])
def load_project():
    app.logger.info(f"LOAD_PROJECT> {request.method}")
    error_message = ''
    source = None
    if request.method == 'POST':
        if "filepath_input" in request.form:
            source = request.form['filepath_input']
        elif "giturl_input" in request.form:
            source = request.form['giturl_input']

        try:
            grab_code(source)
            return redirect(url_for('main'))
        except Exception as e:
            app.logger.warning(e)
            error_message = str(e)

    return render_template('load_project.html', **locals())




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
