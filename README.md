# dbt_docs_single_file
This project demonstrates a script to generate standalone html dbt docs page that can be opened without running dbt serve command.

## Detail
- By default dbt generates an html file that is dependant on several json definition files (manifest.json, catalog.json ...). 
- These are accessible when running dbt serve, but if you open the html directly, browser security limitations prevent access to json files and the webpage breaks. 
- The script incorporates json into the html so it becomes portable. Adapted from (script here)[https://github.com/dbt-labs/dbt-docs/issues/53] to be executable from CLI with argparse.
