from inline_example import inline_example
from pathlib import Path

def base_template():
    """Generates an inline base template for RubberDoc

    Note: you will want to remove the call to `base_template()` 
    in you script file before you run the generated template.  
    Example usage:  

    ```
    from rubberdoc.templates import base_template
    base_template()
    ```
    """
    inline_example(
        example_path=(Path(__file__).parent 
            / 'examples/example_from_script.py'))