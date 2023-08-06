from cellworld2_core import *

def get_resource(resource_type, *args):
    import requests
    url = "https://raw.githubusercontent.com/germanespinosa/cellworld_data/master/%s/%s" % (resource_type, ".".join(args))
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        response.raise_for_status()


def process_list(l, process):
    new_list = get_list_type(process(l[0]))
    if len(l) > 0:
        for i in l:
            new_list.append(process(i))
        return new_list
    else:
        return list()