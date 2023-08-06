from rubberdoc.generator import RubberDoc 
from rubberdoc.config_provider import RubberDocConfig
from rubberdoc.doc_handler import BaseDocHandler


config = RubberDocConfig(path_to_config=None)
config.input['exclude'] = [
    "file_to_exclude.py"
]


class MyDocHandler(BaseDocHandler):
    """Custom DocHandler"""
    
    def wrap_codeblock(self, code: str) -> str:
        """Override the `wrap_codeblock` method to return nothing"""
        return ""

    def wrap_docstring(self, docstring: str) -> str:
        return '**DOCSTRING**  \n' + docstring + '  \n'


rd = RubberDoc(
    config=config,
    doc_handler=MyDocHandler)

rd.generate(
    input_directory=r"path/to/package", 
    output_directory=r"path/to/documentation")
