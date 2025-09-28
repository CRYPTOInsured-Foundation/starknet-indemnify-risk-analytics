from django.db import migrations

SQL = """
-- Enable Timescale extension if missing and create schema.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
    CREATE EXTENSION IF NOT EXISTS timescaledb;
  END IF;
END$$;

-- Ensure schema for analytics exists
CREATE SCHEMA IF NOT EXISTS starknet_indemnify_risk_analytics AUTHORIZATION CURRENT_USER;
"""

REVERSE = """
-- Drop schema (keep extension to avoid breaking other apps)
DROP SCHEMA IF EXISTS starknet_indemnify_risk_analytics CASCADE;
"""

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(SQL, reverse_sql=REVERSE)
    ]
