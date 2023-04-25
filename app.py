import os

from flask import Flask, redirect, render_template, request, send_file, url_for

from pystruct.utils.object_utils import get_all_concrete_object_classes
from pystruct.objects.full_report import FullReport
from pystruct.objects.grab_code import grab_code
from pystruct.utils.object_utils import get_object_class_from_class_name

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'


@app.route('/')
def main():
    table_of_content_dict = {k: v.__name__ for k, v in FullReport.content_dict.items()}
    print(table_of_content_dict)
    print(url_for('obj',  obj_class_name='UMLClassDiagramObj'))
    debug_flag = app.debug
    all_objects = sorted([_cls.prettified_class_name() for _cls in get_all_concrete_object_classes()])
    return render_template('index.html', **locals())


@app.route('/obj/<obj_class_name>')
def obj(obj_class_name):
    cls = get_object_class_from_class_name(obj_class_name.replace(' ', ''))
    html_object = cls().to_html()
    return render_template('objects.html', **locals())


@app.route('/build_obj/<obj_class_name>')
def build_obj(obj_class_name):
    cls = get_object_class_from_class_name(obj_class_name.replace(' ', ''))
    cls().delete()
    html_object = cls().to_html()
    return render_template('objects.html', **locals())


@app.route('/download/<obj_class_name>')
def download_obj(obj_class_name):
    getattr(sys.modules[__name__], obj_class_name.split('.')[0])().data()  # pre load the obj
    filepath = os.path.join(app.root_path, 'report_files/objs/', obj_class_name)
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

