# assert-p4

To translate a P4 program to a C model to be executed by [klee](https://github.com/klee/klee) from its *json* file:

`python src/P4_to_C.py <filename>.json [commands.txt]`

The json representations are obtained from the bmv2 backend of the [p4c](https://github.com/p4lang/p4c) compiler. To generate a json file, you need to build p4c and run:

`p4c/build/p4c-bm2-ss <input-filename>.p4 --toJSON <output-filename>.json`

### Running assert-p4

```
bash assert-p4.sh /path/to/program.p4 [/path/to/commands.txt]
```

or

```
p4c-bm2-ss filename.p4 --toJSON output.json
python src/P4_to_C.py output.json [/path/to/commands.txt] > output.c
clang -emit-llvm -g -c output.c
klee --search=dfs --no-output --optimize output.bc
```

### Dependencies

| Software      | Version   |
| ------------- | --------- |
| p4c           | 0.1       |
| p4c-bm2-ss    | 0.0.5     |
| llvm          | 3.4       |
| klee          | >1.3      |

### Experiments

The experiments folder is organized into a benchmark and a case\_studies folder.

There are 4 different benchmarks: Tables, Actions, Rules, and Assertions. Each one is contained in its own subfolder, which has the appropriate scripts to generate the programs, execute the experiment, and create gnuplot graphs. The gen\_parallel.py script is used to create submodels for parallelization. The parallel\_benchmark.py script can be used to execute all benchmarks with and without optimizations.

Each case study folder contains the used C models and scripts to execute them. You can also find C models with constraint optimizations, submodels for parallelization, and their combination. The run\_klee.sh scripts are used to execute the single threaded models, and the parallel\_klee.sh scripts are used to run the submodels concurrently. 

