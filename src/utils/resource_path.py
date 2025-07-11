def resource_path(relative_path):
    """ Get the absolute path to the resource, works for development and for PyInstaller """
    import os
    import sys

    # Get the base path depending on whether the application is running in a bundle or not
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (PyInstaller)
        base_path = sys._MEIPASS
    else:
        # If the application is run in a normal Python environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)