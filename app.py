import abc
import os
import sys

from flask import Flask, render_template, send_file, request, url_for, redirect

from pystruct.objects.full_report import FullReport
from pystruct.objects.grab_code import grab_code
import pystruct

from pystruct.objects.imports_data_objects import *
from pystruct.objects.metric_tables import *
from pystruct.objects.metric_obj import *
from pystruct.objects.uml_graph_obj import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


@app.route('/')
def main():
    table_of_content_dict = {k: v.__name__ for k, v in FullReport.content_dict.items()}
    debug_flag = app.debug
    # all_objects = sorted([_cls.__name__ for _cls in all_subclasses(AbstractObject)
    #                       if (issubclass(_cls, HTMLObject) and not isinstance(_cls, abc.ABC))])
    all_objects = sorted([_cls.__name__ for _cls in all_subclasses(AbstractObject)
                          if (not isinstance(_cls, abc.ABC))])
    return render_template('index.html', **locals())


@app.route('/obj/<obj_class>')
def obj(obj_class):
    cls = getattr(sys.modules[__name__], obj_class)
    html_object = cls().to_html()
    return render_template('objects.html', **locals())


@app.route('/build_obj/<obj_class>')
def build_obj(obj_class):
    cls = getattr(sys.modules[__name__], obj_class)
    cls().delete()
    html_object = cls().to_html()
    return render_template('objects.html', **locals())


@app.route('/download/<obj_class>')
def download_obj(obj_class):
    getattr(sys.modules[__name__], obj_class.split('.')[0])().data()  # pre load the obj
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
