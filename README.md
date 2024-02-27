# WandbRunCloner

Downloads config/summary/log from wandb and creates new runs with the downloaded data.

## Download

The command `python download_run.py --entity ENTITY --project PROJECT --stage_id STAGE_ID`
will download `config.yaml`, `summary.yaml` and `output.log` into the director `temp/STAGE_ID`.

To remove/change things before saving the data to files, `--config example_config.yaml` can be passed.
For more details on how to customize your config see `example_config.yaml`.


## Upload

Upload the downloaded runs to another project with:
`python upload_run.py --entity ENTITY --project PROJECT --stage_id STAGE_ID`.
If you encounter `wandb: ERROR Error while calling W&B API: run ... was previously created and deleted; try a new run name (<Response [409]>)`
set the flag `--new_stage_id`.

## Switch W&B accounts
To switch between W&B accounts (for example to download it from one account and then upload it to another one)
use `wandb login --relogin`.