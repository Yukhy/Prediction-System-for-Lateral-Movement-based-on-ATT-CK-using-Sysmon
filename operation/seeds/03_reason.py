from sqlalchemy import exc
from settings import Session
from models import Tactic, Technique, Reason
from mitreattack.stix20 import MitreAttackData


mitre_attack_data = MitreAttackData("/resources/enterprise-attack.json")
techniques = mitre_attack_data.get_techniques(remove_revoked_deprecated=True)

for technique in techniques:
    parent_tactics = list()
    for kill_chain_phase in technique.kill_chain_phases:
        parent_tactics.append(kill_chain_phase["phase_name"])

    technique_id = Technique.get_id_by_name(technique.name)
    for tactic in parent_tactics:
        tactic_name = tactic.replace("-", " ") # ex.) "privilege-escalation" -> "privilege escalation"
        record = Reason()
        record.tactic_id = Tactic.get_id_by_name(tactic_name)
        record.technique_id = technique_id
        Session.add(record)
Session.commit()
Session.close()
print("Reason table created.")