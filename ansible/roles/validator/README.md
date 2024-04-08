# validator

This is an Ansible role for IPC Validator installation

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [validator_bin_repo_url](#validator_bin_repo_url)
  - [validator_bootstraps](#validator_bootstraps)
  - [validator_bottom_check_period](#validator_bottom_check_period)
  - [validator_cmt_p2p_host_port](#validator_cmt_p2p_host_port)
  - [validator_cmt_rpc_host_port](#validator_cmt_rpc_host_port)
  - [validator_default_address](#validator_default_address)
  - [validator_ethapi_host_port](#validator_ethapi_host_port)
  - [validator_fendermint_image_name](#validator_fendermint_image_name)
  - [validator_fendermint_image_url](#validator_fendermint_image_url)
  - [validator_ipc_repository_path](#validator_ipc_repository_path)
  - [validator_ipc_repository_url](#validator_ipc_repository_url)
  - [validator_ipc_repository_version](#validator_ipc_repository_version)
  - [validator_min_validator_stake](#validator_min_validator_stake)
  - [validator_min_validators](#validator_min_validators)
  - [validator_name](#validator_name)
  - [validator_package_dependencies_debian](#validator_package_dependencies_debian)
  - [validator_parent_gateway](#validator_parent_gateway)
  - [validator_parent_registry](#validator_parent_registry)
  - [validator_parent_subnet_id](#validator_parent_subnet_id)
  - [validator_permission_mode](#validator_permission_mode)
  - [validator_private_key_path](#validator_private_key_path)
  - [validator_resolver_bootstraps](#validator_resolver_bootstraps)
  - [validator_resolver_host_port](#validator_resolver_host_port)
  - [validator_secrets](#validator_secrets)
  - [validator_subnet_id](#validator_subnet_id)
  - [validator_supply_source_kind](#validator_supply_source_kind)
- [Discovered Tags](#discovered-tags)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### validator_bin_repo_url

`validator_bin_repo_url` is the url of archive
that contains pre-compiled ipc and fendermint binaries.

**_Type:_** string<br />

#### Default value

```YAML
validator_bin_repo_url: https://glif-ipc.s3.ap-northeast-1.amazonaws.com
```

### validator_bootstraps

`validator_bootstraps` is the node that validator
will use as a bootstrap.

**_Type:_** string<br />

#### Default value

```YAML
validator_bootstraps: <PLEASE PUT COMETBFT NODE ID of VALIDATOR-1>@validator-1-cometbft:26656
```

### validator_bottom_check_period

`validator_bottom_check_period` is the bottom-check
period of a validator.

**_Type:_** int<br />

#### Default value

```YAML
validator_bottom_check_period: 30
```

### validator_cmt_p2p_host_port

`validator_cmt_p2p_host_port` is a Comet BFT P2P port.

**_Type:_** integer<br />

#### Default value

```YAML
validator_cmt_p2p_host_port: '3305'
```

### validator_cmt_rpc_host_port

`validator_cmt_rpc_host_port` is a Comet BFT RPC port.

**_Type:_** integer<br />

#### Default value

```YAML
validator_cmt_rpc_host_port: '3306'
```

### validator_default_address

`validator_default_address` is the default address
ipc-cli will use in the --from flag.

**_Type:_** string<br />

#### Default value

```YAML
validator_default_address: '0xbc68608545c51873e1a3e864f7edfbcfe3d70ce7'
```

### validator_ethapi_host_port

`validator_ethapi_host_port` is a Fendermint Eth API port.

**_Type:_** integer<br />

#### Default value

```YAML
validator_ethapi_host_port: '8545'
```

### validator_fendermint_image_name

`validator_fendermint_image_name` is the name fendermint image
shall be tagged with.

**_Type:_** string<br />

#### Default value

```YAML
validator_fendermint_image_name: fendermint:latest
```

### validator_fendermint_image_url

`validator_fendermint_image_url` is the pre-built image of fendermint.

**_Type:_** string<br />

#### Default value

```YAML
validator_fendermint_image_url: glif/lotus:fendermint-amd64
```

### validator_ipc_repository_path

`validator_ipc_repository_path` is local path to
the ipc repository.

**_Type:_** string<br />

#### Default value

```YAML
validator_ipc_repository_path: /home/ubuntu/ipc
```

### validator_ipc_repository_url

`validator_ipc_repository_url` is the URL to the Git repository
that contains the IPC source code.

**_Type:_** string<br />

#### Default value

```YAML
validator_ipc_repository_url: https://github.com/consensus-shipyard/ipc.git
```

### validator_ipc_repository_version

`validator_ipc_repository_version` is the branch/tag/commit name to clone.

**_Type:_** string<br />

#### Default value

```YAML
validator_ipc_repository_version: main
```

### validator_min_validator_stake

`validator_min_validator_stake` is the minimum stake
of a validator in the subnet.

**_Type:_** int<br />

#### Default value

```YAML
validator_min_validator_stake: 1
```

### validator_min_validators

`validator_min_validators` is the minimum number
ov validators in the subnet.

**_Type:_** int<br />

#### Default value

```YAML
validator_min_validators: 4
```

### validator_name

`validator_name` is the name of the validator.

**_Type:_** string<br />

#### Default value

```YAML
validator_name: validator-1
```

### validator_package_dependencies_debian

`validator_package_dependencies_debian` is a list of packages
required to install IPC Validator on Debian-based Linux distributions.

**_Type:_** list<br />

#### Default value

```YAML
validator_package_dependencies_debian:
  - build-essential
  - bzr
  - ca-certificates
  - clang
  - cmake
  - curl
  - gcc
  - git
  - gnupg
  - hwloc
  - jq
  - libhwloc-dev
  - libssl-dev
  - pkg-config
  - protobuf-compiler
  - wget
```

### validator_parent_gateway

`validator_parent_gateway` is a gateway contract
address in the parent network.

**_Type:_** Etherium-like address<br />

#### Default value

```YAML
validator_parent_gateway: '0x0571602E01C06197A9284BBfcCA0092CBdC1f12A'
```

### validator_parent_registry

`validator_parent_registry` is a registry contract
address in the parent network.

**_Type:_** Etherium-like address<br />

#### Default value

```YAML
validator_parent_registry: '0x503C8C5C361f1c978eA9a0cC12629d4b05CA5317'
```

### validator_parent_subnet_id

#### Default value

```YAML
validator_parent_subnet_id: r314159
```

### validator_permission_mode

`validator_permission_mode` is the permission
mode of the subnet.

**_Type:_** string<br />

#### Default value

```YAML
validator_permission_mode: collateral
```

### validator_private_key_path

`validator_private_key_path` is the local path to the validator private key.

**_Type:_** local path<br />

#### Default value

```YAML
validator_private_key_path: /home/ubuntu/.ipc/validator_1
```

### validator_resolver_bootstraps

`validator_resolver_bootstraps` description

**_Type:_** type<br />

#### Default value

```YAML
validator_resolver_bootstraps: /dns/validator-1-fendermint/tcp/26655/p2p/<PLEASE PUT
  PEER_ID of VALIDATOR-1>
```

### validator_resolver_host_port

`validator_resolver_host_port` is a port number of
the resolver host.

**_Type:_** string<br />

#### Default value

```YAML
validator_resolver_host_port: '26655'
```

### validator_secrets

`validator_secrets` is a list of validator secrets.

**_Type:_** dict<br />

#### Default value

```YAML
validator_secrets: []
```

### validator_subnet_id

`validator_subnet_id` is the IPC subnet ID the validator has to be a part of.

**_Type:_** string<br />

#### Default value

```YAML
validator_subnet_id: t410fug7q7fgzeehfgr6qlubzs45z2sjzcbw3nbhpiyi
```

### validator_supply_source_kind

`validator_supply_source_kind` is the kind of
a supply source in the subnet.

**_Type:_** string<br />

#### Default value

```YAML
validator_supply_source_kind: native
```

## Discovered Tags

**_always_**

**_validator:create_subnet_**

**_validator:join_subnet_**

**_validator:prepare_**

**_validator:prune_**

**_validator:pull_bin_**

**_validator:start_**

**_validator:start_bootstrap_**

**_validator:start_relayer_**


## Dependencies

None.

## License

GPLv3

## Author

Ales Dumikau
