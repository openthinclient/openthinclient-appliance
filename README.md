# openthinclient - Virtual Appliance

[Packer](https://packer.io) templates to build the [openthinclient](http://openthinclient.org) Virtual Appliance


### Environment

```
⁖ packer version
Packer v1.8.3
```

### Requirements

You need to place a openthinclient software installer in the following folder to create a successful build:

```
<path to virtual appliance>/installers
```
   
   
### Usage

ℹ Before starting the build process change to the directory of the Virtual Appliance.

This is the first command that should be executed when working with a new
or existing template.

```
packer init [options] otc-appliance_debian.pkr.hcl
```

Install all the missing plugins required in a Packer config. Note that Packer
does not have a state.

This command is always safe to run multiple times. Though subsequent runs may
give errors, this command will never delete anything.


```
Options:
  -upgrade          On top of installing missing plugins, update
                    installed plugins to the latest available
                    version, if there is a new higher one. Note that
                    this still takes into consideration the version
                    constraint of the config.

Helpful commands:

    build           build image(s) from template
    console         creates a console for testing variable interpolation
    init            Install missing plugins or upgrade plugins
    inspect         see components of a template
    plugins         Interact with Packer plugins and catalog
    validate        check that a template is valid
```

This is the second command that should be executed to check that
 a template is valid.
```
packer validate otc-appliance_debian.pkr.hcl
```

#### VirtualBox

```
packer build -only=virtualbox-iso.vbox otc-appliance_debian.pkr.hcl 
```

#### VMware

```
packer build -only=vmware-iso.vmware otc-appliance_debian.pkr.hcl 
```

#### Hyper-V

```
packer build -only=hyperv-iso.hyperv otc-appliance_debian.pkr.hcl 
```

#### VirtualBox and VMware

```
packer build -except=hyperv-iso.hyperv otc-appliance_debian.pkr.hcl
```