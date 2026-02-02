# Lucart 3D Management System

A web-based management application for a 3D printing business, featuring a retro Windows XP aesthetic.

## Modules
- **Authentication:** Admin-only access.
- **Finance:** Income/Expense tracking, Business/Personal separation.
- **Inventory:** Material tracking (Filament, Resin, etc.), Low stock alerts.
- **Orders:** Order lifecycle management, Payment tracking, Material usage deduction.
- **Quotes:** Create and manage quotes, Convert to Orders, Print view.
- **Customers:** Basic CRM and history.

## Setup & Deployment

### Local Development

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database:**
   ```bash
   export FLASK_APP=run.py
   flask db upgrade
   ```

3. **Create Admin User:**
   ```bash
   python create_admin.py <username> <password>
   ```
   Example: `python create_admin.py admin admin`

4. **Run the Application:**
   ```bash
   export FLASK_CONFIG=development
   flask run
   ```
   Access at `http://localhost:5000`.

### Production Deployment

1. **Environment Variables:**
   Copy `.env.example` to `.env` and set the following:
   - `FLASK_CONFIG=production`
   - `SECRET_KEY`: A strong random string.
   - `DATABASE_URL`: Connection string for PostgreSQL (recommended) or other DB.

2. **Database:**
   Ensure your production database is running and accessible. Run migrations:
   ```bash
   flask db upgrade
   ```

3. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```
   *Note: Ensure you are behind a reverse proxy (Nginx, Caddy, etc.) that handles HTTPS.*

## Tech Stack
- Python Flask
- SQLite (Development) / PostgreSQL (Production ready)
- SQLAlchemy ORM
- Flask-Login, Flask-WTF, Flask-Migrate
- XP.css (Retro UI)
