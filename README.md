# DRAGON

This holds the experiment artifacts for the DRAGON paper `insert paper name here...`


**TODO: put the how-to-run/reproduce instructions here**

# Quickstart
`python -m venv <dragon_env> && <dragon_venv>/bin/activate`

`pip install -r pip_freeze_2024.12.31.txt`

**TODO: easiest/quickest option - run eval script**

# Generating AST Data

## Ghidra Server
**TODO: setting up Ghidra server (link to repo)**

Change the parameters at the top to match your setup (e.g. `NJOBS=5`) and
run the scripts below to import binaries into Ghidra from scratch and
export AST data to JSON files:

## Training dataset (our sample of TYDA-min)

`./scripts/export_tydamin_asts.sh`

## ReSym training dataset

`./scripts/export_resym_train_asts.sh`

In this version of Ghidra, these binaries fail to import successfully:
~~~
02ab506
9f89779
2cefb8a
fc2d878
cea8f48
674ee41     # this one doesn't fail, but seems to hang forever, so is excluded
~~~

### Sample Output
Here is what my final status looked like once I successfully reran a couple of
jobs that had hung:

~~~
$ wdb status | grep -v finished | grep Run
Run 1271 (-1271.02ab506) - FAILED during "export_asts_strip" [0:03:17]
Run 1577 (-1577.9f89779) - FAILED during "export_asts_strip" [0:03:33]
Run 2941 (-2941.2cefb8a) - FAILED during "export_asts_strip" [0:03:01]
Run 3725 (-3725.674ee41) running "ghidra_import_debug" [0:27:45] Total: [0:27:45]
Run 3945 (-3945.fc2d878) - FAILED during "export_asts_strip" [0:03:10]
Run 4845 (-4845.cea8f48) - FAILED during "export_asts_strip" [0:02:23]
~~~

## Fixing any jobs that hang
If running with many parallel jobs, you may need to kill it and rerun any
that are hung.

### Check status from within a wdb experiment folder (e.g. `dragon/exps/tydamin_sample.exp`) with:

`wdb status`

or more usefully:

`wdb status | grep -v finished`

### Restart a failed run `N` with:

`wdb run --from <failed_step_name> -f N` # single run

`wdb run --from <failed_step_name> -f X,Y,Z` # multiple runs

`wdb run --from <failed_step_name> -f N --debug` # show output in terminal instead of logfile

### Show logfile for run N

`wdb log N`