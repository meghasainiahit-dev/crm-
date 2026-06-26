from pathlib import Path
import sys

TEMPLATE = {
    "app/database/database.py": """# Database Connection

def connect_db():
    pass
""",

    "app/model/model.py": """# Models
""",

    "app/routes/routes.py": """from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health():
    return {"message": "Service Running"}
""",

    "app/schema/schema.py": """# Pydantic Schemas
""",

    "app/service/service.py": """# Business Logic
""",

    "app/main.py": """from fastapi import FastAPI
from app.routes.routes import router

app = FastAPI(title="SERVICE_NAME")

app.include_router(router)
""",

    ".env": """PORT=8000
DATABASE_URL=
REDIS_URL=
JWT_SECRET=
""",

    "requirements.txt": """fastapi
uvicorn
python-dotenv
""",

    "README.md": "# Service\n"
}


def create_service(name: str):
    root = Path(name)

    for file_path, content in TEMPLATE.items():
        full_path = root / file_path

        full_path.parent.mkdir(parents=True, exist_ok=True)

        if not full_path.exists():
            full_path.write_text(
                content.replace("SERVICE_NAME", name.title()),
                encoding="utf-8"
            )

    packages = [
        "app",
        "app/database",
        "app/model",
        "app/routes",
        "app/schema",
        "app/service",
    ]

    for pkg in packages:
        init_file = root / pkg / "__init__.py"
        init_file.touch(exist_ok=True)

    print(f"\n✅ {name} service created successfully.")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python create_module.py company")
        sys.exit()

    create_service(sys.argv[1])