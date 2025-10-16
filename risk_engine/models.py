from django.db import models


class BaseModel(models.Model):
    """Abstract base model for audit timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProposalAnalytics(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False)
    proposal_id = models.CharField(max_length=66, unique=True)  # maps u256
    proposer_address = models.CharField(max_length=66)
    policy_class = models.CharField(max_length=50)
    subject_matter = models.TextField()
    sum_insured = models.DecimalField(max_digits=78, decimal_places=0)
    premium_payable = models.DecimalField(max_digits=78, decimal_places=0, null=True)
    premium_frequency = models.CharField(max_length=20)
    frequency_factor = models.IntegerField()
    has_kyc = models.BooleanField(default=False)
    risk_score = models.DecimalField(max_digits=78, decimal_places=4, null=True)
    governance_approved = models.BooleanField(default=False)
    risk_analytics_approved = models.BooleanField(default=False)
    proposal_status = models.CharField(max_length=50)
    rejection_reason = models.CharField(max_length=100, null=True, blank=True)
    expiration_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    has_reinsurance = models.BooleanField(default=False)

    class Meta:
        db_table = 'starknet_indemnify_risk_analytics"."proposal_analytics'
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["id", "created_at"], name="proposal_pk_composite")
        ]


class InspectionAnalytics(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False)
    proposal = models.ForeignKey(
        ProposalAnalytics,
        on_delete=models.CASCADE,
        related_name='inspections'
    )
    media_url = models.TextField()  # IPFS/S3 link
    notes = models.TextField(null=True, blank=True)
    analysis_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # ML score
    issue_detected = models.BooleanField(default=False)

    class Meta:
        db_table = 'starknet_indemnify_risk_analytics"."inspection_analytics'
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["id", "created_at"], name="inspection_pk_composite")
        ]


class ClaimAnalytics(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False)
    claim_id = models.CharField(max_length=66, unique=True)
    policy_id = models.CharField(max_length=66)
    proposal_id = models.CharField(max_length=66)
    claimant_address = models.CharField(max_length=66)
    claim_description = models.TextField()
    claim_amount = models.DecimalField(max_digits=78, decimal_places=0)
    approved_settlement_amount = models.DecimalField(max_digits=78, decimal_places=0, default=0)
    policy_class = models.CharField(max_length=50)
    claim_status = models.CharField(max_length=50)
    claim_type = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    risk_analytics_approved = models.BooleanField(default=False)
    governance_approved = models.BooleanField(default=False)
    is_escalated = models.BooleanField(default=False)
    escalation_reason = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'starknet_indemnify_risk_analytics"."claim_analytics'
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["id", "created_at"], name="claim_pk_composite")
        ]


class ClaimEvidenceAnalytics(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False)
    claim = models.ForeignKey(
        ClaimAnalytics,
        on_delete=models.CASCADE,
        related_name='evidence'
    )
    policy_id = models.CharField(max_length=66)
    submission_date = models.BigIntegerField()
    proof_urls = models.JSONField(null=True, blank=True)
    analysis_score = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # ML score
    issue_detected = models.BooleanField(default=False)

    class Meta:
        db_table = 'starknet_indemnify_risk_analytics"."claim_evidence_analytics'
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["id", "submission_date"], name="claim_evidence_pk_composite")
        ]


class PolicyAnalytics(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False)
    policy_id = models.CharField(max_length=66, unique=True)
    proposal_id = models.CharField(max_length=66)
    policyholder_address = models.CharField(max_length=66)
    policy_class = models.CharField(max_length=50)
    subject_matter = models.TextField()
    sum_insured = models.DecimalField(max_digits=78, decimal_places=0)
    premium = models.DecimalField(max_digits=78, decimal_places=0)
    premium_frequency = models.CharField(max_length=20)
    frequency_factor = models.IntegerField()
    start_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    has_claimed = models.BooleanField(default=False)
    aggregate_claim_amount = models.DecimalField(max_digits=78, decimal_places=0, default=0)

    class Meta:
        db_table = 'starknet_indemnify_risk_analytics"."policy_analytics'
        managed = True
        constraints = [
            models.UniqueConstraint(fields=["id", "created_at"], name="policy_pk_composite")
        ]
