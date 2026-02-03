import time
import random
from app import create_app, db
from app.models import Material
from config import Config

class BenchmarkConfig(Config):
    TESTING = True
    # Use a file-based SQLite db for benchmark to persist/handle larger data better than in-memory?
    # Or in-memory is fine for 10k records. Let's use in-memory for speed of setup,
    # but strictly speaking file-based might be more "realistic" I/O wise.
    # However, user said SQLite is acceptable. In-memory is the default in my test config above.
    # Let's use a specific file to ensure it doesn't conflict.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///benchmark.db'

def seed_data(n=10000):
    print(f"Seeding {n} materials...")
    materials = []
    for i in range(n):
        # 20% chance of being low stock
        min_stock = random.randint(10, 100)
        if random.random() < 0.2:
            quantity = random.randint(0, min_stock) # Low stock
        else:
            quantity = random.randint(min_stock + 1, min_stock + 100) # Adequate stock

        materials.append(Material(name=f"Mat{i}", quantity=quantity, min_stock=min_stock))

    db.session.bulk_save_objects(materials)
    db.session.commit()
    print("Seeding complete.")

def benchmark():
    app = create_app(BenchmarkConfig)

    # Clean up existing bench db if any
    import os
    if os.path.exists('benchmark.db'):
        os.remove('benchmark.db')

    with app.app_context():
        db.create_all()
        seed_data(10000)

        # Method 1: Python Filtering (Current)
        start_time = time.time()
        # Explicitly fetching all first, then filtering, matching the code:
        # low_stock_items = [m for m in Material.query.all() if m.quantity <= m.min_stock]
        all_materials = Material.query.all()
        low_stock_python = [m for m in all_materials if m.quantity <= m.min_stock]
        end_time = time.time()
        python_time = end_time - start_time
        print(f"Python Filter Time: {python_time:.4f} seconds (Found {len(low_stock_python)} items)")

        # Method 2: SQL Filtering (Proposed)
        start_time = time.time()
        low_stock_sql = Material.query.filter(Material.quantity <= Material.min_stock).all()
        end_time = time.time()
        sql_time = end_time - start_time
        print(f"SQL Filter Time:    {sql_time:.4f} seconds (Found {len(low_stock_sql)} items)")

        # Improvement
        if sql_time < python_time:
            print(f"Improvement: {python_time / sql_time:.2f}x faster")
        else:
            print(f"No improvement (Slower by {sql_time / python_time:.2f}x)")

    # Cleanup
    if os.path.exists('benchmark.db'):
        os.remove('benchmark.db')

if __name__ == "__main__":
    benchmark()
