from pymongo import MongoClient

from main.core.model.exceptions.database.DatabaseAccessException import DatabaseAccessException
from main.core.model.exceptions.database.DatabaseConfigurationException import DatabaseConfigurationException
from main.core.service.infrastructure.ConfigurationConstants import MONGO_DB_HOST, MONGO_DB_USER, MONGO_DB_PASS, MONGO_DB_PORT, MONGO_DB_NAME


class MongoAdapter:
    def __init__(self, authenticate=False) -> None:
        self._client = None

        if all(v is not None for v in [MONGO_DB_HOST, MONGO_DB_PORT, MONGO_DB_NAME]):
            self.host = MONGO_DB_HOST
            self.port = int(MONGO_DB_PORT)
            self.db_name = MONGO_DB_NAME
        else:
            raise DatabaseConfigurationException("Necessary database access parameters have not been properly defined.")

        self.authenticate = authenticate
        if authenticate:
            if MONGO_DB_USER is None or MONGO_DB_PASS is None:
                raise DatabaseAccessException("Database credentials not defined, check env. variables MONGO_USER and MONGO_PASS")
            else:
                self.__username = MONGO_DB_USER
                self.__password = MONGO_DB_PASS

    def open_db_connection(self):
        if self._client is None:
            if self.authenticate:
                self._client = MongoClient(host=self.host, port=self.port, username=self.__username, password=self.__password)
            else:
                self._client = MongoClient(host=self.host, port=self.port)

    def close_db_connection(self):
        if self._client is not None:
            self._client.close()
            self._client = None
        else:
            raise DatabaseConfigurationException("Connection cannot be closed as not defined properly")

    def get_collection(self, collection_name):
        return self._client[self.db_name][collection_name]
