#!/usr/bin/env python3
import argparse
from pathlib import Path
# import pandas as pd
import subprocess
from tqdm.auto import tqdm
from rich.console import Console

from multiprocessing import Pool
import time

class STATUS:
    Success = 0
    OutFolderExists = 1
    ErrorCode = 2

def run_tygr_eval(eval_args:dict):
    console = Console()
    bin_file = eval_args['bin_file']
    output_folder = eval_args['output_folder']
    tygr_model = eval_args['tygr_model']

    bin_output_folder = output_folder/f'{bin_file.name}.tygr'
    tygr_rcode = -1

    if bin_output_folder.exists():
        status = STATUS.OutFolderExists
        console.print(f'[yellow]Output folder for {bin_file.name} already exists - skipping')
    else:

        bin_output_folder.mkdir()

        with open(bin_output_folder/'log.txt', 'w') as f:
            p = subprocess.run(f'./TYGR datagen {bin_file} {bin_output_folder} --eval {tygr_model}',
                                stdout=f, stderr=subprocess.STDOUT,
                                shell=True)
            tygr_rcode = p.returncode
            status = STATUS.ErrorCode if tygr_rcode != 0 else STATUS.Success
            if tygr_rcode != 0:
                console.print(f'[bold red]TYGR failed for binary {bin_file.name} with error code {tygr_rcode}')

    csv_files = list(bin_output_folder.glob('*.csv'))
    if not csv_files:
        console.print(f'[red]No output CSV file found for binary {bin_file.name}')

    # (status, csv_file, tygr_rcode)
    return (status, csv_files[0] if csv_files else None, tygr_rcode)

def main(args):
    '''
    This script automates the TYGR eval for benchmarks with multiple binaries
    (specifically coreutils)
    '''
    benchmark_binaries = Path(args.benchmark_binaries)
    output_folder = Path(args.output_folder)
    tygr_model = Path(args.tygr_model)

    console = Console()

    output_folder.mkdir(exist_ok=True)

    binaries = [x for x in benchmark_binaries.iterdir() if not x.is_dir()]
    output_csvs = []

    # we assume we are already in the TYGR folder
    with Pool(processes=args.njobs) as pool:
        run_args = [{
            'bin_file': bin_file,
            'output_folder': output_folder,
            'tygr_model': tygr_model
        } for bin_file in binaries]

        console.rule(f'Running TYGR on {len(binaries):,} binaries across {args.njobs} jobs')
        results = []
        for r in tqdm(pool.imap(run_tygr_eval,run_args), total=len(run_args)):
            results.append(r)

    success = all([res[0] == STATUS.Success for res in results])

    return 0 if success else 1

    # combined_df = pd.concat([pd.read_csv(x) for x in output_csvs])
    # combined_df.to_csv(output_folder/'combined_preds.csv', index=False)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('benchmark_binaries', help='Path to folder containing binaries to evaluate')
    p.add_argument('output_folder', help='Output folder')
    p.add_argument('tygr_model', help='TYGR model file to use')
    p.add_argument('-j', '--njobs', type=int, default=1, help='Number of parallel jobs to use')
    args = p.parse_args()
    exit(main(args))
