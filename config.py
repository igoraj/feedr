# List of substances to monitor on the EMA website
SUBSTANCES = ["semaglutide", "liraglutide", "tirzepatide", "dapagliflozin", "sitagliptin", "apremilast"]

# RSS Feed Configuration
RSS_FILENAME = "ema_updates.xml"
RSS_CHANNEL_TITLE = "EMA Medicine Updates"
RSS_CHANNEL_LINK = "https://www.ema.europa.eu/en/medicines"
RSS_CHANNEL_DESCRIPTION = "Monitored updates for specific medicines from the European Medicines Agency."

# GitHub Pages URL configuration for the absolute feed URL
# IMPORTANT: Change these to your GitHub username and repository name
GITHUB_USERNAME = "igoraj"
GITHUB_REPONAME = "feedr"
RSS_FEED_URL = f"https://{GITHUB_USERNAME}.github.io/{GITHUB_REPONAME}/{RSS_FILENAME}"
