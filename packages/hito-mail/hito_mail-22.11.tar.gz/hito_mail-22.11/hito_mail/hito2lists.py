#!/usr/bin/env python

import argparse
import csv
import io
import os
import re
import smtplib
import sys
import unicodedata
from datetime import datetime
from email.message import EmailMessage

import pexpect
import yaml
from hito_tools.core import GlobalParams, debug, exception_handler, info, singleton
from hito_tools.utils import get_config_path_default
from unidecode import unidecode

from .lists_tools.core import get_commit, is_windows, normalize_name, open_git_repo
from .lists_tools.exceptions import (
    ConflictingOptions,
    GitPythonModuleMissing,
    GitRepoNotFound,
    InvalidCSVFormat,
    MissingConfigParams,
    MissingGenListConfig,
    MultipleLists,
    NoListCreated,
    UnsupportedListFmt,
)

GENERAL_LISTS_FORMAT_DEFAULT = "listserv"
PATTERN_VALID_EMAIL = r"\s*[\w\-\.]+@[\w\-\.]+\s*"
PERSON_DEFAULT_LANGUAGE = "fr"
ZIMBRA_EXPECTED_ERRORS = {
    "cdl": ["account.DISTRIBUTION_LIST_EXISTS"],
    "rdlm": ["account.NO_SUCH_MEMBER"],
}
ZMPROV_PROMPT = "prov>"
ZMPROV_CMD_TIMEOUT = 120


@singleton
class CSVParams:
    def __init__(self):
        self.column_name = "NOM_USUEL"
        self.column_givenname = "PRENOM"
        self.column_email = "E_MAIL"
        self.column_pole = "POLE"
        self.column_equipe = "DEPARTEMENT"
        self.column_secondary_teams = "OTHER TEAMS"
        self.column_service = "SERVICE"
        self.column_team_fullname = "TEAM FULLNAME"


class Personne:
    def __init__(self, name, givenname, team, email):
        self.name = name
        self.givenname = givenname
        self.teams = set([team])
        self.email = email

    def add_team(self, team):
        self.teams.add(team)

    def get_name(self):
        return self.name

    def get_givenname(self):
        return self.givenname

    def get_teams(self):
        return self.teams

    def get_email(self):
        return self.email


class EmailList:
    def __init__(self, name, hito_name=None, description=None):
        """
        EmailList constructor

        :param name: list name, used to build its email address
        :param hito_name: list name in Hito. Defaults to name
        :param description: list description in Hito
        """
        self.name = name
        if hito_name:
            self.hito_name = hito_name
        else:
            self.hito_name = name
        self.description = description
        self.members = {}
        self.new = False
        self.ignored = False

    def add_member(self, personne, optout_list={}):
        if personne.get_email() in optout_list and self.name in optout_list[personne.get_email()]:
            debug(
                "INFO: {} opted-out from list {}, not added".format(personne.get_email(), self.name)
            )
            return
        self.members[personne.get_email()] = personne

    def get_description(self) -> str:
        """
        Return the description attribute if it is defined, else the hito_name attribute

        :return: string
        """
        if self.description:
            return self.description
        else:
            return self.hito_name

    def get_member(self, email):
        return self.members[email]

    def get_members(self):
        return self.members.values()

    def get_member_emails(self):
        return self.members.keys()

    def get_name(self):
        return self.name

    def is_new(self):
        return self.new

    def is_ignored(self):
        return self.ignored

    def mark_as_new(self):
        self.new = True

    def mark_as_ignored(self):
        self.ignored = True

    def member_exists(self, email):
        return email in self.members

    def set_description(self, description):
        self.description = description


class ListOfList:
    """
    Class describing the list of lists. This list is implemented as a dict where the key is
    the left part of the list email address and the value is an EmailList message.

    This class provides helper functions to add lists based on the team a person belongs to.
    """

    def __init__(self):
        self.email_lists = {}

    def _add_list(self, list_name, list_hito_name, team_params, email):
        """
        Create a new EmailList object with the listname and add it to the ListOfList dictionary
        using the list short name (left part of list address) as the key

        :param list_name: left part 'before @) of list address
        :param list_hito_name: list name in Hito
        :param team_params: configuration parameters for teams
        :param email:
        :return:
        """
        if "reserved_names" in team_params and list_name in team_params["reserved_names"]:
            info(
                "WARNING: list name {} is reserved, email {} cannot be added".format(
                    list_name, email
                )
            )
            return

        # If an entry exists in team_params to define the team description for the current
        # team, use it. It will be overriden if it has one member who it is the primary team.
        if team_params and list_name in team_params["descriptions"]:
            team_description = team_params["descriptions"][list_name]
        else:
            team_description = None

        if list_name not in self.email_lists:
            self.email_lists[list_name] = EmailList(list_name, list_hito_name, team_description)

    def add_person_lists(
        self,
        email,
        pole,
        equipe_dept,
        service,
        team_fullname,
        max_level,
        selected_pole=None,
        team_params={},
    ):
        """
        Add a person to the lists he is a member of. Each person is considered a member of its
        service list (the smaller entity) and a member of each upper level list.

        :param email:
        :param pole:
        :param equipe_dept:
        :param service:
        :param team_fullname: fullname of the team last token (no matter whether a pole,
                              equipe_dept or service)
        :param max_level:
        :param selected_pole:
        :param team_params:
        :return: list with the name of the created lists
        """

        if "aliases" not in team_params:
            team_params["aliases"] = {}
        if "short_names" not in team_params:
            team_params["short_names"] = {}
        if "reserved_names" not in team_params:
            team_params["reserved_names"] = []
        if "sublist_disabled" not in team_params:
            team_params["sublist_disabled"] = []

        person_lists = set()

        if pole:
            if selected_pole is None or pole == selected_pole:
                pole_name, pole_prefix = list_name_prefix(pole, team_params)
                list_name = pole_name
                self._add_list(list_name, pole, team_params, email)
                person_lists.add(list_name)
                if pole not in team_params["sublist_disabled"]:
                    if equipe_dept and max_level >= 2:
                        equipe_name, equipe_prefix = list_name_prefix(equipe_dept, team_params)
                        list_name = "{}{}".format(pole_prefix, equipe_name)
                        self._add_list(
                            list_name,
                            "{} - {}".format(pole, equipe_dept),
                            team_params,
                            email,
                        )
                        person_lists.add(list_name)
                    if (
                        service
                        and max_level >= 3
                        and equipe_dept not in team_params["sublist_disabled"]
                    ):
                        service_name, _ = list_name_prefix(service, team_params)
                        list_name = "{}{}{}".format(pole_prefix, equipe_prefix, service_name)
                        self._add_list(
                            list_name,
                            "{} - {} - {}".format(pole, equipe_dept, service),
                            team_params,
                            email,
                        )
                        person_lists.add(list_name)
                if team_fullname:
                    self.email_lists[list_name].set_description(team_fullname)

        return person_lists

    def get_list(self, list_name):
        return self.email_lists[list_name]

    def get_list_names(self):
        return self.email_lists.keys()

    def get_lists(self):
        return self.email_lists


def define_column_names(config):
    cvs_params = CSVParams()
    if "names" in config:
        column_names = config["names"]
        if "name" in column_names:
            if "name" in column_names:
                cvs_params.column_name = column_names["name"]
            if "givenname" in column_names:
                cvs_params.column_givenname = column_names["givenname"]
            if "email" in column_names:
                cvs_params.column_email = column_names["email"]
            if "pole" in column_names:
                cvs_params.column_pole = column_names["pole"]
            if "equipe" in column_names:
                cvs_params.column_equipe = column_names["equipe"]
            if "secondary_teams" in column_names:
                cvs_params.column_secondary_teams = column_names["secondary_teams"]
            if "service" in column_names:
                cvs_params.column_service = column_names["service"]
            if "team_fullname" in column_names:
                cvs_params.column_team_fullname = column_names["team_fullname"]
    else:
        debug("INFO: CSV row names not defined into the configuration, using defaults")


def translate_to_ascii(string):
    """
    Helper function to translate a string with accented characters to ASCII and replace all
    consecutive white spaces by a single '-'
    :return: string with only ASCII characters
    """
    ascii_string = unicodedata.normalize("NFD", string).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\W+", "-", ascii_string)


def parse_hito_team(hito_team):
    pole = None
    equipe_dept = None
    service = None
    toks = hito_team.split("-", 3)

    if len(toks) >= 1:
        pole = toks[0].strip()
    if len(toks) >= 2:
        equipe_dept = toks[1].strip()
    if len(toks) >= 3:
        service = toks[2].strip()

    # print("team={}, pole={}, equipe={}, service={}".format(hito_team, pole, equipe_dept, service))

    return pole, equipe_dept, service


def list_name_prefix(team, team_params):
    """
    Build the team component part of the list name based on the aliases and the prefix part of
    the list name of the next level based on aliases and short names

    :param pole:
    :return: team part name, prefix part for lists of next levels
    """

    team = normalize_name(translate_to_ascii(team))

    if team in team_params["aliases"]:
        team_name = team_params["aliases"][team]
    else:
        team_name = team

    if team in team_params["short_names"]:
        if team_params["short_names"][team] is None:
            team_prefix = ""
        else:
            team_prefix = "{}-".format(team_params["short_names"][team])
    else:
        team_prefix = "{}-".format(team_name)

    return team_name, team_prefix


def created_lists(file, email_lists, list_domain="", index_disabled=[]):
    """
    Create a file listing all email lists created. The format of the created file depends on the
    file extension. Default format is a CSV file with fixed-size columns.

    :param file: output file for the list of lists
    :param email_lists: ListOfLists object
    :param list_domain: email domain for lists
    :param index_disabled: list of list description patterns that must not be included
                           in the list
    :return:
    """

    if list_domain == "":
        domain_suffix = ""
    else:
        domain_suffix = format("@{}".format(list_domain))

    html_file = re.match(r".*\.html", file)
    try:
        with open(file, "w", encoding="utf-8") as f:
            if html_file:
                print("<table>", file=f)
                print(
                    "<thead>\n<tr>\n<th>Nom d'équipe</th>\n<th>Liste</th>\n</tr>\n</thead>",
                    file=f,
                )
                print("<tbody>", file=f)
                for _, email_list in sorted(
                    email_lists.items(), key=lambda x: x[1].get_description()
                ):
                    add_list = True
                    for pattern in index_disabled:
                        if re.match(pattern, email_list.get_description()):
                            add_list = False
                    if add_list:
                        print(
                            "<tr>\n<td>{}</td>\n<td>{}{}</td>\n</tr>".format(
                                email_list.get_description(),
                                email_list.get_name(),
                                domain_suffix,
                            ),
                            file=f,
                        )
                print("</tbody>\n</table>", file=f)
            else:
                print("{:70}{}".format("Nom d'équipe", "Liste"), file=f)
                for _, email_list in sorted(email_lists.items(), key=lambda x: x[1].description):
                    add_list = True
                    for pattern in index_disabled:
                        if re.match(pattern, email_list.get_description()):
                            add_list = False
                    if add_list:
                        print(
                            "{:70}{}{}".format(
                                email_list.get_description(),
                                email_list.get_name(),
                                domain_suffix,
                            ),
                            file=f,
                        )

    except Exception:
        info("ERROR: failed to write created lists in {}".format(file))
        raise


def zimbra_update_commands(members_added, members_deleted, team_params, list_name_pattern):
    """
    Function to produce a script with the appropriate Zimbra commands to update the lists

    :param members_added: a dict of EmailList objects
    :param members_deleted: a dict of EmailList objects
    :param team_params: general parameters for the lists to be created
    :param list_name_pattern: lists to be created/updated/deleted or None for all lists.
                              Interpreted as a regex pattern matched against list names
    :return: a list of Zimbra commands
    """

    domain = team_params["email_domain"]
    zimbra_cmds = []

    # First delete removed users: it is necessary to do it first to prevent a user being removed
    # from a list if the add/delete sequence is to change his Zimbra email. In this case, if the
    # add is done first, it will do nothing as the other Zimbra email (primary or alias) is still
    # in the list and the delete will then remove the address originally used.
    # See https://gitlab.in2p3.fr/ijclab-exploit/email-tools/-/issues/37
    for list_name, list_params in sorted(members_deleted.items(), key=lambda x: x[1].name):
        if list_name_pattern and not re.match(list_name_pattern, list_name):
            debug(
                (
                    f"List '{list_name}' deletion ignored as it doesn't match list"
                    f" pattern ({list_name_pattern})"
                )
            )
            list_params.mark_as_ignored()
            continue

        # members_deleted is the result of comparing the previous Hito extraction against the new
        # one: in this case, if is_new() is true it means that the list no longer exists in the
        # the last extraction.
        if list_params.is_new():
            zimbra_cmds.append("ddl {}@{}".format(list_params.get_name(), domain))
        else:
            all_members = "rdlm {}@{}".format(list_params.get_name(), domain)
            for member in list_params.get_members():
                all_members += " {}".format(member.get_email())
            zimbra_cmds.append("{}".format(all_members))

    for list_name, list_params in sorted(members_added.items(), key=lambda x: x[1].name):
        if list_name_pattern and not re.match(list_name_pattern, list_name):
            debug(
                (
                    f"List '{list_name}' addition ignored as it doesn't match list"
                    f" pattern ({list_name_pattern})"
                )
            )
            list_params.mark_as_ignored()
            continue

        zimbra_cmds.append("cdl {}@{}".format(list_params.get_name(), domain))
        zimbra_cmds.append(
            (
                f"mdl {list_params.get_name()}@{domain} description"
                f" '\"{unidecode(list_params.get_description())}\" members - DO NOT EDIT'"
                " zimbraNotes 'created from Hito - DO NOT EDIT'"
            )
        )
        all_members = "adlm {}@{}".format(list_params.get_name(), domain)
        for member in list_params.get_members():
            all_members += " {}".format(member.get_email())
        zimbra_cmds.append("{}".format(all_members))

    return zimbra_cmds


def zimbra_execute(config, commands):
    """
    Function to connect and execute command to a zimbra server
    :param config: Zimbra-related configuration parameters
    :param commands: List of commands in zimbra CLI format
    :return: None
    """
    try:
        zmprov_cmd = (
            f"/usr/bin/ssh -p {config['port']} -i {config['ssh_key_path']}"
            f" {config['user']}@{config['server']} {config['command']}"
        )
        debug(f"Launching Zimbra management command: {zmprov_cmd}")
        zimbra = pexpect.spawn(zmprov_cmd, encoding="utf-8", echo=False)
        # Read the prompt resulting from zmprov start
        zimbra.expect(ZMPROV_PROMPT, timeout=15)
        debug("Successfully connected to the Zimbra server")
    except Exception:
        info(f"ERROR: failed to connect to the Zimbra server ({config['server']})")
        raise
        exit(100)

    if commands == "":
        info("WARNING: Command can not be empty")
    else:
        try:
            for action in commands:
                info(f"Executing {action}...")
                zimbra_cmd, _ = action.split(maxsplit=1)
                zimbra.sendline(action)
                zimbra.expect(ZMPROV_PROMPT, timeout=ZMPROV_CMD_TIMEOUT)
                zimbra_output = zimbra.before
                # Errors can be after the next prompt in the output, get a chance to read it if
                # it is the case
                zimbra.expect([ZMPROV_PROMPT, pexpect.TIMEOUT], timeout=1)
                zimbra_output += zimbra.before
                zimbra_expected_msgs = [re.compile(rf"\s*{action}\s*")]
                if zimbra_cmd in ZIMBRA_EXPECTED_ERRORS:
                    for error_code in ZIMBRA_EXPECTED_ERRORS[zimbra_cmd]:
                        zimbra_expected_msgs.append(re.compile(rf"\s*ERROR:\s*{error_code}.*"))
                for line in zimbra_output.splitlines():
                    for pattern in zimbra_expected_msgs:
                        if pattern.match(line):
                            break
                    else:
                        if line.strip():
                            info(f"{line}")
        except pexpect.TIMEOUT:
            info(f"WARNING: unexpected timeout ({ZMPROV_CMD_TIMEOUT}) during Zimbra command")
        except Exception:
            info("ERROR: an error occured during command execution")
            raise
            exit(100)

        status = zimbra.terminate(force=True)
        if status:
            debug("Successfully disconnected from the Zimbra server")
        else:
            debug("Failed to properly disconnect from the Zimbra server")


def zimbra_update_script(file, zimbra_cmds):
    try:
        with open(file, "w", encoding="utf-8") as script:
            # zmprov input files don't support comments
            for cmd in zimbra_cmds:
                print(cmd, file=script)

    except Exception:
        info("ERROR: failed to write the list update script ({})".format(file))
        raise


def listserv_update_script(file, config, list_name, members_added, members_deleted, optout_list):
    """
    Produces a file containing LISTSERV commands to update the lists. If the file name is None,
    create an in-memory file (SringIO)

    :param file: file name to use. None to create an in-memory file.
    :param config: LISTSERV-related config
    :param list_name: list for which commands will be generated
    :param members_added:  added members for each list
    :param members_deleted: deleted members for each list
    :param optout_list: list opted out (if any) for each user
    :return: number of added and deleted members
    """
    try:
        if listserv_update_script.f:
            pass
    except AttributeError:
        if file:
            listserv_update_script.f = open(file, "w", encoding="utf-8")
        else:
            listserv_update_script.f = io.StringIO()
    except Exception:
        info("ERROR: failed to create LISTSERV script file ({})".format(file))
        raise

    num_members_added = 0
    num_members_deleted = 0
    delete_options = ""
    if config["admin_password"]:
        pw_option = f"PW={config['admin_password']}"
    else:
        pw_option = ""
    print(pw_option)

    try:
        print(
            f"QUIET ADD {list_name} DD={list_name}-add IMPORT {pw_option}",
            file=listserv_update_script.f,
        )
        print('//{}-add DD *"'.format(list_name), file=listserv_update_script.f)
        for member in sorted(members_added.get_members(), key=lambda x: x.get_name()):
            if re.match(PATTERN_VALID_EMAIL, member.get_email()):
                if (
                    member.get_email() in optout_list
                    and list_name in optout_list[member.get_email()]
                ):
                    debug(
                        "INFO: email {} opted-out from list {}, not added".format(
                            member.get_email(), list_name
                        )
                    )
                else:
                    print(
                        "{} {} {}".format(
                            member.get_email(),
                            member.get_givenname(),
                            member.get_name(),
                        ),
                        file=listserv_update_script.f,
                    )
                    num_members_added += 1
            else:
                info(
                    "WARNING: {} {} doesn't have an email address to be added in list {}.".format(
                        member.get_givenname(), member.get_name(), list_name
                    )
                )
        print("/*\n", file=listserv_update_script.f)

        if members_deleted:
            print(
                f"QUIET DELETE {list_name} DD={list_name}-del {delete_options} {pw_option}",
                file=listserv_update_script.f,
            )
            print('//{}-del DD *"'.format(list_name), file=listserv_update_script.f)
            for member in sorted(members_deleted.get_members(), key=lambda x: x.get_name()):
                if re.match(PATTERN_VALID_EMAIL, member.get_email()):
                    print(
                        "{} {} {}".format(
                            member.get_email(),
                            member.get_givenname(),
                            member.get_name(),
                        ),
                        file=listserv_update_script.f,
                    )
                    num_members_deleted += 1
                else:
                    info(
                        (
                            (
                                "WARNING: {} {} doesn't have an email address to be removed"
                                " from the list {}."
                            )
                        ).format(member.get_givenname(), member.get_name(), list_name)
                    )
            print("/*\n", file=listserv_update_script.f)

    except Exception:
        info("ERROR: failed to write LISTSERV script file ({})".format(file))
        raise

    return num_members_added, num_members_deleted


def listserv_execute(config):
    """
    Send an email to LISTSERV with the appropriate commands to update lists

    :param config: LISTSERV-related configuration
    :return:
    """

    mail_subject = "{} ({})".format(
        config["mail_subject"], datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    try:
        if listserv_update_script.f:
            pass
    except Exception:
        info("ERROR: LISTSERV script file descriptor undefined")
        raise

    listserv_update_script.f.seek(0)

    msg = EmailMessage()
    msg.set_content(listserv_update_script.f.read())
    msg["Subject"] = mail_subject
    msg["From"] = config["admin_email"]
    msg["To"] = config["server"]
    smtp_relay = config["smtp_relay"]

    # Send the message via our own SMTP server.
    s = smtplib.SMTP(smtp_relay)
    s.send_message(msg)
    s.quit()


def limesurvey_update_script(file, list_name, members, optout_list):
    m = re.search(r"\.csv$", file)
    if not m:
        file += ".csv"
        info("WARNING: extension .csv added to output file ({})".format(file))

    members_num = 0

    try:
        with open(file, "w", encoding="utf-8") as f:
            print("email;firstname;lastname;language;", file=f)
            for member in sorted(members.get_members(), key=lambda x: x.get_name()):
                if (
                    member.get_email() in optout_list
                    and list_name in optout_list[member.get_email()]
                ):
                    debug(
                        "INFO: email {} opted-out from list {}, not added".format(
                            member.get_email(), list_name
                        )
                    )
                else:
                    print(
                        "{};{};{};{};".format(
                            member.get_email(),
                            member.get_givenname(),
                            member.get_name(),
                            PERSON_DEFAULT_LANGUAGE,
                        ),
                        file=f,
                    )
                    members_num += 1
    except Exception:
        info("ERROR: failed to create Limesurvey CSV file ({})".format(file))
        raise

    return members_num


def load_hito_csv(
    previous,
    options,
    team_params,
    lists_to_create={},
    exclusion_list={},
    optout_list={},
):
    """

    :param previous: True if the previous file must be read instead of the current one,
                     False otherwise
    :param options:
    :param team_params:
    :param exclusion_list:
    :param optout_list:
    :param lists_to_create: if the dictionnary is not empty, use the keys as the list of email
                            list to create
    :return:
    """
    csv_params = CSVParams()

    personnels = {}
    persons_added = {}
    persons_no_team = {}
    persons_no_email = {}
    email_lists = ListOfList()

    if previous:
        filename = options.previous
    else:
        filename = options.csv

    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            rows = csv.DictReader(csvfile, delimiter=";")
            for row in rows:
                if row[csv_params.column_name] == "":
                    continue

                if csv_params.column_service in row:
                    pole, equipe_dept, service = parse_hito_team(row[csv_params.column_service])
                    if csv_params.column_team_fullname in row:
                        # This column contains a full version of the team last token name
                        team_fullname = row[csv_params.column_team_fullname]
                    else:
                        team_fullname = None
                else:
                    raise InvalidCSVFormat(options.csv)

                email = row[csv_params.column_email].lower()
                rattachement = None
                if service:
                    rattachement = service
                elif equipe_dept:
                    rattachement = equipe_dept
                elif pole:
                    rattachement = pole
                else:
                    persons_no_team[
                        "{}-{}".format(
                            row[csv_params.column_name],
                            row[csv_params.column_givenname],
                        )
                    ] = 1
                    if options.warn_unassigned and not options.personnel and not previous:
                        info(
                            (
                                "WARNING: {} {} doesn't belong to any pole and will not be added"
                                " to any list"
                            ).format(
                                row[csv_params.column_givenname],
                                row[csv_params.column_name],
                            )
                        )

                if email in exclusion_list:
                    debug("INFO: {} found in the exclusion list, not added".format(email))
                    exclusion_list[email] = True
                else:
                    personne = Personne(
                        row[csv_params.column_name],
                        row[csv_params.column_givenname],
                        rattachement,
                        email,
                    )
                    personnels[email] = personne

                    # If lists_to_create is not empty, create only those lists
                    if len(lists_to_create.keys()) > 0:
                        person_lists = lists_to_create.keys()

                    # Else add the person to team lists, based on the teams he belongs to
                    # or it is affiliated to (secondary teams)
                    else:
                        person_lists = set()

                        # Main teams
                        person_lists.update(
                            email_lists.add_person_lists(
                                email,
                                pole,
                                equipe_dept,
                                service,
                                team_fullname,
                                options.level,
                                options.pole,
                                team_params,
                            )
                        )

                        # Secondary teams if any defined
                        if (
                            csv_params.column_secondary_teams in row
                            and len(row[csv_params.column_secondary_teams]) > 0
                            and row[csv_params.column_secondary_teams] != "NULL"
                        ):
                            secondary_teams = row[csv_params.column_secondary_teams].split(",")
                            for team in secondary_teams:
                                personne.add_team(team)
                                pole, equipe_dept, service = parse_hito_team(team)
                                # List fullname will be defined by somebody whose
                                # it is the primary team
                                person_lists.update(
                                    email_lists.add_person_lists(
                                        email,
                                        pole,
                                        equipe_dept,
                                        service,
                                        None,
                                        options.level,
                                        options.pole,
                                        team_params,
                                    )
                                )

                    for list_name in person_lists:
                        if list_name not in email_lists.get_list_names():
                            email_lists._add_list(list_name, list_name, team_params, email)
                        person_fullname = "{}-{}".format(
                            row[csv_params.column_name],
                            row[csv_params.column_givenname],
                        )
                        if re.match(PATTERN_VALID_EMAIL, email):
                            if email_lists.get_list(list_name).member_exists(email):
                                info(
                                    (
                                        "WARNING: {} already added to list {} (internal error"
                                        " or duplicated entry)"
                                    ).format(email, list_name)
                                )
                            else:
                                email_lists.get_list(list_name).add_member(personne, optout_list)
                                persons_added[person_fullname] = 1
                        else:
                            info(
                                (
                                    "WARNING: {} {} doesn't have an email address to be"
                                    " added in list {}."
                                ).format(
                                    row[csv_params.column_givenname],
                                    row[csv_params.column_name],
                                    list_name,
                                )
                            )
                            persons_no_email[person_fullname] = 1
    except Exception:
        info("Failed to read {}".format(filename))
        raise

    return (
        email_lists.get_lists(),
        personnels,
        len(persons_added),
        len(persons_no_email),
        persons_no_team,
    )


def hito_changes(new_list_members, previous_list_members):
    updated_list_members = {}

    members_changed = {}

    for list_name in new_list_members.keys():
        for email in new_list_members[list_name].get_member_emails():
            if list_name not in previous_list_members or not previous_list_members[
                list_name
            ].member_exists(email):
                if list_name not in updated_list_members:
                    updated_list_members[list_name] = EmailList(
                        list_name, new_list_members[list_name].get_description()
                    )
                if list_name not in previous_list_members:
                    updated_list_members[list_name].mark_as_new()
                updated_list_members[list_name].add_member(
                    new_list_members[list_name].get_member(email)
                )
                members_changed[new_list_members[list_name].get_member(email)] = True

    return updated_list_members, len(members_changed)


def validate_configuration(config_file, options):
    """
    Load and validate the configuration parameters from the configuration file

    :param config_file: configuration file
    :param opions: command-line options
    :return: configuration dictionnary
    """
    global_params = GlobalParams()

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except Exception:
        info("ERROR: failed to read configuration file ({})".format(config_file))
        raise

    if config is None:
        config = dict()

    if "teams" not in config:
        config["teams"] = {}
    if "aliases" not in config["teams"]:
        config["teams"]["aliases"] = {}
    if "descriptions" not in config["teams"]:
        config["teams"]["descriptions"] = {}
    if "email_domain" not in config["teams"]:
        config["teams"]["email_domain"] = ""
    if "index_disabled" not in config["teams"]:
        config["teams"]["index_disabled"] = []
    if "reserved_names" not in config["teams"]:
        config["teams"]["reserved_names"] = {}
    if "short_names" not in config["teams"]:
        config["teams"]["short_names"] = {}

    if "zimbra" in config:
        if config["zimbra"] is None or "server" not in config["zimbra"]:
            raise MissingConfigParams("zimbra/server", config_file)
        if "port" not in config["zimbra"]:
            raise MissingConfigParams("zimbra/port", config_file)
        if "user" not in config["zimbra"]:
            raise MissingConfigParams("zimbra/user", config_file)
        if "ssh_key_path" not in config["zimbra"]:
            raise MissingConfigParams("zimbra/ssh_key_path", config_file)
        if "command" not in config["zimbra"]:
            raise MissingConfigParams("zimbra/command", config_file)
    elif options.execute and not options.personnel:
        raise MissingConfigParams("zimbra", config_file)

    if "listserv" in config:
        if config["listserv"] is None or "server" not in config["listserv"]:
            raise MissingConfigParams("listserv/server", config_file)
        if "admin_email" not in config["listserv"]:
            raise MissingConfigParams("listserv/admin_email", config_file)
        if "smtp_relay" not in config["listserv"]:
            config["listserv"]["smtp_relay"] = "localhost"
        if "mail_subject" not in config["listserv"]:
            config["listserv"]["mail_subject"] = "LISTSERV update by {}".format(
                global_params.this_script
            )
        if "admin_password" not in config["listserv"]:
            config["listserv"]["admin_password"] = None

    return config


def set_options(
    options=None,
    additional_lists=None,
    config_file=None,
    created_lists=None,
    exclude_list=None,
    execute_cmds=None,
    format=None,
    git_commit=None,
    input_csv=None,
    level=None,
    list_name=None,
    list_pattern=None,
    personnel=None,
    pole=None,
    previous=None,
    reset_lists=None,
    script_file=None,
    verbose=None,
    warn_unassigned=None,
):
    """
    Function to initialize/update options. Basically mimics what is done by argparser in main().
    Not ideal but allows to call this application as a module rather than a command.
    Be sure to maintain the consistency with what argparser does in main().
    """

    # For clarity, define default values here. Note that they cannot be defined as default values
    # of arguments as it would become impossible to distingish between a specified and unspecified
    # argument and make impossible to call this function multiple times without affecting all
    # the options.
    additional_lists_default = None
    created_lists_default = None
    exclude_list_default = None
    execute_cmds_default = None
    format_default = None
    git_commit_default = None
    level_default = 3
    list_name_default = None
    list_pattern_default = None
    personnel_default = False
    pole_default = None
    previous_default = None
    reset_lists_default = False
    script_file_default = None
    verbose_default = None
    warn_unassigned_default = True

    # Initialize options if None
    if not options:
        options = argparse.Namespace()

    # Apply specified or default values for all options
    if input_csv:
        options.csv = input_csv
    elif "csv" not in options or options.csv is None:
        raise Exception("CSV input file not specified")
    if additional_lists:
        options.additions = additional_lists
    elif "additions" not in options:
        options.additions = additional_lists_default
    if config_file:
        options.config = config_file
    elif "config" not in options or options.config is None:
        options.config = get_config_path_default(os.path.dirname(options.csv), __file__)[0]
    if created_lists:
        options.created_lists = created_lists_default
    elif "created_lists" not in options:
        options.created_lists = created_lists_default
    if exclude_list:
        options.exclude_list = exclude_list
    elif "exclude_list" not in options:
        options.exclude_list = exclude_list_default
    if execute_cmds:
        options.execute = execute_cmds
    elif "execute" not in options:
        options.execute = execute_cmds_default
    if format:
        options.format = format
    elif "format" not in options:
        options.format = format_default
    if git_commit:
        options.commit_id = git_commit
    elif "commit_id" not in options:
        options.commit_id = git_commit_default
    if level:
        options.level = level
    elif "level" not in options:
        options.level = level_default
    if list_name:
        options.list_name = list_name
    elif "list_name" not in options:
        options.list_name = list_name_default
    if list_pattern:
        options.list_pattern = list_pattern
    elif "list_pattern" not in options:
        options.list_pattern = list_pattern_default
    if personnel:
        options.personnel = personnel
    elif "personnel" not in options:
        options.personnel = personnel_default
    if pole:
        options.pole = pole
    elif "pole" not in options:
        options.pole = pole_default
    if previous:
        options.previous = previous
    elif "previous" not in options:
        options.previous = previous_default
    if reset_lists:
        options.reset_lists = reset_lists
    elif "reset_lists" not in options:
        options.reset_lists = reset_lists_default
    if script_file:
        options.output = script_file
    elif "output" not in options:
        options.output = script_file_default
    if verbose:
        options.verbose = verbose
    elif "verbose" not in options:
        options.verbose = verbose_default
    if warn_unassigned:
        options.warn_unassigned = warn_unassigned
    elif "warn_unassigned" not in options:
        options.warn_unassigned = warn_unassigned_default

    # Check that one of --execute, --output or --created-list has been specified
    if not options.execute and not options.output and not options.created_lists:
        raise Exception("One of --execute, --output or --created-lists must be specified")

    # Check mutually exclusive options not checked by the argparser
    if options.execute and options.output:
        raise ConflictingOptions("execute", "script")
    if options.previous and options.reset_lists:
        raise ConflictingOptions("previous", "reset_lists")
    if options.commit_id and options.reset_lists:
        raise ConflictingOptions("git_commit", "reset_lists")
    if options.commit_id and options.previous:
        raise ConflictingOptions("git_commit", "previous")
    if options.list_pattern and options.personnel:
        raise ConflictingOptions("list_pattern", "personnel")

    # Other option checks
    if options.created_lists:
        if not options.reset_lists:
            raise Exception("--created-lists option requires --reset-lists")
        elif options.personnel:
            info("WARNING: option --created-lists ignored with --personnel")
            options.created_lists = None

    if options.list_pattern and not options.reset_lists:
        raise Exception("--list-pattern option requires --reset-lists")

    return options


def update_lists(options=None):
    global_params = GlobalParams()
    csv_params = CSVParams()

    # Initialize options if they were not defined, applying defaults.
    # After this point, the application will behave the same whether it was called as a
    # command or as a module.
    options = set_options(options)

    global_params.verbose = options.verbose
    global_params.this_script = os.path.basename(__file__)

    if not options.reset_lists:
        if options.previous:
            if os.path.abspath(options.previous) == os.path.abspath(options.csv):
                info(
                    (
                        "WARNING: current and previous Hito extractions are the same file,"
                        " result may be unexpected"
                    )
                )
        else:
            try:
                csv_repo = open_git_repo(options.csv)
                csv_repo_git = csv_repo.git()
            except GitPythonModuleMissing:
                raise Exception(
                    "module GitPython not available: use --reset-lists or --previous option"
                )
            except GitRepoNotFound:
                raise Exception(
                    (
                        f"Git repository path associated with {options.csv} not found,"
                        f" use --previous option"
                    )
                )

            csv_file_repo_path = os.path.relpath(options.csv, csv_repo.working_dir)
            changed_files = [item.a_path for item in csv_repo.index.diff(None)]
            csv_file_commited = True
            if csv_file_repo_path.replace("\\", "/") in changed_files:
                debug("Hito extraction modified since last commit (changes not yet committed)")
                csv_file_commited = False
            else:
                if len(changed_files) > 0 and is_windows():
                    debug("Check if CSV file name casing looks correct")
                    csv_file_repo_path_lower = csv_file_repo_path.lower()
                    changed_files_lower = [p.lower() for p in changed_files]
                    if csv_file_repo_path_lower.replace("\\", "/") in changed_files_lower:
                        raise Exception("CSV file name casing looks incorrect, use the right one")
                debug("Hito extraction not modified since last commit")
                debug(
                    "Number of changed files in Git working directory = {} ({})".format(
                        len(changed_files), ", ".join(changed_files)
                    )
                )

            if options.commit_id or csv_file_commited:
                if options.commit_id:
                    previous_csv_commit_hash = options.commit_id
                else:
                    previous_csv_commit_hash = csv_repo_git.log(
                        "--skip",
                        "1",
                        "--max-count",
                        "1",
                        '--format="%H"',
                        "--",
                        csv_file_repo_path,
                    )
                    if len(previous_csv_commit_hash) > 0:
                        previous_csv_commit_hash = previous_csv_commit_hash.replace('"', "")
                    else:
                        if is_windows():
                            info("WANING: CSV file name casing may be incorrect, please check it")
                        raise Exception(
                            (
                                f"No previous version of the CSV file ({options.csv}) found"
                                f" in the Git repository"
                            )
                        )
                previous_csv_commit = get_commit(csv_repo, previous_csv_commit_hash)
                previous_csv_commit_tree = previous_csv_commit.tree
                commit_str = "commit {}".format(previous_csv_commit.hexsha)
            else:
                previous_csv_commit_tree = csv_repo.active_branch.commit.tree
                commit_str = "last commit"
            if os.path.basename(csv_file_repo_path) == csv_file_repo_path:
                debug("Searching for {} in {} blobs".format(csv_file_repo_path, commit_str))
                entries_oid = [
                    e.hexsha for e in previous_csv_commit_tree.blobs if e.name == csv_file_repo_path
                ]
            else:
                debug("Searching for {} in {} trees".format(csv_file_repo_path, commit_str))
                for directory in previous_csv_commit_tree.trees:
                    entries_oid = [
                        e.hexsha
                        for e in directory.blobs
                        if os.path.join(directory.name, e.name) == csv_file_repo_path
                    ]
            if len(entries_oid) > 0:
                csv_file_oid = entries_oid[0]
                debug("File {} OID = {}".format(csv_file_repo_path, csv_file_oid))
            else:
                raise Exception("CSV file {} not part of the Git repository".format(options.csv))

            last_csv_content = csv_repo_git.cat_file("-p", csv_file_oid)
            options.previous = "{}.previous".format(options.csv)
            with open(options.previous, "w", encoding="utf-8") as f:
                debug(
                    "Writing previous contents of CSV file retrieved from Git into {}".format(
                        options.previous
                    )
                )
                # Add the final LF to avoid false differences
                f.write(last_csv_content + "\n")

    lists_from_config = {}
    additional_lists = {}
    exclusion_list = {}
    optout_list = {}

    config = validate_configuration(options.config, options)
    team_params = config["teams"]

    if "csv_columns" in config:
        define_column_names(config["csv_columns"])

    if options.additions:
        try:
            with open(options.additions, "r", encoding="utf-8") as f:
                additional_lists = yaml.safe_load(f)
        except Exception:
            info("ERROR: failed to load the additional lists ({})".format(options.additions))
            raise

        if options.personnel:
            optout_attr = "personnel-lists-optout"
        else:
            optout_attr = "lists-optout"
        for email, email_params in additional_lists.items():
            email = email.lower()
            if optout_attr in email_params:
                optout_list[email] = email_params[optout_attr]

    if options.exclude_list:
        if options.personnel:
            if (
                "exclusion_list" in config
                and "rows" in config["exclusion_list"]
                and "email" in config["exclusion_list"]["rows"]
            ):
                column_email = config["exclusion_list"]["rows"]["email"]
            else:
                column_email = csv_params.column_email
            try:
                with open(options.exclude_list, "r", encoding="utf-8") as csvfile:
                    rows = csv.DictReader(csvfile, delimiter=";")
                    for row in rows:
                        exclusion_list[row[column_email].lower()] = False
                # debug('Exclusion list: {}'.format(exclusion_list))
            except Exception:
                info(
                    "ERROR: failed to read the list of emails to exclude ({})".format(
                        options.exclude_list
                    )
                )
                raise
        else:
            info("WARNING: --exclude-list is ignored if --personnel is not used")

    # When building lists of the whole personnel, list names to create a either passed as an
    # option or retrieved from the configuration file. Create them before reading the CSV file,
    # after checking configuration consistency

    if options.personnel:
        if options.format:
            list_format = options.format
        else:
            list_format = None
        if options.list_name:
            list_names = [options.list_name]
        else:
            list_names = None
        if "general_lists" in config:
            if list_format is None and "format" in config["general_lists"]:
                list_format = config["general_lists"]["format"]
            if list_names is None and "lists" in config["general_lists"]:
                list_names = config["general_lists"]["lists"]
        if list_format is None:
            list_format = GENERAL_LISTS_FORMAT_DEFAULT
        if options.execute:
            if list_format != "listserv":
                raise ConflictingOptions("execute", f"format={options.format}")
            elif "listserv" not in config:
                raise MissingConfigParams("listserv", options.config)
        if list_format == "limesurvey" and len(list_names) > 1:
            raise MultipleLists(list_names, list_format)
        if len(list_names) == 0:
            raise MissingGenListConfig
        else:
            for list_name in list_names:
                lists_from_config[list_name] = None

    # Process personnel CSV file

    (
        list_members,
        personnels,
        persons_added_num,
        persons_no_email_num,
        persons_no_team,
    ) = load_hito_csv(False, options, team_params, lists_from_config, exclusion_list, optout_list)

    if len(list_members) == 0:
        raise NoListCreated(options.pole)

    for email, found in exclusion_list.items():
        if not found:
            info(
                (
                    f"WARNING: email {email} present in exclusion list but not found in the"
                    f" input CSV ({options.csv})"
                )
            )

    # Process the previous version of the personnel CSV file, if specified
    # Ignore exclusion/opt-out lists when reading the CSV to ensure that these persons will be
    # added to the update list as the additional-lists file is not versioned (the previous
    # version cannot be specified)

    if options.previous:
        previous_list_members, _, _, _, _ = load_hito_csv(
            True, options, team_params, lists_from_config
        )
        list_members_added, persons_added_num = hito_changes(list_members, previous_list_members)
        info(
            "Number of lists with new members: {} ({})".format(
                len(list_members_added.keys()),
                ", ".join([x.get_name() for x in list_members_added.values()]),
            )
        )
        list_members_deleted, persons_deleted_num = hito_changes(
            previous_list_members, list_members
        )
        info(
            "Number of lists with deleted members: {} ({})".format(
                len(list_members_deleted.keys()),
                ", ".join([x.get_name() for x in list_members_deleted.values()]),
            )
        )
    else:
        list_members_added = list_members
        for email_list in list_members_added.values():
            email_list.mark_as_new()
        list_members_deleted = {}
        persons_deleted_num = 0

    # Write commands to build lists

    if additional_lists:
        for email, email_params in additional_lists.items():
            email = email.lower()
            if email in personnels:
                personne = personnels[email]
            else:
                debug(
                    (
                        f"INFO: email entry {email} in additional lists doesn't exist in the"
                        f" CSV file ({options.csv})"
                    )
                )
                if "name" in email_params:
                    name = email_params["name"]
                else:
                    name = ""
                if "givenname" in email_params:
                    givenname = email_params["givenname"]
                else:
                    givenname = ""
                personne = Personne(name, givenname, "", email)
            if options.personnel:
                list_attr = "personnel-lists"
            else:
                list_attr = "lists"
            if list_attr in email_params:
                for list_name in email_params[list_attr]:
                    # if --personnel has been specified, ignore additional entries not relevant
                    # for the personnel lists
                    if list_name not in list_members_added and (
                        not options.personnel or list_name in lists_from_config
                    ):
                        if options.previous:
                            debug(
                                "INFO: additional list {} for {} doesn't exist, creating it".format(
                                    list_name, email
                                )
                            )
                            list_members_added[list_name] = EmailList(list_name)
                        else:
                            info(
                                "WARNING: additional list {} for {} doesn't exist".format(
                                    list_name, email
                                )
                            )
                    if list_name in list_members_added:
                        list_members_added[list_name].add_member(personne)

    if options.personnel:
        num_members_added = {}
        num_members_deleted = {}
        for list_name in list_members_added.keys():
            if list_name in list_members_deleted:
                members_deleted = list_members_deleted[list_name]
            else:
                members_deleted = None
            if list_format == "listserv":
                (
                    num_members_added[list_name],
                    num_members_deleted[list_name],
                ) = listserv_update_script(
                    options.output,
                    config["listserv"],
                    list_name,
                    list_members_added[list_name],
                    members_deleted,
                    optout_list,
                )
            elif list_format == "limesurvey":
                # Has already been checked as part of option processing, should not happen except
                # if something wrong is done when building list_members_added
                if len(list_members_added.keys()) > 1:
                    print(
                        (
                            "ERROR: multiple lists are not supported for Limesurvey"
                            " format (internal error)"
                        )
                    )
                    raise MultipleLists(", ".join(list_members_added.keys()), list_format)
                num_members_added[list_name] = limesurvey_update_script(
                    options.output,
                    list_name,
                    list_members_added[list_name],
                    optout_list,
                )
                if members_deleted:
                    info(
                        (
                            "WARNING: it is not possible to delete from Limesurvey the removed"
                            " members. You should manually delete them or remove --previous"
                            " option to generate the full list."
                        )
                    )
                    info(
                        "WARNING: the users to delete are {}".format(
                            ", ".join([x.get_email() for x in members_deleted.get_members()])
                        )
                    )
                    members_deleted = None
            else:
                raise UnsupportedListFmt(list_name, list_format)

        if options.execute:
            if list_format == "listserv":
                listserv_execute(config["listserv"])
            else:
                raise Exception("--execute with --personnel is supported only for LISTSERV")

        print("\n-------------------- SUMMARY --------------------")
        print("Number of lists created: {}".format(len(list_members_added)))
        for list_name in list_members_added.keys():
            print(
                "Total number of persons added in list {}: {}".format(
                    list_name, num_members_added[list_name]
                )
            )
            if members_deleted:
                print(
                    "Total number of persons removed from list {}: {}".format(
                        list_name, num_members_deleted[list_name]
                    )
                )
        print("-------------------------------------------------")

    else:
        # Check if one of --execute or --output has been specified. Else only the list of lists
        # must be generated
        if options.execute or options.output:
            zimbra_cmds = zimbra_update_commands(
                list_members_added,
                list_members_deleted,
                team_params,
                options.list_pattern,
            )
            if options.execute:
                zimbra_execute(config["zimbra"], zimbra_cmds)
            else:
                zimbra_update_script(options.output, zimbra_cmds)

            print("\n-------------------- SUMMARY --------------------")
            print(
                "Number of lists created: {}".format(
                    len([x for x in list_members_added.values() if not x.is_ignored()])
                )
            )
            print(
                "  Number of new lists: {}".format(
                    len(
                        [
                            x
                            for x in list_members_added.values()
                            if x.is_new() and not x.is_ignored()
                        ]
                    )
                )
            )
            num_ignored_lists = len([x for x in list_members_added.values() if x.is_ignored()])
            if num_ignored_lists > 0:
                print(f"  Number of ignored lists: {num_ignored_lists}")
                total_persons_remark = " (including ignored lists)"
            else:
                total_persons_remark = ""
            print(
                "  Number of deleted lists: {}".format(
                    len(
                        [
                            x
                            for x in list_members_deleted.values()
                            if x.is_new() and not x.is_ignored()
                        ]
                    )
                )
            )
            print(f"Total number of persons {total_persons_remark}: {len(personnels)}")
            print("  Number of persons added to a list: {}".format(persons_added_num))
            if persons_deleted_num > 0:
                print("  Number of persons removed from a list: {}".format(persons_deleted_num))
            print("  Number of persons not belonging to any team: {}".format(len(persons_no_team)))
            print("  Number of persons without email: {}".format(persons_no_email_num))
            print("-------------------------------------------------")

        if options.created_lists:
            created_lists(
                options.created_lists,
                list_members_added,
                team_params["email_domain"],
                team_params["index_disabled"],
            )


def main():
    # Search the config file in the current directory first
    config_file_path, config_file_name = get_config_path_default()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--additional-lists",
        dest="additions",
        help="YAML file describing people to add or remove from lists",
    )
    parser.add_argument(
        "--config",
        help="Configuration file (D: {} in the CSV directory or {})".format(
            config_file_name, config_file_path
        ),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Print debugging messsages",
    )
    parser.add_argument("--created-lists", help="File name for storing created lists")
    output_opt = parser.add_mutually_exclusive_group()
    output_opt.add_argument(
        "--execute",
        action="store_true",
        default=False,
        help="Execute commands rather than creating a script",
    )
    output_opt.add_argument(
        "--output",
        "--script",
        default=None,
        help="Shell script name to configure Zimbra",
    )
    previous_opt = parser.add_mutually_exclusive_group()
    previous_opt.add_argument("--previous", help="CSV file containing the previous Hito extraction")
    previous_opt.add_argument(
        "--git-commit",
        "--commit-id",
        dest="commit_id",
        help="Git commit hash to use to retrieve the previous version the Hito extraction",
    )
    previous_opt.add_argument(
        "--reset-lists",
        action="store_true",
        default=False,
        help="Redefine the list from scratch rather than from previous version",
    )
    group_list_opts = parser.add_argument_group(
        "Group lists", "Lists built from personnel group membership"
    )
    group_list_opts.add_argument(
        "--ignore-unassigned",
        dest="warn_unassigned",
        action="store_false",
        default=True,
        help="Do not issue a warning if somebody doesn't belong to any team",
    )
    group_list_opts.add_argument(
        "--level",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="Max number of group level to process",
    )
    group_list_opts.add_argument(
        "--list-pattern",
        default=None,
        help="Name of lists to generate, can be a regexp",
    )
    group_list_opts.add_argument("--pole", help="Process only lists related to this pole")
    personnel_list_opts = parser.add_argument_group(
        "Personnel list", "Lists containing all the personnel"
    )
    personnel_list_opts.add_argument(
        "--personnel",
        action="store_true",
        default=False,
        help="Write the personnel list instead of the lists",
    )
    personnel_list_opts.add_argument(
        "--exclude-list",
        help="CSV file containing a list of emails to exclude (requires --personnel)",
    )
    parser.add_argument(
        "--format",
        choices=["limesurvey", "listserv"],
        help="Format of the output script",
    )
    personnel_list_opts.add_argument(
        "--list-name",
        help="Name of the list to create (overrides lists specified in the configuration file",
    )
    parser.add_argument("csv", help="Personnel file")
    options = parser.parse_args()

    update_lists(options=options)


if __name__ == "__main__":
    sys.excepthook = exception_handler
    exit(main())
