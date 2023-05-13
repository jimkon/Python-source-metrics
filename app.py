import os

from flask import Flask, redirect, render_template, request, send_file, url_for

from pystruct.plat.dataset_controller import DatasetController
from pystruct.objects.full_report import FullReport
from pystruct.utils.object_utils import get_all_concrete_object_classes
from pystruct.utils.object_utils import get_object_class_from_class_name

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'
debug_flag = True
print(f"{debug_flag=}")

dataset_controller = DatasetController()


@app.route('/')
def main():
    if dataset_controller.current_dataset is None:
        return redirect(url_for('new_project'))

    table_of_content_dict = {k: v.__name__ for k, v in FullReport.content_dict.items()}
    return render_template('index.html', **locals(), **globals())


@app.route('/debug')
def debug():
    existing_objs = sorted([obj.stem for obj in dataset_controller.current_dataset.objects_directory.rglob('*') if obj.is_file()])
    all_objects = sorted([_cls.name() for _cls in get_all_concrete_object_classes()])
    return render_template('debug.html', **locals(), **globals())



@app.route('/obj/<obj_class_name>')
def obj(obj_class_name):
    cls = get_object_class_from_class_name(obj_class_name.replace(' ', ''))
    html_object = cls().to_html()
    return render_template('objects.html', **locals(), **globals())


@app.route('/build_obj/<obj_class_name>')
def build_obj(obj_class_name):
    cls = get_object_class_from_class_name(obj_class_name.replace(' ', ''))
    cls().delete()
    html_object = cls().to_html()
    return render_template('objects.html', **locals(), **globals())


@app.route('/download/<obj_class_name>')
def download_obj(obj_class_name):
    cls = get_object_class_from_class_name(obj_class_name.replace(' ', ''))
    cls().data()
    filepath = os.path.join(app.root_path, 'report_files/objs/', obj_class_name)
    app.logger.info(f"{filepath}")
    return send_file(filepath, as_attachment=True)


@app.route('/project/new/', methods=['GET', 'POST'])
def new_project():
    app.logger.info(f"NEW_PROJECT> {request.method}")
    error_message = ''
    source = None
    if request.method == 'POST':
        try:
            if "filepath_input" in request.form:
                source = request.form['filepath_input']
                dataset_controller.new(dir_path=source)
            elif "giturl_input" in request.form:
                source = request.form['giturl_input']
                dataset_controller.new(git_url=source)

            return redirect(url_for('main'))
        except Exception as e:
            app.logger.warning(e)
            error_message = str(e)

    return render_template('new_project.html', **locals(), **globals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

