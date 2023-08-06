<a id="autonomy.cli.helpers.deployment"></a>

# autonomy.cli.helpers.deployment

Deployment helpers.

<a id="autonomy.cli.helpers.deployment.run_deployment"></a>

#### run`_`deployment

```python
def run_deployment(build_dir: Path, no_recreate: bool = False, remove_orphans: bool = False) -> None
```

Run deployment.

<a id="autonomy.cli.helpers.deployment.build_deployment"></a>

#### build`_`deployment

```python
def build_deployment(keys_file: Path, build_dir: Path, deployment_type: str, dev_mode: bool, force_overwrite: bool, number_of_agents: Optional[int] = None, password: Optional[str] = None, packages_dir: Optional[Path] = None, open_aea_dir: Optional[Path] = None, open_autonomy_dir: Optional[Path] = None, agent_instances: Optional[List[str]] = None, log_level: str = INFO, substitute_env_vars: bool = False, image_version: Optional[str] = None, use_hardhat: bool = False, use_acn: bool = False) -> None
```

Build deployment.

<a id="autonomy.cli.helpers.deployment.update_multisig_address"></a>

#### update`_`multisig`_`address

```python
def update_multisig_address(service_path: Path, address: str) -> None
```

Update the multisig address on the service config.

<a id="autonomy.cli.helpers.deployment.build_and_deploy_from_token"></a>

#### build`_`and`_`deploy`_`from`_`token

```python
def build_and_deploy_from_token(token_id: int, keys_file: Path, chain_type: str, rpc_url: Optional[str], service_contract_address: Optional[str], skip_image: bool, n: Optional[int], aev: bool = False) -> None
```

Build and run deployment from tokenID.

