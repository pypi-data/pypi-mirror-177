from sqlalchemy import orm, ForeignKeyConstraint

from viggocore.database import db
from viggocore.common.subsystem import entity


class DomainOrg(entity.Entity, db.Model):

    attributes = ['cnpj', 'insc_est', 'razao_social', 'nome_fantasia']
    attributes += entity.Entity.attributes

    domain = orm.relationship(
        'Domain', backref=orm.backref('domain_org_domain'))
    cnpj = db.Column(db.String(14), nullable=False)
    insc_est = db.Column(db.String(14), nullable=True)
    razao_social = db.Column(db.String(100), nullable=False)
    nome_fantasia = db.Column(db.String(100), nullable=False)

    __table_args__ = (ForeignKeyConstraint(['id'], ['domain.id']),)

    def __init__(self, id, cnpj, razao_social, nome_fantasia, insc_est=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.nome_fantasia = nome_fantasia
        self.insc_est = insc_est

    @classmethod
    def individual(cls):
        return 'domain_org'
