# assert-p4

`assert-p4` is an assertion-based tool for verification of P4 programs using symbolic execution.

Using our assertion language, a P4 program can be annotated with assertions expressing general network correctness properties.

The annotated P4 program is then automatically transformed into a C model, which is symbolically executed using [KLEE](http://klee.github.io/).

If an assertion is violated in any of the possible execution paths of the P4 program, a message is displayed informing such violation.

## Setup

The following automated options are available to setup an environment for assert-p4:

* Bash script to install dependencies on Ubuntu 16.04
* Virtual machine setup using Vagrant

Please note that both setup methods will take a while to finish.

### Dependencies

| Software      | Version   |
| ------------- | --------- |
| Python        | 2.7       |
| p4c           | 0.1       |
| p4c-bm2-ss    | 0.0.5     |
| LLVM          | 3.4       |
| KLEE          | >1.3      |

#### KLEE modifications for assert-p4

By default, assert-p4 relies on [a modified version of KLEE 1.3](https://github.com/gnmartins/klee/tree/1.3.x) to display violated assertions. 

This version includes a new function called `klee_print_once`, which is used to display the symbolic execution results in a more readable format.

If you prefer to use a different version of KLEE, adjustments in the translated C model will be necessary in order to properly display the verification results.

### Bash script for Ubuntu 16.04

All necessary dependencies can be installed running `setup.sh`.

The script appends lines to `~/.profile` making all required binaries available in `$PATH`.

### Vagrant

To install Vagrant, please refer to the [official documentation](https://www.vagrantup.com/docs/installation/).

Please install the [vagrant-disksize plugin](https://github.com/sprotheroe/vagrant-disksize) before running `vagrant up`.
```
vagrant plugin install vagrant-disksize
vagrant up
```
After logging in the VM using `vagrant ssh`, the assert-p4 files will be located under `/vagrant`.

The binaries for all required softwares will be available in `$PATH`.

## Running assert-p4

Running assert-p4 consists of:
1. Generating the JSON representation of the P4 software through `p4c-bm2-ss`
2. Translating the JSON file into a C model with `python src/P4_to_C.py`
3. Compiling the C model into LLVM bytecode with `clang`
4. Using `klee` to perform the symbolic execution of the bytecode

Assuming all required dependencies are available in your `$PATH`, the above steps translate to the following commands:
```
p4c-bm2-ss /path/to/program.p4 --toJSON output.json
python src/P4_to_C.py output.json [/path/to/commands.txt]
clang -emit-llvm -g -c output.c
klee --search=dfs --no-output --optimize output.bc
```

Alternatively, you can run the `assert-p4.sh` script from the root directory of this repository:
```
bash assert-p4.sh /path/to/program.p4 [/path/to/commands.txt]
```

## Experiments

Navigating to `experiments/case_studies`, there is a folder for each case studied.

Inside each folder, you will find:
* an annotated P4 program
* the JSON representation generated with `p4c-bm2-ss`
* the translated C model

Along with these files, documentation is avaiable describing the software, the assertions annotated within the program, and the expected output of the verification process.

## Ongoing work

We are working to release optimizations and improvements for `assert-p4`.

These optimizations comprehend techniques such as program slicing and directed symbolic execution, which will accelerate the verification time of complex P4 programs (e.g. [switch.p4](https://github.com/p4lang/switch)).

## Features not supported

Some features from the P4 language are not supported by `assert-p4` yet. 
We intend to improve and extend the functionalities of this tool.

The currently unsupported features are:
* table annotations
* ternary matches
* range matches
* _extern_ elements *(WORDING)*

## Contact information

Please feel free to contact us should any questions arise. Your feedback is greatly appreciated.

| | |
| - | - |
| Gabriel Martins | <gnmartins@inf.ufrgs.br> |
| Marinho Barcellos | <marinho@inf.ufrgs.br> |
| Miguel Neves | <mcneves@inf.ufrgs.br> |
| | |
