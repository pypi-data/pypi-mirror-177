"""
Script that uses pylint to check codes and print custom
warnings and errors messages here.
"""
import os
from typing import NoReturn, Tuple, List, Dict
from collections import defaultdict
import attr
# Pylint imports
from pylint.lint.run import _cpu_count
from pylint.lint.pylinter import PyLinter
from pylint.lint.base_options import _make_run_options
from pylint.config import find_default_config_files
from pylint.config.config_initialization import _config_initialization
from pylint.reporters.base_reporter import BaseReporter
from pylint.message import Message
# Local imports
from pyci.utils import retrieve_current_dir, find_code
from pyci.reporters import PyCILogger


class CustomReporter(BaseReporter):
    """Custom Reporter for Pylint and its errors."""

    def __init__(self) -> NoReturn:
        super(BaseReporter).__init__()
        self.path_strip_prefix = os.getcwd() + os.sep
        self._errors = defaultdict(list)

    def _display(self, layout):
        pass

    def handle_message(self, msg: Message) -> NoReturn:
        """Personal method to append the errors in a better way"""
        self._errors[msg.path].append({
            'line': msg.line,
            'col': msg.column,
            'msg': f"{msg.msg_id} {msg.msg}",
            'type': msg.msg_id[0],
            'code': find_code(msg.line, msg.end_line, msg.abspath)
        })

    @property
    def errors(self) -> List[Dict[str, str]] | None:
        """Method to return a better structure of errors"""
        if not self._errors:
            return None
        return self._errors

    def on_set_current_module(self, module: str = None, filepath: str | None = None) -> None:
        """Hook called when a module starts to be analyzed."""


@attr.s(slots=True)
class PylintRunner:
    """Class to perform a personal Pylint validation to catch all the errors or
    messages that comes from the codes."""
    # Add the options to run
    _options = attr.ib(default=(("Commands", "Commands",),), type=Tuple[str])
    files = attr.ib(default=None, type=str | Tuple[str] | List[str])
    folder = attr.ib(default=None, type=str)
    # Some configuration files, as the .rcFile
    _rcFile = attr.ib(default=None, type=str)
    # The Linter and the base reporter
    _linter = attr.ib(default=None, type=PyLinter)
    _reporter = attr.ib(default=CustomReporter, type=CustomReporter)

    def __attrs_post_init__(self) -> NoReturn:
        #!TODO Add also other parameters as the possibility to add custom rc files.
        # Check if the user has passed some _rcFile. If not, then use the default one.
        if not self._rcFile:
            self._rcFile = str(next(find_default_config_files(), None))
        # Initialize the reporter
        self._reporter = self._reporter()
        # Now, initialize the linter
        self._linter = PyLinter(
            _make_run_options(self),
            option_groups=self._options,
            pylintrc=self._rcFile,
        )
        # Add some linter configurations
        self._linter.load_default_plugins()
        self._linter.disable("I")
        self._linter.enable("c-extension-no-member")
        if self._linter.config.jobs < 0:
            raise ValueError(
                f"Jobs number ({self._linter.config.jobs}) should be greater than or equal to 0")
        if self._linter.config.jobs == 0:
            self._linter.config.jobs = _cpu_count()

    def __check_files(self) -> None:
        """Method to check the files and see if you can find
        some errors on them.

        Raises:
        ----------------------------------------------------------
            - NotImplementedError: For some not implemented options.
        """
        # Check if you have add files (or folders) to check.
        if self.files:
            raise NotImplementedError(
                "The option to review independent files it's not available at the time.")
        if self.folder:
            raise NotImplementedError(
                "The option to review an entire folder it's not available at the time.")
        # If you don't add nothing, then check whatever you can find on the repository
        _args = retrieve_current_dir()
        # ------------------------------- #
        # Once you've finished the process of selecting the arguments to review
        #!TODO Later, add the possibility here to choose between the customReporter
        #!TODO for the terminal and the custom reporter for the web app.
        _args = _config_initialization(
            self._linter, _args, self._reporter, config_file=self._rcFile, verbose_mode=False
        )
        # If you can't find arguments, report that to the user
        if not _args:
            print(
                f"There are no files to review for the given path '{_args}'.")
            return
        # Now, check the files with the linter
        self._linter.check(_args)

    def run(self) -> None:
        """Method to run the linter."""
        logger = PyCILogger()  # Initialize the logger
        # First, call the check_files method
        self.__check_files()
        # From here, retrieve the errors.
        errors = self._reporter.errors
        # If you don't have any errors...
        if not errors:
            logger.no_errors(
                "[bold green]You don't have any errors![/bold green] Nice job!", ci_tool="Pylint")
            return
        # If you've errors
        logger.log(errors, ci_tool='Pylint')
        return


if __name__ == '__main__':
    PR = PylintRunner()
    PR.run()
