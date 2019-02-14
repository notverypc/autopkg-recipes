# autopkg-recipes

## Slacker PostProcessor

This requires requests to be installed:
```
pip install requests
```
This is based on the Slack notification post-processor for AutoPkg/JSSImporter that Graham Pugh created:
https://grahamrpugh.com/2017/12/22/slack-for-autopkg-jssimporter.html

### Customising notifications:
Change the following values to match your environment.
```
AUTOPKGICON = "https://avatars0.githubusercontent.com/u/5170557?s=200&v=4"
ICONEMOJI=":ghost:"
USERNAME = "AutoPKG"
```
## Microsoft Office Recipes
These recipes are based on the Office 365 recipes by dataJAR (https://github.com/autopkg/dataJAR-recipes) and the Pull Request from aysiu.
These recipes download and import the full installer pkgs for Microsoft Office 365 apps into Munki and using the "installer_choices_xml" will NOT to install MAU.
This is accomplished via the Office 365 recipes from rtrouton-recipes.
These in turn, utilise the fwlink's found on macadmins.software
