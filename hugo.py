import json
import os
from datetime import datetime


def format_rating(rating):
    full_stars = "⭐" * int(rating)
    if rating % 1 >= 0.5:  # Check if there's a half star
        half_star = "🌟"
    else:
        half_star = ""
    return full_stars + half_star


# Function to create markdown file
def create_md_file(
    author, title, date, description, tags, rating, review, output_dir, pageLink
):
    filename = f"{output_dir}/{title.lower().replace(' ', '_').replace(':', '_').replace('__', '_')}.md"

    with open(filename, "w") as f:
        try:
            f.write("+++\n")
            f.write(f'author = "{author}"\n')
            f.write(f'title = "{title}"\n')
            f.write(f'date = "{date}"\n')
            f.write(f'description = "{description}"\n')
            f.write("tags = [\n")
            for tag in tags:
                f.write(f'    "{tag}",\n')
            f.write("]\n")
            f.write("+++\n")
            f.write(f"Rating: {format_rating(rating)}\n")
            f.write("\n")
            f.write(f"{review}\n")
            f.write("\n")
            f.write(f"\n[🍅 Rotten Tomatoes Info 🍅](www.rottentomatoes.com/{pageLink})")
        except Exception as e:
            print("ERROR:", title, e, rating)


tag = "tv"
# Read JSON data
with open(f"{tag}.json") as f:
    data = json.load(f)

output_dir = tag  # replace with your desired directory
os.makedirs(output_dir, exist_ok=True)  # create the directory if it doesn't exist

# Iterate over the reviews
for item in data["ratings"]:
    try:
        title = item["media"]["title"]
        pageLink = item["media"]["pageLink"]
        date = datetime.fromtimestamp(
            item["createTime"] / 1000
        ).isoformat()  # convert timestamp to date
        description = f"Olshansky's review of {title}"
        tags = [tag]  # replace with your actual tags
        rating = item["review"]["score"]
        if "review" not in item["review"]:
            review = "Olshansky was too lazy to write a review for this one..."
        else:
            review = item["review"]["review"]
        create_md_file(
            "Daniel Olshansky",
            title,
            date,
            description,
            tags,
            rating,
            review,
            output_dir,
            pageLink,
        )
    except KeyError as e:
        print("KeyError:", item["media"]["title"], e)
