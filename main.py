from monitors.ema import EmaMonitor
from rss.generator import RssGenerator
import config

def main():
    print("Starting EMA monitoring process...")
    
    # Initialize the specific monitor
    ema_monitor = EmaMonitor(substances=config.SUBSTANCES)
    
    # Fetch all items and new updates
    all_items, new_updates = ema_monitor.fetch_items()
    
    if new_updates:
        print(f"\n✅ Found {len(new_updates)} new updates.")
        for update in new_updates:
            print(f"  - [{update['substance'].upper()}] {update['product']}: {update['title']}")
    else:
        print("\n✅ No new updates found since last check.")

    # Initialize the RSS generator with channel info from config
    rss_generator = RssGenerator(
        filename=config.RSS_FILENAME,
        channel_title=config.RSS_CHANNEL_TITLE,
        channel_link=config.RSS_CHANNEL_LINK,
        channel_description=config.RSS_CHANNEL_DESCRIPTION
    )
    
    # Generate the RSS feed using all items
    rss_generator.generate(all_items=all_items)
        
    print("\nMonitoring process finished.")

if __name__ == "__main__":
    main()
