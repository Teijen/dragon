
NJOBS=80
DRAGON_DATA_FOLDER=~/dragon_data
BIN_FOLDER=$DRAGON_DATA_FOLDER/tydamin_sample

###########################################
# run this from the top-level dragon folder
###########################################

ORIG_DIR=`pwd`

# create wildebeest experiment
cd ./exps
wdb create import-dataset tydamin_sample.exp -p bin_folder=$BIN_FOLDER

# run experiment (import into Ghidra, extract ASTs and AST var data)
cd tydamin_sample.exp
time wdb run -j$NJOBS

cd $ORIG_DIR
