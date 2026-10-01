from urllib.parse import quote_plus


PLATFORMS = {

    "home": [
        "Amazon",
        "IKEA",
        "Flipkart"
    ],

    "party": [
        "Swiggy",
        "Zomato",
        "OYO"
    ],

    "jewelry": [
        "Amazon",
        "Flipkart"
    ]
}


def search_url(
    platform: str,
    query: str
) -> str:

    encoded_query = quote_plus(query)


    urls = {

        "Amazon":
            f"https://www.amazon.in/s?k={encoded_query}",

        "Flipkart":
            f"https://www.flipkart.com/search?q={encoded_query}",

        "IKEA":
            f"https://www.ikea.com/in/en/search/?q={encoded_query}",

        "Swiggy":
            f"https://www.swiggy.com/search?query={encoded_query}",

        "Zomato":
            f"https://www.zomato.com/search?query={encoded_query}",

        "OYO":
            f"https://www.oyorooms.com/search?location={encoded_query}"
    }


    return urls[platform]


def enrich(
    items,
    domain
):

    platforms = PLATFORMS[domain]

    output = []


    for index, item in enumerate(items):

        platform = platforms[
            index % len(platforms)
        ]


        item["platform"] = platform


        item["search_url"] = search_url(
            platform,
            item.get(
                "search_query",
                item["name"]
            )
        )


        output.append(item)


    return output