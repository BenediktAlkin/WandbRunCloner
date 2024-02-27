# WandbRunCloner

Downloads config/summary/log from wandb and creates new runs with the downloaded data.

## Download

The command `python download_run.py --entity ENTITY --project PROJECT --stage_id STAGE_ID`
will download `config.yaml`, `summary.yaml` and `output.log` into the director `temp/STAGE_ID`.

To remove/change things before saving the data to files, `--config example_config.yaml` can be passed.
For more details on how to customize your config see `example_config.yaml`.


## Upload

TODO