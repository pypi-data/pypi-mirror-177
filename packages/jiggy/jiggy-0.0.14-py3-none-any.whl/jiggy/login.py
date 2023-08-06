import platform
import sys

def is_notebook() -> bool:
    """
    Returns True if code is executed in a notebook (Jupyter, Colab, QTconsole), False otherwise.
    https://stackoverflow.com/a/39662359
    """
    try:
        shell_class = get_ipython().__class__
        for parent_class in shell_class.__mro__:
            if parent_class.__name__ == "ZMQInteractiveShell":
                return True  # Jupyter notebook, Google colab or qtconsole
        return False
    except NameError:
        return False  # Probably standard Python interpreter

# ipywidgets

