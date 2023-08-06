import os
import viggocore
import vclocal

from flask_cors import CORS

from viggocore import System
# from vclocal.subsystem.sysadmin import ibge_sync
# from vclocal.subsystem.parametrizacao.localidade \
#     import regiao, uf, mesorregiao, microrregiao, municipio

from vcorg.subsystem.sysadmin import domain_org
from vcorg.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES


system = System('vcorg',
                [domain_org.subsystem],
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(viggocore.SystemFlask):

    def __init__(self):
        super().__init__(system, vclocal.system)

    def configure(self):
        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        vcorg_database_uri = os.getenv('VCORG_DATABASE_URI', None)
        if vcorg_database_uri is None:
            raise Exception('VCORG_DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for MySQL
            # export VCORG_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/vcorg
            self.config['SQLALCHEMY_DATABASE_URI'] = vcorg_database_uri
