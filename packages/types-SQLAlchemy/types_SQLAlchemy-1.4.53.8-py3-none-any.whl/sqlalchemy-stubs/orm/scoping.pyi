from typing import Any

from ..util import memoized_property

class ScopedSessionMixin:
    def __call__(self, **kw): ...
    def configure(self, **kwargs) -> None: ...

class scoped_session(ScopedSessionMixin):
    session_factory: Any
    registry: Any
    def __init__(self, session_factory, scopefunc: Any | None = ...) -> None: ...
    def remove(self) -> None: ...
    def query_property(self, query_cls: Any | None = ...): ...
    # dynamically proxied from class Session
    bind: Any
    identity_map: Any
    autoflush: Any
    autocommit: bool
    @property
    def dirty(self): ...
    @property
    def deleted(self): ...
    @property
    def new(self): ...
    @property
    def is_active(self): ...
    @property
    def no_autoflush(self) -> None: ...
    @memoized_property
    def info(self): ...
    @classmethod
    def close_all(cls) -> None: ...
    @classmethod
    def identity_key(cls, *args, **kwargs): ...
    @classmethod
    def object_session(cls, instance): ...
    def __contains__(self, instance): ...
    def __iter__(self): ...
    def add(self, instance, _warn: bool = ...) -> None: ...
    def add_all(self, instances) -> None: ...
    def begin(self, subtransactions: bool = ..., nested: bool = ..., _subtrans: bool = ...): ...
    def begin_nested(self): ...
    def close(self) -> None: ...
    def commit(self) -> None: ...
    def connection(
        self, bind_arguments: Any | None = ..., close_with_result: bool = ..., execution_options: Any | None = ..., **kw
    ): ...
    def delete(self, instance) -> None: ...
    def execute(
        self,
        statement,
        params: Any | None = ...,
        execution_options=...,
        bind_arguments: Any | None = ...,
        _parent_execute_state: Any | None = ...,
        _add_event: Any | None = ...,
        **kw,
    ): ...
    def expire(self, instance, attribute_names: Any | None = ...) -> None: ...
    def expire_all(self) -> None: ...
    def expunge(self, instance) -> None: ...
    def expunge_all(self) -> None: ...
    def flush(self, objects: Any | None = ...) -> None: ...
    def get(
        self,
        entity,
        ident,
        options: Any | None = ...,
        populate_existing: bool = ...,
        with_for_update: Any | None = ...,
        identity_token: Any | None = ...,
        execution_options: Any | None = ...,
    ): ...
    def get_bind(
        self,
        mapper: Any | None = ...,
        clause: Any | None = ...,
        bind: Any | None = ...,
        _sa_skip_events: Any | None = ...,
        _sa_skip_for_implicit_returning: bool = ...,
    ): ...
    def is_modified(self, instance, include_collections: bool = ...): ...
    def bulk_save_objects(
        self, objects, return_defaults: bool = ..., update_changed_only: bool = ..., preserve_order: bool = ...
    ): ...
    def bulk_insert_mappings(self, mapper, mappings, return_defaults: bool = ..., render_nulls: bool = ...) -> None: ...
    def bulk_update_mappings(self, mapper, mappings) -> None: ...
    def merge(self, instance, load: bool = ..., options: Any | None = ...): ...
    def query(self, *entities, **kwargs): ...
    def refresh(self, instance, attribute_names: Any | None = ..., with_for_update: Any | None = ...) -> None: ...
    def rollback(self) -> None: ...
    def scalar(self, statement, params: Any | None = ..., execution_options=..., bind_arguments: Any | None = ..., **kw): ...
    def scalars(self, statement, params: Any | None = ..., execution_options=..., bind_arguments: Any | None = ..., **kw): ...

ScopedSession = scoped_session
