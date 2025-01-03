#!/usr/bin/env python3
import subprocess
from pathlib import Path

def has_debug_info(binfile:Path) -> bool:
    p = subprocess.run(f'file {binfile} | grep "with debug_info, not stripped"', shell=True, stdout=subprocess.PIPE)
    return p.stdout
    # file <file> | grep <EXP_ARCH>

def is_expected_arch(binfile:Path, expected_arch_string:str) -> bool:
    p = subprocess.run(f'file {binfile} | grep "{expected_arch_string}"', shell=True, stdout=subprocess.PIPE)
    return p.stdout
    # file <file> | grep <EXP_ARCH>

def is_expected_opt(binfile:Path, expected_opt_string:str) -> bool:
    p = subprocess.run(f'objdump --dwarf=info {binfile} | grep DW_AT_producer | head -1 | grep {expected_opt_string}',
                        shell=True, stdout=subprocess.PIPE)
    return p.stdout
    # objdump --dwarf=info <file> | grep DW_AT_producer | head -1 | grep <OPT>

def main():
    bm_folder = Path.home()/'dragon_data/benchmarks'

    # expected output of file command for each architecture we build
    expected_arch_str = {
        'arm64': 'ARM aarch64',
        'armhf': 'ARM, EABI5',
        'x86':   'Intel 80386',
        'x64':   'x86-64',
    }

    for coreutils_folder in bm_folder.glob('coreutils_*'):
        _, arch, opt = coreutils_folder.name.split('_')
        print(f'Checking coreutils build for arch={arch}, opt={opt}')

        #is_expected_arch(coreutils_folder/'sum')
        import random
        bins = [x for x in coreutils_folder.iterdir()]
        # i = random.randint(0, len(bins)-1)

        for binfile in bins:
            if not has_debug_info(binfile):
                raise Exception(f'Binary {binfile} does not have debug info')

            if not is_expected_arch(binfile, expected_arch_str[arch]):
                raise Exception(f'Binary {binfile} does not have expected arch {expected_arch_str[arch]}')

            if not is_expected_opt(binfile, opt):
                raise Exception(f'Binary {binfile} does not have expected opt {opt}')

if __name__ == '__main__':
    main()
