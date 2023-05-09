from mitreattack.stix20 import MitreAttackData
from settings import Session
from models import Technique
from sqlalchemy import exc


mitre_attack_data = MitreAttackData("/resources/enterprise-attack.json")
techniques = mitre_attack_data.get_techniques(remove_revoked_deprecated=True)

for row in techniques:
    record = Technique()
    record.external_id = row.external_references[0].external_id
    if "." in record.external_id:
        record.is_subtechnique = True
    else:
        record.is_subtechnique = False
    record.name = row.name
    record.description = row.description
    Session.add(record)
Session.commit()
Session.close()
print("Technique table created.")