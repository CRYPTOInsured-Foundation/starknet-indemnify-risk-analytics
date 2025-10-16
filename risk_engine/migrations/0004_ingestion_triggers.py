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
    (id, proposal_id, proposer_address, premium_payable)
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
    (id, claim_id, proposal_id, claim_amount, approved_settlement_amount)
    VALUES (NEW.id, NEW.id, NEW.proposal_id, NEW.claimAmount, NEW.approvedSettlementAmount);
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
        ('risk_engine', '0003_convert_to_hypertables'),
    ]
    operations = [
        migrations.RunSQL(SQL, reverse_sql=REVERSE)
    ]
