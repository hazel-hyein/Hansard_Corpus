"""
Enter script name

Enter short description of the script
"""

__date__ = "2024-07-23"
__author__ = "NedeeshaWeerasuriya"
__version__ = "0.1"


# %% --------------------------------------------------------------------------
# Import Modules
import internetarchive as ia


search_results = ia.search_items(
        "(Great Exhibition) AND mediatype:(texts) AND format:(text) AND language:(English)"
    )
print(search_results.num_found)

counter = 0

data = {}
format_set = set()

for result in search_results:
    counter += 1
    print(counter)
    item = ia.get_item(result["identifier"])
    files = item.get_files()

    for file in files:
        format_set.add(file.format)
        if file.format == "DjVuTXT" or file.format == "Text PDF":
            print(file)
            data[file.name] = ia.download(
                result["identifier"],
                file,
                formats=["DjVuTXT", "Text PDF"],
                destdir="outputs",
                no_directory=True,
            )


# %%
