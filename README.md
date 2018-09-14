# assert-p4

To translate a P4 program to a C model to be executed by [klee](https://github.com/klee/klee) from its *json* file:

`python src/P4_to_C.py <filename>.json [commands.txt]`

The json representations are obtained from the bmv2 backend of the [p4c](https://github.com/p4lang/p4c) compiler. To generate a json file, you need to build p4c and run:

`p4c/build/p4c-bm2-ss <input-filename>.p4 --toJSON <output-filename>.json`

## Running assert-p4

```
bash assert-p4.sh /path/to/program.p4 [/path/to/commands.txt]
```

or

```
p4c-bm2-ss filename.p4 --toJSON output.json
python src/P4_to_C.py output.json [/path/to/commands.txt]
clang -emit-llvm -g -c output.c
klee --search=dfs --no-output --optimize output.bc
```

## Dependencies

| Software      | Version   |
| ------------- | --------- |
| p4c           | 0.1       |
| p4c-bm2-ss    | 0.0.5     |
| LLVM          | 3.4       |
| KLEE          | >1.3      |

## Setting up an environment for assert-p4

The following automated options are available to setup an environment for assert-p4:

* Bash script to install dependencies on Ubuntu 16.04
* Virtual machine setup using Vagrant

Please note that both setup methods will take a while to finish.

#### Bash script
All necessary dependencies can be installed running `setup.sh`.

Please refer to `.profile` for the location of `p4c`, `clang` and `klee` binaries.

#### Vagrant
To install Vagrant, please refer to the [official documentation](https://google.com).

Please install the [vagrant-disksize plugin](https://github.com/sprotheroe/vagrant-disksize) before running `vagrant up`.
```
vagrant plugin install vagrant-disksize
vagrant up
```
After logging in the VM using `vagrant ssh`, the assert-p4 files will be located under `/vagrant`.

#### KLEE modifications for assert-p4

By default, assert-p4 relies on [a modified version of KLEE 1.3](https://github.com/gnmartins/klee/tree/1.3.x) to display violated assertions. 

This version includes a new function called `klee_print_once` which is used to display the symbolic execution results in a more user friendly way.

If you prefer to use a different version of KLEE, adjustments in the translated C model will be necessary in order to properly display the verification results.

## Experiments

The experiments folder is organized into a benchmark and a case\_studies folder.

There are 4 different benchmarks: Tables, Actions, Rules, and Assertions. Each one is contained in its own subfolder, which has the appropriate scripts to generate the programs, execute the experiment, and create gnuplot graphs. The gen\_parallel.py script is used to create submodels for parallelization. The parallel\_benchmark.py script can be used to execute all benchmarks with and without optimizations.

Each case study folder contains the used C models and scripts to execute them. You can also find C models with constraint optimizations, submodels for parallelization, and their combination. The run\_klee.sh scripts are used to execute the single threaded models, and the parallel\_klee.sh scripts are used to run the submodels concurrently. 
