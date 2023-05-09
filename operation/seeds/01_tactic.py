from mitreattack.stix20 import MitreAttackData
from settings import Session
from models import Tactic
from sqlalchemy import exc

mitre_attack_data = MitreAttackData("/resources/enterprise-attack.json")
tactics = mitre_attack_data.get_tactics(remove_revoked_deprecated=True)

for row in tactics:
    record = Tactic()
    record.external_id = row.external_references[0].external_id
    record.name = row.name
    record.description = row.description
    Session.add(record)
Session.commit()
Session.close()
print("Tactic table created.")