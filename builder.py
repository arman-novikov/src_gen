from data import work_dir_creator, Data
from configer import config_creator
from commoner import common_creator
from proper import props_creator
from mainer import main_creator
from initer import ini_creator
from scripter import script_creator
from readmer import readme_creator


def build(data):
    work_dir_creator(data)
    config_creator(data)
    common_creator(data)
    props_creator(data)
    main_creator(data)
    ini_creator(data)
    script_creator(data)
    readme_creator(data)


if __name__ == "__main__":
    build(Data())
