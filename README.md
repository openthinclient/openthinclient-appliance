# openthinclient-appliance

[Packer](https://packer.io) templates to build the [openthinclient](http://openthinclient.org) appliance


### Environment

```shell
⁖ packer version
Packer v1.6.3
```

### Requirements

To create a successful build you need to place a openthinclient software installer in
the following folder:

* installers

    This folder should be used for the new installer
    

### Use existing template

To perform a build simply run the following commands:


#### Check syntax

```
$ packer validate otc-appliance_debian64.json
```

#### build virtualbox only

```
$ packer build -only=virtualbox-iso otc-appliance_debian64.json 
```

#### build vmware only

```
$ packer build -only=vmware-iso otc-appliance_debian64.json 
```

#### build for virtualbox and vmware 

```
$ packer build otc-appliance_debian64.json
```
