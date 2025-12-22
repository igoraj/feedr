import xml.etree.ElementTree as ET
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

        # Build the RSS structure
        rss = ET.Element("rss", version="2.0", attrib={"xmlns:atom": "http://www.w3.org/2005/Atom"})
        channel = ET.SubElement(rss, "channel")

        ET.SubElement(channel, "title").text = self.channel_title
        ET.SubElement(channel, "link").text = self.channel_link
        ET.SubElement(channel, "description").text = self.channel_description
        ET.SubElement(channel, "lastBuildDate").text = formatdate(datetime.now().timestamp())
        
        # Add self-referencing atom link with the absolute URL
        atom_link = ET.SubElement(channel, "atom:link")
        atom_link.set("href", self.feed_url)
        atom_link.set("rel", "self")
        atom_link.set("type", "application/rss+xml")

        # Add items, respecting max_items
        for item_data in sorted_item_data[:max_items]:
            item_elem = ET.Element("item")

            ET.SubElement(item_elem, "title").text = item_data.get("title", "No Title")
            ET.SubElement(item_elem, "link").text = item_data.get("link", "")
            ET.SubElement(item_elem, "guid").text = item_data.get("id") or item_data.get("link")
            ET.SubElement(item_elem, "description").text = item_data.get("description", "")
            
            pub_date_elem = ET.SubElement(item_elem, "pubDate")
            pub_date_elem.text = formatdate(parse_date(item_data).timestamp())

            channel.append(item_elem)

        # Write to file
        tree = ET.ElementTree(rss)
        ET.indent(tree, space="  ", level=0)
        tree.write(self.filename, encoding="utf-8", xml_declaration=True)

        print(f"RSS feed updated. Total items: {len(channel.findall('item'))}")

