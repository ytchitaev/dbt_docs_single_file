import argparse
import os
import json
import re

# example usage (PowerShell)
"""
python build_standalone_dbt_docs.py `
--dbt_project_dir "C:\git\dbt_project\models\" `
--standalone_html_output_dir "C:\git\dbt_project\" `
--standalone_html_output_filename "dbt_docs.html" `
--encoding "utf-8" `
--ignore_projects "project1,another_project2"
"""


def load_file_content(file_path: str, encoding: str) -> str:
    """Load content from a file."""
    with open(file_path, "r", encoding=encoding) as f:
        content = f.read()
    return content


def load_json_file(file_path: str, encoding: str) -> dict:
    """Load JSON data from a file."""
    with open(file_path, "r", encoding=encoding) as f:
        json_data = json.loads(f.read())
    return json_data


def write_file_content(file_path: str, content: str, encoding: str) -> None:
    """Write content to a file."""
    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)


def update_html_file(
    dbt_project_dir: str,
    standalone_html_output_dir: str,
    standalone_html_output_filename: str,
    ignore_projects: list,
    encoding: str,
) -> None:
    """Update HTML file with DBT project information."""
    index_file_path = os.path.join(dbt_project_dir, "target", "index.html")
    manifest_file_path = os.path.join(dbt_project_dir, "target", "manifest.json")
    catalog_file_path = os.path.join(dbt_project_dir, "target", "catalog.json")

    content_index = load_file_content(index_file_path, encoding)
    json_manifest = load_json_file(manifest_file_path, encoding)
    json_catalog = load_json_file(catalog_file_path, encoding)

    search_str = 'o=[i("manifest","manifest.json"+t),i("catalog","catalog.json"+t)]'

    for element_type in ["nodes", "sources", "macros", "parent_map", "child_map"]:
        for key in list(json_manifest.get(element_type, {}).keys()):
            for ignore_project in ignore_projects:
                if re.match(rf"^.*\.{ignore_project}\.", key):
                    del json_manifest[element_type][key]

    new_str = (
        "o=[{label: 'manifest', data: "
        + json.dumps(json_manifest)
        + "},{label: 'catalog', data: "
        + json.dumps(json_catalog)
        + "}]"
    )
    new_content = content_index.replace(search_str, new_str)

    output_file_path = os.path.join(
        standalone_html_output_dir, standalone_html_output_filename
    )
    write_file_content(output_file_path, new_content, encoding)


def main():
    parser = argparse.ArgumentParser(
        description="Update HTML file with DBT project information."
    )
    parser.add_argument(
        "--dbt_project_dir",
        type=str,
        required=True,
        default="C:\\git\\product-dof\\transformation\\",
        help="DBT project directory",
    )
    parser.add_argument(
        "--standalone_html_output_dir",
        type=str,
        required=True,
        default="C:\\git\\product-dof\\",
        help="Standalone HTML output directory",
    )
    parser.add_argument(
        "--standalone_html_output_filename",
        type=str,
        required=True,
        default='product-dof.html"',
        help="Standalone HTML output filename",
    )
    parser.add_argument(
        "--encoding",
        type=str,
        required=True,
        default="utf-8",
        help="Default encoding for all read write actions",
    )
    parser.add_argument(
        "--ignore_projects",
        type=str,
        default="",
        help="Comma-separated list of projects to ignore",
    )

    args = parser.parse_args()

    DBT_PROJECT_DIR = args.dbt_project_dir
    STANDALONE_HTML_OUTPUT_DIR = args.standalone_html_output_dir
    STANDALONE_HTML_OUTPUT_FILENAME = args.standalone_html_output_filename
    IGNORE_PROJECTS = args.ignore_projects.split(",")
    ENCODING = args.encoding

    update_html_file(
        DBT_PROJECT_DIR,
        STANDALONE_HTML_OUTPUT_DIR,
        STANDALONE_HTML_OUTPUT_FILENAME,
        IGNORE_PROJECTS,
        ENCODING,
    )


if __name__ == "__main__":
    main()
