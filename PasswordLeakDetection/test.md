Manifest
===============

1. [Overview](#overview)
2. [Manifest Data Format](#manifest-data-format)
3. [Manifest defaults](#manifest-defaults)
4. [Infrastructure images](#infrastructure-images)
5. [Service-Entry images](#service-entry-images)
6. [Using Create Parameters In Image](#using-create-parameters-in-image)


<a name="overview"></a>
Overview
========

Manifest is used to provide C-MEP information about the location and version of Pre-OnBoarding images to pull and use.

Those images are:
* Connector
* MQTT Broker
* Cert-issuer (CSH only)
* Module Manager (optional)

Manifest also allows pulling image not specified above. In that case, container using this particular image will be created and started.
> A container created that way can by configured using `create_parameters_v3` image label set in the container's image. For information about how to set create parameters label, please check "Using Create Parameters In Image" section.

> Container started this way, will be removed at the end of `register_device` execution.

> Note that order of images list in manifest is relevant: it will be reflected as pull (and start) order.

Manifest allow also to pull service-entry images without creating and starting them.
> Note For this to work, a keyword `service_entry` should be set as `true`.
> For more information about service-entry images, please check [Running Service Entry Commands Using Command Line](C-MEP-Run-Service-Entry.md) page

Manifests are delivered as json files from artifactory or base64 encoded strings

<a name="manifest-data-format"></a>
Manifest Data Format:
=====================
#### Data format:
```json
{
  "name": "<descriptive name>",
  "images": [
     {
        "name": "<image name>",
        "location": "<image location on registry>",
        "tag": "<image tag>",
        "service_entry": true/false
     }
  ]
}
```
Fields description:
* `name` is a descriptive name of the manifest. It may include a string with information allowing identifying version of the manifest.
* `images` is the list of images to pull during the pre-onboarding process.
    * `images.name` is the name of image container to create and use.
    * `images.location` is repo path to the image on the registry.
    * `images.tag` is the Image tag.
    * `images.service_entry` specify this image as a service_entry image if set to `true`

#### Example #1:
vanguard-infra-generic/cmep/<CMEP_RELEASE>/cmep-manifest-csh.json
```json
{
  "name": "3.0.102",
  "images": [
    {
      "tag": "3.0.102",
      "name": "mqtt-broker",
      "location": "msi/vanguard-infra/cmep/mqtt-broker"
    },
    {
      "tag": "2.0.3",
      "name": "certificate-issuer",
      "location": "msi/vanguard-infra/cmep/certificate_issuer"
    },
    {
      "tag": "1.3.4",
      "name": "csh_connector",
      "location": "msi/vanguard-infra/cmep/csh_connector"
    },
    {
      "tag": "3.0.102",
      "name": "module_manager",
      "location": "msi/vanguard-infra/cmep/module_manager"
    }
  ]
}
```

#### Example #2:

```json
{
	"name": "cmep-3.0.102",
	"images": [
		{
			"name": "mqtt-broker",
			"location": "msi/vanguard-infra/cmep/mqtt-broker",
			"tag": "3.0.102"
		},
		{
			"name": "module_manager",
			"location": "msi/vanguard-infra/cmep/module_manager",
			"tag": "3.0.102"
		},
		{
			"name": "onprem-connector",
			"location": "msi/vanguard-infra/cmep/cmep_connector",
			"tag": "3.0.102"
		}
	]
}
```

> Note: An `onprem` manifest doesn't need to provide a `certificate-issuer` part.

#### Example #3:

```json
{
    "name": "cmep-3.0.48",
    "images": [
        {
            "tag": "3.0.48",
            "name": "onprem-connector",
            "location": "msi/vanguard-infra/cmep/cmep_connector"
        },
        {
            "tag": "3.0.48",
            "name": "mqtt-broker",
            "location": "msi/vanguard-infra/cmep/mqtt-broker"
        },
        {
            "tag": "3.0.48",
            "name": "foo-bar",
            "location": "msi/vanguard-infra/cmep/foo"
        },
        {
            "tag": "2.3.17",
            "name": "foo-bar-baz",
            "location": "msi/vanguard-infra/cmep/foo"
        }
    ]
}
```

> Container **foo-bar** and **foo-bar-baz** will be created and started apart from pulling their images. These containers will be removed after finish, regardless of their exit code. Images used by containers will also be removed.

#### Example #4:

```json
{
    "name": "cmep-3.0.48",
    "images": [
        {
            "tag": "3.0.48",
            "name": "onprem-connector",
            "location": "msi/vanguard-infra/cmep/cmep_connector"
        },
        {
            "tag": "3.0.48",
            "name": "mqtt-broker",
            "location": "msi/vanguard-infra/cmep/mqtt-broker"
        },
        {
            "tag": "v1",
            "name": "Service entry image",
            "location": "msi/vanguard-cmep/test-images/service-entry",
            "service_entry": true
        },
        {
            "tag": "v2",
            "name": "Another Service entry image",
            "location": "msi/vanguard-cmep/test-images/service-entry",
            "service_entry": true
        }
    ]
}
```

> Images `msi/vanguard-cmep/test-images/service-entry:v1` and `msi/vanguard-cmep/test-images/service-entry:v2` will be downloaded only.

<a name="manifest-defaults"></a>
Manifest defaults
=====================
In case of manifest was required, but it was not provided to cmep script, default images will be used.

* For CSH connected: `/artifactory/vanguard-infra-generic/<CMEP_VERSION>/cmep-manifest-csh.json`
* For OnPrem `/artifactory/vanguard-infra-generic/<CMEP_VERSION>/cmep-manifest-onprem.json`

<a name="infrastructure-images"></a>
Infrastructure images
=====================
By default, images mentioned in manifest are only used **until proper DEV_CFG is downloaded and parsed**. There is an option to override this behavior:
- *certificate_issuer*, *mqtt_broker* and *configuration_connector* have optional **infrastructure_image** (true,false) field in DEV_CFG
- *csh_connector*, *onprem-connector*, *mqtt-broker* and *certificate_issuer* have option **--infrastructure_image** label (true,false) in their images

> **infrastructure_image** from DEV_CFG overrides image label


<a name="service-entry-images"></a>
Service-Entry images
====================
Service-entry images are pulled **if provided during register_device or upgrade** and are not removed, these images will be marked as the active service-entry image for their respective label.
If more than one service-entry image exist on the host-level with the same label, then the one defined in manifest will be used when running service-entry.
A host_task service exists to update service-entry images in the current manifest


<a name="using-create-parameters-in-image"></a>
Using Create Parameters In Image
==================================
Create parameters of containers created from manifest data can be provided by adding a label `create_parameters_v3` in container's image.

`create_parameters_v3` label should contain a dictionary similar to application configuration in DEV_CFG base64 decoded.

For Example

A container with the below desired create parameters,
```json
{
  "capabilities": ["NET_BIND_SERVICE"],
  "client_api": "yes",
  "cmd": "/bin/sleep 42",
  "domain": "alpha.legion.com",
  "environment_variables": {"env_1": "Alpharius is that you ?!"},
  "healthcheck": {"cmd": "/bin/true", "interval": "20s", "timeout": "1s", "retries": 2},
  "hostname": "hydra.dominatus",
  "init_proc": true,
  "limits": {
    "ulimit_nofile": "2048:4096",
    "max_memory": "402020k",
    "max_pids": 20,
    "cpu_shares": 400,
    "cpuset": "1"
  },
  "sysctl": ["net.ipv4.ip_local_port_range=50000 65535"],
  "mounts": {
    "volumes": {
      "exclusive": ["/omegon:rw"]
    }
  },
  "network_parameters": {"expose": ["0.0.0.0:20202:20202/tcp"]}
}
```

It will be saved as image label `create_parameters_v3`
```shell
[root@g13-xbwk36-podman-latest ~]# podman inspect 0ed673fd0cf6945b4c7d6465f4355d2f90f42e36311a0b33200b705022a05b63 --format '{{.Config.Labels.create_parameters_v3}}'
ewogICAgImNhcGFiaWxpdGllcyI6IFsKICAgICAgICAiTkVUX0JJTkRfU0VSVklDRSIKICAgIF0s
CiAgICAiY2xpZW50X2FwaSI6ICJ5ZXMiLAogICAgImNtZCI6ICIvYmluL3NsZWVwIDQyIiwKICAg
ICJkb21haW4iOiAiYWxwaGEubGVnaW9uLmNvbSIsCiAgICAiZW52aXJvbm1lbnRfdmFyaWFibGVz
IjogewogICAgICAgICJlbnZfMSI6ICJBbHBoYXJpdXMgaXMgdGhhdCB5b3UgPyEiCiAgICB9LAog
ICAgImhlYWx0aGNoZWNrIjogewogICAgICAgICJjbWQiOiAiL2Jpbi90cnVlIiwKICAgICAgICAi
aW50ZXJ2YWwiOiAiMjBzIiwKICAgICAgICAidGltZW91dCI6ICIxcyIsCiAgICAgICAgInJldHJp
ZXMiOiAyCiAgICB9LAogICAgImhvc3RuYW1lIjogImh5ZHJhLmRvbWluYXR1cyIsCiAgICAiaW5p
dF9wcm9jIjogdHJ1ZSwKICAgICJsaW1pdHMiOiB7CiAgICAgICAgInVsaW1pdF9ub2ZpbGUiOiAi
MjA0ODo0MDk2IiwKICAgICAgICAibWF4X21lbW9yeSI6ICI0MDIwMjBrIiwKICAgICAgICAibWF4
X3BpZHMiOiAyMCwKICAgICAgICAiY3B1X3NoYXJlcyI6IDQwMCwKICAgICAgICAiY3B1c2V0Ijog
IjEiCiAgICB9LAogICAgInN5c2N0bCI6IFsKICAgICAgICAibmV0LmlwdjQuaXBfbG9jYWxfcG9y
dF9yYW5nZT01MDAwMCA2NTUzNSIKICAgIF0sCiAgICAibW91bnRzIjogewogICAgICAgICJ2b2x1
bWVzIjogewogICAgICAgICAgICAiZXhjbHVzaXZlIjogWwogICAgICAgICAgICAgICAgIi9vbWVn
b246cnciCiAgICAgICAgICAgIF0KICAgICAgICB9CiAgICB9LAogICAgIm5ldHdvcmtfcGFyYW1l
dGVycyI6IHsKICAgICAgICAiZXhwb3NlIjogWwogICAgICAgICAgICAiMC4wLjAuMDoyMDIwMjoy
MDIwMi90Y3AiCiAgICAgICAgXQogICAgfQp9
```