import click
import requests
import json
from utils import create_message

@click.command()
@click.option('--webhook_url', default="")

def send_alert(webhook_url):
    """Simple program that greets NAME for a total of COUNT times."""

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

if __name__ == '__main__':
    send_alert()