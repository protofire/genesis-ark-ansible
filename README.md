

# IPC Subnet Creation Microservice

This microservice is designed to create an IPC subnet based on user-provided parameters. It uses Ansible as the underlying automation tool and is written in Python.

<!-- vscode-markdown-toc -->
* [Architecture](#Architecture)
* [Usage](#Usage)
	* [Prerequisites](#Prerequisites)
* [Available Commands](#AvailableCommands)
* [Configuration](#Configuration)
	* [API Config](#APIConfig)
	* [Ansible Config](#AnsibleConfig)
		* [Validator Role](#ValidatorRole)
	* [Runner CLI](#RunnerCLI)
		* [User Parameters](#UserParameters)
		* [Infrastructure Config](#InfrastructureConfig)
* [Requirements](#Requirements)
* [Contributing](#Contributing)

<!-- vscode-markdown-toc-config
	numbering=false
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->

## <a name='Architecture'></a>Architecture

The microservice consists of several components:

- `cli/runner`: This module contains the Runner CLI - a command-line tool for interacting with the microservice API.
- `ansible/roles`: This directory contains Ansible roles that define the tasks required to create an IPC subnet.
- `app/v1`: This module contains Flask-based APIs for interacting with the microservice.

## <a name='Usage'></a>Usage

To use this microservice, you'll need to complete the following prerequisites:

### <a name='Prerequisites'></a>Prerequisites

1. **Start MongoDB**: Make sure MongoDB is running on your system. You can use Docker Compose to start MongoDB in detached mode:

```bash
docker-compose up mongo -d
```

2. **Start the API**: Start the Flask API:

```bash
flask --app app run --debug
```

3. **Install the Runner CLI**: Install the Runner CLI using pip:

```bash
pip install --editable .
```

Once you've completed these steps, you can use the Runner CLI to interact with the microservice.

## <a name='AvailableCommands'></a>Available Commands

The following commands are available:

- `runner subnets create`: Creates a new IPC subnet based on the provided parameters.
- `runner subnets delete`: Deletes an existing IPC subnet.
- `runner subnets install-blockscout`: Installs Blockscout on the created subnet.
- `runner subnets reset-blockscout`: Resets Blockscout on the created subnet.
- `runner subnets update-blockscout`: Updates Blockscout on the created subnet.

## <a name='Configuration'></a>Configuration

The microservice uses a combination of configuration files and environment variables to manage its settings.

### <a name='APIConfig'></a>API Config

File location: [app/config.py](app/config.py)

| Config Option | Description | Default Value |
| --- | --- | --- |
| DEBUG | Enable debug mode | False |
| SECRET_KEY | Secret key for the application | os.environ.get("APP_SECRET_KEY", "dev") |
| INVENTORIES_DIR | Directory path for inventories | {project_root}/ansible/inventories |
| PRIVATE_DATA_DIR | Directory path for private data | {project_root}/ansible/jobs |
| PLAYBOOKS_DIR | Directory path for playbooks | {project_root}/ansible/playbooks |
| MONGO_URI | MongoDB connection URI | mongodb://root:root@localhost/admin |
| ROLES_PATH | Directory path for Ansible roles | {project_root}/ansible/roles |
| MAINNET_RPC_URL | Mainnet RPC URL | https://api.node.glif.io/rpc/v1 |
| CALIBNET_RPC_URL | Calibnet RPC URL | https://api.calibration.node.glif.io/rpc/v1 |
| DEVELOPMENT | Enable development mode | False (only set to True in DevelopmentConfig) |

Note that the `project_root` variable is used to construct the directory paths for inventories, private data, playbooks, and roles. The DEVELOPMENT config option is only set to True in the DevelopmentConfig class.

### <a name='AnsibleConfig'></a>Ansible Config

#### <a name='ValidatorRole'></a>Validator Role

File location: [ansible/roles/validator/defaults/main.yml](ansible/roles/validator/defaults/main.yml)

| Config Option | Description | Default Value |
| --- | --- | --- |
| validator_fendermint_image_url | Pre-built image of fendermint | glif/lotus:fendermint-amd64 |
| validator_fendermint_image_name | Name fendermint image shall be tagged with | fendermint:latest |
| validator_bin_repo_url | URL of archive containing pre-compiled ipc and fendermint binaries | https://glif-ipc.s3.ap-northeast-1.amazonaws.com |
| validator_nodejs_version | Version of nodejs required by contracts | 18 |
| validator_private_key_path | Local path to the validator private key | /home/ubuntu/.ipc/validator_1 |
| validator_parent_subnet_id | IPC parent subnet ID the validator subnet belongs to | r314159 |
| validator_subnet_id | IPC subnet ID the validator has to be a part of | t410fug7q7fgzeehfgr6qlubzs45z2sjzcbw3nbhpiyi |
| validator_cmt_p2p_host_port | Comet BFT P2P port | 26656 |
| validator_cmt_rpc_host_port | Comet BFT RPC port | 26657 |
| validator_ethapi_host_port | Fendermint Eth API port | 8545 |
| validator_bootstraps | Node that validator will use as a bootstrap | <PLEASE PUT COMETBFT NODE ID of VALIDATOR-1>@validator-1-cometbft:26656 |
| validator_resolver_bootstraps | Resolver bootstraps for the validator | /dns/validator-1-fendermint/tcp/26655/p2p/<PLEASE PUT PEER_ID of VALIDATOR-1> |
| validator_default_address | Default address ipc-cli will use in the --from flag | 0xbc68608545c51873e1a3e864f7edfbcfe3d70ce7 |
| validator_secrets | List of validator secrets | [] |
| validator_supply_source_kind | Kind of supply source in the subnet | native |
| validator_permission_mode | Permission mode of the subnet | collateral |
| validator_ipc_repository_path | Local path to the ipc repository | /home/ubuntu/ipc |
| validator_ipc_repository_url | URL of the ipc repository | https://github.com/consensus-shipyard/ipc.git |
| validator_ipc_repository_version | Version of the ipc repository | main |
| validator_min_validator_stake | Minimum validator stake | 1 |
| validator_min_validators | Minimum number of validators | 4 |
| validator_name | Name of the validator | validator-1 |
| validator_package_dependencies_debian | Debian package dependencies for the validator | ["git", "curl", "wget", "apt-transport-https", "ca-certificates", "software-properties-common"] |
| validator_parent_gateway | Parent gateway for the validator | 0x6d25fbFac9e6215E03C687E54F7c74f489949EaF |
| validator_parent_registry | Parent registry for the validator | 0xc938B2B862d4Ef9896E641b3f1269DabFB2D2103 |
| validator_resolver_host_port | Resolver host and port for the validator | 26655 |

Please note that some of these variables have placeholder values that need to be replaced with actual values.

Also note that the role does not build the IPC Stack but pulls it from the S3 repository managed by Glif. That allows for faster node launch.

**IMPORTANT**: You have to deploy the registry and gateway contracts before you attempt to create a subnet using them.

### <a name='RunnerCLI'></a>Runner CLI

This microservice is still a work in progress! To get started, you can manually specify user parameters and infra configuration in the [cli/runner/subnets/utils.py](cli/runner/subnets/utils.py) file.

#### <a name='UserParameters'></a>User Parameters

##### Top-Level Fields

| Field | Description |
| --- | --- |
| id | Unique identifier |
| appChainName | Application chain name |
| networkTypeFor | Network type for |
| isPrivate | Whether the network is private |
| networkType | Type of network (e.g. "fvm") |
| minStake | Minimum stake required |
| bottomUp | Bottom-up value |
| topDown | Top-down value |
| state | Current state (e.g. "inProgress") |
| userId | User ID associated with the request |

##### Nodes Array

| Field | Description |
| --- | --- |
| id | Unique node identifier |
| isArchive | Whether the node is archival |
| name | Node name (e.g. "validator_1") |
| cpu | CPU specification |
| memory | Memory specification |
| location | Geographic location (e.g. "us-east-1") |
| cloud | Cloud provider (e.g. "AWS") |
| createdAt | Timestamp when the node was created |
| updatedAt | Timestamp when the node was last updated |
| PrivateKey | Private key associated with the node |
| stake | Stake value associated with the node |

#### <a name='InfrastructureConfig'></a>Infrastructure Config

##### Top-Level Fields

| Field | Description |
| --- | --- |
| _id | Unique identifier |
| project_id | Project ID associated with the request |
| customer_id | Customer ID associated with the request |
| infrastructurestatus | Current infrastructure status (e.g. "CREATION_INITIALIZED") |

##### Instance Connections Array

| Field | Description |
| --- | --- |
| nodeId | Unique node identifier |
| ipAddress | IP address associated with the node |

## <a name='Requirements'></a>Requirements
The following dependencies are required to run this microservice:

- flask
- ansible-runner
- jsonschema
- toml
- PyYAML
- requests
- pymongo[srv]
- Flask-PyMongo
- click
- eth-keys
- web3

You can install these dependencies using `pip` and the `requirements.txt` file.

## <a name='Contributing'></a>Contributing

Contributions to this microservice are welcome! If you'd like to contribute, please fork this repository and submit a pull request with your changes.