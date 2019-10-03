from main.core.model.exceptions.NoSuchTopologyElementException import NoSuchTopologyElementException
from main.core.model.topology.servers.ApplicationServer import ApplicationServer
from main.core.model.topology.servers.DatabaseServer import DatabaseServer


class TopologyBuilder:

    @staticmethod
    def instantiate_topology(elements):
        _topology_elements = {}
        for element in elements:
            if not hasattr(_topology_elements, element):
                _topology_elements[element] = []

            if element == "application-servers":
                for app_server in elements[element]:
                    _app_server = ApplicationServer(app_server['name'])
                    _app_server.attach_cpus(app_server['cpus'])
                    _app_server.attach_disks(app_server['disks'])
                    _topology_elements[element].append(_app_server)
            elif element == 'database-servers':
                for db_server in elements[element]:
                    _db_server = DatabaseServer(db_server['name'])
                    _db_server.attach_disks(db_server['disks'])
                    _topology_elements[element].append(_db_server)
            else:
                raise NoSuchTopologyElementException("Element '%s' is not part of the predefined topology set." % element)

        return _topology_elements
