from argparse import ArgumentParser
import wandb
import yaml
from pathlib import Path

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default="https://api.wandb.ai/")
    parser.add_argument("--entity", type=str, required=True)
    parser.add_argument("--project", type=str, required=True)
    parser.add_argument("--stage_id", type=str, required=True)
    parser.add_argument("--config", type=str)
    return vars(parser.parse_args())


def main(host, entity, project, stage_id, config):
    # setup
    print(f"connecting to {host}")
    wandb.login(host=host)
    api = wandb.Api()
    path = f"{entity}/{project}/{stage_id}"
    print(f"searching run {path}")
    run = api.run(path)
    if config is not None:
        with open(config) as f:
            config = yaml.safe_load(f)

    # make output dir
    out = Path(f"temp/{stage_id}")
    out.mkdir(parents=True)

    # download run config
    run_config = run.config
    if config is not None and "config" in config:
        for key in config["config"].get("delete", []):
            run_config.pop(key)
    # add name to config
    run_config["name"] = run.name
    with open(out / "config.yaml", "w") as f:
        yaml.safe_dump(run_config, f)

    # download summary
    summary = dict(run.summary)
    # remove weird objects
    summary.pop("_wandb")
    with open(out / f"summary.yaml", "w") as f:
        yaml.safe_dump(summary, f)

    # download log
    file = run.file("output.log")
    if file.sizeBytes > 0:
        file.download(out.as_posix(), replace=True)
        with open(out / f"output.log") as f:
            log = f.read()
        if config is not None and "log" in config:
            if "replace" in config["log"]:
                for replace in config["log"]["replace"]:
                    log = log.replace(replace["pattern"], replace["replacement"])
            if "delete" in config["log"]:
                lines = log.split("\n")
                for pattern in config["log"]["delete"]:
                    lines = [line for line in lines if pattern not in line]
                log = "\n".join(lines)
            with open(out / f"output.log", "w") as f:
                f.write(log)
    else:
        print(f"no stdout log found")

    # download metrics
    rows = []
    for row in run.scan_history():
        row = [item for item in row if item[0] != "_"]
        rows.append(row)
    with open(out / f"history.yaml", "w") as f:
        yaml.safe_dump(rows, f)

    print("fin")




if __name__ == "__main__":
    main(**parse_args())