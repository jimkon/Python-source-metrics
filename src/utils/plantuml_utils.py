import os
import tempfile
import threading

import plantuml

from src.configs import PATH_FILES_DIR
from src.html.html_pages import ImageHTML
from src.utils.logs import log_plantuml, log_yellow

PLANTUML_LOCAL_SERVER_URL = 'http://localhost:8080/img/'
PLANTUML_GLOBAL_SERVER_URL = 'http://www.plantuml.com/plantuml/img/'


def _check_local_plantuml_server():
    try:
        pl = plantuml.PlantUML(PLANTUML_LOCAL_SERVER_URL)
        pl.processes("""@startuml
Bob -> Alice : helloasdasdasd
@enduml""")
    except ConnectionRefusedError as ce:
        return False
    return True


def produce_uml_diagram_from_text_file(input_text_filepath, output_path):
    if _check_local_plantuml_server():
        log_plantuml(f"(LOCALHOST) Converting UML diagram image ({output_path}) from input text file ({input_text_filepath})")
        pl = plantuml.PlantUML(PLANTUML_LOCAL_SERVER_URL)
    else:
        log_plantuml(f"(WEB) Converting UML diagram image ({output_path}) from input text file ({input_text_filepath})")
        pl = plantuml.PlantUML(PLANTUML_GLOBAL_SERVER_URL)
    pl.processes_file(input_text_filepath, outfile=output_path, directory='')


def plantuml_doc_to_html_image(plantuml_doc, temp_dir):
    temp_file = tempfile.NamedTemporaryFile(suffix="_temp_uml_text_file.txt", dir=temp_dir, delete=False)
    file_pointer = open(temp_file.name, 'w')
    file_pointer.write(plantuml_doc)

    infile_name, outfile_name = temp_file.name, f"{temp_file.name}.png"

    try:
        produce_uml_diagram_from_text_file(infile_name,
                                           output_path=outfile_name)
        file_pointer.close()
        os.unlink(file_pointer.name)
        return ImageHTML.from_image_file(outfile_name).html()
    except plantuml.PlantUMLError as pe:
        log_yellow(f'PlantUMLError failed: {infile_name} will not be produced.')

    except Exception as e:
        log_yellow(f'PLANTUML failed: {infile_name} will not be produced. {e.__class__}')
        return f"<div>The following error occurred while processing the doc:" \
               f"<br>{plantuml_doc}" \
               f"<br>{e}</div>"


class PlantUMLImageProductionThread(threading.Thread):
    def __init__(self, uml_doc, _dir):
        threading.Thread.__init__(self)
        self._uml_doc = uml_doc
        self._dir = _dir
        self._result = None

    def run(self):
        import random
        id = random.randint(0, 1000)
        log_plantuml(f'Thread {id} started')
        self._result = plantuml_doc_to_html_image(self._uml_doc, self._dir)
        log_plantuml(f'-Thread {id} finished')

    def result(self):
        return self._result


def produce_plantuml_diagrams_in_html_images(plantuml_docs):
    temp_dir = tempfile.TemporaryDirectory(dir=PATH_FILES_DIR, prefix="temp_plantUML_images_")

    html_images = []
    for doc in plantuml_docs:
        html = plantuml_doc_to_html_image(doc, temp_dir.name)
        html_images.append(html)

    return html_images


def produce_plantuml_diagrams_in_html_images_multithreading(plantuml_docs):
    temp_dir = tempfile.TemporaryDirectory(dir=PATH_FILES_DIR, prefix="temp_plantUML_images_")

    threads = []
    for doc in plantuml_docs:

        thread = PlantUMLImageProductionThread(doc, temp_dir.name)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    html_images = [thread.result() for thread in threads]

    return html_images



