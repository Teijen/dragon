
NJOBS=80
DRAGON_DATA_FOLDER=~/dragon_data
BIN_FOLDER=${dragon_data}/tydamin_sample

###########################################
# run this from the top-level dragon folder
###########################################

cd ./exps
wdb create import-dataset tydamin_sample.exp -p bin_folder=$BIN_FOLDER
cd tydamin_sample.exp

time wdb run -j$NJOBS
