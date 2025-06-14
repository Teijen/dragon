
EXP_FOLDER=./exps/binja_tydamin_sample.exp
NUM_HOPS=5
DATASET_FOLDER=./binjaDatasets/tydamin_sample_"$NUM_HOPS"hops
TEST_SPLIT=0.1

###########################################
# run this from the top-level dragon folder
###########################################

time dragon build --from-exps $DATASET_FOLDER $NUM_HOPS $EXP_FOLDER --split-test $TEST_SPLIT --dedup-funcs
