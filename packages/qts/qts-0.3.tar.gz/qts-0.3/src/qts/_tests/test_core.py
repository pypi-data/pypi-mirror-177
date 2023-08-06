import os
import typing

import pytest

import qts


def test_set_wrapper_succeeds(pytester: pytest.Pytester, wrapper: qts.Wrapper) -> None:
    content = f"""
    import sys

    import qts


    def test():
        assert {wrapper.module_name!r} not in sys.modules
        wrapper = qts.wrapper_by_name(name={wrapper.module_name!r})
        qts.set_wrapper(wrapper)
        from qts import QtCore
        imported_top_level_module_name = QtCore.QObject.__module__.partition('.')[0]
        assert imported_top_level_module_name == {wrapper.module_name!r}
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    argnames=["second_wrapper"],
    argvalues=[
        [qts.wrapper],
        [qts.Wrapper(family="", name="fake", major_version=0, module_name="")],
        [None],
    ],
)
def test_setting_twice_raises(second_wrapper: typing.Optional[qts.Wrapper]) -> None:
    with pytest.raises(qts.WrapperAlreadySelectedError):
        qts.set_wrapper(second_wrapper)  # type: ignore[arg-type]


def test_setting_invalid_wrapper_raises(pytester: pytest.Pytester) -> None:
    content = f"""
    import pytest

    import qts


    def test():
        with pytest.raises(qts.InvalidWrapperError):
            qts.set_wrapper(None)
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


def test_importing_with_invalid_wrapper_raises(
    pytester: pytest.Pytester,
    qt_module: qts._tests.QtModule,
) -> None:
    content = f"""
    import pytest

    import qts


    def test():
        qts.wrapper = 37
        with pytest.raises(qts.InvalidWrapperError):
            from qts import {qt_module.name}
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


def test_checking_with_no_available_wrappers_raises() -> None:
    with pytest.raises(qts.NoWrapperAvailableError):
        qts.available_wrapper(wrappers=[])


def test_checking_with_multiple_available_wrappers_raises() -> None:
    with pytest.raises(qts.MultipleWrappersAvailableError):
        qts.available_wrapper(wrappers=list(qts.available_wrappers()) * 2)


def test_an_available_wrapper_with_no_available_wrappers_raises() -> None:
    with pytest.raises(qts.NoWrapperAvailableError):
        qts.an_available_wrapper(wrappers=[])


def test_an_available_wrapper_with_returns() -> None:
    assert qts.an_available_wrapper() == qts.available_wrapper()


def test_importing_without_setting_auto_picks(
    pytester: pytest.Pytester,
    qt_module: qts._tests.QtModule,
    wrapper: qts.Wrapper,
) -> None:
    content = f"""
    import pytest

    import qts


    def test():
        assert qts.wrapper is None
        from qts import {qt_module.name}
        assert qts.wrapper.name == {wrapper.name!r}
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


def test_importing_without_setting_auto_picks_from_environment_variable(
    pytester: pytest.Pytester,
    qt_module: qts._tests.QtModule,
    wrapper: qts.Wrapper,
) -> None:
    content = f"""
    import os

    import qts


    def test():
        assert qts.wrapper is None
        os.environ["QTS_WRAPPER"] = {wrapper.name!r}
        from qts import {qt_module.name}
        assert qts.wrapper.name == {wrapper.name!r}
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


def test_autoset_wrapper_works_with_valid_wrapper(
    pytester: pytest.Pytester,
    wrapper: qts.Wrapper,
) -> None:
    content = f"""
    import os

    import qts


    def test():
        assert qts.wrapper is None
        os.environ["QTS_WRAPPER"] = {wrapper.name!r}
        qts.autoset_wrapper()
        assert qts.wrapper.name == {wrapper.name!r}
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


def test_autoset_wrapper_raises_with_invalid_wrapper(
    pytester: pytest.Pytester,
) -> None:
    content = f"""
    import os

    import pytest

    import qts


    def test():
        assert qts.wrapper is None
        os.environ["QTS_WRAPPER"] = "not a wrapper"
        with pytest.raises(qts.InvalidWrapperError):
            qts.autoset_wrapper()
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


def test_check_already_imported_wrappers_finds_none(pytester: pytest.Pytester) -> None:
    content = f"""
    import sys

    import qts


    def test():
        already_imported = qts.check_already_imported_wrappers()
        assert already_imported == []
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.mark.parametrize(argnames=["module_name"], argvalues=[["PyQt4"], ["PySide"]])
def test_check_already_imported_wrappers_raises_for_only_unsupported(
    module_name: str,
    pytester: pytest.Pytester,
) -> None:
    content = f"""
    import sys

    import pytest

    import qts

    sys.modules[{module_name!r}] = None

    def test():
        with pytest.raises(qts.UnsupportedWrappersError):
            qts.check_already_imported_wrappers()
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    argnames=["module_name"],
    argvalues=[[module.name] for module in qts.supported_wrappers],
)
@pytest.mark.parametrize(
    argnames=["unsupported_module_names"],
    argvalues=[[[]], [["PyQt4"]], [["PySide"]], [["PyQt4", "PySide"]]],
)
def test_check_already_imported_wrappers_returns(
    module_name: str,
    unsupported_module_names: str,
    pytester: pytest.Pytester,
) -> None:
    content = f"""
    import sys

    import pytest

    import qts

    sys.modules[{module_name!r}] = None
    for module_name in {unsupported_module_names}:
        sys.modules[module_name] = None

    def test():
        found = qts.check_already_imported_wrappers()
        found_names = [module.name for module in found]
        assert found_names == [{module_name!r}]
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


def test_check_already_imported_wrappers_returns_select_wrappers(
    pytester: pytest.Pytester,
) -> None:
    content = f"""
    import sys

    import pytest

    import qts

    sys.modules["PyQt5"] = None
    sys.modules["PyQt6"] = None

    def test():
        wrappers = [qts.pyqt_6_wrapper, qts.pyside_6_wrapper]
        found = qts.check_already_imported_wrappers(wrappers=wrappers)
        assert found == [qts.pyqt_6_wrapper]
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    argnames=["module", "another_module"],
    argvalues=[
        [module, next(iter(set(qts.supported_wrappers) - {module}))]
        for module in qts.supported_wrappers
    ],
)
def test_set_wrapper_raises_if_another_is_already_imported(
    module: qts.Wrapper,
    another_module: qts.Wrapper,
    pytester: pytest.Pytester,
) -> None:
    content = f"""
    import sys

    import pytest

    import qts

    sys.modules[{another_module.name!r}] = None

    def test():
        with pytest.raises(qts.OtherWrapperAlreadyImportedError):
            qts.set_wrapper(qts.wrapper_by_name(name={module.name!r}))
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    argnames=["module"],
    argvalues=[[module] for module in qts.supported_wrappers],
)
def test_autoset_wrapper_uses_already_imported(
    module: qts.Wrapper,
    pytester: pytest.Pytester,
) -> None:
    content = f"""
    import sys

    import pytest

    import qts

    sys.modules[{module.name!r}] = None

    def test():
        qts.autoset_wrapper()
        assert qts.wrapper == qts.wrapper_by_name(name={module.name!r})
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)
