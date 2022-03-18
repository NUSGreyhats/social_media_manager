import re


def replace_string(row_dict: dict, string: str) -> str:
    """Remove excess format strings with no keys"""
    to_be_replaced = re.findall(r"\{(.*?)\}", string)
    for format_string in to_be_replaced:
        if format_string not in row_dict.keys():
            continue
        string =string.replace(f"{{{format_string}}}", row_dict[format_string])
    return string


if __name__ == "__main__":
    print(
        replace_string(
            {
                "test": "replaced",
            },
            "test{test}test %sest %t{t}",
        )
    )
