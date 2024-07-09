# blockscout

Ansible role to manage blockscout.

## Table of content

- [Requirements](#requirements)
- [Default Variables](#default-variables)
  - [blockscout_host](#blockscout_host)
  - [blockscout_jsonrpc_host](#blockscout_jsonrpc_host)
  - [blockscout_network_name](#blockscout_network_name)
  - [blockscout_repo_dest](#blockscout_repo_dest)
  - [blockscout_repo_url](#blockscout_repo_url)
  - [blockscout_repo_version](#blockscout_repo_version)
- [Discovered Tags](#discovered-tags)
- [Dependencies](#dependencies)
- [License](#license)
- [Author](#author)

---

## Requirements

- Minimum Ansible version: `2.1`

## Default Variables

### blockscout_host

`blockscout_host` is equivalent of BLOCKSCOUT_HOST env var.

**_Type:_** string<br />

#### Default value

```YAML
blockscout_host: explorer.mycelium.calibration.node.glif.io
```

### blockscout_jsonrpc_host

`blockscout_jsonrpc_host` is the domain name or ip address
of the json rpc endpoint.

**_Type:_** string<br />

#### Default value

```YAML
blockscout_jsonrpc_host: api.mycelium.calibration.node.glif.io
```

### blockscout_network_name

`blockscout_network_name` is the name of the network
blockscout is pointed to.

**_Type:_** string<br />

#### Default value

```YAML
blockscout_network_name: Mycelium Calibration
```

### blockscout_repo_dest

`blockscout_repo_dest` is the path
in the local filesystem where blockscout
repo will be cloned to.

**_Type:_** string<br />

#### Default value

```YAML
blockscout_repo_dest: default
```

### blockscout_repo_url

`blockscout_repo_url` is the url of
blockscout Git repository.

**_Type:_** string<br />

#### Default value

```YAML
blockscout_repo_url: default
```

### blockscout_repo_version

`blockscout_repo_version` is the commit/branch/tag
of the blockscout repo to clone.

**_Type:_** string<br />

#### Default value

```YAML
blockscout_repo_version: default
```

## Discovered Tags

**_blockscout:install_**

**_blockscout:reset_**

**_blockscout:update_**


## Dependencies

None.

## License

MIT

## Author

Ales Dumikau
