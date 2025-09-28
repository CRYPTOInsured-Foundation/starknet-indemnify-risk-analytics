# from django.db import migrations

# SQL = """
# DO $$
# BEGIN
#   IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
#     PERFORM create_hypertable('inspection_analytics', 'created_at', if_not_exists => TRUE);
#     PERFORM create_hypertable('proposal_analytics', 'submission_date', if_not_exists => TRUE);
#     PERFORM create_hypertable('claim_analytics', 'submission_date', if_not_exists => TRUE);
#     PERFORM create_hypertable('claim_evidence_analytics', 'submission_date', if_not_exists => TRUE);
#     PERFORM create_hypertable('policy_analytics', 'created_at', if_not_exists => TRUE);
#   END IF;
# END$$;
# """

# class Migration(migrations.Migration):
#     dependencies = [('risk_engine', '0001_initial')]
#     operations = [migrations.RunSQL(SQL)]




# from django.db import migrations

# class Migration(migrations.Migration):
#     dependencies = [
#         ('risk_engine', '0001_initial'),
#     ]

#     operations = [
#         migrations.RunSQL(
#             "CREATE EXTENSION IF NOT EXISTS timescaledb;",
#             reverse_sql="DROP EXTENSION IF EXISTS timescaledb CASCADE;"
#         ),
#         migrations.RunSQL(
#             "SELECT create_hypertable('inspection_analytics', 'created_at', if_not_exists => TRUE);"
#         ),
#         migrations.RunSQL(
#             "SELECT create_hypertable('proposal_analytics', 'submission_date', if_not_exists => TRUE);"
#         ),
#         migrations.RunSQL(
#             "SELECT create_hypertable('claim_analytics', 'submission_date', if_not_exists => TRUE);"
#         ),
#         migrations.RunSQL(
#             "SELECT create_hypertable('claim_evidence_analytics', 'submission_date', if_not_exists => TRUE);"
#         ),
#         migrations.RunSQL(
#             "SELECT create_hypertable('policy_analytics', 'created_at', if_not_exists => TRUE);"
#         ),
#     ]



# from django.db import migrations

# SQL = """
# DO $$
# BEGIN
#     IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
#         PERFORM create_hypertable('starknet_indemnify_risk_analytics.inspection_analytics', 'created_at', if_not_exists => TRUE);
#         PERFORM create_hypertable('starknet_indemnify_risk_analytics.proposal_analytics', 'submission_date', if_not_exists => TRUE);
#         PERFORM create_hypertable('starknet_indemnify_risk_analytics.claim_analytics', 'submission_date', if_not_exists => TRUE);
#         PERFORM create_hypertable('starknet_indemnify_risk_analytics.claim_evidence_analytics', 'submission_date', if_not_exists => TRUE);
#         PERFORM create_hypertable('starknet_indemnify_risk_analytics.policy_analytics', 'created_at', if_not_exists => TRUE);
#     END IF;
# END$$;
# """

# class Migration(migrations.Migration):
#     dependencies = [
#         ('risk_engine', '0001_initial'),
#     ]
#     operations = [
#         migrations.RunSQL(SQL)
#     ]



# from django.db import migrations

# SQL = """
# DO $$
# DECLARE
#     tbl TEXT;
#     time_col TEXT;
#     pk_name TEXT;
# BEGIN
#     -- Define hypertable mapping
#     FOR tbl, time_col IN
#         SELECT unnest(ARRAY[
#             'inspection_analytics',
#             'proposal_analytics',
#             'claim_analytics',
#             'claim_evidence_analytics',
#             'policy_analytics'
#         ]),
#         unnest(ARRAY[
#             'created_at',
#             'submission_date',
#             'submission_date',
#             'submission_date',
#             'created_at'
#         ])
#     LOOP
#         -- Find primary key constraint name
#         SELECT conname
#         INTO pk_name
#         FROM pg_constraint
#         WHERE conrelid = format('starknet_indemnify_risk_analytics.%I', tbl)::regclass
#           AND contype = 'p'
#         LIMIT 1;

#         IF pk_name IS NOT NULL THEN
#             EXECUTE format('ALTER TABLE starknet_indemnify_risk_analytics.%I DROP CONSTRAINT %I', tbl, pk_name);
#             EXECUTE format(
#                 'ALTER TABLE starknet_indemnify_risk_analytics.%I ADD PRIMARY KEY (id, %I)',
#                 tbl, time_col
#             );
#         END IF;

#         -- Convert to hypertable
#         EXECUTE format(
#             'SELECT create_hypertable(''starknet_indemnify_risk_analytics.%I'', %L, if_not_exists => TRUE)',
#             tbl, time_col
#         );
#     END LOOP;
# END$$;
# """

# class Migration(migrations.Migration):
#     dependencies = [
#         ('risk_engine', '0001_initial'),
#     ]

#     operations = [
#         migrations.RunSQL(SQL),
#     ]




# from django.db import migrations

# SQL = """
# DO $$
# BEGIN
#     IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
#         -- First convert parent tables (no FKs pointing at them)
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.proposal_analytics',
#             'submission_date',
#             if_not_exists => TRUE
#         );

#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.claim_analytics',
#             'submission_date',
#             if_not_exists => TRUE
#         );

#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.policy_analytics',
#             'created_at',
#             if_not_exists => TRUE
#         );

#         -- Now convert child tables that depend on parents
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.inspection_analytics',
#             'created_at',
#             if_not_exists => TRUE
#         );

#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.claim_evidence_analytics',
#             'submission_date',
#             if_not_exists => TRUE
#         );
#     END IF;
# END$$;
# """

# class Migration(migrations.Migration):

#     dependencies = [
#         ('risk_engine', '0001_initial'),
#     ]

#     operations = [
#         migrations.RunSQL(SQL)
#     ]






from django.db import migrations

# SQL = """
# DO $$
# BEGIN
#     IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
#         -- Proposal analytics
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.proposal_analytics',
#             'created_at',
#             if_not_exists => TRUE
#         );

#         -- Claim analytics
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.claim_analytics',
#             'created_at',
#             if_not_exists => TRUE
#         );

#         -- Policy analytics
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.policy_analytics',
#             'created_at',
#             if_not_exists => TRUE
#         );

#         -- Inspection analytics (depends on ProposalAnalytics)
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.inspection_analytics',
#             'created_at',
#             if_not_exists => TRUE
#         );

#         -- Claim evidence analytics (depends on ClaimAnalytics)
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.claim_evidence_analytics',
#             'created_at',
#             if_not_exists => TRUE
#         );
#     END IF;
# END$$;
# """


# SQL = """
# DO $$
# BEGIN
#     IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.proposal_analytics',
#             'created_at',
#             if_not_exists => TRUE,
#             create_default_indexes => FALSE
#         );

#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.claim_analytics',
#             'created_at',
#             if_not_exists => TRUE,
#             create_default_indexes => FALSE
#         );

#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.policy_analytics',
#             'created_at',
#             if_not_exists => TRUE,
#             create_default_indexes => FALSE
#         );

#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.inspection_analytics',
#             'created_at',
#             if_not_exists => TRUE,
#             create_default_indexes => FALSE
#         );

#         PERFORM create_hypertable(
#             'starknet_indemnify_risk_analytics.claim_evidence_analytics',
#             'created_at',
#             if_not_exists => TRUE,
#             create_default_indexes => FALSE
#         );
#     END IF;
# END$$;
# """

# class Migration(migrations.Migration):

#     dependencies = [
#         ('risk_engine', '0001_initial'),
#     ]

#     operations = [
#         migrations.RunSQL(SQL)
#     ]




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
