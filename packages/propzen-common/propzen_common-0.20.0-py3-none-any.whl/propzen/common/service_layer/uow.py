import abc
from propzen.common.domain import repository


class AbstractUnitOfWork(abc.ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def collect_new_events(self):
        events = []
        for repo in self.get_repos():
            for entity in repo.seen:
                events.extend(entity.events)
                entity.events.clear()

        events.sort(key=lambda evt: evt.timestamp)
        for event in events:
            yield event

    def get_repos(self) -> repository.TrackableRepository:
        return [
            getattr(self, attr) for attr in dir(self)
            if (
                not callable(getattr(self, attr))
                and not attr.startswith('__')
                and isinstance(getattr(self, attr), repository.TrackableRepository))]

    @abc.abstractmethod
    def commit(self):
        ...

    @abc.abstractmethod
    def rollback(self):
        ...

    @abc.abstractmethod
    def close_session(self):
        ...

    @property
    @abc.abstractmethod
    def session(self):
        ...
