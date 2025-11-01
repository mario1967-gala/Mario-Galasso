#!/usr/bin/env python3
"""Verifica schema database"""
import sys
sys.path.insert(0, '/home/user/Mario-Galasso')

from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    columns = inspector.get_columns('domande_verifica')

    print("📊 SCHEMA TABELLA domande_verifica:")
    print("="*60)
    for col in columns:
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        default = f" DEFAULT {col['default']}" if col['default'] else ""
        print(f"  {col['name']:<20} {str(col['type']):<15} {nullable}{default}")

    print("\n✅ Nuove colonne Rubrica Ministeriale:")
    for col in columns:
        if col['name'] in ['livello', 'tempo_stimato', 'distrattori']:
            print(f"  ✓ {col['name']}: {col['type']}")
