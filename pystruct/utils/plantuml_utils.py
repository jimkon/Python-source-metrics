import threading
import uuid

import plantuml

from pystruct.html_utils.html_pages import ImageHTML
from pystruct.utils.logs import log_plantuml

PLANTUML_LOCAL_SERVER_URL = 'http://localhost:8080/img/'
PLANTUML_DOCKER_SERVER_URL = 'http://plantuml:8080/img/'
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
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = PlantUMLService()
            log_plantuml(f"PlantUMLService: Instance is created.")
        return cls.__instance

    def __init__(self, multithreading=False):
        self._multithreading_flag = multithreading
        self._plant_uml_server = None
        self.reset_plant_uml_server()

    def reset_plant_uml_server(self):
        def init_plantuml(url):
            log_plantuml(f"Attempting to connect to a local Plant UML server: {url}")
            plant_uml_server = plantuml.PlantUML(url)
            log_plantuml(f"Sending test message...")
            res = plant_uml_server.processes(plantuml_text="""@startuml\nBob -> Alice : hello\n@enduml""")
            log_plantuml(f"Response length {len(res)}")
            return plant_uml_server

        try:
            self._plant_uml_server = init_plantuml(PLANTUML_LOCAL_SERVER_URL)
            log_plantuml(f"(LOCALHOST) Plant UML is running locally: {PLANTUML_LOCAL_SERVER_URL}")
        except (plantuml.PlantUMLConnectionError, ConnectionRefusedError, OSError) as local_connection_error:
            try:
                self._plant_uml_server = init_plantuml(PLANTUML_DOCKER_SERVER_URL)
                log_plantuml(f"(DOCKER) Plant UML is running on web: {PLANTUML_DOCKER_SERVER_URL}")
            except (plantuml.PlantUMLConnectionError, ConnectionRefusedError) as docker_connection_error:
                self._plant_uml_server = init_plantuml(PLANTUML_WEB_SERVER_URL)
                log_plantuml(f"(WEB) Plant UML is running on web: {PLANTUML_WEB_SERVER_URL}")

    def convert_doc_to_html_image(self, doc, error_message=''):
        try:
            log_plantuml(f"Processing plantUML document (size={len(doc)})..")
            raw_image_data = self._plant_uml_server.processes(plantuml_text=doc)
            image_html = ImageHTML(raw_image_data)
            log_plantuml(f"PlantUML document (size={len(doc)}) is done.")
            return image_html
        # except plantuml.PlantUMLHTTPError as http_error:
        except Exception as e:
            if error_message is None:
                raise
            else:
                log_plantuml(f"WARNING: PlantUML document (size={len(doc)}) failed.")
                error_message_uml = f"""{error_message} Error: {e}"""
                return error_message_uml

    def convert_multiple_docs_to_html_images(self, docs):
        if self._multithreading_flag:
            try:
                raise NotImplementedError
                # return self._send_multiple_requests(docs) doesn't work right now
            except Exception as exception:
                log_plantuml(
                    f"Processing {len(docs)} documents with multithreading failed with {exception=}. Switching to linear.")
                self._multithreading_flag = False

        html_images = [self.convert_doc_to_html_image(doc) for doc in docs]
        return html_images

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
    serv = PlantUMLService.get_instance()
    docs = ["""@startuml\nBob -> Alice : hello\n@enduml""", """@startuml\nBob -> Alice : hello\n@enduml"""]
    res = serv.convert_multiple_docs_to_html_images(docs)
    print(res)
