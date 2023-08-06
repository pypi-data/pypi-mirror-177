from typing import Any, ClassVar


class PyXrayCErrorMixin:
    msg_template: ClassVar[str]

    def __init__(self, **context: Any) -> None:
        self.__dict__ = context

    def __repr__(self) -> str:
        return self.msg_template.format(**self.__dict__)


class ConfigError(PyXrayCErrorMixin, RuntimeError):
    pass


class DependencyError(ConfigError):
    msg_template = "{name!r} is not found, please install it and try again"

    def __init__(self, *, name: str) -> None:
        super().__init__(name=name)
