from typing import Dict, List, Optional

from dependency_injector.containers import Container

from . import base


class Service(base.Service, base.ContainerResource):
    def __init__(self, container: Container, name: str):
        super().__init__(container)

        self._name = name
        self._resource_containers: Dict[str, Container] = dict()
        self._resources: Dict[str, base.Resource] = dict()

        if hasattr(container, 'resources'):
            for name, provider in container.resources.providers.items():
                res_container = container.resources(name)
                self._resource_containers[name] = res_container
                self._resources[name] = res_container.instance(res_container)

    @property
    def name(self) -> str:
        return self._name

    @property
    def resources(self) -> List[base.Resource]:
        return list(self._resources.values())

    def get_resource(self, name) -> Optional[base.Resource]:
        return self._resources.get(name)

    def sync_startup(self, application=None, module=None, *args, **kwargs):
        super().sync_startup(application=application, module=module, service=self, *args, **kwargs)

        for r in self.resources:
            r.sync_startup(application=application, module=module, service=self, *args, **kwargs)

    def sync_shutdown(self, application=None, module=None, *args, **kwargs):
        for r in self.resources:
            r.sync_shutdown(application=application, module=module, service=self, *args, **kwargs)

        super().sync_shutdown(application=application, module=module, service=self, *args, **kwargs)

    async def startup(self, application=None, module=None, *args, **kwargs):
        await super().startup(application=application, module=module, service=self, *args, **kwargs)

        for r in self.resources:
            await r.startup(application=application, module=module, service=self, *args, **kwargs)

    async def shutdown(self, application=None, module=None, *args, **kwargs):
        for r in self.resources:
            await r.shutdown(application=application, module=module, service=self, *args, **kwargs)

        await super().shutdown(application=application, module=module, service=self, *args, **kwargs)


class SessionService(Service, base.SessionResource):
    def sync_session_begin(self, application=None, module=None, *args, **kwargs):
        super().sync_session_begin(application=application, module=module, service=self, *args, **kwargs)

        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_begin(application=application, module=module, service=self, *args, **kwargs)

    def sync_session_finish(self, application=None, module=None, *args, **kwargs):
        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_finish(application=application, module=module, service=self, *args, **kwargs)

        super().sync_session_finish(application=application, module=module, service=self, *args, **kwargs)

    async def session_begin(self, application=None, module=None, *args, **kwargs):
        await super().session_begin(application=application, module=module, service=self, *args, **kwargs)

        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_begin(application=application, module=module, service=self, *args, **kwargs)

    async def session_finish(self, application=None, module=None, *args, **kwargs):
        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_finish(application=application, module=module, service=self, *args, **kwargs)

        await super().session_finish(application=application, module=module, service=self, *args, **kwargs)
