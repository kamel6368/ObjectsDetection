import yaml


def config(path):
    stream = open('Resources/config.yaml', 'r')
    dict = yaml.load(stream)

    keys = path.split('/')
    for key in keys:
        val = dict[key]
        dict = val

    return val
