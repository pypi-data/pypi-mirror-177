# -*- coding: utf-8 -*-


class ConflictingOptions(Exception):
    """
    Raised when using conflicting command options that cannot be handled by the parser
    """

    def __init__(self, option1, option2):
        self.msg = "Command options {} and {} are mutually exclusive".format(option1, option2)

    def __str__(self):
        return repr(self.msg)


class ConflictingConfigParams(Exception):
    """
    Raised when using conflicting conflicting parameters in the configuration file
    """

    def __init__(self, file, option1, option2):
        self.msg = "Configuration parameters {} and {} are mutually exclusive in {}".format(
            option1, option2, file
        )

    def __str__(self):
        return repr(self.msg)


class GitCommitNotFound(Exception):
    """
    Raised when a commit cannot be found in the repository history
    """

    def __init__(self, commit_hash):
        self.msg = "Commit {} cannot be found in Git history".format(commit_hash)

    def __str__(self):
        return repr(self.msg)


class GitCommitHashNotUnique(Exception):
    """
    Raised when several commits match the given commit hash prefix
    """

    def __init__(self, commit_hash):
        self.msg = "Several commits match the hash prefix {}".format(commit_hash)

    def __str__(self):
        return repr(self.msg)


class GitPythonModuleMissing(Exception):
    """
    Raised when the GitPython module is required but not available
    """

    def __init__(self):
        self.msg = "GitPython module is required for using Git"

    def __str__(self):
        return repr(self.msg)


class GitRepoNotFound(Exception):
    """
    Raised when no Git repository associated with a filename cannot be found
    """

    def __init__(self, filename):
        self.msg = "{} file is not part of a Git repository".format(filename)

    def __str__(self):
        return repr(self.msg)


class InvalidCSVFormat(Exception):
    """
    Raised when the CSV file doesn't have the required columns
    """

    def __init__(self, filename):
        self.msg = "CSV input file ({}) is missing required columns".format(filename)

    def __str__(self):
        return repr(self.msg)


class MissingConfigParams(Exception):
    """
    Raised when no a required parameter is missing in the configuration file
    """

    def __init__(self, param, file):
        self.msg = "Parameter '{}' is missing in the configuration file ({})".format(param, file)

    def __str__(self):
        return repr(self.msg)


class MissingGenListConfig(Exception):
    """
    Raised when no there is not configuration for lists of all persons
    """

    def __init__(self):
        self.msg = (
            "Configuration is missing for general lists (--personnel) and"
            " --list-name is not present"
        )

    def __str__(self):
        return repr(self.msg)


class MultipleLists(Exception):
    """
    Raised when several lists are created but the output format doesn't support it
    """

    def __init__(self, list_names, list_format):
        self.msg = "Multiple lists ({}) not supported by the output format ({})".format(
            list_names, list_format
        )

    def __str__(self):
        return repr(self.msg)


class NoListCreated(Exception):
    """
    Raised when no list is created as a result of command options
    """

    def __init__(self, selected_pole):
        self.msg = "No list created : check --pole value ({})".format(selected_pole)

    def __str__(self):
        return repr(self.msg)


class OptionParsingError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class UnsupportedListFmt(Exception):
    """
    Raised when the output format requested is not supported for the current list
    """

    def __init__(self, list_name, fmt):
        self.msg = "Unsupported format for list {} ({})".format(list_name, fmt)

    def __str__(self):
        return repr(self.msg)
