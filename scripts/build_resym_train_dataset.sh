
EXP_FOLDER=./exps/binja_resym_trainbins.exp
NUM_HOPS=5
DATASET_FOLDER=./binjaDatasets/resym_train_"$NUM_HOPS"hops

###########################################
# run this from the top-level dragon folder
###########################################

time dragon build --from-exps $DATASET_FOLDER $NUM_HOPS $EXP_FOLDER --func-list ./scripts/resym_train_funcs.csv
