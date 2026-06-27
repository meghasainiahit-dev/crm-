# CRM Microservice Backend

## Project Structure

```
crm-app/

company/
department/
employee/
shared/
scripts/
```

---

# Create Virtual Environment

```bash
python3 -m venv env
```

Linux

```bash
source env/bin/activate
```

Windows

```bash
env\Scripts\activate
```

---

# Install Requirements

```bash
pip install -r requirements.txt
```

---

# Run Company Service

```bash
cd company

uvicorn app.main:app \
--reload \
--host 0.0.0.0 \
--port 8001
```

Swagger

```
http://localhost:8001/docs
```

---

# Run Department Service

```bash
cd department

uvicorn app.main:app \
--reload \
--host 0.0.0.0 \
--port 8002
```

Swagger

```
http://localhost:8002/docs
```

---

# Run Employee Service

```bash
cd employee

uvicorn app.main:app \
--reload \
--host 0.0.0.0 \
--port 8003
```

---

# Run All Services

```bash
python dev.py
```

---

# Stop All Services

```bash
python stop.py
```

---

# Development Ports

| Service | Port |
|---------|------|
| Company | 8001 |
| Department | 8002 |
| Employee | 8003 |

---

# Database

Every service has its own database.

Company

```
company_db
```

Department

```
department_db
```

Employee

```
employee_db
```

---

# Rules

- Every service has its own database.
- Never access another service database directly.
- Communication should happen through REST APIs.
- JWT is verified locally using the shared auth package.
- Shared code should stay inside the `shared` folder.
