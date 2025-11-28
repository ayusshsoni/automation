from bs4 import BeautifulSoup
import pandas as pd
import os

data = {"title": [], "price": [], "link": []}

data_dir = "data"

for file_name in os.listdir(data_dir):
    if not file_name.endswith(".html"):
        continue

    file_path = os.path.join(data_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    title = None
    link = None
    price = None

    # --- Attempt to find Title and Link ---
    # Based on mobile_0.html structure: a.a-link-normal > h2 > span
    # This targets the anchor tag that wraps the title, and then the span containing the text.
    product_link_tag = soup.select_one(
        "a.a-link-normal.s-line-clamp-2.s-line-clamp-3-for-col-12.s-link-style.a-text-normal"
    )

    if product_link_tag:
        # The title text is inside a span within the h2, which is inside the link tag
        title_span = product_link_tag.select_one("h2 span")
        if title_span:
            title = title_span.get_text(strip=True)
            link = "https://www.amazon.in" + product_link_tag.get("href", "")
        else:
            # Fallback if title is directly within h2 or link text itself
            title_h2 = product_link_tag.select_one("h2")
            if title_h2:
                title = title_h2.get_text(strip=True)
                link = "https://www.amazon.in" + product_link_tag.get("href", "")
            else:
                title = product_link_tag.get_text(strip=True)
                link = "https://www.amazon.in" + product_link_tag.get("href", "")
    else:
        # Alternative structure for title and link (e.g., non-sponsored products)
        # Check for the h2 > a > span pattern (from previous attempts)
        alt_title_link_element = soup.select_one(
            "h2 a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style"
        )
        if alt_title_link_element:
            title = alt_title_link_element.get_text(strip=True)
            link = "https://www.amazon.in" + alt_title_link_element.get("href", "")
        else:
            # One more fallback for generic product links (like in images)
            img_parent_link = soup.select_one("div.s-product-image-container a.a-link-normal")
            if img_parent_link:
                # If we get a link from the image, try to find a nearby title element
                title_nearby = soup.select_one("h2 span.a-size-medium.a-color-base.a-text-normal")
                if title_nearby:
                    title = title_nearby.get_text(strip=True)
                    link = "https://www.amazon.in" + img_parent_link.get("href", "")


    # --- Attempt to find Price ---
    # The span.a-offscreen inside a.a-price is still the most reliable here.
    # It appears within an <a> tag that also wraps the price display.
    price_offscreen_tag = soup.select_one(
        "a.a-link-normal span.a-price span.a-offscreen"
    )

    if price_offscreen_tag:
        price = price_offscreen_tag.get_text(strip=True)
        # Clean up price: remove currency symbol and commas
        price = (
            price.replace("₹", "")
            .replace("$", "")
            .replace(",", "")
            .replace("£", "")
            .strip()
        )
    else:
        # Fallback if the price is structured differently, e.g., not inside an <a> with the offscreen span.
        # This targets directly the a-price-whole/fraction structure
        price_whole_tag = soup.select_one("span.a-price-whole")
        price_fraction_tag = soup.select_one("span.a-price-fraction")
        if price_whole_tag:
            price_str = price_whole_tag.get_text(strip=True)
            if price_fraction_tag:
                price_str += "." + price_fraction_tag.get_text(strip=True)
            price = (
                price_str.replace(",", "")
                .replace("₹", "")
                .replace("$", "")
                .replace("£", "")
                .strip()
            )


    # If we couldn't get a title or a link (which are essential), skip this item entirely.
    if not title or not link:
        print(f"Warning: Could not extract title/link from {file_name}. Skipping.")
        continue

    data["title"].append(title)
    data["price"].append(price)  # price can be None if not found
    data["link"].append(link)

df = pd.DataFrame(data)

os.makedirs("output", exist_ok=True)
output_csv_path = os.path.join("output", "amazon_products.csv")
df.to_csv(output_csv_path, index=False, encoding="utf-8")

print("Saved:", len(df), "rows to", output_csv_path)