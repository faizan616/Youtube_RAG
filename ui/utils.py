import html


def escape_html(text: str) -> str:

    if text is None:
        return ""

    return html.escape(
        str(text)
    )