"""
This is a script to parse through a log file and output useful information.

Usage:
python log_analyzer </path/to/log>

Information to find:
1) SDK used
2) All render IDs with ready-to-go vg-cli scripts
3) All lines with Exceptions (list of all exeptions)
4) All lines with Errors (list of all errors)
5)

TODO:
3. Catalog what exceptions are being thrown.
4. Catalog what errors are being thrown.
5. ZenDesk API - find tickets that match?
6. Come up with a definite output format
"""

import re
import sys
from pathlib import Path
from Patterns import Patterns


def main():
    file_name = sys.argv[1]
    file_text = Path(file_name).read_text()

    # Find static values: agent_id (SDK), api key, and account id
    agent_id = re.search(Patterns.agent_id.value, file_text).groups()[0]
    api_key = re.search(Patterns.api_key.value, file_text).groups()[0]
    account_id = re.search(Patterns.account_id.value, file_text).groups()[0]
    lines_where_exceptions_occur = []
    lines_where_errors_occur = []
    render_ids = set()
    line_number = 1

    for line in open(file_name):
        # Check Exceptions
        for match in re.finditer(Patterns.exceptions.value, line):
            lines_where_exceptions_occur.append(line_number)

        # Check Errors
        for match in re.finditer(Patterns.errors.value, line):
            lines_where_errors_occur.append(line_number)

        # Check RenderIds
        for match in re.finditer(Patterns.render_id.value, line):
            renderid = match.group(1)
            if not renderid == "NONE":
                render_ids.add(match.group(1))

        line_number = line_number + 1

    # Output results
    print("Agent Id: " + agent_id)
    print("Account Id: " + account_id)
    print("Api Key:" + api_key)
    print("Render Ids: " + '\n'.join(render_ids))
    print("Exceptions occur on lines: " + str(lines_where_exceptions_occur))
    print("Errors occur on lines: " + str(lines_where_errors_occur))

    for renderid in render_ids:
        print(construct_vg_cli_rerender(account_id, api_key, renderid))


def construct_vg_cli_rerender(account_id, api_key, render_id):
    return "vg-cli rerender " + account_id + "/" + render_id + " --api-key " + api_key


main()
