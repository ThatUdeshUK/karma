import argparse
import json
import os


def write_results(dataset_path, dataset=None):
    """Writes the dataset as JSON to the file at given path

    Args:
        dataset_path (str): Path of the dataset json file
        dataset (dataset): Dataset to be written
    """
    if dataset is None:
        dataset = {}
    with open(dataset_path, 'w') as f:
        j = json.dumps(dataset, indent=4)
        print(j, file=f)
    print("Wrote results output:", dataset_path)


def create_if_not_exist(path, data=None):
    """Write a file at given path if it doesn't exist

    Args:
        path (str): Path of the file
        data: Initial data to be written
    """
    if data is None:
        data = {}
    if not os.access(path, os.W_OK):
        with open(path, 'w') as f:
            j = json.dumps(data)
            print(j, file=f)


def create_dir_if_not_exist(path):
    """Create a directory at given path if it doesn't exist

    Args:
        path (str): Path of the directory
    """
    if not os.path.exists(path):
        os.makedirs(path)


class WriteableDir(argparse.Action):
    """argparse module action to validate writable directory arguments

    Args:
        argparse (argparse.Action): argparse Action
    """

    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
                "writable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.W_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError(
                "writable_dir:{0} is not a readable dir".format(prospective_dir))
