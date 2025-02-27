# assert-p4

## Overview

assert-p4 is an assertion-based tool for verifying P4 programs using symbolic execution.

Using our assertion language, a P4 program can be annotated with assertions expressing general network correctness properties.

The annotated P4 program is then automatically transformed into a C model, which is symbolically executed using [KLEE](http://klee.github.io/).

If an assertion is violated in any of the possible execution paths of the P4 program, a message is displayed informing such violation.

## Virtual machine setup using Vagrant

* Install [vagrant-disksize plugin](https://github.com/sprotheroe/vagrant-disksize) before running `vagrant up`.
```
vagrant plugin install vagrant-disksize
vagrant up
```
* `setup.sh` installs dependencies on Ubuntu 16.04. The script appends lines to `~/.profile` making all required binaries available in `$PATH`.

| Software      | Version   |
| ------------- | --------- |
| Python        | 2.7       |
| p4c           | 0.1       |
| p4c-bm2-ss    | 0.0.5     |
| LLVM          | 3.4       |
| KLEE          | >1.3      |

By default, assert-p4 relies on [a modified version of KLEE 1.3](https://github.com/gnmartins/klee/tree/1.3.x) to display violated assertions. 
This version includes a new function called `klee_print_once`, which is used to display the symbolic execution results in a more readable format.
If you prefer to use a different version of KLEE, adjustments in the translated C model will be necessary in order to properly display the verification results.

* After logging in the VM using `vagrant ssh`, the assert-p4 files will be located under `/vagrant`.

## Running assert-p4

Pipeline:

1. Generating the JSON representation of the P4 software through `p4c-bm2-ss`
2. Translating the JSON file into a C model with `python src/P4_to_C.py`
3. Compiling the C model into LLVM bytecode with `clang`
4. Using `klee` to perform the symbolic execution of the bytecode

The above steps translate to the following commands:
```
p4c-bm2-ss /path/to/program.p4 --toJSON output.json
python src/P4_to_C.py output.json [/path/to/commands.txt]
clang -emit-llvm -g -c output.c
klee --search=dfs --no-output --optimize output.bc
```

Alternative one-shot command:
```
bash assert-p4.sh /path/to/program.p4 [/path/to/commands.txt]
```

There is also an _experimental_ Python script for running the tool, which can be used as follows:
```
./assert-p4.py /path/to/program.p4 [/path/to/commands.txt] [--help]
```

## Experiments

Inside the `experiments/case_studies` folder there are examples of programs verified with assert-p4.

For each case study, there is an annotated P4 program and a README.md file, which documents the meaning of each annotated assertion, the steps to verify the program, and the expected output of assert-p4.

## Validating C models

In this repository, we also present a script that performs the validation of the C models generated by assert-p4.

The validation process consists of checking whether the C model emits the same output packets as [BMv2](https://github.com/p4lang/behavioral-model) while processing test cases generated by [p4pktgen](https://github.com/p4pktgen/p4pktgen).

![validation-algorithm](/src/validation/validation-algorithm.png)

For further details on the algorithm, please refer to the thoroughly documented [validation script](/src/validation.py).

To validate models generated by assert-p4 for a P4 program, invoke the validation script as follows:
```
sudo ./src/validation.py /path/to/program.p4 [--p4c /path/to/p4c-bm2-ss] [--p4pktgen /path/to/p4pktgen] [--max-test-cases N] [--keep-files] [--help]
```

During runtime, the script outputs the result of each test separately indicating if it succeeded (i.e. the output packets were the same) or if it failed, in this case also showing the difference between the packets.

At the end, a summary of the validation process is shown, indicating the elapsed time and the percentage of successful tests, as exemplified below.
```
sudo ./src/validation.py ./experiments/case_studies/stag/stag.p4 --max-test-cases 16

...

###############################################################
### Summary
P4 Program: stag.p4
Total tests: 16

Successful tests: 16 (100.00%)
Failed tests: 0 (0.00%)
###############################################################
Elapsed time: 11.62 seconds
```

If you encounter any failed tests, please let us know so we can fix any inconsistencies with the C model being generated by assert-p4.

## Ongoing work

We are working to release optimizations and improvements for assert-p4.

These optimizations comprehend techniques such as program slicing and directed symbolic execution, which will accelerate the verification time of complex P4 programs (e.g. [switch.p4](https://github.com/p4lang/switch)).

## Features not supported

Some features from the P4 language are not supported by `assert-p4` yet. 
We intend to improve and extend the functionalities of this tool.

The currently unsupported features are:
* table annotations
* ternary matches
* range matches
* extern elements

## Contact information

Related papers:

* [Uncovering Bugs in P4 Programs with Assertion-based Verification, SOSR 2018](https://klevchen.ece.illinois.edu/pubs/assertp4-sosr18.pdf), older code repos:
	* https://github.com/LucasMFreire/assert-p4
	* https://github.com/ufrgs-networks-group/assert-p4
* [Verification of P4 Programs in Feasible Time using Assertions, CoNEXT 2018](https://marinho-barcellos.github.io/publication/2018-conext-neves/2018-conext-neves.pdf)

Please feel free to contact us should any questions arise. Your feedback is greatly appreciated.

| | |
| - | - |
| Gabriel Martins | <gabrielnmartins@gmail.com> |
| Marinho Barcellos | <marinho@inf.ufrgs.br> |
| Miguel Neves | <mcneves@inf.ufrgs.br> |
| | |
