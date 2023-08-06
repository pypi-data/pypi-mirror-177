import typing

import qts


class QtsError(Exception):
    """Base exception class for all qts exceptions.

    Do not raise directly.
    """


class InternalError(QtsError):
    """Raised when things that should not happen do, and they aren't the user's fault."""


class InvalidWrapperError(QtsError):
    """Raised when an invalid wrapper is specified."""

    def __init__(self, wrapper: object):
        super().__init__(f"Unknown wrapper specified: {wrapper!r}")


class MultipleWrappersAvailableError(QtsError):
    """Raised when searching for one wrapper but multiple are available."""

    def __init__(
        self,
        searched: typing.Iterable[qts.Wrapper],
        found: typing.Iterable[qts.Wrapper],
    ):
        searched_list = ", ".join(wrapper.module_name for wrapper in searched)
        found_list = ", ".join(wrapper.module_name for wrapper in found)
        super().__init__(f"Found {found_list} while searching through {searched_list}")


class NoWrapperAvailableError(QtsError):
    """Raised when searching for wrappers and none are available."""

    def __init__(self, wrappers: typing.Iterable[qts.Wrapper]):
        wrapper_list = ", ".join(wrapper.module_name for wrapper in wrappers)
        super().__init__(
            f"No wrapper module available when searching for: {wrapper_list}"
        )


class OtherWrapperAlreadyImportedError(QtsError):
    """Raised when wrappers have already been imported but a call is made to set
    another.
    """

    def __init__(
        self,
        requested: qts.Wrapper,
        already_imported: typing.Collection[qts.Wrapper],
    ):
        already_imported_string = ", ".join(module.name for module in already_imported)
        super().__init__(
            f"Requested {requested.name} but only others are already imported:"
            f" {already_imported_string}"
        )


def name_or_repr(wrapper: qts.Wrapper) -> str:
    try:
        return wrapper.name
    except AttributeError:
        return repr(wrapper)


class UnsupportedWrappersError(QtsError):
    """Raised when autosetting a wrapper but unsupported wrappers have already been
    imported.
    """

    def __init__(self, module_names: typing.Collection[str]) -> None:
        s = ", ".join(sorted(module_names))
        super().__init__(f"Unsupported wrappers have already been imported: f{s}")


class WrapperAlreadySelectedError(QtsError):
    """Raised when attempting to set a wrapper but one has already been selected."""

    def __init__(
        self,
        existing_wrapper: qts.Wrapper,
        requested_wrapper: qts.Wrapper,
    ):
        existing = name_or_repr(wrapper=existing_wrapper)
        requested = name_or_repr(wrapper=requested_wrapper)
        super().__init__(
            f"Wrapper {existing} already selected while requesting {requested}",
        )
