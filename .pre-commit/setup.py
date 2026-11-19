"""One-time repo bootstrap: initialize git (if needed) and install pre-commit hooks.

The pre-commit config lives at `.pre-commit/config.yaml` (not the default
`.pre-commit-config.yaml` at the repo root). The `--config` flag below points
pre-commit at it. For manual runs, pass the same flag:

    uv run pre-commit --config .pre-commit/config.yaml run --all-files

Or set the env var once in your shell:

    export PRE_COMMIT_CONFIG=.pre-commit/config.yaml
"""

import os
import subprocess
import sys

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')


def main() -> int:
    if not os.path.isdir('.git'):
        print('Initializing git repository...')
        subprocess.run(['git', 'init'], check=True)
    else:
        print('Git repository already initialized.')

    print('Installing pre-commit hooks...')
    subprocess.run(
        ['uv', 'run', 'pre-commit', 'install', '--config', CONFIG_PATH], check=True
    )

    print('Setup complete.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
