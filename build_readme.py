import feedparser
import pathlib
import re

root = pathlib.Path(__file__).parent.resolve()

def replace_chunk(content, marker, chunk):
    r = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return r.sub(chunk, content)


def fetch_blog_entries():
    entries = feedparser.parse("https://www.cedricbonhomme.org/blog/index.xml")["entries"]
    print("Number of entries in the RSS feed:")
    print(len(entries))
    return [
        {
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
        }
        for entry in entries
    ]


if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    entries = fetch_blog_entries()[:5]
    entries_md = "\n".join(
        ["* [{title}]({url})".format(**entry) for entry in entries]
    )
    rewritten = replace_chunk(readme_contents, "blog", entries_md)
    readme.open("w").write(rewritten)

