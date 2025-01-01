
NJOBS=80
DRAGON_DATA_FOLDER=~/dragon_data
BENCHMARKS_FOLDER=$DRAGON_DATA_FOLDER/benchmarks

###########################################
# run this from the top-level dragon folder
###########################################

export_benchmark_asts () {
    bm_folder=$1
    bm_name=`basename $bm_folder`
    exp_folder="$bm_name"_benchmark.exp

    orig_dir=`pwd`

    echo "------------ Creating experiment for benchmark: $bm_name ------------"

    # create wildebeest experiment
    cd ./exps
    wdb create import-dataset $exp_folder -p bin_folder=$bm_folder

    # run experiment (import into Ghidra, extract ASTs and AST var data)
    cd $exp_folder
    time wdb run -j$NJOBS

    cd $orig_dir
}

for dir in "$BENCHMARKS_FOLDER"/*/     # list directories in the form "/tmp/dirname/"
do
    dir=${dir%*/}      # remove the trailing "/"
    export_benchmark_asts $dir
done
