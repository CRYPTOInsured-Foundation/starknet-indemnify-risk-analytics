# from django.db import migrations

# SQL = """
# DO $$
# BEGIN
#   -- === INSPECTION ANALYTICS ===
#   CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_inspection()
#   RETURNS trigger LANGUAGE plpgsql AS $$
#   BEGIN
#     INSERT INTO starknet_indemnify_risk_analytics.inspection_analytics
#       (inspection_id, proposal_id, created_at)
#     VALUES (NEW.id, NEW.proposal_id, NEW.created_at);
#     RETURN NEW;
#   END;
#   $$;

#   DROP TRIGGER IF EXISTS trg_ingest_inspection ON starknet_indemnify_policy_service.inspections;
#   CREATE TRIGGER trg_ingest_inspection
#     AFTER INSERT ON starknet_indemnify_policy_service.inspections
#     FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_inspection();

#   ALTER TABLE starknet_indemnify_risk_analytics.inspection_analytics
#     SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');

#   BEGIN
#     PERFORM add_compression_policy('inspection_analytics', INTERVAL '7 days');
#     PERFORM add_retention_policy('inspection_analytics', INTERVAL '1 year');
#   EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Inspection compression/retention skipped: %', SQLERRM; END;

#   -- Continuous aggregate: daily
#   CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.inspection_analytics_daily
#   WITH (timescaledb.continuous) AS
#   SELECT time_bucket('1 day', created_at) AS day_bucket, AVG(ml_score) AS avg_score
#   FROM starknet_indemnify_risk_analytics.inspection_analytics
#   GROUP BY day_bucket;

#   -- === PROPOSAL ANALYTICS ===
#   CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_proposal()
#   RETURNS trigger LANGUAGE plpgsql AS $$
#   BEGIN
#     INSERT INTO starknet_indemnify_risk_analytics.proposal_analytics
#       (proposal_id, proposer_id, submission_date, premium_payable)
#     VALUES (NEW.id, NEW.proposer_id, NEW.submission_date, NEW.premium_payable);
#     RETURN NEW;
#   END;
#   $$;

#   DROP TRIGGER IF EXISTS trg_ingest_proposal ON starknet_indemnify_policy_service.proposals;
#   CREATE TRIGGER trg_ingest_proposal
#     AFTER INSERT ON starknet_indemnify_policy_service.proposals
#     FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_proposal();

#   ALTER TABLE starknet_indemnify_risk_analytics.proposal_analytics
#     SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');

#   BEGIN
#     PERFORM add_compression_policy('proposal_analytics', INTERVAL '7 days');
#     PERFORM add_retention_policy('proposal_analytics', INTERVAL '1 year');
#   EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Proposal compression/retention skipped: %', SQLERRM; END;

#   CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.proposal_analytics_daily
#   WITH (timescaledb.continuous) AS
#   SELECT time_bucket('1 day', submission_date) AS day_bucket, AVG(premium_payable::numeric) AS avg_premium
#   FROM starknet_indemnify_risk_analytics.proposal_analytics
#   GROUP BY day_bucket;

#   -- === CLAIM ANALYTICS ===
#   CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim()
#   RETURNS trigger LANGUAGE plpgsql AS $$
#   BEGIN
#     INSERT INTO starknet_indemnify_risk_analytics.claim_analytics
#       (claim_id, proposal_id, submission_date, claim_amount, approved_settlement_amount)
#     VALUES (NEW.id, NEW.proposal_id, NEW.submissionDate, NEW.claimAmount, NEW.approvedSettlementAmount);
#     RETURN NEW;
#   END;
#   $$;

#   DROP TRIGGER IF EXISTS trg_ingest_claim ON starknet_indemnify_policy_service.claims;
#   CREATE TRIGGER trg_ingest_claim
#     AFTER INSERT ON starknet_indemnify_policy_service.claims
#     FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim();

#   ALTER TABLE starknet_indemnify_risk_analytics.claim_analytics
#     SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');

#   BEGIN
#     PERFORM add_compression_policy('claim_analytics', INTERVAL '7 days');
#     PERFORM add_retention_policy('claim_analytics', INTERVAL '1 year');
#   EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Claim compression/retention skipped: %', SQLERRM; END;

#   CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_analytics_daily
#   WITH (timescaledb.continuous) AS
#   SELECT time_bucket('1 day', submission_date) AS day_bucket, SUM(claim_amount::numeric) AS total_claims
#   FROM starknet_indemnify_risk_analytics.claim_analytics
#   GROUP BY day_bucket;

#   -- === CLAIM EVIDENCE ANALYTICS ===
#   CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim_evidence()
#   RETURNS trigger LANGUAGE plpgsql AS $$
#   BEGIN
#     INSERT INTO starknet_indemnify_risk_analytics.claim_evidence_analytics
#       (claim_evidence_id, claim_id, submission_date, proof_count)
#     VALUES (NEW.id, NEW.claim_id, NEW.submissionDate, COALESCE(array_length(NEW.proofUrls, 1), 0));
#     RETURN NEW;
#   END;
#   $$;

#   DROP TRIGGER IF EXISTS trg_ingest_claim_evidence ON starknet_indemnify_policy_service.claim_evidences;
#   CREATE TRIGGER trg_ingest_claim_evidence
#     AFTER INSERT ON starknet_indemnify_policy_service.claim_evidences
#     FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim_evidence();

#   ALTER TABLE starknet_indemnify_risk_analytics.claim_evidence_analytics
#     SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');

#   BEGIN
#     PERFORM add_compression_policy('claim_evidence_analytics', INTERVAL '7 days');
#     PERFORM add_retention_policy('claim_evidence_analytics', INTERVAL '1 year');
#   EXCEPTION WHEN OTHERS THEN RAISE NOTICE 'Claim evidence compression/retention skipped: %', SQLERRM; END;

#   CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_evidence_analytics_daily
#   WITH (timescaledb.continuous) AS
#   SELECT time_bucket('1 day', submission_date) AS day_bucket, AVG(proof_count) AS avg_proofs
#   FROM starknet_indemnify_risk_analytics.claim_evidence_analytics
#   GROUP BY day_bucket;

# END$$;
# """

# REVERSE = """
# -- Drops (triggers & functions)
# DROP TRIGGER IF EXISTS trg_ingest_inspection ON starknet_indemnify_policy_service.inspections;
# DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_inspection();

# DROP TRIGGER IF EXISTS trg_ingest_proposal ON starknet_indemnify_policy_service.proposals;
# DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_proposal();

# DROP TRIGGER IF EXISTS trg_ingest_claim ON starknet_indemnify_policy_service.claims;
# DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_claim();

# DROP TRIGGER IF EXISTS trg_ingest_claim_evidence ON starknet_indemnify_policy_service.claim_evidences;
# DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_claim_evidence();
# """

# class Migration(migrations.Migration):
#     initial = True
#     dependencies = []
#     operations = [
#         migrations.RunSQL(SQL, reverse_sql=REVERSE)
#     ]






# from django.db import migrations

# class Migration(migrations.Migration):
#     initial = True
#     dependencies = [ ('risk_engine', '0001_initial')]

#     operations = [
#         # --- INSPECTION ANALYTICS ---
#         migrations.RunSQL(
#             """
#             CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_inspection()
#             RETURNS trigger LANGUAGE plpgsql AS $$
#             BEGIN
#                 INSERT INTO starknet_indemnify_risk_analytics.inspection_analytics
#                     (inspection_id, proposal_id, created_at)
#                 VALUES (NEW.id, NEW.proposal_id, NEW.created_at);
#                 RETURN NEW;
#             END;
#             $$;
#             """
#         ),
#         migrations.RunSQL(
#             "DROP TRIGGER IF EXISTS trg_ingest_inspection ON starknet_indemnify_policy_service.inspections;"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE TRIGGER trg_ingest_inspection
#             AFTER INSERT ON starknet_indemnify_policy_service.inspections
#             FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_inspection();
#             """
#         ),
#         migrations.RunSQL(
#             "ALTER TABLE starknet_indemnify_risk_analytics.inspection_analytics "
#             "SET (timescaledb.compress, timescaledb.compress_orderby = 'created_at DESC');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_compression_policy('inspection_analytics', INTERVAL '7 days');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_retention_policy('inspection_analytics', INTERVAL '1 year');"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.inspection_analytics_daily
#             WITH (timescaledb.continuous) AS
#             SELECT time_bucket('1 day', created_at) AS day_bucket, AVG(ml_score) AS avg_score
#             FROM starknet_indemnify_risk_analytics.inspection_analytics
#             GROUP BY day_bucket;
#             """
#         ),

#         # --- PROPOSAL ANALYTICS ---
#         migrations.RunSQL(
#             """
#             CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_proposal()
#             RETURNS trigger LANGUAGE plpgsql AS $$
#             BEGIN
#                 INSERT INTO starknet_indemnify_risk_analytics.proposal_analytics
#                     (proposal_id, proposer_id, submission_date, premium_payable)
#                 VALUES (NEW.id, NEW.proposer_id, NEW.submission_date, NEW.premium_payable);
#                 RETURN NEW;
#             END;
#             $$;
#             """
#         ),
#         migrations.RunSQL(
#             "DROP TRIGGER IF EXISTS trg_ingest_proposal ON starknet_indemnify_policy_service.proposals;"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE TRIGGER trg_ingest_proposal
#             AFTER INSERT ON starknet_indemnify_policy_service.proposals
#             FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_proposal();
#             """
#         ),
#         migrations.RunSQL(
#             "ALTER TABLE starknet_indemnify_risk_analytics.proposal_analytics "
#             "SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_compression_policy('proposal_analytics', INTERVAL '7 days');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_retention_policy('proposal_analytics', INTERVAL '1 year');"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.proposal_analytics_daily
#             WITH (timescaledb.continuous) AS
#             SELECT time_bucket('1 day', submission_date) AS day_bucket, AVG(premium_payable::numeric) AS avg_premium
#             FROM starknet_indemnify_risk_analytics.proposal_analytics
#             GROUP BY day_bucket;
#             """
#         ),

#         # --- CLAIM ANALYTICS ---
#         migrations.RunSQL(
#             """
#             CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim()
#             RETURNS trigger LANGUAGE plpgsql AS $$
#             BEGIN
#                 INSERT INTO starknet_indemnify_risk_analytics.claim_analytics
#                     (claim_id, proposal_id, submission_date, claim_amount, approved_settlement_amount)
#                 VALUES (NEW.id, NEW.proposal_id, NEW.submissionDate, NEW.claimAmount, NEW.approvedSettlementAmount);
#                 RETURN NEW;
#             END;
#             $$;
#             """
#         ),
#         migrations.RunSQL(
#             "DROP TRIGGER IF EXISTS trg_ingest_claim ON starknet_indemnify_policy_service.claims;"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE TRIGGER trg_ingest_claim
#             AFTER INSERT ON starknet_indemnify_policy_service.claims
#             FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim();
#             """
#         ),
#         migrations.RunSQL(
#             "ALTER TABLE starknet_indemnify_risk_analytics.claim_analytics "
#             "SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_compression_policy('claim_analytics', INTERVAL '7 days');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_retention_policy('claim_analytics', INTERVAL '1 year');"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_analytics_daily
#             WITH (timescaledb.continuous) AS
#             SELECT time_bucket('1 day', submission_date) AS day_bucket, SUM(claim_amount::numeric) AS total_claims
#             FROM starknet_indemnify_risk_analytics.claim_analytics
#             GROUP BY day_bucket;
#             """
#         ),

#         # --- CLAIM EVIDENCE ANALYTICS ---
#         migrations.RunSQL(
#             """
#             CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim_evidence()
#             RETURNS trigger LANGUAGE plpgsql AS $$
#             BEGIN
#                 INSERT INTO starknet_indemnify_risk_analytics.claim_evidence_analytics
#                     (claim_evidence_id, claim_id, submission_date, proof_count)
#                 VALUES (NEW.id, NEW.claim_id, NEW.submissionDate, COALESCE(array_length(NEW.proofUrls, 1), 0));
#                 RETURN NEW;
#             END;
#             $$;
#             """
#         ),
#         migrations.RunSQL(
#             "DROP TRIGGER IF EXISTS trg_ingest_claim_evidence ON starknet_indemnify_policy_service.claim_evidences;"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE TRIGGER trg_ingest_claim_evidence
#             AFTER INSERT ON starknet_indemnify_policy_service.claim_evidences
#             FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim_evidence();
#             """
#         ),
#         migrations.RunSQL(
#             "ALTER TABLE starknet_indemnify_risk_analytics.claim_evidence_analytics "
#             "SET (timescaledb.compress, timescaledb.compress_orderby = 'submission_date DESC');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_compression_policy('claim_evidence_analytics', INTERVAL '7 days');"
#         ),
#         migrations.RunSQL(
#             "SELECT add_retention_policy('claim_evidence_analytics', INTERVAL '1 year');"
#         ),
#         migrations.RunSQL(
#             """
#             CREATE MATERIALIZED VIEW IF NOT EXISTS starknet_indemnify_risk_analytics.claim_evidence_analytics_daily
#             WITH (timescaledb.continuous) AS
#             SELECT time_bucket('1 day', submission_date) AS day_bucket, AVG(proof_count) AS avg_proofs
#             FROM starknet_indemnify_risk_analytics.claim_evidence_analytics
#             GROUP BY day_bucket;
#             """
#         ),
#     ]









from django.db import migrations

SQL = """
-- === INSPECTION ANALYTICS ===
CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_inspection()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO starknet_indemnify_risk_analytics.inspection_analytics
    (id, proposal_id, created_at)
    VALUES (NEW.id, NEW.proposal_id, NEW.created_at);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_ingest_inspection ON starknet_indemnify_policy_service.inspections;
CREATE TRIGGER trg_ingest_inspection
AFTER INSERT ON starknet_indemnify_policy_service.inspections
FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_inspection();

-- === PROPOSAL ANALYTICS ===
CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_proposal()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO starknet_indemnify_risk_analytics.proposal_analytics
    (id, proposal_id, proposer_address, submission_date, premium_payable)
    VALUES (NEW.id, NEW.id, NEW.proposer_address, NEW.submission_date, NEW.premium_payable);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_ingest_proposal ON starknet_indemnify_policy_service.proposals;
CREATE TRIGGER trg_ingest_proposal
AFTER INSERT ON starknet_indemnify_policy_service.proposals
FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_proposal();

-- === CLAIM ANALYTICS ===
CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO starknet_indemnify_risk_analytics.claim_analytics
    (id, claim_id, proposal_id, submission_date, claim_amount, approved_settlement_amount)
    VALUES (NEW.id, NEW.id, NEW.proposal_id, NEW.submissionDate, NEW.claimAmount, NEW.approvedSettlementAmount);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_ingest_claim ON starknet_indemnify_policy_service.claims;
CREATE TRIGGER trg_ingest_claim
AFTER INSERT ON starknet_indemnify_policy_service.claims
FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim();

-- === CLAIM EVIDENCE ANALYTICS ===
CREATE OR REPLACE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim_evidence()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO starknet_indemnify_risk_analytics.claim_evidence_analytics
    (id, claim_id, submission_date, proof_urls)
    VALUES (NEW.id, NEW.claim_id, NEW.submissionDate, NEW.proofUrls);
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_ingest_claim_evidence ON starknet_indemnify_policy_service.claim_evidences;
CREATE TRIGGER trg_ingest_claim_evidence
AFTER INSERT ON starknet_indemnify_policy_service.claim_evidences
FOR EACH ROW EXECUTE FUNCTION starknet_indemnify_risk_analytics.fn_ingest_claim_evidence();
"""

REVERSE = """
DROP TRIGGER IF EXISTS trg_ingest_inspection ON starknet_indemnify_policy_service.inspections;
DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_inspection();

DROP TRIGGER IF EXISTS trg_ingest_proposal ON starknet_indemnify_policy_service.proposals;
DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_proposal();

DROP TRIGGER IF EXISTS trg_ingest_claim ON starknet_indemnify_policy_service.claims;
DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_claim();

DROP TRIGGER IF EXISTS trg_ingest_claim_evidence ON starknet_indemnify_policy_service.claim_evidences;
DROP FUNCTION IF EXISTS starknet_indemnify_risk_analytics.fn_ingest_claim_evidence();
"""

class Migration(migrations.Migration):
    dependencies = [
        ('risk_engine', '0002_convert_to_hypertables'),
    ]
    operations = [
        migrations.RunSQL(SQL, reverse_sql=REVERSE)
    ]
