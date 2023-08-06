import sys

import click
from cli_passthrough import cli_passthrough
from cli_passthrough.utils import write_to_log
from slackd.utils import create_message
import requests
import json   


CONTEXT_SETTINGS = {"ignore_unknown_options": True, "allow_extra_args": True}

# CLI entry point
@click.command(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """Entry point"""
    write_to_log("\nNEW CMD = {}".format(" ".join(sys.argv[1:])))
    write_to_log("\nNEW CMD = {}".format(" ".join(sys.argv[1:])), "stderr")

    exit_status = cli_passthrough(" ".join(ctx.args), interactive=False)

    # TODO - call code to parse dbt results and send slack alerts here.
    url = webhook_url
    alert_text = ""
    f = open('./target/run_results.json')
    data = json.load(f)
    failed_message = [x for x in data["results"] if x["status"] != "pass"]
    for message in failed_message:
        alert_text = alert_text + (str(message) + "\n" + "@Xiuyang")

    send_message = create_message(
        table_name=data["args"]["select"][0],
        invocation_id=data["metadata"]["invocation_id"],
        timestamp=data["metadata"]["generated_at"]
    )
    x = requests.post(url, json = send_message)

    sys.exit(exit_status)

if __name__ == "__main__":
    cli(obj={})