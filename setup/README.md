# Setting up an environment for assert-p4

The following automated options are available:

* Bash script to install dependencies on Ubuntu 16.04
* Virtual machine setup using Vagrant

Please note that both setup methods will take a while to finish.

### Bash script
All necessary dependencies can be installed running `setup.sh`.

Please refer to `.profile` for the location of `p4c`, `clang` and `klee` binaries.

### Vagrant
To install Vagrant, please refer to the [official documentation](https://google.com).

Please install the [vagrant-disksize plugin](https://github.com/sprotheroe/vagrant-disksize) before running `vagrant up`.
```
vagrant plugin install vagrant-disksize
vagrant up
```
After logging in the VM using `vagrant ssh`, the assert-p4 files will be located under `/vagrant`.
