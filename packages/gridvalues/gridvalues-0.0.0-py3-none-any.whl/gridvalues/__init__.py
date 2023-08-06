from importlib.resources import files

with files(__package__).joinpath("VERSION").open("r") as t:
    version = t.readline().strip()
