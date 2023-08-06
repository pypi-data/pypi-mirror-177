import logging
import subprocess


def run_command(*commands: str):
    process = subprocess.run([*commands], capture_output=True)
    if process.returncode != 0:
        raise EnvironmentError(f'Return code {process.returncode} {process.stderr.decode()} {process.stdout.decode()}')
    logging.debug(process)
    return process.stdout.decode()
