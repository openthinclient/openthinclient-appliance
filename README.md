# openthinclient-appliance

[Packer](https://packer.io) templates to build the [openthinclient](http://openthinclient.org) appliance


### Environment

```shell
⁖ packer version
Packer v0.12.1
```

### Requirements

To create a successful build you need to place a openthinclient software installer in
one of the following folders:

* installers

    This folder should be used for the new installer
    
* data/installer-legacy

    This folder will accept the old legacy installer as a jar file


### Use existing template

To perform a build simply run the following commands:


#### Check syntax

```
$ packer validate otc-appliance_debian32.json
```

#### build virtualbox only

```
$ packer build -only=virtualbox-iso otc-appliance_debian32.json 
```

#### build vmware only

```
$ packer build -only=vmware-iso otc-appliance_debian32.json 
```

#### build for virtualbox and vmware 

```
$ packer build otc-appliance_debian32.json
```
