import pandas as pd
from flask import Flask, redirect, render_template, request, send_file, url_for, escape

from pystruct.objects.full_report import FullReport
from pystruct.plat.dataset_controller import DatasetController
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
    filepath = dataset_controller.current_dataset.objects_directory / "html" / f"{obj_class_name}.html"
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


@app.route('/debug')
def debug():
    existing_objs = sorted([obj.stem for obj in dataset_controller.current_dataset.objects_directory.rglob('*') if obj.is_file()])
    all_objects = sorted([_cls.name() for _cls in get_all_concrete_object_classes()])
    return render_template('debug.html', **locals(), **globals())


@app.route('/debug/test_all_objects')
def test_all_objects():
    all_objects = [_cls for _cls in get_all_concrete_object_classes()]

    results = []
    for obj_class in all_objects:
        try:
            _cls = get_object_class_from_class_name(obj_class.name().replace(' ', ''))
            result = _cls().build()
        except Exception as e:
            build_result = f"{e.__class__.__name__}: {str(e)}"
        else:
            build_result = f"Success (len={len(result)})"

        obj_res = {
            'object': f"<a href={url_for('build_obj', obj_class_name=obj_class.name())}>{obj_class.name()}</a>",
            'build result': build_result
        }
        results.append(obj_res)

    results_df = pd.DataFrame(results).sort_values('build result', ascending=True)
    objects_table = results_df.to_html(escape=False)
    return render_template('test_all_objects.html', **locals(), **globals())


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

