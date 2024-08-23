import importlib.util
import sys

module_name = 'app'

spec = importlib.util.find_spec(module_name)
if spec is None:
    print(f"Can't find the {module_name} module")
else:
    print(f"Found {module_name} at {spec.origin}")

from app import create_app

app = create_app()
print("App created successfully.")

