
NJOBS=8
DRAGON_DATA_FOLDER=/home/logan/Dev/IntermediateDragon/dragonBinaries
BIN_FOLDER=$DRAGON_DATA_FOLDER/resym_train

###########################################
# run this from the top-level dragon folder
###########################################

ORIG_DIR=`pwd`

# create wildebeest experiment
cd ./exps
wdb create import-dataset-binja binja_resym_trainbins.exp -p bin_folder=$BIN_FOLDER

# run experiment (import into Ghidra, extract ASTs and AST var data)
cd binja_resym_trainbins.exp
time wdb run -j$NJOBS

cd $ORIG_DIR
