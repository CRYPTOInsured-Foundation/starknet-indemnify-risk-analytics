from django.db import migrations

SQL = """
SET search_path TO starknet_indemnify_risk_analytics, public;

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN

    -- Create hypertables (idempotent, safe)
    PERFORM create_hypertable('proposal_analytics', 'created_at', if_not_exists => TRUE, migrate_data => TRUE);
    PERFORM create_hypertable('claim_analytics', 'created_at', if_not_exists => TRUE, migrate_data => TRUE);
    PERFORM create_hypertable('policy_analytics', 'created_at', if_not_exists => TRUE, migrate_data => TRUE);
    PERFORM create_hypertable('inspection_analytics', 'created_at', if_not_exists => TRUE, migrate_data => TRUE);
    PERFORM create_hypertable('claim_evidence_analytics', 'created_at', if_not_exists => TRUE, migrate_data => TRUE);

    -- Optionally set chunk interval (adjust based on ingestion rate)
    BEGIN
      PERFORM set_chunk_time_interval('proposal_analytics', INTERVAL '1 day');
      PERFORM set_chunk_time_interval('claim_analytics', INTERVAL '1 day');
      PERFORM set_chunk_time_interval('policy_analytics', INTERVAL '1 day');
      PERFORM set_chunk_time_interval('inspection_analytics', INTERVAL '1 day');
      PERFORM set_chunk_time_interval('claim_evidence_analytics', INTERVAL '1 day');
    EXCEPTION WHEN undefined_function THEN 
      RAISE NOTICE 'set_chunk_time_interval skipped: %', SQLERRM; 
    END;

    -- Optionally enable compression for older data
    BEGIN
      ALTER TABLE proposal_analytics SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');
      PERFORM add_compression_policy('proposal_analytics', INTERVAL '7 days');
    EXCEPTION WHEN OTHERS THEN 
      RAISE NOTICE 'proposal_analytics compression skipped: %', SQLERRM; 
    END;

    BEGIN
      ALTER TABLE claim_analytics SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');
      PERFORM add_compression_policy('claim_analytics', INTERVAL '7 days');
    EXCEPTION WHEN OTHERS THEN 
      RAISE NOTICE 'claim_analytics compression skipped: %', SQLERRM; 
    END;

    BEGIN
      ALTER TABLE policy_analytics SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');
      PERFORM add_compression_policy('policy_analytics', INTERVAL '7 days');
    EXCEPTION WHEN OTHERS THEN 
      RAISE NOTICE 'policy_analytics compression skipped: %', SQLERRM; 
    END;

    BEGIN
      ALTER TABLE inspection_analytics SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');
      PERFORM add_compression_policy('inspection_analytics', INTERVAL '7 days');
    EXCEPTION WHEN OTHERS THEN 
      RAISE NOTICE 'inspection_analytics compression skipped: %', SQLERRM; 
    END;

    BEGIN
      ALTER TABLE claim_evidence_analytics SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');
      PERFORM add_compression_policy('claim_evidence_analytics', INTERVAL '7 days');
    EXCEPTION WHEN OTHERS THEN 
      RAISE NOTICE 'claim_evidence_analytics compression skipped: %', SQLERRM; 
    END;

  ELSE
    RAISE NOTICE 'TimescaleDB extension not found; hypertable & policy creation skipped.';
  END IF;
END$$;
"""

REVERSE = """
-- reverse intentionally left blank to avoid accidental data loss
"""

class Migration(migrations.Migration):
    dependencies = [
        ('risk_engine', '0002_initial'),
    ]
    operations = [migrations.RunSQL(SQL, reverse_sql=REVERSE)]
