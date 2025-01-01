#!/usr/bin/env python3
import os
from pathlib import Path
from rich.console import Console
import subprocess

def main():
    EXPS_FOLDER=Path('exps')
    DATASETS_FOLDER=Path('datasets')
    ##################################################

    console = Console()

    num_hops = 5
    benchmark_exps = list(EXPS_FOLDER.glob('*_benchmark.exp'))

    resym_exp = list(filter(lambda x: 'resym_test' in x.name, benchmark_exps))[0]
    other_exps = [x for x in benchmark_exps if x != resym_exp]

    def benchmark_name_from_folder(exp_folder:Path) -> str:
        return exp_folder.stem[:-len("_benchmark")]

    def get_dataset_folder(exp_folder:Path, nhops:int) -> str:
        return str(DATASETS_FOLDER/f'{benchmark_name_from_folder(exp_folder)}_{nhops}hops')

    console.rule(f'Building ReSym test dataset')
    subprocess.call(['time', 'dragon', 'build', '--from-exps',
                    get_dataset_folder(resym_exp, num_hops), str(num_hops), str(resym_exp),
                    '--func-list', './scripts/resym_test_funcs.csv'])

    for exp in other_exps:
        bm_name = benchmark_name_from_folder(exp)
        console.rule(f'Bulding {bm_name}')
        subprocess.call(['time', 'dragon', 'build', '--from-exps',
                        get_dataset_folder(exp, num_hops), str(num_hops), str(exp)])

if __name__ == '__main__':
    main()