from abc import (
    ABC,
    abstractmethod,
)


class Client(ABC):

    @abstractmethod
    def get(self, filter_condition=None):
        pass


class SqlClient(Client):
    def get(self, filter_condition=None):
        if filter_condition:
            pass

        return {'data': 'entity from SQL', 'filter': filter_condition}


class MongoClient(Client):
    def get(self, filter_condition=None):
        if filter_condition:
            pass

        return {'data': 'entity from MongoDB', 'filter': filter_condition}


class BaseRepository:
    def __init__(self, client: Client):
        self._client = client

    def _get(self, filter_condition=None):
        return self._client.get(filter_condition)

    # Other basic CRUD methods


class Entity1Repository(BaseRepository):
    def get(self):
        return self._get()

    def get_active(self):
        active_filter = {'status': 'active'}
        return self._get(filter_condition=active_filter)


class Entity2Repository(BaseRepository):
    def get(self):
        return self._get()

    def get_inactive(self):
        inactive_filter = {'status': 'inactive'}
        return self._get(filter_condition=inactive_filter)


class Service:
    def __init__(self, entity1_repo: Entity1Repository, entity2_repo: Entity2Repository):
        self.entity1_repo = entity1_repo
        self.entity2_repo = entity2_repo

    def logic(self):
        entity1 = self.entity1_repo.get_active()
        entity2 = self.entity2_repo.get()
        return entity1, entity2
