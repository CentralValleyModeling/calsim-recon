from pathlib import Path

from dash import dcc

DATA_DIR = Path(__file__).parent


def load_markdown(
    file: str | Path,
    relative_to_data_dir: bool = True,
) -> dcc.Markdown:
    if relative_to_data_dir is True:
        p = DATA_DIR / file
    else:
        p = Path(file).resolve()

    if not p.exists():
        raise FileNotFoundError(p)

    with open(p, "r") as P:
        content = P.read()
    return dcc.Markdown(
        children=content,
        id=f"markdown-content-{p.stem}",
    )
