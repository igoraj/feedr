from lxml import etree
from datetime import datetime
from email.utils import formatdate
from typing import List, Dict, Any, Optional

class RssGenerator:
    def __init__(self, filename: str, channel_title: str, channel_link: str, channel_description: str, feed_url: str):
        self.filename = filename
        self.channel_title = channel_title
        self.channel_link = channel_link
        self.channel_description = channel_description
        self.feed_url = feed_url

    def generate(self, all_items: List[Dict[str, Any]], max_items: int = 50):
        print(f"Generating RSS feed at {self.filename}...")

        # Sort items by date (newest first)
        def parse_date(item):
            date_str = item.get("date")
            if not date_str:
                return datetime.min
            try:
                # Format: 'Tue, 30 Sep 2025 13:49:00 +0200'
                return datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                try:
                    # Fallback for other formats if necessary
                    return datetime.fromisoformat(date_str)
                except ValueError:
                    return datetime.min

        sorted_item_data = sorted(all_items, key=parse_date, reverse=True)

        # Determine the last build date from the newest item
        if sorted_item_data:
            latest_date = parse_date(sorted_item_data[0])
            last_build_date = formatdate(latest_date.timestamp())
        else:
            last_build_date = formatdate(datetime.now().timestamp())

        # Build the RSS structure
        NSMAP = {
            "atom": "http://www.w3.org/2005/Atom",
            "content": "http://purl.org/rss/1.0/modules/content/",
            "dc": "http://purl.org/dc/elements/1.1/"
        }
        rss = etree.Element("rss", version="2.0", nsmap=NSMAP)
        channel = etree.SubElement(rss, "channel")

        etree.SubElement(channel, "title").text = self.channel_title
        etree.SubElement(channel, "link").text = self.channel_link
        etree.SubElement(channel, "description").text = etree.CDATA(self.channel_description)
        etree.SubElement(channel, "lastBuildDate").text = last_build_date
        
        atom_link = etree.SubElement(channel, etree.QName(NSMAP["atom"], "link"))
        atom_link.set("href", self.feed_url)
        atom_link.set("rel", "self")
        atom_link.set("type", "application/rss+xml")

        # Add items, respecting max_items
        for item_data in sorted_item_data[:max_items]:
            item_elem = etree.SubElement(channel, "item")

            etree.SubElement(item_elem, "title").text = item_data.get("title", "No Title")
            etree.SubElement(item_elem, "link").text = item_data.get("link", "")
            
            guid_elem = etree.SubElement(item_elem, "guid")
            guid_elem.text = item_data.get("id") or item_data.get("link")
            guid_elem.set("isPermaLink", "true")

            etree.SubElement(item_elem, "description").text = etree.CDATA(item_data.get("description", ""))
            
            pub_date_elem = etree.SubElement(item_elem, "pubDate")
            
            # Ensure the date is parsed and then formatted consistently
            parsed_date = parse_date(item_data)
            if parsed_date != datetime.min:
                pub_date_elem.text = formatdate(parsed_date.timestamp())
            else:
                pub_date_elem.text = "No Date Available"

        # Write to file
        tree = etree.ElementTree(rss)
        tree.write(self.filename, pretty_print=True, xml_declaration=True, encoding="utf-8")

        print(f"RSS feed updated. Total items: {len(channel.findall('item'))}")

