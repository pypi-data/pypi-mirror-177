"""
Collector plugin for maven artifacts
"""

from tempfile import NamedTemporaryFile
from typing import Any, Dict, Optional

from packageurl import PackageURL  # type: ignore

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.context import Context
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.result import Result

_DEFAULT_MAVEN_EXT = "tar.gz"
_MAVEN_DEP_PLUGIN = "org.apache.maven.plugins:maven-dependency-plugin:2.5.1"


class CollectMavenPlugin(SerialCollectorPlugin):
    """
    Collector plugin for maven artifacts
    """

    supported_purl_types = ["maven"]
    required_commands = ["mvn"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: Context, config: Optional[Dict] = None) -> None:
        super().__init__(context=context, config=config)
        self.extra_opts = []
        if self.config is not None:
            if "maven_command" in self.config:
                self.required_commands = [self.config["maven_command"]]
            if "maven_opts" in self.config:
                self.extra_opts = self.config["maven_opts"]

    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds: Optional[CredObject] = None):
        """
        Copy a component to the local collection directory structure
        """
        purl = PackageURL.from_string(comp.purl)
        result = self.check_purl_specified_url(purl, repo_url)
        if not result.is_success():
            return result

        extension = purl.qualifiers.get("type", _DEFAULT_MAVEN_EXT)

        password_list = []
        if creds is not None:
            password_list = [creds.password]

        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.namespace}")

        self.get_logger().info(
            msg="Copying maven artifact:",
            indent_level=2,
        )

        self.get_logger().info(
            msg=f"source: {repo_url}",
            indent_level=3,
        )

        self.get_logger().info(
            msg=f"destination: {target_dir}",
            indent_level=3,
        )

        settings_content = """<settings>
            <servers>
                <server>
                    <id>repoId</id>
                    <username>${repo.login}</username>
                    <password>${repo.pwd}</password>
                </server>
            </servers>
        </settings>
        """

        with NamedTemporaryFile(mode="w+") as settings_file:
            settings_file.write(settings_content)
            settings_file.flush()

            command = [
                self.required_commands[0],
                f"{_MAVEN_DEP_PLUGIN}:get",
                f"--settings={settings_file.name}",
                f"-DremoteRepositories=repoId::::{repo_url}",
                f"-Dpackaging={extension}",
                f"-Dartifact={purl.namespace}:{purl.name}:{purl.version}",
                f"-Ddest={target_dir}/{purl.name}-{purl.version}.{extension}",
            ]

            if creds is not None:
                command.extend(
                    [f"-Drepo.login={creds.username}", f"-Drepo.pwd={creds.password}"]
                )

            command.extend(self.extra_opts)

            run_result = self.run_command(command, password_list)
            if run_result.returncode != 0:
                msg = f"Failed to download maven artifact {purl.namespace}:{purl.name}:{purl.version} type={extension}"
                self.get_logger().debug(msg=msg, indent_level=2)
                return Result.retry(message=msg)

            if extension != "pom":
                command = [
                    self.required_commands[0],
                    f"{_MAVEN_DEP_PLUGIN}:get",
                    f"--settings={settings_file.name}",
                    f"-DremoteRepositories=repoId::::{repo_url}",
                    "-Dpackaging=pom",
                    f"-Dartifact={purl.namespace}:{purl.name}:{purl.version}",
                    f"-Ddest={target_dir}/{purl.name}-{purl.version}.pom",
                ]

                if creds is not None:
                    command.extend(
                        [
                            f"-Drepo.login={creds.username}",
                            f"-Drepo.pwd={creds.password}",
                        ]
                    )

                command.extend(self.extra_opts)

                run_result = self.run_command(command, password_list)
                if run_result.returncode != 0:
                    msg = f"Failed to download pom for maven artifact {purl.namespace}:{purl.name}:{purl.version}"
                    self.get_logger().debug(msg=msg, indent_level=2)
                    return Result.retry(message=msg)

        return Result.success()
