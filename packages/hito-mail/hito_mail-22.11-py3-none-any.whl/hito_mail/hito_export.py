#!/usr/bin/env python

"""
Script to export data from Hito as input to hito2lists. Before exporting the data, if the output
file is in a Git repository, the script checks that the working directory is clean. And after the
export, it commits the new file.
"""

import argparse
import os
import re
import socket
import subprocess
import sys

import hito_nsip.hito2nsip as h2n
import yaml
from git import Actor, IndexFile, InvalidGitRepositoryError, Remote, Repo
from hito_tools.core import GlobalParams, debug, exception_handler, info
from hito_tools.utils import get_config_path_default

import hito_mail.hito2lists as h2l

from .lists_tools.exceptions import ConflictingConfigParams, MissingConfigParams


def validate_configuration(config_file):
    """
    Load and validate the configuration parameters from the configuration file

    :param config_file: configuration file
    :return: configuration dictionnary
    """
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception:
        info("ERROR: failed to read configuration file ({})".format(config_file))
        raise

    if config is None or "hito" not in config:
        raise MissingConfigParams("hito", config_file)
    else:
        if config["hito"] is None or "server" not in config["hito"]:
            raise MissingConfigParams("hito/server", config_file)
        elif "database" not in config["hito"]:
            raise MissingConfigParams("hito/database", config_file)
        elif "db_user" not in config["hito"]:
            raise MissingConfigParams("hito/db_user", config_file)
        elif "db_password" not in config["hito"]:
            raise MissingConfigParams("hito/db_password", config_file)
        elif "request" not in config["hito"]:
            raise MissingConfigParams("hito/request", config_file)

    if "hito2lists" not in config:
        raise MissingConfigParams("hito2lists", config_file)
    else:
        if "csv_file" not in config["hito2lists"]:
            raise MissingConfigParams("hito2lists/csv_file", config_file)
        if "additional_lists" not in config["hito2lists"]:
            config["hito2lists"]["additional_lists"] = None
        if "config_file" not in config["hito2lists"]:
            config["hito2lists"]["config_file"] = None
        if "reset_lists" not in config["hito2lists"]:
            config["hito2lists"]["reset_lists"] = False
        if "update_listserv" not in config["hito2lists"]:
            config["hito2lists"]["update_listserv"] = False
        if "update_zimbra" not in config["hito2lists"]:
            config["hito2lists"]["update_zimbra"] = False
        if "zimbra_script" not in config["hito2lists"]:
            config["hito2lists"]["zimbra_script"] = None
        if config["hito2lists"]["update_zimbra"] and config["hito2lists"]["zimbra_script"]:
            raise ConflictingConfigParams(
                "hito2lists/update_zimbra", "hito2lists/zimbra_script", config_file
            )

    if "hito2annuaire" in config:
        if "check-emails-script" not in config["hito2annuaire"]:
            config["hito2annuaire"]["check-emails-script"] = None
        if "config-file" not in config["hito2annuaire"]:
            raise MissingConfigParams("hito2annuaire/config-file", config_file)
        if "dry-run" not in config["hito2annuaire"]:
            config["hito2annuaire"]["dry-run"] = False
        if "email-fixes" not in config["hito2annuaire"]:
            raise MissingConfigParams("hito2annuaire/email-fixes", config_file)
        if "hito-reseda-mappings" not in config["hito2annuaire"]:
            raise MissingConfigParams("hito2annuaire/hito-reseda-mappings", config_file)

    if "git" not in config:
        config["git"] = dict()
    # If both Zimbra and LISTSERV updated are disabled, do not commit the new CSV.
    # For testing purpose only...
    if (
        not config["hito2lists"]["update_listserv"]
        and config["hito2lists"]["update_zimbra"] is False
    ):
        info(
            "WARNING: Both Zimbra and LISTSERV updated are disabled: commit of the new CSV disabled"
        )
        config["git"]["enabled"] = False
    else:
        config["git"]["enabled"] = True
        if "author_name" not in config["git"]:
            config["git"]["author_name"] = "{} script".format(os.path.basename(__file__))
        if "author_email" not in config["git"]:
            config["git"]["author_email"] = "noreply@{}".format(socket.getfqdn())
        if "commit_message" not in config["git"]:
            config["git"]["commit_message"] = "Update from Hito"
        if "push_remote" not in config["git"]:
            config["git"]["push_remote"] = None
        if "ssh_key" in config["git"]:
            if not os.access(config["git"]["ssh_key"], os.R_OK):
                raise Exception(
                    "Git SSH key ({}) not found or not readable".format(config["git"]["ssh_key"])
                )
        elif config["git"]["push_remote"]:
            raise MissingConfigParams("git/ssh_key", config_file)

    return config


def zimbra_update_requested(config):
    """
    Return True if Zimbra lists must be updated, else False. Conditions for returning True:
    - config['hitolists']['update_zimbra'] == True
    - config['hitolists']['update_zimbra'] == None and config['hitolists']['zimbra_script'] defined

    :param config:
    :return: boolean
    """
    return config["hito2lists"]["update_zimbra"] or (
        config["hito2lists"]["update_zimbra"] is None and config["hito2lists"]["zimbra_script"]
    )


def git_cleanup(repo, csv_file):
    """
    Function doing the Git repository cleanup if the update fails after doing the export

    :param repo: Git repository object
    :param csv_file: Hito CSV export path
    :return: None
    """
    git_index = IndexFile(repo)
    git_index.checkout(csv_file, force=True)


def main():
    global_params = GlobalParams()
    config_file_path = get_config_path_default()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=config_file_path,
        help="Configuration file (D: {})".format(config_file_path),
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        default=False,
        help="Git push of a new CSV disabled",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print debugging messsages",
    )
    options = parser.parse_args()

    global_params.verbose = options.verbose

    config = validate_configuration(options.config)

    export_csv = config["hito2lists"]["csv_file"]
    this_script_dir = os.path.realpath(os.path.dirname(__file__))
    output_dir = os.path.realpath(os.path.dirname(export_csv))

    if not os.path.exists(output_dir):
        raise Exception("Directory '{}' doesn't exist".format(output_dir))
    elif not os.path.isdir(output_dir):
        raise Exception("'{}' is not a directory".format(output_dir))
    elif output_dir == this_script_dir:
        raise Exception(
            "Output file is in this script directory ({}): not supported yet".format(output_dir)
        )
    elif not os.path.exists(export_csv):
        raise Exception(
            "A previous version of the CSV file ({}) must exist but none found".format(export_csv)
        )

    try:
        git_repo = Repo(output_dir)
        git_index = IndexFile(git_repo)
    except InvalidGitRepositoryError:
        git_repo = None
        info("Directory '{}' is not a Git repository: not supported yet".format(output_dir))
        return

    if len(git_index.diff(paths=export_csv, other=None)) > 0:
        raise Exception(
            (
                "Repository contains uncommited changes for {}:"
                " commit them before running this script"
            ).format(export_csv)
        )

    info("Exporting data from Hito into {}...".format(export_csv))
    cmd_return = subprocess.run(
        [
            "/usr/bin/mysql",
            "-h",
            config["hito"]["server"],
            "-u",
            config["hito"]["db_user"],
            "-p{}".format(config["hito"]["db_password"]),
            "-D",
            config["hito"]["database"],
        ],
        input=config["hito"]["request"],
        encoding="utf-8",
        capture_output=True,
    )
    if cmd_return.returncode != 0:
        debug("Error executing command {}".format(cmd_return.args))
        raise Exception(
            "Error executing Hito request on {} at {}:\n{}".format(
                config["hito"]["database"], config["hito"]["server"], cmd_return.stderr
            )
        )
    csv_contents = re.sub("\t", ";", cmd_return.stdout)

    with open(export_csv, "w", encoding="utf-8") as csv:
        csv.write(csv_contents)

    if git_repo.is_dirty():
        if zimbra_update_requested(config):
            info("Updating Zimbra lists...")
            try:
                h2l_options = h2l.set_options(
                    None,
                    input_csv=export_csv,
                    additional_lists=config["hito2lists"]["additional_lists"],
                    config_file=config["hito2lists"]["config_file"],
                    execute_cmds=config["hito2lists"]["update_zimbra"],
                    reset_lists=config["hito2lists"]["reset_lists"],
                    script_file=config["hito2lists"]["zimbra_script"],
                    verbose=options.verbose,
                )
                h2l.update_lists(h2l_options)
            except Exception:
                info("ERROR: failed to update Zimbra lists")
                git_cleanup(git_repo, export_csv)
                raise

        if config["hito2lists"]["update_listserv"]:
            info("Updating LISTSERV lists...")
            try:
                h2l_options = h2l.set_options(
                    None,
                    input_csv=export_csv,
                    additional_lists=config["hito2lists"]["additional_lists"],
                    config_file=config["hito2lists"]["config_file"],
                    execute_cmds=config["hito2lists"]["update_listserv"],
                    personnel=True,
                    reset_lists=config["hito2lists"]["reset_lists"],
                    verbose=options.verbose,
                )
                h2l.update_lists(h2l_options)
            except Exception:
                info("ERROR: failed to update Zimbra lists")
                git_cleanup(git_repo, export_csv)
                raise

        if config["git"]["enabled"]:
            info("Committing new version of {}...".format(export_csv))
            try:
                git_index.add(export_csv)
                actor = Actor(config["git"]["author_name"], config["git"]["author_email"])
                git_index.commit(config["git"]["commit_message"], author=actor)
            except Exception:
                info(
                    (
                        "ERROR: failed to commit the new version of the Hito export,"
                        " fix it before rerunning the script"
                    )
                )
                raise

            if not options.no_push and config["git"]["push_remote"]:
                info("Pushing changes to {}...".format(config["git"]["push_remote"]))
                ssh_cmd = "ssh -i {}".format(config["git"]["ssh_key"])
                remote = Remote(git_repo, config["git"]["push_remote"])
                with git_repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
                    remote.push()

        # Directory update is not incremental so there is no reason to postpone committing the
        # next Hito extraction to Git after its execution
        if "hito2annuaire" in config:
            info("Updating IJCLab directory...")
            try:
                h2n_options = h2n.set_options(
                    None,
                    hito_agents_csv=export_csv,
                    email_fixes=config["hito2annuaire"]["email-fixes"],
                    hito_reseda_mappings=config["hito2annuaire"]["hito-reseda-mappings"],
                    check_emails_script=config["hito2annuaire"]["check-emails-script"],
                    config_file=config["hito2annuaire"]["config-file"],
                    execute=not config["hito2annuaire"]["dry-run"],
                )
                h2n.update_nsip(h2n_options)
            except Exception:
                info("ERROR: failed to update IJCLab directory")
                raise

    else:
        info("No change in Hito data: nothing done")


if __name__ == "__main__":
    sys.excepthook = exception_handler
    exit(main())
