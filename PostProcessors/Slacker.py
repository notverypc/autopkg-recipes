#!/usr/bin/python
#
# Copyright 2019 Ben Reilly
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from autopkglib import Processor, ProcessorError

import subprocess
import os.path
import json
import requests

# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/

__all__ = ["Slacker"]

class Slacker(Processor):
    description = ("Posts to Slack via webhook based on output of a MunkiImporter. "
                    "Based on Graham Pugh's slacker.py - https://github.com/grahampugh/recipes/blob/master/PostProcessors/slacker.py"
                    "and "
                    "@thehill idea on macadmin slack - https://macadmins.slack.com/archives/CBF6D0B97/p1542379199001400"
                    "Takes elements from " "https://gist.github.com/devStepsize/b1b795309a217d24566dcc0ad136f784"
                    "and "
                    "https://github.com/autopkg/nmcspadden-recipes/blob/master/PostProcessors/Yo.py")

    input_variables = {
        "munki_info": {
            "required": False,
            "description": ("Munki info dictionary to use to display info.")
        },
        "munki_repo_changed": {
            "required": False,
            "description": ("Whether or not item was imported.")
        },
        "webhook_url": {
            "required": False,
            "description": ("Slack webhook.")
        }
    }
    output_variables = {
    }

    __doc__ = description

    def main(self):
        was_imported = self.env.get("munki_repo_changed")
        munkiInfo = self.env.get("munki_info")
        webhook_url = self.env.get("webhook_url")

        # Slack Custom Settings
        ICONEMOJI = ":ghost:"
        AUTOPKGICON = "https://avatars0.githubusercontent.com/u/5170557?s=200&v=4"
        USERNAME = "AutoPKG"

        if was_imported:
            name = self.env.get("munki_importer_summary_result")["data"]["name"]
            version = self.env.get("munki_importer_summary_result")["data"]["version"]
            pkg_path = self.env.get("munki_importer_summary_result")["data"]["pkg_repo_path"]
            pkginfo_path = self.env.get("munki_importer_summary_result")["data"]["pkginfo_path"]
            catalog = self.env.get("munki_importer_summary_result")["data"]["catalogs"]
            if name:
                slack_text = "*New item added to repo:*\nTitle: *%s*\nVersion: *%s*\nCatalog: *%s\n*Pkg Path: *%s*\nPkginfo Path: *%s*" % (name, version, catalog, pkg_path, pkginfo_path)
                slack_data = {'text': slack_text, 'icon_url': AUTOPKGICON, 'username': USERNAME}

                response = requests.post(
                webhook_url, json=slack_data)
                if response.status_code != 200:
                    raise ValueError(
                                'Request to slack returned an error %s, the response is:\n%s'
                                % (response.status_code, response.text)
                                )


if __name__ == "__main__":
    processor = Slacker()
    processor.execute_shell()
