import plantuml

from src.utils.logs import log_pink


def produce_uml_diagram_from_text_file(input_text_filepath, output_path):
    log_pink(f"Converting UML diagram image ({output_path}) from input text file ({input_text_filepath}")
    pl = plantuml.PlantUML('http://www.plantuml.com/plantuml/img/')
    pl.processes_file(input_text_filepath, outfile=output_path, directory='')
