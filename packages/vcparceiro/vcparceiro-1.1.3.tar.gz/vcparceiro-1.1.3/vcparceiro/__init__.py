import os
import viggocore
import vclocal

from flask_cors import CORS

from viggocore.system import System
# from vclocal.subsystem.sysadmin import ibge_sync
# from vclocal.subsystem.parametrizacao.localidade \
#     import regiao, uf, mesorregiao, microrregiao, municipio

from vcparceiro.subsystem import parceiro
from vcparceiro.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES


system = System('vcparceiro',
                [parceiro.subsystem],
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(viggocore.SystemFlask):

    def __init__(self):
        super().__init__(system, vclocal.system)
        # VCLocal
        #     ibge_sync.subsystem, regiao.subsystem, uf.subsystem,
        #     mesorregiao.subsystem, microrregiao.subsystem,
        #     municipio.subsystem,
        #     # VCParceiro
        #     parceiro.subsystem
        # )

    def configure(self):
        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        vcparceiro_database_uri = os.getenv('VCPARCEIRO_DATABASE_URI', None)
        if vcparceiro_database_uri is None:
            raise Exception('DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for Postgres
            # export VCPARCEIRO_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/vcparceiro
            self.config['SQLALCHEMY_DATABASE_URI'] = vcparceiro_database_uri
