import os
import viggocore

from viggocore.system import System
from flask_cors import CORS
from vclocal.subsystem.common import endereco
from vclocal.subsystem.sysadmin import ibge_sync
from vclocal.subsystem.parametrizacao.localidade \
    import regiao, uf, mesorregiao, microrregiao, municipio
from vclocal.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES


system = System('vclocal',
                [endereco.subsystem, ibge_sync.subsystem, regiao.subsystem,
                 mesorregiao.subsystem, uf.subsystem, microrregiao.subsystem,
                 municipio.subsystem],
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(viggocore.SystemFlask):

    def __init__(self):
        super().__init__(system)

    def configure(self):
        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        vclocal_database_uri = os.getenv('VCLOCAL_DATABASE_URI', None)
        if vclocal_database_uri is None:
            raise Exception('VCLOCAL_DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for Postgres
            # export VCLOCAL_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/vclocal
            self.config['SQLALCHEMY_DATABASE_URI'] = vclocal_database_uri
