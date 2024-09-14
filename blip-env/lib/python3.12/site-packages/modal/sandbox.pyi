import google.protobuf.message
import modal.app
import modal.client
import modal.cloud_bucket_mount
import modal.gpu
import modal.image
import modal.io_streams
import modal.mount
import modal.network_file_system
import modal.object
import modal.scheduler_placement
import modal.secret
import modal.volume
import modal_proto.api_pb2
import os
import typing
import typing_extensions

class _Sandbox(modal.object._Object):
    _result: typing.Optional[modal_proto.api_pb2.GenericResult]
    _stdout: modal.io_streams._StreamReader
    _stderr: modal.io_streams._StreamReader
    _stdin: modal.io_streams._StreamWriter
    _task_id: typing.Optional[str]
    _tunnels: typing.Optional[typing.List[modal_proto.api_pb2.TunnelData]]

    @staticmethod
    def _new(
        entrypoint_args: typing.Sequence[str],
        image: modal.image._Image,
        mounts: typing.Sequence[modal.mount._Mount],
        secrets: typing.Sequence[modal.secret._Secret],
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem
        ] = {},
        block_network: bool = False,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: typing.Sequence[int] = [],
        unencrypted_ports: typing.Sequence[int] = [],
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> _Sandbox: ...
    @staticmethod
    async def create(
        *entrypoint_args: str,
        app: typing.Optional[modal.app._App] = None,
        environment_name: typing.Optional[str] = None,
        image: typing.Optional[modal.image._Image] = None,
        mounts: typing.Sequence[modal.mount._Mount] = (),
        secrets: typing.Sequence[modal.secret._Secret] = (),
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem
        ] = {},
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        block_network: bool = False,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike],
            typing.Union[modal.volume._Volume, modal.cloud_bucket_mount._CloudBucketMount],
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: typing.Sequence[int] = [],
        unencrypted_ports: typing.Sequence[int] = [],
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        client: typing.Optional[modal.client._Client] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> _Sandbox: ...
    def _hydrate_metadata(self, handle_metadata: typing.Optional[google.protobuf.message.Message]): ...
    @staticmethod
    async def from_id(sandbox_id: str, client: typing.Optional[modal.client._Client] = None) -> _Sandbox: ...
    async def wait(self, raise_on_termination: bool = True): ...
    async def tunnels(self, timeout: int = 50) -> typing.List[modal_proto.api_pb2.TunnelData]: ...
    async def terminate(self): ...
    async def poll(self) -> typing.Optional[int]: ...
    async def _get_task_id(self): ...
    async def exec(self, *cmds: str, pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None): ...
    @property
    def stdout(self) -> modal.io_streams._StreamReader: ...
    @property
    def stderr(self) -> modal.io_streams._StreamReader: ...
    @property
    def stdin(self) -> modal.io_streams._StreamWriter: ...
    @property
    def returncode(self) -> typing.Optional[int]: ...
    @staticmethod
    def list(
        *, app_id: typing.Optional[str] = None, client: typing.Optional[modal.client._Client] = None
    ) -> typing.AsyncGenerator[_Sandbox, None]: ...

class Sandbox(modal.object.Object):
    _result: typing.Optional[modal_proto.api_pb2.GenericResult]
    _stdout: modal.io_streams.StreamReader
    _stderr: modal.io_streams.StreamReader
    _stdin: modal.io_streams.StreamWriter
    _task_id: typing.Optional[str]
    _tunnels: typing.Optional[typing.List[modal_proto.api_pb2.TunnelData]]

    def __init__(self, *args, **kwargs): ...
    @staticmethod
    def _new(
        entrypoint_args: typing.Sequence[str],
        image: modal.image.Image,
        mounts: typing.Sequence[modal.mount.Mount],
        secrets: typing.Sequence[modal.secret.Secret],
        timeout: typing.Optional[int] = None,
        workdir: typing.Optional[str] = None,
        gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
        cloud: typing.Optional[str] = None,
        region: typing.Union[str, typing.Sequence[str], None] = None,
        cpu: typing.Optional[float] = None,
        memory: typing.Union[int, typing.Tuple[int, int], None] = None,
        network_file_systems: typing.Dict[
            typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
        ] = {},
        block_network: bool = False,
        volumes: typing.Dict[
            typing.Union[str, os.PathLike], typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount]
        ] = {},
        pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
        encrypted_ports: typing.Sequence[int] = [],
        unencrypted_ports: typing.Sequence[int] = [],
        _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
        _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
    ) -> Sandbox: ...

    class __create_spec(typing_extensions.Protocol):
        def __call__(
            self,
            *entrypoint_args: str,
            app: typing.Optional[modal.app.App] = None,
            environment_name: typing.Optional[str] = None,
            image: typing.Optional[modal.image.Image] = None,
            mounts: typing.Sequence[modal.mount.Mount] = (),
            secrets: typing.Sequence[modal.secret.Secret] = (),
            network_file_systems: typing.Dict[
                typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem
            ] = {},
            timeout: typing.Optional[int] = None,
            workdir: typing.Optional[str] = None,
            gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None,
            cloud: typing.Optional[str] = None,
            region: typing.Union[str, typing.Sequence[str], None] = None,
            cpu: typing.Optional[float] = None,
            memory: typing.Union[int, typing.Tuple[int, int], None] = None,
            block_network: bool = False,
            volumes: typing.Dict[
                typing.Union[str, os.PathLike],
                typing.Union[modal.volume.Volume, modal.cloud_bucket_mount.CloudBucketMount],
            ] = {},
            pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None,
            encrypted_ports: typing.Sequence[int] = [],
            unencrypted_ports: typing.Sequence[int] = [],
            _experimental_scheduler_placement: typing.Optional[modal.scheduler_placement.SchedulerPlacement] = None,
            client: typing.Optional[modal.client.Client] = None,
            _experimental_gpus: typing.Sequence[typing.Union[None, bool, str, modal.gpu._GPUConfig]] = [],
        ) -> Sandbox: ...
        async def aio(self, *args, **kwargs) -> Sandbox: ...

    create: __create_spec

    def _hydrate_metadata(self, handle_metadata: typing.Optional[google.protobuf.message.Message]): ...

    class __from_id_spec(typing_extensions.Protocol):
        def __call__(self, sandbox_id: str, client: typing.Optional[modal.client.Client] = None) -> Sandbox: ...
        async def aio(self, *args, **kwargs) -> Sandbox: ...

    from_id: __from_id_spec

    class __wait_spec(typing_extensions.Protocol):
        def __call__(self, raise_on_termination: bool = True): ...
        async def aio(self, *args, **kwargs): ...

    wait: __wait_spec

    class __tunnels_spec(typing_extensions.Protocol):
        def __call__(self, timeout: int = 50) -> typing.List[modal_proto.api_pb2.TunnelData]: ...
        async def aio(self, *args, **kwargs) -> typing.List[modal_proto.api_pb2.TunnelData]: ...

    tunnels: __tunnels_spec

    class __terminate_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    terminate: __terminate_spec

    class __poll_spec(typing_extensions.Protocol):
        def __call__(self) -> typing.Optional[int]: ...
        async def aio(self, *args, **kwargs) -> typing.Optional[int]: ...

    poll: __poll_spec

    class ___get_task_id_spec(typing_extensions.Protocol):
        def __call__(self): ...
        async def aio(self, *args, **kwargs): ...

    _get_task_id: ___get_task_id_spec

    class __exec_spec(typing_extensions.Protocol):
        def __call__(self, *cmds: str, pty_info: typing.Optional[modal_proto.api_pb2.PTYInfo] = None): ...
        async def aio(self, *args, **kwargs): ...

    exec: __exec_spec

    @property
    def stdout(self) -> modal.io_streams.StreamReader: ...
    @property
    def stderr(self) -> modal.io_streams.StreamReader: ...
    @property
    def stdin(self) -> modal.io_streams.StreamWriter: ...
    @property
    def returncode(self) -> typing.Optional[int]: ...

    class __list_spec(typing_extensions.Protocol):
        def __call__(
            self, *, app_id: typing.Optional[str] = None, client: typing.Optional[modal.client.Client] = None
        ) -> typing.Generator[Sandbox, None, None]: ...
        def aio(
            self, *, app_id: typing.Optional[str] = None, client: typing.Optional[modal.client.Client] = None
        ) -> typing.AsyncGenerator[Sandbox, None]: ...

    list: __list_spec

def __getattr__(name): ...

_default_image: modal.image._Image
