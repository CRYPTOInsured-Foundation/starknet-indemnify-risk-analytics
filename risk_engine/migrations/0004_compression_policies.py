# from django.db import migrations

# class Migration(migrations.Migration):

#     dependencies = [
#         ('risk_engine', '0002_convert_to_hypertables'),
#         ('risk_engine', '0003_ingestion_triggers'),
#     ]

#     operations = [
#         # Usually empty unless you manually add something
#     ]






# from django.db import migrations

# SQL = """
# DO $$
# BEGIN
#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.inspection_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');
#         PERFORM add_compression_policy('inspection_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('inspection_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Inspection compression/retention skipped: %', SQLERRM; END;

#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.proposal_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');
#         PERFORM add_compression_policy('proposal_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('proposal_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Proposal compression/retention skipped: %', SQLERRM; END;

#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.claim_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');
#         PERFORM add_compression_policy('claim_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('claim_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Claim compression/retention skipped: %', SQLERRM; END;

#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.claim_evidence_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');
#         PERFORM add_compression_policy('claim_evidence_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('claim_evidence_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Claim evidence compression/retention skipped: %', SQLERRM; END;

#     -- Continuous aggregates
#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.inspection_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', created_at) AS day_bucket, AVG(analysis_score) AS avg_score
#     FROM starknet_indemnify_risk_analytics.inspection_analytics
#     GROUP BY day_bucket;

#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.proposal_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', submission_date) AS day_bucket, AVG(premium_payable::numeric) AS avg_premium
#     FROM starknet_indemnify_risk_analytics.proposal_analytics
#     GROUP BY day_bucket;

#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', submission_date) AS day_bucket, SUM(claim_amount::numeric) AS total_claims
#     FROM starknet_indemnify_risk_analytics.claim_analytics
#     GROUP BY day_bucket;

#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_evidence_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', submission_date) AS day_bucket, AVG(array_length(proof_urls,1)) AS avg_proofs
#     FROM starknet_indemnify_risk_analytics.claim_evidence_analytics
#     GROUP BY day_bucket;

# END$$;
# """

# class Migration(migrations.Migration):
#     dependencies = [
#         ('risk_engine', '0003_ingestion_triggers'),
#     ]
#     operations = [
#         migrations.RunSQL(SQL)
#     ]






# from django.db import migrations

# SQL = """
# DO $$
# BEGIN
#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.inspection_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');
#         PERFORM add_compression_policy('inspection_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('inspection_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Inspection compression/retention skipped: %', SQLERRM; END;

#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.proposal_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');
#         PERFORM add_compression_policy('proposal_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('proposal_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Proposal compression/retention skipped: %', SQLERRM; END;

#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.claim_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');
#         PERFORM add_compression_policy('claim_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('claim_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Claim compression/retention skipped: %', SQLERRM; END;

#     BEGIN
#         ALTER TABLE starknet_indemnify_risk_analytics.claim_evidence_analytics
#             SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');
#         PERFORM add_compression_policy('claim_evidence_analytics', INTERVAL '7 days');
#         PERFORM add_retention_policy('claim_evidence_analytics', INTERVAL '1 year');
#     EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Claim evidence compression/retention skipped: %', SQLERRM; END;

#     -- Continuous aggregates
#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.inspection_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', created_at::timestamp) AS day_bucket, AVG(analysis_score) AS avg_score
#     FROM starknet_indemnify_risk_analytics.inspection_analytics
#     GROUP BY day_bucket;

#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.proposal_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', submission_date::timestamp) AS day_bucket, AVG(premium_payable::numeric) AS avg_premium
#     FROM starknet_indemnify_risk_analytics.proposal_analytics
#     GROUP BY day_bucket;

#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', submission_date::timestamp) AS day_bucket, SUM(claim_amount::numeric) AS total_claims
#     FROM starknet_indemnify_risk_analytics.claim_analytics
#     GROUP BY day_bucket;

#     CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_evidence_analytics_daily
#     WITH (timescaledb.continuous) AS
#     SELECT time_bucket('1 day', submission_date::timestamp) AS day_bucket, AVG(array_length(proof_urls,1)) AS avg_proofs
#     FROM starknet_indemnify_risk_analytics.claim_evidence_analytics
#     GROUP BY day_bucket;

# END$$;
# """

# class Migration(migrations.Migration):
#     dependencies = [
#         ('risk_engine', '0003_ingestion_triggers'),
#     ]
#     operations = [
#         migrations.RunSQL(SQL)
#     ]






# Generated by Django 5.2.3 on 2025-09-27 20:00

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('risk_engine', '0003_ingestion_triggers'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            -- Convert main tables to hypertables
            SELECT create_hypertable('starknet_indemnify_risk_analytics.inspection_analytics', 'created_at', if_not_exists => TRUE);
            SELECT create_hypertable('starknet_indemnify_risk_analytics.proposal_analytics', 'created_at', if_not_exists => TRUE);
            SELECT create_hypertable('starknet_indemnify_risk_analytics.claim_analytics', 'created_at', if_not_exists => TRUE);
            SELECT create_hypertable('starknet_indemnify_risk_analytics.claim_evidence_analytics', 'created_at', if_not_exists => TRUE);

            -- Apply compression policies
            ALTER TABLE starknet_indemnify_risk_analytics.inspection_analytics SET (timescaledb.compress, timescaledb.compress_segmentby='id');
            SELECT add_compression_policy('starknet_indemnify_risk_analytics.inspection_analytics', INTERVAL '30 days');

            ALTER TABLE starknet_indemnify_risk_analytics.proposal_analytics SET (timescaledb.compress, timescaledb.compress_segmentby='id');
            SELECT add_compression_policy('starknet_indemnify_risk_analytics.proposal_analytics', INTERVAL '30 days');

            ALTER TABLE starknet_indemnify_risk_analytics.claim_analytics SET (timescaledb.compress, timescaledb.compress_segmentby='id');
            SELECT add_compression_policy('starknet_indemnify_risk_analytics.claim_analytics', INTERVAL '30 days');

            ALTER TABLE starknet_indemnify_risk_analytics.claim_evidence_analytics SET (timescaledb.compress, timescaledb.compress_segmentby='id');
            SELECT add_compression_policy('starknet_indemnify_risk_analytics.claim_evidence_analytics', INTERVAL '30 days');

            -- Continuous aggregates: daily summaries
            CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.inspection_analytics_daily
            WITH (timescaledb.continuous) AS
            SELECT time_bucket('1 day', created_at::timestamptz) AS day_bucket,
                   AVG(analysis_score) AS avg_score
            FROM starknet_indemnify_risk_analytics.inspection_analytics
            GROUP BY day_bucket;

            CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.proposal_analytics_daily
            WITH (timescaledb.continuous) AS
            SELECT time_bucket('1 day', created_at::timestamptz) AS day_bucket,
                   AVG(premium_payable::numeric) AS avg_premium
            FROM starknet_indemnify_risk_analytics.proposal_analytics
            GROUP BY day_bucket;

            CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_analytics_daily
            WITH (timescaledb.continuous) AS
            SELECT time_bucket('1 day', created_at::timestamptz) AS day_bucket,
                   SUM(claim_amount::numeric) AS total_claims
            FROM starknet_indemnify_risk_analytics.claim_analytics
            GROUP BY day_bucket;

            CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_evidence_analytics_daily
            WITH (timescaledb.continuous) AS
            SELECT time_bucket('1 day', created_at::timestamptz) AS day_bucket,
                   AVG(array_length(proof_urls,1)) AS avg_proofs
            FROM starknet_indemnify_risk_analytics.claim_evidence_analytics
            GROUP BY day_bucket;
            """,
            reverse_sql="""
            DROP MATERIALIZED VIEW IF EXISTS starknet_indemnify_risk_analytics.inspection_analytics_daily;
            DROP MATERIALIZED VIEW IF EXISTS starknet_indemnify_risk_analytics.proposal_analytics_daily;
            DROP MATERIALIZED VIEW IF EXISTS starknet_indemnify_risk_analytics.claim_analytics_daily;
            DROP MATERIALIZED VIEW IF EXISTS starknet_indemnify_risk_analytics.claim_evidence_analytics_daily;
            """
        ),
    ]
