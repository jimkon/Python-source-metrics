import threading
import uuid

import plantuml

from src.html.html_pages import ImageHTML
from src.utils.logs import log_plantuml

PLANTUML_LOCAL_SERVER_URL = 'http://localhost:8080/img/'
PLANTUML_WEB_SERVER_URL = 'http://www.plantuml.com/plantuml/img/'


class WorkerThread(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self._task = task
        self._result = None

    def run(self):
        id = uuid.uuid4().hex[:6]
        log_plantuml(f'Thread {id} started')
        self._result = self._task()
        log_plantuml(f'-- Thread {id} finished')

    def result(self):
        return self._result


class PlantUMLService:
    @staticmethod
    def _check_local_plantuml_server():
        try:
            pl = plantuml.PlantUML(PLANTUML_LOCAL_SERVER_URL)
            pl.processes("""@startuml\nBob -> Alice : hello\n@enduml""")
        except ConnectionRefusedError as ce:
            return False
        return True

    def __init__(self, multithreading=False):
        self._multithreading_flag = multithreading

        if PlantUMLService._check_local_plantuml_server():
            log_plantuml(f"(LOCALHOST) Plant UML running locally: {PLANTUML_LOCAL_SERVER_URL}")
            self._plant_uml_server = plantuml.PlantUML(PLANTUML_LOCAL_SERVER_URL)
        else:
            log_plantuml(f"(WEB) Plant UML running on web: {PLANTUML_WEB_SERVER_URL}")
            self._plant_uml_server = plantuml.PlantUML(PLANTUML_WEB_SERVER_URL)

    def convert_doc_to_html_image(self, doc):
        log_plantuml(f"Processing plantUML document (size={len(doc)})..")
        raw_image_data = self._plant_uml_server.processes(plantuml_text=doc)
        image_html = ImageHTML(raw_image_data)
        log_plantuml(f"PlantUML document (size={len(doc)}) is done.")

        return image_html

    def convert_multiple_docs_to_html_images(self, docs):
        if self._multithreading_flag:
            return self._send_multiple_requests(docs)
        else:
            return [self.convert_doc_to_html_image(doc) for doc in docs]

    def _send_multiple_requests(self, docs):
        threads = []
        for doc in docs:
            thread = WorkerThread(lambda: self.convert_doc_to_html_image(doc))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        html_images = [thread.result() for thread in threads]
        return html_images


if __name__ == "__main__":
    serv = PlantUMLService()
    docs = ["""@startuml\nBob -> Alice : hello\n@enduml""", """@startuml\nBob -> Alice : hello\n@enduml"""]
    res = serv.convert_multiple_docs_to_html_images(docs)
    print(res)




