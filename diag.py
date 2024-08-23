import importlib.util
import sys
import os

def print_directory_contents(path):
    print(f"\nContents of {path}:")
    for item in os.listdir(path):
        print(f"  {item}")
        if os.path.isfile(os.path.join(path, item)):
            with open(os.path.join(path, item), 'r') as f:
                print(f"    First few lines:")
                for i, line in enumerate(f):
                    if i >= 5:  # Print first 5 lines
                        break
                    print(f"      {line.strip()}")

def diagnose_import():
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    module_name = 'app'
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"Can't find the {module_name} module")
    else:
        print(f"Found {module_name} at {spec.origin}")
        
        # Try to import the module
        try:
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)
            print(f"Successfully imported {module_name}")
            
            # Check if create_app exists
            if hasattr(app_module, 'create_app'):
                print("create_app function found in the module")
            else:
                print("create_app function not found in the module")
                print(f"Available attributes: {dir(app_module)}")
        except Exception as e:
            print(f"Error importing {module_name}: {e}")

    try:
        from app import create_app
        print("Successfully imported create_app")
    except ImportError as e:
        print(f"ImportError: {e}")

    # Print contents of the app directory
    app_dir = os.path.join(os.getcwd(), 'app')
    if os.path.exists(app_dir):
        print_directory_contents(app_dir)
    else:
        print(f"\nDirectory not found: {app_dir}")

if __name__ == "__main__":
    diagnose_import()