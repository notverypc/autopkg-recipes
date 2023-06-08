¡# autopkg-recipes

## SlackPostCurl
This is a replacement for my previous Slacker PostProcessor. It has no dependencies and works with AutoPKG 2.7

You'll need to create a webhook in Slack:
https://slack.com/intl/en-gb/help/articles/115005265063-Incoming-webhooks-for-Slack

Add this repo:
``` 
autopkg repo-add notverypc/autopkg-recipes 
```

Then run a recipe or recipes, replacing the webhook_url:
``` shell
autopkg run myRecipe.munki MakeCatalogs.munki --post="com.github.notverypc.autopkg-recipes.postprocessors/SlackPostCurl" --key webhook_url="https://hooks.slack.com/services/XXXXXXX"
```

Or run using a recipe list:
``` shell
autopkg run --recipe-list="/path/to/my/RecipeList.txt" -post="com.github.notverypc.autopkg-recipes.postprocessors/SlackPostCurl" --key webhook_url="https://hooks.slack.com/services/XXXXXXX" 
```

This will post to the channel linked to your webhook using the default `slack_username` AutoPKG.

The following can keys can be added to the command:
	`slack_channel` = Slack channel (for overriding the default)
	`slack_icon_emoji` = Slack display emoji markup.
	`slack_icon_url` = Slack display icon URL.
	`slack_username` = Slack message display name.

If you wanted to use the AutoPKG icon:

```shell
autopkg run --recipe-list="/path/to/my/RecipeList.txt" -post="com.github.notverypc.autopkg-recipes.postprocessors/SlackPostCurl" --key webhook_url="https://hooks.slack.com/services/XXXXXXX" --key slack_icon_url="https://avatars0.githubusercontent.com/u/5170557?s=200&v=4"
```

If you wanted to override the slack channel as well:
```shell
autopkg run --recipe-list="/path/to/my/RecipeList.txt" -post="com.github.notverypc.autopkg-recipes.postprocessors/SlackPostCurl" --key webhook_url="https://hooks.slack.com/services/XXXXXXX" --key slack_icon_url="https://avatars0.githubusercontent.com/u/5170557?s=200&v=4" --key slack_channel="testing"
```
 

## Slacker PostProcessor
*** This is Deprecated and will no longer be updated. Please use SlackPostCurl instead. ***

## Microsoft Office Recipes
These recipes are based on the Office 365 recipes by dataJAR (https://github.com/autopkg/dataJAR-recipes) and the Pull Request from aysiu.

These recipes download and import the full installer pkgs for Microsoft Office 365 apps into Munki and using the "installer_choices_xml" will NOT to install MAU.

This is accomplished via the Office 365 recipes from rtrouton-recipes.

These in turn, utilise the fwlink's found on macadmins.software
