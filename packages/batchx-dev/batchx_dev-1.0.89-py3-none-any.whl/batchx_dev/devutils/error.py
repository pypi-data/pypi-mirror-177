import subprocess as sp
import traceback

from .debug import debug_print


# handle errors
def handle_exception(
    exception: Exception,
    identifier: str = "",
    message: str | None = None,
    exit_code: int | None = None,
    reraise: bool = True,
    verbose: bool = True,
):

    msg = """
    Caught Exception in {id} command.
    Exception:
        {exception}
    Stacktrace:
        {stacktrace}
    """.format(
        id=identifier,
        exception=exception,
        stacktrace=traceback.format_exc(),
    )

    if message is not None:
        extra = """

        Custom message:
            {msg}
        """.format(
            msg=message
        )
        msg = msg + extra

    if exit_code is not None:
        extra = """

        Exit code:
            {code}
        """.format(
            code=exit_code
        )
        msg = msg + extra

    debug_print(msg, verbose=verbose)
    if reraise:
        raise Exception(msg) from None
    else:
        return
