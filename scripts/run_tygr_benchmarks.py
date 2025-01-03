#!/usr/bin/env python3
import os
from pathlib import Path
from rich.console import Console
import subprocess

class cd:
    def __init__(self, newpath:Path) -> None:
        '''
        newpath: The path to change directories to. Once the with block exits,
                 the current directory will be restored.
        '''
        self.newpath = newpath

    def __enter__(self):
        self.savedpath = self.newpath.cwd()
        os.chdir(self.newpath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedpath)

def main():
    DRAGON_DATA_FOLDER=Path.home()/'dragon_data'
    BENCHMARKS_FOLDER=DRAGON_DATA_FOLDER/'benchmarks'
    TYGR_FOLDER=Path.home()/'dev/TYGR'
    OUT_FOLDER=Path('tygr_evals').absolute()
    ##################################################

    console = Console()
    OUT_FOLDER.mkdir(exist_ok=True)

    benchmarks = [
        ('coreutils',       'x64.O0.base.model'),
        ('nginx',           'x64.O0.base.model'),
        ('openssl_arm64',   'aarch64.O0.base.model'),
        ('openssl_O0',      'x64.O0.base.model'),
        ('openssl_O1',      'x64.O1.base.model'),
        ('openssl_O2',      'x64.O2.base.model'),
        ('openssl_O3',      'x64.O3.base.model'),
    ]

    # TODO: run complex together
    # TODO: run each coreutils config in parallel
        # - arm64 O0
        # - arm64 O1
        # ...
        # - x64 O3

    run_tygr_eval = Path('scripts/run_tygr_eval.py').absolute()

    with cd(TYGR_FOLDER):
        for bm_name, model in benchmarks:
            console.rule(f'Evaluating {bm_name} using model {model}')
            bins_folder = BENCHMARKS_FOLDER/bm_name
            out_folder = OUT_FOLDER/f'{bm_name}.tygr'
            model_file = TYGR_FOLDER/'model/MODEL_base'/model
            subprocess.call(['time', run_tygr_eval, bins_folder, out_folder, model_file])

if __name__ == '__main__':
    main()
