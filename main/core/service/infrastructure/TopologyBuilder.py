from main.core.model.exceptions.request.NoSuchElementException import NoSuchElementException
from main.core.model.topology.servers.ApplicationServer import ApplicationServer
from main.core.model.topology.servers.DatabaseServer import DatabaseServer

APP_SERVERS = "application-servers"
DB_SERVERS = "database-servers"


class TopologyBuilder:

    @staticmethod
    def instantiate_topology(elements, sim_env):
        _topology_elements = {}
        for element in elements:
            if not hasattr(_topology_elements, element):
                _topology_elements[element] = []

            if element == APP_SERVERS:
                for app_server in elements[element]:
                    _app_server = ApplicationServer(app_server['name'], sim_env)
                    _app_server.attach_cpus(app_server['cpus'])
                    _app_server.attach_disks(app_server['disks'])
                    _topology_elements[element].append(_app_server)
            elif element == DB_SERVERS:
                for db_server in elements[element]:
                    _db_server = DatabaseServer(db_server['name'], sim_env)
                    _db_server.attach_disks(db_server['disks'])
                    _topology_elements[element].append(_db_server)
            else:
                raise NoSuchElementException("Element '%s' is not part of the predefined topology set." % element)

        return _topology_elements
