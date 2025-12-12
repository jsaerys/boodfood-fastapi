# FastAPI Setup & Run Guide

## Overview
Your FastAPI application is now fully functional with a comprehensive form-based UI for testing all endpoints. All endpoints have been validated and are working correctly (100% test pass rate).

## What's Included

### 1. **FastAPI Backend** (`fastapi_app/`)
- Modular architecture: Routers → Services → Repositories
- CORS middleware enabled for cross-origin requests
- Flask-SQLAlchemy integration for database access
- JWT authentication implemented
- All major endpoints working:
  - ✅ Authentication (register, login)
  - ✅ User management
  - ✅ Tables/Mesas listing
  - ✅ Menu items retrieval
  - ✅ Orders/Pedidos creation
  - ✅ Reservations/Reservas creation

### 2. **Interactive Web Form UI** (`static/api_test.html`)
- Modern, styled HTML form interface
- All endpoints accessible via simple forms
- Token-based authentication (JWT)
- Real-time API response display
- Client-side error handling

### 3. **Testing Suite**
- **Smoke tests** (`scripts/run_smoke_tests.py`): Automated testing of all endpoints
- **Debug script** (`scripts/debug_endpoints.py`): Interactive endpoint testing

## Quick Start

### Option A: Run FastAPI Only (Port 8000)
```powershell
cd C:\Users\LENOVO\Desktop\Proyec11
$env:PYTHONPATH = '.'
python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 8000 --reload
```

Access the API at: `http://localhost:8000/api/v1`

### Option B: Run Flask + FastAPI (Recommended for Full Testing)

**Terminal 1 - Flask (Port 5000):**
```powershell
cd C:\Users\LENOVO\Desktop\Proyec11
python app.py
```

**Terminal 2 - FastAPI (Port 8000):**
```powershell
cd C:\Users\LENOVO\Desktop\Proyec11
$env:PYTHONPATH = '.'
python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 8000 --reload
```

Then open the UI at: `http://localhost:5000/static/api_test.html`

## Testing

### Run All Tests (8 endpoints, 100% pass rate):
```powershell
cd C:\Users\LENOVO\Desktop\Proyec11
$env:PYTHONPATH = '.'
python .\scripts\run_smoke_tests.py
```

### Run Interactive Debug Script:
```powershell
cd C:\Users\LENOVO\Desktop\Proyec11
$env:PYTHONPATH = '.'
python .\scripts\debug_endpoints.py
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Users
- `GET /api/v1/usuarios/me` - Get current user profile (requires auth)

### Mesas/Tables
- `GET /api/v1/mesas` - List all tables

### Menu
- `GET /api/v1/menu` - Get menu items

### Pedidos/Orders
- `POST /api/v1/pedidos` - Create new order (requires auth)
- Items structure: `{"menu_item_id": int, "cantidad": int, "precio_unitario": decimal}`

### Reservas/Reservations
- `POST /api/v1/reservas` - Create new reservation (requires auth)
- Date format: `"2025-12-15 19:00"` (YYYY-MM-DD HH:MM)

## Using the Web Form UI

1. Navigate to `http://localhost:5000/static/api_test.html`
2. **Register**: Fill in the registration form with name, email, password, phone, and address
3. **Login**: Use the email/password from registration to login
4. **Token Display**: JWT token will display after successful login (auto-stored locally)
5. **Mesas**: View all available tables
6. **Menú**: View all menu items
7. **Crear Pedido**: Create an order by selecting items
8. **Crear Reserva**: Create a reservation by entering date, time, and number of people
9. **Ver Perfil**: View your user profile

## Database

**Connection Details:**
- Host: `mysql.enlinea.sbs`
- Port: `3311`
- Database: `f58_brandon`
- User credentials: See `config.py`

## Troubleshooting

### Port Already in Use
If port 8000 is in use:
```powershell
# Use a different port
python -m uvicorn fastapi_app.asgi:app --host 0.0.0.0 --port 8001
```

### Database Connection Issues
- Verify MySQL server is running
- Check credentials in `config.py`
- Ensure database exists: `f58_brandon`

### Import Errors
Ensure `PYTHONPATH` is set correctly:
```powershell
$env:PYTHONPATH = '.'
```

## Architecture

```
Proyec11/
├── fastapi_app/          # FastAPI package
│   ├── routers/          # HTTP endpoint definitions
│   ├── services/         # Business logic layer
│   ├── repositories/     # Data access layer
│   ├── schemas/          # Pydantic validation models
│   └── asgi.py          # ASGI entrypoint
├── app.py               # Flask application
├── config.py            # Configuration
├── models/              # SQLAlchemy ORM models
├── static/              # HTML/CSS/JS assets
│   └── api_test.html    # Interactive form UI
├── routes/              # Flask routes (legacy)
├── scripts/             # Utility scripts
│   ├── run_smoke_tests.py    # Test suite
│   └── debug_endpoints.py    # Debug tool
└── templates/           # Flask templates (legacy)
```

## Key Files Modified/Created

### New Files:
- `fastapi_app/schemas/__init__.py` - Pydantic schemas
- `fastapi_app/routers/` - All endpoint definitions
- `fastapi_app/services/` - Business logic
- `fastapi_app/repositories/` - Data access
- `scripts/run_smoke_tests.py` - Test suite
- `scripts/debug_endpoints.py` - Debug script
- `static/api_test.html` - Form UI

### Modified Files:
- `fastapi_app/services/reservas_service.py` - Fixed reserva model mapping
- Database models in `models/__init__.py` - Already aligned

## Next Steps

1. **Manual Testing**: Use the web form UI at `http://localhost:5000/static/api_test.html`
2. **Automated Testing**: Run `python .\scripts\run_smoke_tests.py` to verify all endpoints
3. **Integration**: Connect your frontend to the FastAPI endpoints on port 8000
4. **Production**: Configure proper error handling, logging, and security settings

## Support

All endpoints have been validated and tested. If you encounter any issues:
1. Check the error message in the response
2. Run the debug script to see detailed endpoint behavior
3. Review the test output for status codes and error details

---

**Status**: ✅ FastAPI Fully Functional
- Test Pass Rate: 100% (8/8 endpoints)
- All major features working
- Form UI ready for use
- Database integration verified
