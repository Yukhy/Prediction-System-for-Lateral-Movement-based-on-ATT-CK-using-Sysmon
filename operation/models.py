from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from settings import Engine, Base, Session

class Tactic(Base):
    __tablename__ = "tactics"
    id = Column(Integer, primary_key=True)
    external_id = Column(String(6), unique=True, nullable=False)
    name = Column(String(255))
    description = Column(Text())

    def __init__(self):
        Tactic.metadata.create_all(bind=Engine)
    
    def num_of_row():
        return Session.query(Tactic).count()
    
    def get_id_by_name(name :str):
        return Session.query(Tactic).filter(Tactic.name == name).first().id

class Technique(Base):
    __tablename__ = "techniques"
    id = Column(Integer, primary_key=True)
    external_id = Column(String(9), unique=True, nullable=False)
    name = Column(String(255))
    description = Column(Text())
    is_subtechnique = Column(Boolean)

    def __init__(self):
        Technique.metadata.create_all(bind=Engine)
    
    def num_of_row():
        return Session.query(Technique).count()

    def get_id_by_name(name :str):
        return Session.query(Technique).filter(Technique.name == name).first().id
    
    def get_id_by_external_id(external_id: str):
        return Session.query(Technique).filter(Technique.external_id == external_id).first().id

class Command(Base):
    __tablename__ = "commands"
    id = Column(Integer, primary_key=True)
    command = Column(Text())
    technique_id = Column(ForeignKey('techniques.id',onupdate='CASCADE', ondelete='CASCADE'))
    
    def __init__(self):
        Command.metadata.create_all(bind=Engine)

    def num_of_row():
        return Session.query(Command).count()

# TacticsとTechniquesの中間テーブル
class Reason(Base):
    __tablename__ = "reasons"
    id = Column(Integer, primary_key=True)
    tactic_id = Column(ForeignKey('tactics.id',onupdate='CASCADE', ondelete='CASCADE'))
    technique_id = Column(ForeignKey('techniques.id',onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self):
        Reason.metadata.create_all(bind=Engine)
    
    def num_of_row():
        return Session.query(Reason).count()