import time
from app import create_app
from app.extensions import db
from app.models import AppSetting
from sqlalchemy import event
from sqlalchemy.engine import Engine

app = create_app('default')

query_count = 0

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    global query_count
    query_count += 1

with app.app_context():
    db.create_all()
    AppSetting.set('electricity_rate', '0.25')
    AppSetting.set('labor_rate', '20.0')
    AppSetting.set('default_margin', '0.30')
    AppSetting.set('consumables_cost', '2.0')

    query_count = 0
    start = time.time()

    for _ in range(100):
        elec_rate = float(AppSetting.get('electricity_rate', 0.25))
        labor_rate = float(AppSetting.get('labor_rate', 20.0))
        margin = float(AppSetting.get('default_margin', 0.30))
        consumables = float(AppSetting.get('consumables_cost', 2.0))

    end = time.time()
    print(f"Queries: {query_count}")
    print(f"Time: {end - start:.4f}s")
