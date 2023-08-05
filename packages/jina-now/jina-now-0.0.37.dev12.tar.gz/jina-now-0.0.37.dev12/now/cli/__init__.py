import os
import pathlib
import platform
import signal
import sys
import warnings
from argparse import Namespace
from os.path import expanduser as user

import cpuinfo

from now import __version__ as version
from now.deployment.deployment import cmd

warnings.filterwarnings("ignore")

cur_dir = pathlib.Path(__file__).parents[1].resolve()

os.environ['JINA_CHECK_VERSION'] = 'False'
os.environ['JCLOUD_LOGLEVEL'] = 'ERROR'


def _get_run_args():
    from now.cli.parser import get_main_parser

    parser = get_main_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        exit()
    args, unknown = parser.parse_known_args()

    # clean up the args with None values
    args = {k: v for k, v in vars(args).items() if v is not None}
    # Convert args back to Namespace
    args = Namespace(**args)

    if unknown:
        raise Exception('unknown args: ', unknown)

    return args


def _is_latest_version(suppress_on_error=True):
    try:
        import json
        from urllib.request import Request, urlopen

        from jina import __version__

        req = Request(
            'https://api.jina.ai/latest', headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urlopen(
            req, timeout=5
        ) as resp:  # 'with' is important to close the resource after use
            latest_ver = json.load(resp)['version']
            from packaging.version import Version

            latest_ver = Version(latest_ver)
            cur_ver = Version(__version__)
            if cur_ver < latest_ver:
                from jina.logging.predefined import default_logger

                default_logger.warning(
                    f'You are using Jina version {cur_ver}, however version {latest_ver} is available. '
                    f'You should consider upgrading via the "pip install --upgrade jina" command.'
                )
                return False
        return True
    except Exception:
        if not suppress_on_error:
            raise


def _get_kind_path() -> str:
    os_type = platform.system().lower()
    # kind needs no distinction of architecture type
    kind_path, _ = cmd('which kind')
    kind_path = kind_path.strip()
    if not kind_path:
        if not os.path.exists(user('~/.cache/jina-now/kind')):
            print('kind not found. Installing kind')
            cmd(
                f'/bin/bash {cur_dir}/scripts/install_kind.sh {os_type}',
                std_output=True,
            )
        kind_path = user('~/.cache/jina-now/kind')
    else:
        kind_path = kind_path.decode('utf-8')
    return kind_path


def _get_kubectl_path() -> str:
    os_type = platform.system().lower()
    arch = 'x86_64'
    if os_type == 'darwin':
        if 'm1' in cpuinfo.get_cpu_info().get('brand_raw').lower():
            arch = 'arm64'
        else:
            arch = platform.machine()
    elif os_type == 'linux':
        arch = platform.machine()

    # kubectl needs `intel` or `m1` for apple os
    # for linux no need of architecture type
    kubectl_path, _ = cmd('which kubectl')
    kubectl_path = kubectl_path.strip()
    if not kubectl_path:
        if not os.path.isfile(user('~/.cache/jina-now/kubectl')):
            print('kubectl not found. Installing kubectl')
            cmd(
                f'/bin/bash {cur_dir}/scripts/install_kubectl.sh {os_type} {arch}',
                std_output=True,
            )
        kubectl_path = user('~/.cache/jina-now/kubectl')
    else:
        kubectl_path = kubectl_path.decode('utf-8')
    return kubectl_path


def cli(args=None):
    """The main entrypoint of the CLI"""
    if len(sys.argv) != 1 and not ('-h' in sys.argv[1:] or '--help' in sys.argv[1:]):
        print(f'Initialising Jina NOW v{version} ...')

    if not args:
        args = _get_run_args()
    args = vars(args)  # Make it a dict from Namespace

    if '--version' in sys.argv[1:]:
        from now import __version__

        print(__version__)
        exit(0)

    os.environ['JINA_LOG_LEVEL'] = 'CRITICAL'
    os_type = platform.system().lower()
    arch = 'x86_64'
    if os_type == 'darwin':
        if 'm1' in cpuinfo.get_cpu_info().get('brand_raw').lower():
            arch = 'arm64'
        else:
            arch = platform.machine()
    elif os_type == 'linux':
        arch = platform.machine()

    args['kubectl_path'] = _get_kubectl_path()
    args['kind_path'] = _get_kind_path()
    from now.run_all_k8s import run_k8s

    return run_k8s(os_type=os_type, arch=arch, **args)


if __name__ == '__main__':
    cli()
