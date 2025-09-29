from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('risk_engine', '0004_ingestion_triggers'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            -- Convert main tables to hypertables (safe positional args)
            SELECT create_hypertable('starknet_indemnify_risk_analytics.inspection_analytics'::regclass, 'created_at', NULL, NULL, NULL, TRUE, TRUE);
            SELECT create_hypertable('starknet_indemnify_risk_analytics.proposal_analytics'::regclass, 'created_at', NULL, NULL, NULL, TRUE, TRUE);
            SELECT create_hypertable('starknet_indemnify_risk_analytics.claim_analytics'::regclass, 'created_at', NULL, NULL, NULL, TRUE, TRUE);
            SELECT create_hypertable('starknet_indemnify_risk_analytics.claim_evidence_analytics'::regclass, 'created_at', NULL, NULL, NULL, TRUE, TRUE);

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
