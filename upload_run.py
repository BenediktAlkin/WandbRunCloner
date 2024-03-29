from argparse import ArgumentParser
from pathlib import Path

import wandb
import yaml
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default="https://api.wandb.ai/")
    parser.add_argument("--entity", type=str, required=True)
    parser.add_argument("--project", type=str, required=True)
    parser.add_argument("--stage_id", type=str, required=True)
    parser.add_argument("--new_stage_id", action="store_true")
    return vars(parser.parse_args())


def main(host, entity, project, stage_id, new_stage_id):
    # setup
    print(f"connecting to {host}")
    wandb.login(host=host)
    # get output dir
    out = Path(f"temp/{stage_id}")

    # load config
    with open(out / "config.yaml") as f:
        config = yaml.safe_load(f)
    name = config.pop("name")

    # load summary
    with open(out / f"summary.yaml") as f:
        summary = yaml.safe_load(f)

    # load log
    with open(out / f"output.log") as f:
        log = f.read()
    lines = log.split("\n")

    # load history
    with open(out / f"history.yaml") as f:
        history = yaml.safe_load(f)

    # create run
    wandb.init(
        entity=entity,
        project=project,
        id=None if new_stage_id else stage_id,
        name=name,
        save_code=False,
    )
    wandb.config.update(config)
    wandb.summary.update(summary)
    # print logs
    for line in lines:
        print(line)
    # log history
    for row in tqdm(history):
        wandb.log(row)
    wandb.finish()
    print("fin")


if __name__ == "__main__":
    main(**parse_args())
