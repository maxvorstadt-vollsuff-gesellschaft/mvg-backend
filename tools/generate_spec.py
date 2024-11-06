import os
import sys
import json
import yaml
from unittest.mock import Mock
from fastapi import FastAPI


# Mock the database module before it's imported
sys.modules['src.database'] = Mock()
sys.modules['src.database'].get_db = lambda: None
sys.modules['src.database'].database = Mock()
sys.modules['src.database'].engine = Mock()
sys.modules['src.database'].SessionLocal = Mock()

# Mock other commonly imported modules that might cause issues
sys.modules['fastapi_keycloak'] = Mock()
sys.modules['databases'] = Mock()

# Add the project root directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

def create_test_app():
    app = FastAPI()
    
    # Now we can safely import routes
    from src.routes import auth, events, member, quotes, chug, card
    
    # Add all routers
    app.include_router(auth.router)
    app.include_router(events.router)
    app.include_router(member.router)
    app.include_router(quotes.router)
    app.include_router(chug.router)
    app.include_router(card.router)
    
    return app

def generate_openapi_yaml():
    app = create_test_app()
    
    openapi_schema = app.openapi()
    
    # Save as JSON
    with open("openapi.json", "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    # Save as YAML
    with open("openapi.yaml", "w") as f:
        yaml.dump(openapi_schema, f, sort_keys=False)

if __name__ == "__main__":
    from unittest.mock import Mock
    generate_openapi_yaml()