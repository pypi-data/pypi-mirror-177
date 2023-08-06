import json
import os
import subprocess as sp
import sys
import traceback
from functools import partial
from pathlib import Path
from time import sleep

from batchx import bx

from .CTE import DEFAULT_MEMORY_MB, DEFAULT_VCPUS
from .debug import debug_print
from .io import save_json


# main functions
def run_command(
    command: str,
    identifier: str = "",
    output_fp: Path | str | None = None,
    verbose: bool = True,
    cwd: Path | str | None = None,
    shell: bool = True,
    acceptable_exit_codes: tuple[int, ...] | None = (0,),
) -> int:
    debug_print("{} command".format(identifier), command, verbose=verbose, long=False)

    run_subprocess = partial(
        sp.run,
        command,
        cwd=cwd,
        shell=shell,
        stderr=sp.PIPE,
        encoding="utf-8",
    )

    if output_fp is None:
        completed_subprocess = run_subprocess()
    else:
        with open(output_fp, "w") as f:
            completed_subprocess = run_subprocess(stdout=f)

    exit_code = completed_subprocess.returncode
    debug_print("stdout", completed_subprocess.stdout, verbose=verbose, long=True)
        
    if acceptable_exit_codes is not None:
        _raise_value_error_on_unacceptable_exit_code(
            exit_code=exit_code,
            acceptable_exit_codes=acceptable_exit_codes,
            error_message=completed_subprocess.stderr,
        )
    return exit_code


def run_bx_job(
    tool: str,
    inputs: dict,
    output_fp=None,
    environment: str | None = None,
    vcpus=DEFAULT_VCPUS,
    memory_mb=DEFAULT_MEMORY_MB,
    timeout_s: int = 15 * 60,
    verbose: bool = True,
    acceptable_exit_codes: tuple[int, ...] | None = (0,),
):

    # Initialize
    identifier = "{t} bx job submit".format(t=tool)
    debug_print("{}".format(identifier), verbose=verbose, long=False)

    output_json = dict()
    if environment is None:
        environment = os.environ["BATCHX_ENV"]

    # bx submit
    bx.connect()
    job_service = bx.JobService()

    submit_request = _get_bx_submit_request(
        job_service,
        identifier=identifier,
        tool=tool,
        inputs=inputs,
        environment=environment,
        vcpus=vcpus,
        memory_mb=memory_mb,
        timeout_s=timeout_s,
        verbose=verbose,
    )

    submit_response = job_service.Run(submit_request)
    debug_print("{} Response".format(identifier), submit_response, verbose=verbose)

    # check potential error message
    exit_code = getattr(submit_response, "exit_code", 1)
    output_json = getattr(submit_response, "output_json", None)
    error_message = getattr(submit_response, "error_message", None)

    # handle outputs
    if output_json is not None:
        outputs = json.loads(output_json)
    else:
        outputs = None

    if output_fp is not None:
        save_json(output_json, outputs)
    else:
        pass

    # debug prints
    debug_print(
        "{} exit_code".format(identifier), exit_code, verbose=verbose, long=False
    )
    debug_print(
        "{} output_json".format(identifier), output_json, verbose=verbose, long=True
    )
    debug_print(
        "{} error_message".format(identifier), error_message, verbose=verbose, long=True
    )

    # raise error on non-acceptable exit code
    if acceptable_exit_codes is not None:
        _raise_value_error_on_unacceptable_exit_code(
            exit_code=exit_code,
            acceptable_exit_codes=acceptable_exit_codes,
            error_message=error_message,
        )

    return exit_code, error_message, outputs


# helpers
def _raise_value_error_on_unacceptable_exit_code(
    exit_code: int,
    acceptable_exit_codes: tuple[int, ...] = (0,),
    error_message: str | None = None,
):
    if exit_code not in acceptable_exit_codes:
        msg = """
        Exit code {c} not in acceptable exit codes {a}
        """.format(
            c=exit_code, a=acceptable_exit_codes
        )

        if error_message is not None:
            extra = """

            Error message:
                {msg}
            """.format(
                msg=error_message
            )
            msg = msg + extra

        raise ValueError(msg)
    return


def _get_bx_submit_request(
    job_service,
    identifier: str,
    tool: str,
    inputs: dict,
    environment: str | None = None,
    vcpus=DEFAULT_VCPUS,
    memory_mb=DEFAULT_MEMORY_MB,
    timeout_s: int = 15 * 60,
    verbose: bool = True,
):

    request = job_service.SubmitRequest(
        environment=environment,
        image=tool,
        vcpus=vcpus,
        memory=memory_mb,
        timeout=timeout_s,
        input_json=json.dumps(inputs),
    )
    debug_print("{} Request".format(identifier), request, verbose=verbose)
    return request
