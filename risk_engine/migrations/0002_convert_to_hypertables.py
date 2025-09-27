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



from django.db import migrations

SQL = """
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'timescaledb') THEN
        PERFORM create_hypertable('starknet_indemnify_risk_analytics.inspection_analytics', 'created_at', if_not_exists => TRUE);
        PERFORM create_hypertable('starknet_indemnify_risk_analytics.proposal_analytics', 'submission_date', if_not_exists => TRUE);
        PERFORM create_hypertable('starknet_indemnify_risk_analytics.claim_analytics', 'submission_date', if_not_exists => TRUE);
        PERFORM create_hypertable('starknet_indemnify_risk_analytics.claim_evidence_analytics', 'submission_date', if_not_exists => TRUE);
        PERFORM create_hypertable('starknet_indemnify_risk_analytics.policy_analytics', 'created_at', if_not_exists => TRUE);
    END IF;
END$$;
"""

class Migration(migrations.Migration):
    dependencies = [
        ('risk_engine', '0001_initial'),
    ]
    operations = [
        migrations.RunSQL(SQL)
    ]
