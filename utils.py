def print_header(text):
    length = len(text)
    padding = 5
    border = "+" + "-" * padding + "-"*length + "-" * padding + "+"
    title = "\n|" + " " * padding + text + " " * padding + "|\n"
    header = border + title + border
    print(header)