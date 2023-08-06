import binascii
from base64 import b64decode
from importlib.machinery import PathFinder
from os import path
from pathlib import Path
import re
import sys

from metaflow._vendor import click


class CheckException(Exception):
    headline = "Installation validation failed: "

    def __init__(self, mitigation):
        self._mitigation = mitigation

    def mitigation(self):
        return self._mitigation


class ModuleResolutionException(CheckException):
    def __init__(self, module_name, mitigation=None):
        super().__init__(mitigation)
        self.module_name = module_name
        self.package_paths = [p for p in sys.path if p.endswith("site-packages")]

    def __str__(self):
        return "Unable to resolve module '{}'.".format(self.module_name)


class InstallValidationException(CheckException):
    def __init__(self, message, mitigation=None):
        super().__init__(mitigation)
        self.message = message

    def __str__(self):
        return self.message


NO_METAFLOW_INSTALL_MESSAGE = "Resolution of 'metaflow' module succeeded but no Metaflow installation was detected."

EXISTING_METAFLOW_MESSAGE = """An existing Metaflow installation was found at:

{}
"""

MISSING_EXTENSIONS_MESSAGE = (
    "The Outerbounds Platform extensions for Metaflow was not found."
)

BAD_EXTENSION_MESSAGE = (
    "Mis-installation of the Outerbounds Platform extension package has been detected."
)


class Narrator:
    def __init__(self, verbose):
        self.verbose = verbose

    def announce_section(self, name):
        if not self.verbose:
            click.secho("Validating {}...".format(name), nl=False)

    def section_ok(self):
        if not self.verbose:
            click.secho("\U0001F600")

    def section_not_ok(self):
        if not self.verbose:
            click.secho("\U0001F641")

    def announce_check(self, name):
        if self.verbose:
            click.secho("Checking {}...".format(name), nl=False)

    def ok(self, force=False):
        if self.verbose or force:
            click.secho("OK", fg="green")

    def not_ok(self, reason=None, force=False):
        if self.verbose or force:
            if reason is None:
                click.secho("NOT OK", fg="red")
            else:
                message = click.style("NOT OK", fg="red")
                message = "{} {}".format(
                    message, click.style("(" + reason + ")", fg="white")
                )
                click.secho(message)

    def show_error(self, err):
        if self.verbose:
            click.echo("")
            click.secho(err.headline, fg="red", nl=False)
            click.secho(str(err))
            mitigation = err.mitigation()
            if mitigation is not None:
                click.secho(mitigation, bold=True)


class Checker:
    def check(self):
        pass


class InstallChecker(Checker):
    def __init__(self, narrator):
        self.narrator = narrator

    def check(self):
        try:
            self.narrator.announce_section("installed packages")
            self.narrator.announce_check("Outerbounds Metaflow package")
            self.check_ob_metaflow()
            self.narrator.ok()

            self.narrator.announce_check("Outerbounds Platform extensions package")
            self.check_ob_extension()
            self.narrator.ok()
            return True
        except CheckException as e:
            self.narrator.not_ok()
            self.narrator.show_error(e)
            return False

    def check_ob_metaflow(self):
        spec = PathFinder.find_spec("metaflow")
        # We can't resolve metaflow module.
        if spec is None:
            raise ModuleResolutionException("metaflow")
        # We can resolve the module but we need to
        # make sure we're getting it from the correct
        # package.
        basedir = Path(path.join(path.dirname(spec.origin), ".."))
        # Next, let's check for parallel installations of ob-metaflow
        # and OSS metaflow. This can cause problems because they
        # overwrite each other.
        found = list(basedir.glob("metaflow-*.dist-info"))
        if len(found) > 0:
            # We found an existing OSS Metaflow install.
            raise InstallValidationException(
                EXISTING_METAFLOW_MESSAGE.format(click.style(str(found[0]), bold=True)),
                mitigation="Please remove any existing Metaflow installations and reinstall the Outerbounds package.",
            )
        # For completeness, let's verify ob_metaflow is really installed.
        # Should never get here since importing Metaflow's vendored version of click
        # would've failed much earlier on.
        found = list(basedir.glob("ob_metaflow-*.dist-info"))
        if len(found) == 0:
            raise InstallValidationException(
                NO_METAFLOW_INSTALL_MESSAGE,
                mitigation="Please uninstall and reinstall the Outerbounds package.",
            )

    def check_ob_extension(self):
        spec = PathFinder.find_spec("metaflow")
        basedir = Path(path.join(path.dirname(spec.origin), ".."))
        # Metaflow install looks fine. Let's verify the correct extensions were installed.
        extensions = Path(basedir, "metaflow_extensions", "outerbounds")
        # Outerbounds extensions not found at all
        if not extensions.exists():
            raise InstallValidationException(
                MISSING_EXTENSIONS_MESSAGE,
                mitigation="Please remove any existing Metaflow installations and reinstall the Outerbounds package.",
            )
        subdirs = [
            d.name
            for d in extensions.glob("*")
            if d.is_dir() and not d.name.startswith("__")
        ]
        subdirs.sort()
        if subdirs != ["config", "plugins", "toplevel"]:
            raise InstallValidationException(
                BAD_EXTENSION_MESSAGE,
                mitigation="Please uninstall & reinstall the Outerbounds package.",
            )


class ConfigEntrySpec:
    def __init__(self, name, expr, expected=None):
        self.name = name
        self.expr = re.compile(expr)
        self.expected = expected


def get_config_specs():
    return [
        ConfigEntrySpec("METAFLOW_DATASTORE_SYSROOT_S3", "s3://[a-z0-9\-]+/metaflow"),
        ConfigEntrySpec("METAFLOW_DATATOOLS_S3ROOT", "s3://[a-z0-9\-]+/data"),
        ConfigEntrySpec("METAFLOW_DEFAULT_AWS_CLIENT_PROVIDER", "obp", expected="obp"),
        ConfigEntrySpec("METAFLOW_DEFAULT_DATASTORE", "s3", expected="s3"),
        ConfigEntrySpec("METAFLOW_DEFAULT_METADATA", "service", expected="service"),
        ConfigEntrySpec(
            "METAFLOW_KUBERNETES_NAMESPACE", "jobs\-default", expected="jobs-default"
        ),
        ConfigEntrySpec("METAFLOW_KUBERNETES_SANDBOX_INIT_SCRIPT", "eval \$\(.*"),
        ConfigEntrySpec("METAFLOW_SERVICE_AUTH_KEY", "[a-zA-Z0-9!_\-\.]+"),
        ConfigEntrySpec("METAFLOW_SERVICE_URL", "https://metadata\..*"),
        ConfigEntrySpec("METAFLOW_UI_URL", "https://ui\..*"),
        ConfigEntrySpec("OBP_AUTH_SERVER", "auth\..*"),
    ]


class ConfigurationChecker(Checker):
    def __init__(self, narrator):
        self.narrator = narrator

    def check(self):
        self.narrator.announce_section("local Metaflow config")
        from metaflow import metaflow_config

        has_err = False
        config = metaflow_config.init_config()
        for spec in get_config_specs():
            self.narrator.announce_check("config entry " + spec.name)
            if spec.name not in config:
                if not has_err:
                    has_err = True
                reason = "Missing"
                if spec.expected is not None:
                    reason = "".join([reason, ", expected '{}'".format(spec.expected)])
                self.narrator.not_ok(reason=reason)
            else:
                v = config[spec.name]
                if spec.expr.fullmatch(v) is None:
                    if not has_err:
                        has_err = True
                    if spec.name.find("AUTH") == -1:
                        reason = "Have '{}'".format(v)
                        if spec.expected is not None:
                            reason += ", expected '{}'".format(spec.expected)
                    else:
                        reason = "Bad value"
                    self.narrator.not_ok(reason=reason)
                else:
                    self.narrator.ok()
        if has_err:
            self.narrator.section_not_ok()
        else:
            self.narrator.section_ok()
        return not has_err


@click.group(help="The Outerbounds Platform CLI", no_args_is_help=True)
def cli(**kwargs):
    pass


@cli.command(help="Check packages and configuration for common errors")
@click.option(
    "-n",
    "--no-config",
    is_flag=True,
    default=False,
    show_default=True,
    help="Skip validating local Metaflow configuration",
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="Verbose output")
def check(no_config, verbose):
    narrator = Narrator(verbose)
    ic = InstallChecker(narrator)
    icr = ic.check()
    ccr = True
    if icr:
        narrator.section_ok()
    else:
        narrator.section_not_ok()
    if icr:
        if not no_config:
            cc = ConfigurationChecker(narrator)
            ccr = cc.check()
    if not icr or not ccr:
        sys.exit(1)


@cli.command(help="Decode Outerbounds Platform configuration strings")
@click.option(
    "-o",
    "--out",
    default="~/.metaflowconfig/config2.json",
    help="Metaflow configuration file path",
    show_default=True,
)
@click.option(
    "-e",
    "--echo",
    is_flag=True,
    help="Print decoded configuration to stdout",
)
@click.argument("encoded_config", required=False)
def configure(encoded_config=None, out=None, echo=None):
    if encoded_config is None:
        encoded_config = "".join(sys.stdin.readlines()).replace("\n", "")
    if encoded_config == "" or encoded_config is None:
        sys.exit(1)
    try:
        unpacked = unpack_configuration(encoded_config)
    except binascii.Error:
        click.secho("Decoding config text failed", fg="red")
        sys.exit(1)
    if echo:
        click.secho(unpacked)
    else:
        out = path.expandvars(path.expanduser(out))
        with open(out, mode="x") as fd:
            fd.write(unpacked)


def unpack_configuration(text):
    if text.startswith("echo -ne"):
        return unpack_shell_blob(text)
    else:
        return unpack_base64_blob(text)


def unpack_shell_blob(text):
    text = text.replace('echo -ne "', "")
    return text[0:-1]


def unpack_base64_blob(text):
    text_bytes = bytes(text, "UTF-8")
    return b64decode(text_bytes, validate=True).decode("UTF-8")
