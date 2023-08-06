import logging
import time

import typer

from fluxvault import FluxAgent, FluxKeeper

PREFIX = "FLUXVAULT"

app = typer.Typer(rich_markup_mode="rich", add_completion=False)


def configure_logs(log_to_file, logfile_path, debug):
    vault_log = logging.getLogger("fluxvault")
    aiotinyrpc_log = logging.getLogger("aiotinyrpc")
    level = logging.DEBUG if debug else logging.INFO

    formatter = logging.Formatter(
        "%(asctime)s: fluxvault: %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"
    )

    vault_log.setLevel(level)
    aiotinyrpc_log.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(logfile_path, mode="a")
    file_handler.setFormatter(formatter)

    vault_log.addHandler(stream_handler)
    aiotinyrpc_log.addHandler(stream_handler)
    if log_to_file:
        aiotinyrpc_log.addHandler(file_handler)
        vault_log.addHandler(file_handler)


@app.command()
def keeper(
    vault_dir: str = typer.Option(
        "vault",
        "--vault-dir",
        "-s",
        envvar=f"{PREFIX}_VAULT_DIR",
        show_envvar=False,
    ),
    comms_port: int = typer.Option(
        8888,
        "--comms-port",
        "-p",
        envvar=f"{PREFIX}_COMMS_PORT",
        show_envvar=False,
    ),
    app_name: str = typer.Option(
        None,
        "--app-name",
        "-a",
        envvar=f"{PREFIX}_APP_NAME",
        show_envvar=False,
    ),
    polling_interval: int = typer.Option(
        300,
        "--polling-interval",
        "-i",
        envvar=f"{PREFIX}_POLLING_INTERVAL",
        show_envvar=False,
    ),
    run_once: bool = typer.Option(
        False,
        "--run-once",
        "-o",
        envvar=f"{PREFIX}_RUN_ONCE",
        show_envvar=False,
        help="Contact agents once and bail",
    ),
    agent_ips: str = typer.Option(
        "",
        envvar=f"{PREFIX}_AGENT_IPS",
        show_envvar=False,
    ),
    signing_key: str = typer.Option(
        "",
        envvar=f"{PREFIX}_SIGNING_KEY",
        show_envvar=False,
    ),
):

    agent_ips = agent_ips.split(",")
    agent_ips = list(filter(None, agent_ips))

    flux_keeper = FluxKeeper(
        vault_dir=vault_dir,
        comms_port=comms_port,
        app_name=app_name,
        agent_ips=agent_ips,
        signing_key=signing_key,
    )

    log = logging.getLogger("fluxvault")

    while True:
        flux_keeper.poll_all_agents()
        if run_once:
            break
        log.info(f"sleeping {polling_interval} seconds...")
        time.sleep(polling_interval)


@app.command()
def agent(
    bind_address: str = typer.Option(
        "0.0.0.0",
        "--bind-address",
        "-b",
        envvar=f"{PREFIX}_BIND_ADDRESS",
        show_envvar=False,
    ),
    bind_port: int = typer.Option(
        8888,
        "--bind-port",
        "-p",
        envvar=f"{PREFIX}_BIND_PORT",
        show_envvar=False,
    ),
    enable_local_fileserver: bool = typer.Option(
        False,
        "--fileserver",
        "-s",
        envvar=f"{PREFIX}_FILESERVER",
        show_envvar=False,
        help="Serve vault files to other components",
    ),
    local_fileserver_port: int = typer.Option(
        "2080",
        "--fileserver-port",
        "-z",
        envvar=f"{PREFIX}_FILESERVER_PORT",
        show_envvar=False,
        help="For multi-component apps",
    ),
    managed_files: str = typer.Option(
        "",
        "--manage-files",
        "-m",
        envvar=f"{PREFIX}_MANAGED_FILES",
        show_envvar=False,
        help="Comma seperated files we want from keeper",
    ),
    working_dir: str = typer.Option(
        "/tmp",
        "--working-dir",
        "-i",
        envvar=f"{PREFIX}_WORKING_DIR",
        show_envvar=False,
        help="Where files will be stored",
    ),
    whitelisted_addresses: str = typer.Option(
        "",
        "--whitelist-addresses",
        "-w",
        envvar=f"{PREFIX}_WHITELISTED_ADDRESSES",
        show_envvar=False,
        help="Comma seperated addresses to whitelist",
    ),
    verify_source_address: bool = typer.Option(
        True,
        "--verify-source-address",
        "-z",
        envvar=f"{PREFIX}_VERIFY_SOURCE_ADDRESS",
        show_envvar=False,
        help="Matches source ip to your whitelist",
    ),
    signed_vault_connections: bool = typer.Option(
        False,
        "--signed-vault-connections",
        "-k",
        envvar=f"{PREFIX}_SIGNED_VAULT_CONNECTIONS",
        show_envvar=False,
        help="Expects all keeper connections to be signed",
    ),
):

    whitelisted_addresses = whitelisted_addresses.split(",")
    whitelisted_addresses = list(filter(None, whitelisted_addresses))
    managed_files = managed_files.split(",")
    managed_files = list(filter(None, managed_files))

    agent = FluxAgent(
        bind_address=bind_address,
        bind_port=bind_port,
        enable_local_fileserver=enable_local_fileserver,
        local_fileserver_port=local_fileserver_port,
        managed_files=managed_files,
        working_dir=working_dir,
        whitelisted_addresses=whitelisted_addresses,
        verify_source_address=verify_source_address,
        signed_vault_connections=signed_vault_connections,
    )

    agent.run()


@app.callback()
def main(
    debug: bool = typer.Option(
        False,
        "--debug",
        envvar=f"{PREFIX}_DEBUG",
        show_envvar=False,
        help="Enable extra debug logging",
    ),
    enable_logfile: bool = typer.Option(
        False,
        "--log-to-file",
        "-l",
        envvar=f"{PREFIX}_ENABLE_LOGFILE",
        show_envvar=False,
        help="Turn on logging to file",
    ),
    logfile_path: str = typer.Option(
        "/tmp/fluxvault.log",
        "--logfile-path",
        "-p",
        envvar=f"{PREFIX}_LOGFILE_PATH",
        show_envvar=False,
    ),
):
    configure_logs(enable_logfile, logfile_path, debug)


def entrypoint():
    """Called by console script"""
    app()


if __name__ == "__main__":
    app()
