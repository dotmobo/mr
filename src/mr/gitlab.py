import gitlab
from collections import OrderedDict
from .progressbar import printProgressBar


def get_response_from_gitlab(url, token):
    gl = gitlab.Gitlab(url=url, private_token=token)

    projects = gl.projects.list(get_all=True, starred=True)
    response = OrderedDict()
    printProgressBar(
        0, len(projects), prefix="Chargement:", suffix="Complet", length=50
    )
    for i, project in enumerate(projects):
        response[project.name] = set()
        mrs = project.mergerequests.list(get_all=True, state="opened")
        for mr in mrs:
            response[project.name].add(mr)
        printProgressBar(
            i + 1, len(projects), prefix="Chargement:", suffix="Complet", length=50
        )
    return response
