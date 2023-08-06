"""Integration between SQLAlchemy and Kyuubi.

Some code based on
https://github.com/zzzeek/sqlalchemy/blob/rel_0_5/lib/sqlalchemy/databases/sqlite.py
which is released under the MIT license.
"""

from pyhive.sqlalchemy_hive import HiveDialect
from pyhive import hive

'''
    "set:hiveconf:kyuubi.engine.share.level":"USER",
    "set:hiveconf:kyuubi.session.cluster": "apollorno",
    "set:hivevar:spark.yarn.queue": "mmd-anomaly-detection-high-mem",
    "kyuubi.proxy.batchAccount":"b_dss_mmd",
    "use:database": "P_cm_cps_T"
'''


class KyuubiDialect(HiveDialect):
    name = b'kyuubi'

    @classmethod
    def dbapi(cls):
        return hive

    def create_connect_args(self, url):
        kwargs = {
            'host': url.host,
            'port': url.port or 10000,
            'username': url.username,
            'password': url.password,
            'database': url.database or 'default',
            'configuration': {
                "set:hiveconf:kyuubi.engine.share.level": "USER",
                "set:hiveconf:kyuubi.session.cluster": "apollorno",
                "set:hivevar:spark.yarn.queue": "mmd-anomaly-detection-high-mem",
                "kyuubi.proxy.batchAccount": "b_dss_mmd",
                "use:database": "P_cm_cps_T"
            }
        }
        kwargs.update(url.query)
        return [], kwargs
