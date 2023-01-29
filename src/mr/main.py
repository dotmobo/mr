import configparser
import click
from datetime import datetime
from .bcolors import bcolors
from .gitlab import get_response_from_gitlab

@click.command()
@click.option('--wip', is_flag=True, show_default=True, default=False, help='Include WIP MRs')
def run(wip):
    config = configparser.ConfigParser()
    config.read("config.ini")
    url = config["gitlab"]["url"]
    token = config["gitlab"]["token"]

    try:
        response = get_response_from_gitlab(url, token)
    except Exception as e:
        click.echo(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")
        return

    message = f"\n{bcolors.OKGREEN}Merge requests au {datetime.strftime(datetime.now(), '%d/%m/%Y')}{bcolors.ENDC}\n"
    message += f"{bcolors.OKBLUE}WIP: {wip}{bcolors.ENDC}\n"

    for project_name, mrs in response.items():
        filtered_mrs = [m for m in mrs if wip or (("WIP") not in m.title and ("Draft") not in m.title)]
        if len(filtered_mrs) > 0:
            message += f"\n{bcolors.WARNING}{project_name}{bcolors.ENDC}:\n"
            for mr in filtered_mrs:
                valid = (
                    "✅"
                    if mr.merge_status == "can_be_merged" and mr.has_conflicts is False
                    else "❌"
                )
                upvotes = f"{bcolors.OKGREEN}+{mr.upvotes}{bcolors.ENDC}"
                downvotes = f"{bcolors.FAIL}-{mr.downvotes}{bcolors.ENDC}"
                approved = (
                    "🙋"
                    if mr.approvals.get().approved is True
                    else "🙅"
                )
                message += f"{valid} {approved} {upvotes}/{downvotes} {bcolors.OKCYAN}{mr.source_branch} ⇢ {mr.target_branch}{bcolors.OKCYAN} {bcolors.OKBLUE}{mr.title}{bcolors.ENDC} ({mr.web_url})\n"

    click.echo(message)



if __name__ == "__main__":
    run()
