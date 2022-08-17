import plantuml


def produce_uml_diagram_from_text_file(input_text_filepath):
    pl = plantuml.PlantUML('http://www.plantuml.com/plantuml/img/')
    pl.processes_file(input_text_filepath, directory='')
