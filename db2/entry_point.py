from stix_shifter_utils.utils.entry_point_base import EntryPointBase
from .stix_transmission.db2_ping_connector import DB2PingConnector
from stix_shifter_utils.modules.base.stix_transmission.base_sync_connector import BaseSyncConnector
from .stix_transmission.synchronous_dummy_delete_connector import SynchronousDummyDeleteConnector
from .stix_transmission.db2_results_connector import DB2ResultsConnector
from .stix_transmission.db2_api_client import DB2Client
from .stix_transmission.db2_query_connection import DB2QueryConnector
from .stix_translation.data_mapper import DataMapper
from .stix_translation.query_translator import QueryTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import JSONToStix
import os

class EntryPoint(EntryPointBase):

    # python main.py translate synchronous_dummy query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate synchronous_dummy:dialect1 query '{}' "[ipv4-addr:value = '127.0.0.1']"
    # python main.py translate synchronous_dummy:dialect2 query '{}' "[ipv4-addr:value = '127.0.0.1']"

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(options)
        self.set_async(False)
        if connection:
            api_client = DB2Client(connection, configuration)
            base_sync_connector = BaseSyncConnector()
            ping_connector = DB2PingConnector(api_client)
            query_connector = DB2QueryConnector(api_client)
            status_connector = base_sync_connector
            results_connector = DB2ResultsConnector(api_client)
            delete_connector = SynchronousDummyDeleteConnector(api_client)

            self.set_results_connector(results_connector)
            self.set_status_connector(status_connector)
            self.set_delete_connector(delete_connector)
            self.set_query_connector(query_connector)
            self.set_ping_connector(ping_connector)
        else:

            self.setup_translation_simple('default')      #   <-------------
            # all the lines below can be replaced with one line configuration |

            # query_translator = QueryTranslator()
            # basepath = os.path.dirname(__file__)
            # filepath = os.path.abspath(
            #     os.path.join(basepath, "stix_translation", "json", "to_stix_map.json"))
            # results_translator = JSONToStix(filepath)
            #
            # dialect = 'dialect1'
            # data_mapper = DataMapper(options, dialect=dialect)
            # self.add_dialect(dialect, data_mapper=data_mapper, query_translator=query_translator, results_translator=results_translator, default=True)
            #
            # dialect = 'dialect2'
            # data_mapper = DataMapper(options, dialect=dialect)
            # self.add_dialect(dialect, data_mapper=data_mapper, query_translator=query_translator, results_translator=results_translator, default=False)
