# Environment Configuration

* Manual installation on Ubuntu 16.04 OR
* Use Vagrant to setup a VM in VirtualBox

### Manual installation
All necessary dependencies can be installed running `setup.sh`.
Please refer to `.profile` for the location of `p4c`, `clang` and `klee` binaries.

### Using Vagrant
To install Vagrant, refer to the [official documentation](https://google.com).
Please install the [vagrant-disksize plugin](https://github.com/sprotheroe/vagrant-disksize) before running `vagrant up`.
```
vagrant plugin install vagrant-disksize
vagrant up
```
After logging in the VM using `vagrant ssh`, the assert-p4 files will be located under `/vagrant`.