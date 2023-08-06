from typing import Dict, List, Optional

from dependency_injector.containers import Container

from . import base, service


class Module(base.Module, base.ContainerResource):
    def __init__(self, container: Container):
        super().__init__(container)

        self._resource_containers: Dict[str, Container] = dict()
        self._resources: Dict[str, base.Resource] = dict()

        if hasattr(container, 'resources'):
            for name, provider in container.resources.providers.items():
                res_container = container.resources(name)
                self._resource_containers[name] = res_container
                self._resources[name] = res_container.instance(res_container)

        self._service_containers: Dict[str, Container] = dict()
        self._services: Dict[str, service.Service] = dict()

        if hasattr(container, 'services'):
            for name, provider in container.services.providers.items():
                service_container = container.services(name)
                self._service_containers[name] = service_container
                self._services[name] = service_container.instance(service_container, name)

    @property
    def resources(self) -> List[base.Resource]:
        return list(self._resources.values())

    def get_resource(self, name) -> Optional[base.Resource]:
        return self._resources.get(name)

    @property
    def services(self) -> List[base.Service]:
        return list(self._services.values())

    def get_service(self, name) -> Optional[base.Service]:
        return self._services.get(name)

    def sync_startup(self, application=None, *args, **kwargs):
        super().sync_startup(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            r.sync_startup(application=application, module=self, *args, **kwargs)

        for s in self.services:
            s.sync_startup(application=application, module=self, *args, **kwargs)

    def sync_shutdown(self, application=None, *args, **kwargs):
        for s in self.services:
            s.sync_shutdown(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            r.sync_shutdown(application=application, module=self, *args, **kwargs)

        super().sync_shutdown(application=application, module=self, *args, **kwargs)

    async def startup(self, application=None, *args, **kwargs):
        await super().startup(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            await r.startup(application=application, module=self, *args, **kwargs)

        for s in self.services:
            await s.startup(application=application, module=self, *args, **kwargs)

    async def shutdown(self, application=None, *args, **kwargs):
        for s in self.services:
            await s.shutdown(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            await r.shutdown(application=application, module=self, *args, **kwargs)

        await super().shutdown(application=application, module=self, *args, **kwargs)


class SessionModule(Module, base.SessionResource):
    def sync_session_begin(self, application=None, *args, **kwargs):
        super().sync_session_begin(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_begin(application=application, module=self, *args, **kwargs)

        for r in self.services:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_begin(application=application, module=self, *args, **kwargs)

    def sync_session_finish(self, application=None, *args, **kwargs):
        for r in self.services:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_finish(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            r.sync_session_finish(application=application, module=self, *args, **kwargs)

        super().sync_session_finish(application=application, module=self, *args, **kwargs)

    async def session_begin(self, application=None, *args, **kwargs):
        await super().session_begin(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_begin(application=application, module=self, *args, **kwargs)

        for r in self.services:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_begin(application=application, module=self, *args, **kwargs)

    async def session_finish(self, application=None, *args, **kwargs):
        for r in self.services:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_finish(application=application, module=self, *args, **kwargs)

        for r in self.resources:
            if not isinstance(r, base.SessionResource):
                continue
            await r.session_finish(application=application, module=self, *args, **kwargs)

        await super().session_finish(application=application, module=self, *args, **kwargs)
