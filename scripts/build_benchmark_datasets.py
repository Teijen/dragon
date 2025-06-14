#!/usr/bin/env python3
import os
from pathlib import Path
from rich.console import Console
import subprocess

def main():
    EXPS_FOLDER=Path('exps')
    DATASETS_FOLDER=Path('binjaDatasets')
    ##################################################

    console = Console()

    num_hops = 5
    benchmark_exps = list(EXPS_FOLDER.glob('*_benchmark_binja.exp'))

    resym_list = list(filter(lambda x: 'resym_test' in x.name, benchmark_exps))
    resym_exp = resym_list[0] if resym_list else None
    complex_exps = list(filter(lambda x: 'complex' in x.name, benchmark_exps))
    other_exps = [x for x in benchmark_exps if x != resym_exp and x not in complex_exps]

    def benchmark_name_from_folder(exp_folder:Path) -> str:
        return exp_folder.stem[:-len("_benchmark")]

    def get_dataset_folder(exp_folder:Path, nhops:int) -> Path:
        return DATASETS_FOLDER/f'{benchmark_name_from_folder(exp_folder)}_{nhops}hops'

    # ------------ ReSym Test
    resym_test_dspath = get_dataset_folder(resym_exp, num_hops) if resym_list else None
    if resym_test_dspath and not resym_test_dspath.exists():
        console.rule(f'Building [cyan]ReSym test[/] dataset')
        subprocess.call(['time', 'dragon', 'build', '--from-exps',
                        str(resym_test_dspath), str(num_hops), str(resym_exp),
                        '--func-list', './dragon/scripts/resym_test_funcs.csv'])

    # ------------ Complex
    complex_dspath = [get_dataset_folder(exp_folder, num_hops) for exp_folder in complex_exps if 'redis' not in exp_folder.name][0]
    if not complex_dspath.exists():
        console.rule(f'Building [cyan]complex[/] dataset')
        subprocess.call(['time', 'dragon', 'build', '--from-exps', str(complex_dspath), str(num_hops), *[str(exp) for exp in complex_exps]])

    # ------------ Others (coreutils)
    for exp in other_exps:
        exp_dspath = get_dataset_folder(exp, num_hops)
        if not exp_dspath.exists():
            bm_name = benchmark_name_from_folder(exp)
            console.rule(f'Bulding [cyan]{bm_name}[/] dataset')
            subprocess.call(['time', 'dragon', 'build', '--from-exps', str(exp_dspath), str(num_hops), str(exp)])

if __name__ == '__main__':
    main()