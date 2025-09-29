from django.apps import AppConfig
from django.db import connection
from django.db.models.signals import post_migrate

HYPERTABLES = {
    "proposal_analytics": "created_date",
    "inspection_analytics": "created_at",
    "claim_analytics": "created_date",
    "claim_evidence_analytics": "submission_date",
    "policy_analytics": "created_at",
}


def init_timescale(sender, **kwargs):
    with connection.cursor() as cursor:
        for table_name, time_column in HYPERTABLES.items():
            # Check if table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'starknet_indemnify_risk_analytics' 
                      AND table_name = %s
                );
            """, [table_name])
            exists = cursor.fetchone()[0]

            if exists:
                cursor.execute(f"""
                    SELECT create_hypertable(
                        'starknet_indemnify_risk_analytics.{table_name}', 
                        '{time_column}', 
                        if_not_exists => TRUE
                    );
                """)
                print(f"✅ Timescale hypertable created for '{table_name}' on '{time_column}'")
            else:
                print(f"⚠ Table '{table_name}' does not exist yet. Skipping Timescale init.")


class RiskEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'risk_engine'

    def ready(self):
        # Ensure hypertable creation runs after migrations
        post_migrate.connect(init_timescale, sender=self)

        # # Import any signals for ingestion or ML triggers
        # import risk_analytics.signals  # noqa: F401

