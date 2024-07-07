#!/usr/bin/env python

# Imports
import os
import sys
from pathlib import Path

import environ


# Initialize environment variables
env = environ.Env()


# Run the code only if the file is run directly
if __name__ == "__main__":
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))

    try:
        # Try to import the execute_from_command_line function
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            # Try to import django
            import django
        except ImportError:
            # Raise an ImportError if the django module is not found
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise


    # Get the current path
    current_path = Path(__file__).parent.resolve()


    # Add the path to the apps directory to the sys.path
    sys.path.append(str(current_path / "apps"))


    # Execute the command line
    execute_from_command_line(sys.argv)
