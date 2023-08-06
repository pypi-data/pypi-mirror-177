import argparse
import importlib.resources
from importlib.resources import files, as_file
import os


def datafiles():
    # I find it easier to just list the names of the
    # data files I intend to use in a package.
    mydatafilenames = {"readfromfile": "readme.json", "writetofile": "writetome.json"}

    main_group_parser = argparse.ArgumentParser(
        description="A package datafiles example"
    )
    main_group_parser.add_argument(
        "-l", "--list", action="store_true", help="List package data files"
    )
    main_group_parser.add_argument(
        "-r", "--readme", action="store_true", help="Outputs data/readme.json"
    )
    main_group_parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copies data/readme.json to data/writetome.json",
    )
    main_group_parser.add_argument(
        "-w", "--writetome", action="store_true", help="Outputs data/writetome.json"
    )
    main_group_parser.add_argument(
        "-d", "--delete", action="store_true", help="Delete data/writetome.json"
    )

    my_args = main_group_parser.parse_args()

    if my_args.list:
        for key in mydatafilenames:
            datafilename = mydatafilenames[key]
            my_traversable_resource_container = importlib.resources.files(
                "pkgexampledatafiles.data"
            ).joinpath(datafilename)
            my_pathlib_context_manager = importlib.resources.as_file(
                my_traversable_resource_container
            )
            with my_pathlib_context_manager as fullfilepath:
                print(fullfilepath)

    if my_args.readme:
        my_readfromfilename = mydatafilenames["readfromfile"]
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatafiles.data"
        ).joinpath(my_readfromfilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            try:
                with open(fullfilepath, "r") as myfile:
                    text = myfile.read()
                    print(text)
            except FileNotFoundError:
                print("File does not exist")

    if my_args.copy:
        my_readfromfilename = mydatafilenames["readfromfile"]
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatafiles.data"
        ).joinpath(my_readfromfilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            try:
                with open(fullfilepath, "r") as myfile:
                    text = myfile.read()
                    print(text)
            except FileNotFoundError:
                print("File does not exist")
                text = ""
        my_writetofilename = mydatafilenames["writetofile"]
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatafiles.data"
        ).joinpath(my_writetofilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            with open(fullfilepath, "w") as myfile:
                myfile.writelines(text)

    if my_args.writetome:
        my_writetofilename = mydatafilenames["writetofile"]
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatafiles.data"
        ).joinpath(my_writetofilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            try:
                with open(fullfilepath, "r") as myfile:
                    text = myfile.read()
                    print(text)
            except FileNotFoundError:
                print("File does not exist")

    if my_args.delete:
        my_writetofilename = mydatafilenames["writetofile"]
        my_traversable_resource_container = importlib.resources.files(
            "pkgexampledatafiles.data"
        ).joinpath(my_writetofilename)
        my_pathlib_context_manager = importlib.resources.as_file(
            my_traversable_resource_container
        )
        with my_pathlib_context_manager as fullfilepath:
            os.remove(fullfilepath)
