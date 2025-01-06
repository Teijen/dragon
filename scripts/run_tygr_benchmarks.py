#!/usr/bin/env python3
import os
from pathlib import Path
from rich.console import Console
import time
from datetime import  timedelta
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

class print_runtime:
    '''
    Times the code inside the with block, then prints out the elapsed runtime
    when the code finished
    '''
    def __init__(self, name:str='') -> None:
        self.start_time = 0.0
        self.stop_time = 0.0
        self.name = name

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, etype, value, traceback):
        self.stop_time = time.time()
        print((f'{self.name} Runtime: {timedelta(seconds=int(self.runtime_sec))}').strip())

    @property
    def runtime_sec(self) -> float:
        return self.stop_time - self.start_time

def main():
    DRAGON_DATA_FOLDER=Path.home()/'dragon_data'
    BENCHMARKS_FOLDER=DRAGON_DATA_FOLDER/'benchmarks'
    TYGR_FOLDER=Path.home()/'dev/TYGR'
    OUT_FOLDER=Path('tygr_evals').absolute()
    ##################################################

    console = Console()
    OUT_FOLDER.mkdir(exist_ok=True)

    benchmarks = [
        # verify that redis can finish first...
        ('complex-redis',       'x64.O0.base.model',        1),
        ('complex',             'x64.O0.base.model',        4),
        ('coreutils_arm64_O0',  'aarch64.O0.base.model',    15),
        ('coreutils_arm64_O1',  'aarch64.O1.base.model',    15),
        ('coreutils_arm64_O2',  'aarch64.O2.base.model',    15),
        ('coreutils_arm64_O3',  'aarch64.O3.base.model',    15),
        ('coreutils_armhf_O0',  'arm32.O0.base.model',      15),
        ('coreutils_armhf_O1',  'arm32.O1.base.model',      15),
        ('coreutils_armhf_O2',  'arm32.O2.base.model',      15),
        ('coreutils_armhf_O3',  'arm32.O3.base.model',      15),
        ('coreutils_x64_O0',    'x64.O0.base.model',        15),
        ('coreutils_x64_O1',    'x64.O1.base.model',        15),
        ('coreutils_x64_O2',    'x64.O2.base.model',        15),
        ('coreutils_x64_O3',    'x64.O3.base.model',        15),
        ('coreutils_x86_O0',    'x86.O0.base.model',        15),
        ('coreutils_x86_O1',    'x86.O1.base.model',        15),
        ('coreutils_x86_O2',    'x86.O2.base.model',        15),
        ('coreutils_x86_O3',    'x86.O3.base.model',        15),
    ]

    run_tygr_eval = Path('scripts/run_tygr_eval.py').absolute()

    with cd(TYGR_FOLDER):
        for bm_name, model, njobs in benchmarks:
            console.rule(f'Evaluating [bold green]{bm_name}[/] using model {model}')
            bins_folder = BENCHMARKS_FOLDER/bm_name
            out_folder = OUT_FOLDER/f'{bm_name}.tygr'
            model_file = TYGR_FOLDER/'model/MODEL_base'/model
            with print_runtime(f'{bm_name}'):
                subprocess.call([run_tygr_eval, bins_folder, out_folder, model_file, f'-j{njobs}'])

if __name__ == '__main__':
    main()
