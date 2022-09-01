#!/usr/local/autopkg/python
"""See docstring for SlackPostCurl class

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

        Based on Shawn Maddock's gist https://gist.github.com/smaddock/4b9a1cb7ce26398136aec1521359ff9b
        Based on the Teams post processor by Andy Semak (@asemak)
        Based on Graham Pugh's slacker.py - "
        https://github.com/grahampugh/recipes/blob/master/PostProcessors/slacker.py
        and @thehill idea on macadmin slack - https://macadmins.slack.com/archives/CBF6D0B97/p1542379199001400

Takes elements from:
- https://github.com/autopkg/grahampugh-recipes/blob/main/JamfUploaderProcessors/JamfUploaderSlacker.py
- https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784
- https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py
"""

import json

from time import sleep
from autopkglib import Processor, ProcessorError, URLGetter


__all__ = ["SlackPostCurl"]


class SlackPostCurl(URLGetter):
    """Posts to Slack via webhook based on output of a MunkiImporter."""

    description = __doc__
    input_variables = {
        "munki_info": {
            "required": False,
            "description": "Munki info dictionary to use to display info.",
        },
        "munki_repo_changed": {
            "required": False,
            "description": "Whether or not item was imported.",
        },
        "slack_channel": {
            "description": "Slack channel (for overriding the default).",
            "required": False,
        },
        "slack_icon_emoji": {
            "description": "Slack display emoji markup.",
            "required": False,
        },
        "slack_icon_url": {
            "default": "",
            "description": "Slack display icon URL.",
            "required": False,
        },
        "slack_username": {
            "default": "AutoPKG",
            "description": "Slack message display name.",
            "required": False,
        },
        "webhook_url": {"description": "Slack webhook.", "required": True},
    }
    output_variables = {}

    def slack_status_check(self, proc_stdout):
        """Return a message dependent on the HTTP response"""
        if proc_stdout == "ok":
            self.output("Slack webhook sent successfully")
            return "break"
        else:
            self.output("WARNING: Slack webhook failed to send")
            self.output(proc_stdout, verbose_level=2)

    def main(self):
        was_imported = self.env.get("munki_repo_changed")
        munkiInfo = self.env.get("munki_info")
        webhook_url = self.env.get("webhook_url")
        slack_channel = self.env.get("slack_channel")
        slack_icon_emoji = self.env.get("slack_icon_emoji") or ""
        slack_icon_url = self.env.get("slack_icon_url") or ""
        slack_username = self.env.get("slack_username")

        if was_imported:
            name = self.env.get("munki_importer_summary_result")[
                "data"]["name"]
            version = self.env.get("munki_importer_summary_result")[
                "data"]["version"]
            pkg_path = self.env.get("munki_importer_summary_result")["data"][
                "pkg_repo_path"
            ]
            pkginfo_path = self.env.get("munki_importer_summary_result")["data"][
                "pkginfo_path"
            ]
            catalog = self.env.get("munki_importer_summary_result")[
                "data"]["catalogs"]
            if name:
                slack_text = (
                    "*New Item Added to Munki:*\nTitle: *%s*\nVersion: *%s*\nCatalog: *%s*\nPkg Path: *%s*\nPkginfo Path: *%s*"
                    % (name, version, catalog, pkg_path, pkginfo_path)
                )
                slack_data = {
                    "text": slack_text,
                    "username": slack_username,
                }
                if slack_channel:
                    slack_data["channel"] = slack_channel
                if slack_icon_emoji:
                    slack_data["icon_emoji"] = slack_icon_emoji
                if slack_icon_url:
                    slack_data["icon_url"] = slack_icon_url

                json_data = json.dumps(slack_data)

            # Build the headers
            count = 0
            while True:
                count += 1
                self.output("Slack webhook post attempt {}".format(
                    count), verbose_level=2)
                curl_cmd = [
                    self.curl_binary(),
                    "--data",
                    json_data,
                    "--header",
                    "Content-Type: application/json",
                    "--request",
                    "POST",
                    "--show-error",
                    "--silent",
                    webhook_url,
                ]
                (
                    proc_stdout,
                    proc_stderr,
                ) = self.execute_curl(curl_cmd)
                # check HTTP response
                if self.slack_status_check(proc_stdout) == "break":
                    break
                if count >= 5:
                    self.output(
                        "Slack webhook send did not succeed after 5 attempts")
                    self.output(f"HTTP Response: {proc_stderr}")
                    raise ProcessorError("ERROR: Slack webhook failed to send")
                sleep(10)


if __name__ == "__main__":
    processor = SlackPostCurl()
    processor.execute_shell()
