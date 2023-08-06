#!/usr/bin/env python3
"""
This module contains functions to get data from the Cisco Support APIs.

The functions are ordered as followed:
- Cisco Support API call functions
- Print functions for Cisco Support API call functions in Nornir style
"""


import json
import time
from typing import Literal, NoReturn
import requests
from cisco_support import SNI, EoX, SS
from cisco_support.utils import getToken as cisco_support_get_token
from nornir_maze.utils import (
    print_task_name,
    task_host,
    task_info,
    task_error,
    iterate_all,
    exit_error,
)


#### Cisco Support API Error Lists ###########################################################################

# fmt: off
SNI_ERRORS = [
    "NO_RECORDS_FOUND", "EXCEEDED_OUTPUT", "API_MISSING_PARAMETERS", "API_INVALID_INPUT", "EXCEEDED_INPUTS",
    "API_NOTAUTHORIZED", "API_ERROR_01",
]
EOX_ERRORS = [
    "SSA_GENERIC_ERR", "SSA_ERR_001", "SSA_ERR_003", "SSA_ERR_007", "SSA_ERR_009", "SSA_ERR_010",
    "SSA_ERR_011", "SSA_ERR_012", "SSA_ERR_013", "SSA_ERR_014", "SSA_ERR_015", "SSA_ERR_016", "SSA_ERR_018",
    "SSA_ERR_022", "SSA_ERR_023", "SSA_ERR_024", "SSA_ERR_028", "SSA_ERR_030", "SSA_ERR_031", "SSA_ERR_032",
    "SSA_ERR_033", "SSA_ERR_034", "SSA_ERR_036", "SSA_ERR_037",
]
SS_ERRORS = [
    "S3_BASEPID_NO_SUPPORT", "S3_BASEPID_REQ", "S3_HW_INFORMATION_NOT_SUPPORTED", "S3_INV_BASEPID",
    "S3_INV_BASEPID", "S3_INV_CURR_IMG_REL", "S3_INV_IMAGE", "S3_INV_INPUT", "S3_INV_MDFID", "S3_INV_MDFID",
    "S3_INV_QUERY_PARAM", "S3_INV_QUERY_PARAM", "S3_INV_QUERY_PARAM", "S3_INV_QUERY_PARAM",
    "S3_INV_QUERY_PARAM", "S3_INV_QUERY_PARAM", "S3_INV_RELEASE", "S3_INV_RELEASE_IMAGE",
    "S3_MDFID_NO_SUPPORT", "S3_MDFID_REQ", "S3_NO_SOFT_AVL",
    "S3_SERVICE_EXCEPTION_OCCURED",
]
# fmt: on


#### Helper Functions ########################################################################################


def success(value: bool) -> Literal["CISCOAPIResult <Success: True>", "CISCOAPIResult <Success: False>"]:
    """
    TBD
    """
    if value:
        return "CISCOAPIResult <Success: True>"
    return "CISCOAPIResult <Success: False>"


def cisco_support_exit_error(
    task_text: str,
    api: Literal["sni", "eox", "ss"],
    api_response: dict,
) -> NoReturn:
    """
    TBD
    """
    print_task_name(text=task_text)
    print(task_error(text=f"Verify Cisco support {api.upper()} API data", changed=False))
    print(f"'Verify Cisco support {api.upper()} API data' -> {success(False)}")

    # Print additional information depending which Cisco support API has been used
    for value in iterate_all(iterable=api_response, returned="value"):
        if value is None:
            continue

        if api.lower() in "sni" and value in SNI_ERRORS:
            print(f"-> SNI API-Error: {value}")
            continue

        if api.lower() in "eox" and value in EOX_ERRORS:
            if "ErrorResponse" in api_response:
                print(f"-> EOX API-Error: {value}")
                continue
            print("-> The EOX API returned None. Could be a bug in the API.")
            break

        if api.lower() in "ss":
            if value in SS_ERRORS:
                print(f"-> SS API-Error: {value}")
                continue
            print("-> The initial PID list contains invalid PIDs. The returned PID list is not identical.")
            break

        if api.lower() not in ["sni", "eox", "ss"]:
            print(f"-> Unknown API: {api.upper()}")
            break

    # Print the whole api_response
    print("\n" + json.dumps(api_response, indent=4))

    # Exit the script with a proper message
    exit_error(
        task_text=f"CISCO-API get {api.upper()} data",
        text="ALERT: GET CISCO SUPPORT API DATA FAILED!",
        msg="-> Analyse the error message and identify the root cause",
    )


def verify_cisco_support_api_data(serials_dict: dict, verbose: bool = False, silent: bool = False) -> bool:
    """
    This function verifies the serials_dict which has been filled with data by various functions of these
    module like eox_by_serial_numbers, sni_get_coverage_summary_by_serial_numbers, etc. and verifies that
    there are no invalid serial numbers. In case of invalid serial numbers, the script quits with an error
    message.
    """
    print_task_name(text="Verify Cisco support SNI/EOX/SS API data")

    # Verify that the serials_dict dictionary contains no wrong serial numbers
    for value in iterate_all(iterable=serials_dict, returned="value"):
        if value is None:
            continue

        if value in SNI_ERRORS:
            if not silent:
                print(task_error(text="Verify Cisco support SNI API data", changed=False))
                print(f"'Verify Cisco support SNI API data' -> {success(False)}")
                print(f"-> SNI API-Error: {value}")
            return False

        if value in EOX_ERRORS:
            if not silent:
                print(task_error(text="Verify Cisco support EOX API data", changed=False))
                print(f"'Verify Cisco support EOX API data' -> {success(False)}")
                print(f"-> EOX API-Error: {value}")
            return False

        if value in SS_ERRORS:
            if not silent:
                print(task_error(text="Verify Cisco support SS API data", changed=False))
                print(f"'Verify Cisco support SS API data' -> {success(False)}")
                print(f"-> SS API-Error: {value}")
            return False

    if not silent:
        print(task_info(text="Verify Cisco support SNI/EOX/SS API data", changed=False))
        print(f"'Verify Cisco support SNI/EOX/SS API data' -> {success(True)}")
        if verbose:
            print("\n" + json.dumps(serials_dict, indent=4))

    return True


#### Cisco Support API call functions ########################################################################


def cisco_support_check_authentication(api_creds: tuple, verbose: bool = False, silent: bool = False) -> bool:
    """
    This function checks to Cisco support API authentication by generating an bearer access token. In case
    of an invalid API client key or secret a error message is printed and the script exits.
    """
    task_name = "CISCO-API check OAuth2 client credentials grant flow"

    try:
        # Try to generate an barer access token
        token = cisco_support_get_token(*api_creds, verify=None, proxies=None)

        if not silent:
            print_task_name(text=task_name)
            print(task_info(text=task_name, changed=False))
            print(f"'Bearer access token generation' -> {success(True)}")
            if verbose:
                print(f"-> Bearer token: {token}")

        return True

    except KeyError:
        if not silent:
            print_task_name(text=task_name)
            print(task_error(text=task_name, changed=False))
            print(f"'Bearer access token generation' -> {success(False)}")
            print("-> Invalid API client key and/or secret provided")

        return False


def get_sni_owner_coverage_by_serial_number(serial_dict: dict, api_creds: tuple) -> dict:
    """
    This function takes the serial_dict which contains all serial numbers and the Cisco support API creds to
    get the owner coverage by serial number with the cisco-support library. The result of each serial will
    be added with a new key to the dict. The function returns the updated serials dict. The format of the
    serials_dict need to be as below.
    "<serial>": {
        "host": "<hostname>",
        ...
    },
    """
    # pylint: disable=invalid-name

    task_text = "CISCO-API get owner coverage status by serial number"

    # Backoff sleep and attempt values
    RETRY_ATTEMPTS = 20
    SLEEP = 1
    SLEEP_MULTIPLIER = 1
    # Maximum serial number API parameter value
    MAX_SR_NO = 75

    sni = SNI(*api_creds)

    # Create a dictionary with the key "serial_numbers" to fill with the API response chunks
    owner_coverage_status = {}
    owner_coverage_status["serial_numbers"] = []

    # Loop over a list with all serial numbers with a step incrementation of MAX_SR_NO
    for index in range(0, len(list(serial_dict.keys())), MAX_SR_NO):

        # Re-try the Cisco support API call with a backoff again in case of an error
        for _ in range(RETRY_ATTEMPTS):
            # Create a chunk list with the maximum allowed elements specified by MAX_SR_NO
            serial_chunk = list(serial_dict.keys())[index : index + MAX_SR_NO]

            # Call the Cisco support API for the serial_chunk list
            try:
                response = sni.getOwnerCoverageStatusBySerialNumbers(sr_no=serial_chunk)
            except requests.exceptions.JSONDecodeError:
                continue

            # Break out of the range() loop if ErrorResponse is not present in the API response
            if "ErrorResponse" not in response:
                # Update the owner_coverage_status dict
                for item in response["serial_numbers"]:
                    owner_coverage_status["serial_numbers"].append(item)
                break

            # SLEEP and continue with next range() loop attempt
            time.sleep(SLEEP)
            SLEEP = SLEEP * SLEEP_MULTIPLIER

        # Ending for loop as iterable exhausted
        else:
            cisco_support_exit_error(task_text=task_text, api="sni", api_response=response)

    # Add all records to the serial_dict dictionary
    for record in owner_coverage_status["serial_numbers"]:
        serial_dict[record["sr_no"]]["SNIgetOwnerCoverageStatusBySerialNumbers"] = record

    return serial_dict


def get_sni_coverage_summary_by_serial_numbers(serial_dict: dict, api_creds: tuple) -> dict:
    """
    This function takes the serial_dict which contains all serial numbers and the Cisco support API creds to
    get the coverage summary by serial number with the cisco-support library. The result of each serial will
    be added with a new key to the dict. The function returns the updated serials dict. The format of the
    serials_dict need to be as below.
    "<serial>": {
        "host": "<hostname>",
        ...
    },
    """
    # pylint: disable=invalid-name,too-many-locals

    task_text = "CISCO-API get coverage summary data by serial number"

    # Backoff sleep and attempt values
    RETRY_ATTEMPTS = 20
    SLEEP = 1
    SLEEP_MULTIPLIER = 1
    # Maximum serial number API parameter value
    MAX_SR_NO = 75

    sni = SNI(*api_creds)

    # Create a dictionary with the key "serial_numbers" to fill with the API response chunks
    coverage_summary = {}
    coverage_summary["serial_numbers"] = []

    # Loop over a list with all serial numbers with a step incrementation of MAX_SR_NO
    for index in range(0, len(list(serial_dict.keys())), MAX_SR_NO):

        # Part 1: Get the total number of pages for the serial_chunk list
        # Re-try the Cisco support API call with a backoff again in case of an error
        for _ in range(RETRY_ATTEMPTS):
            # Create a chunk list with the maximum allowed elements specified by MAX_SR_NO
            serial_chunk = list(serial_dict.keys())[index : index + MAX_SR_NO]

            # Call the Cisco support API for the serial_chunk list to get the total number of pages
            try:
                response = sni.getCoverageSummaryBySerialNumbers(sr_no=serial_chunk, page_index=1)
            except requests.exceptions.JSONDecodeError:
                continue

            # If the pagination details are present
            # Break out of the range() loop if ErrorResponse is not present in the API response
            if "pagination_response_record" in response:
                # Get the total number of pages to create API calls for all pages
                num_pages = response["pagination_response_record"]["last_index"]
                break

            # SLEEP and continue with next range() loop attempt
            time.sleep(SLEEP)
            SLEEP = SLEEP * SLEEP_MULTIPLIER

        # Ending for loop as iterable exhausted
        else:
            cisco_support_exit_error(task_text=task_text, api="sni", api_response=response)

        # Part 2: Get the API data for each page of the serial_chunk list
        # Call the Cisco support API for each page of the serial_chunk list
        for page in range(1, num_pages + 1):
            # Re-try the Cisco support API call with a backoff again in case of an error
            for _ in range(RETRY_ATTEMPTS):
                # Call the Cisco support API for the serial_chunk list
                try:
                    response = sni.getCoverageSummaryBySerialNumbers(sr_no=serial_chunk, page_index=page)
                except requests.exceptions.JSONDecodeError:
                    continue

                # If the pagination details are present
                # Break out of the range() loop if ErrorResponse is not present in the API response
                if "pagination_response_record" in response:
                    # Update the owner_coverage_status dict
                    for item in response["serial_numbers"]:
                        coverage_summary["serial_numbers"].append(item)
                    break

                # SLEEP and continue with next range() loop attempt
                time.sleep(SLEEP)
                SLEEP = SLEEP * SLEEP_MULTIPLIER

            # Ending for loop as iterable exhausted
            else:
                cisco_support_exit_error(task_text=task_text, api="sni", api_response=response)

    # Add all records to the serial_dict dictionary
    for record in coverage_summary["serial_numbers"]:
        serial_dict[record["sr_no"]]["SNIgetCoverageSummaryBySerialNumbers"] = record

    return serial_dict


def get_eox_by_serial_numbers(serial_dict: dict, api_creds: tuple) -> dict:
    """
    This function takes the serial_dict which contains all serial numbers and the Cisco support API creds to
    run get the end of life data by serial number with the cisco-support library. The result of each serial
    will be added with a new key to the dict. The function returns the updated serials dict. The format of
    the serials_dict need to be as below.
    "<serial>": {
        "host": "<hostname>",
        ...
    },
    """
    # pylint: disable=invalid-name,too-many-locals

    # Backoff SLEEP and attempt values
    RETRY_ATTEMPTS = 20
    SLEEP = 1
    SLEEP_MULTIPLIER = 1
    # Maximum serial number API parameter value
    MAX_SR_NO = 20

    task_text = "CISCO-API get EoX data by serial number"

    eox = EoX(*api_creds)

    # Create a dictionary with the key "EOXRecord" to fill with the API response chunks
    end_of_life = {}
    end_of_life["EOXRecord"] = []

    # Loop over a list with all serial numbers with a step incrementation of MAX_SR_NO
    for index in range(0, len(list(serial_dict.keys())), MAX_SR_NO):

        # Part 1: Get the total number of pages for the serial_chunk list
        # Re-try the Cisco support API call with a backoff again in case of an error
        for _ in range(RETRY_ATTEMPTS):
            # Create a chunk list with the maximum allowed elements specified by MAX_SR_NO
            serial_chunk = list(serial_dict.keys())[index : index + MAX_SR_NO]

            # Call the Cisco support API for the serial_chunk list to get the total number of pages
            try:
                response = eox.getBySerialNumbers(serialNumber=serial_chunk, pageIndex=1)
            except requests.exceptions.JSONDecodeError:
                continue

            # If the pagination details are present
            # Break out of the range() loop if ErrorResponse is not present in the API response
            if "PaginationResponseRecord" in response:
                # Get the total number of pages to create API calls for all pages
                num_pages = response["PaginationResponseRecord"]["LastIndex"]
                break

            # SLEEP and continue with next range() loop attempt
            time.sleep(SLEEP)
            SLEEP = SLEEP * SLEEP_MULTIPLIER

        # Ending for loop as iterable exhausted
        else:
            cisco_support_exit_error(task_text=task_text, api="eox", api_response=response)

        # Part 2: Get the API data for each page of the serial_chunk list
        # Call the Cisco support API for each page of the serial_chunk list
        for page in range(1, num_pages + 1):
            # Re-try the Cisco support API call with a backoff again in case of an error
            for _ in range(RETRY_ATTEMPTS):
                # Call the Cisco support API for the serial_chunk list
                try:
                    response = eox.getBySerialNumbers(serialNumber=serial_chunk, pageIndex=page)
                except requests.exceptions.JSONDecodeError:
                    continue

                # If the pagination details are present
                # Break out of the range() loop if ErrorResponse is not present in the API response
                if "PaginationResponseRecord" in response:
                    # Update the owner_coverage_status dict
                    for item in response["EOXRecord"]:
                        end_of_life["EOXRecord"].append(item)
                    break

                # SLEEP and continue with next range() loop attempt
                time.sleep(SLEEP)
                SLEEP = SLEEP * SLEEP_MULTIPLIER

            # Ending for loop as iterable exhausted
            else:
                cisco_support_exit_error(task_text=task_text, api="eox", api_response=response)

    for record in end_of_life["EOXRecord"]:
        # The response value of "EOXInputValue" can be a single serial number or a comma separated string of
        # serial numbers as the API response can collect multiple same EoX response together
        for sr_no in record["EOXInputValue"].split(","):
            serial_dict[sr_no]["EOXgetBySerialNumbers"] = record

    return serial_dict


def get_ss_suggested_release_by_pid(serial_dict: dict, api_creds: tuple, pid_list: list = False) -> dict:
    """
    This function takes the serial_dict which contains all serial numbers and the Cisco support API creds to
    get the suggested software release by the PID with the cisco-support library. The result of each serial
    will be added with a new key to the dict. The function returns the updated serials dict. The format of
    the serials_dict need to be as below.
    "<serial>": {
        "host": "<hostname>",
        ...
    },
    """
    # pylint: disable=invalid-name,too-many-locals,too-many-branches

    task_text = "CISCO-API get suggested release data by pid"

    # Backoff sleep and attempt values
    RETRY_ATTEMPTS = 20
    SLEEP = 1
    SLEEP_MULTIPLIER = 1
    # Maximum serial number API parameter value
    MAX_PID = 10

    if not pid_list:
        # Create a list with the product ids of all devices from the serials dict
        pid_list = [
            item["SNIgetCoverageSummaryBySerialNumbers"]["orderable_pid_list"][0]["orderable_pid"]
            for item in serial_dict.values()
        ]

    # Remove pids if the match the condition for startswith
    rm_prefixes = ["UCSC-C220-M5SX", "AIR-CAP"]
    pid_list = [pid for pid in pid_list if not any(pid.startswith(prefix) for prefix in rm_prefixes)]
    # Remove pids if the match the condition for endswith
    rm_suffixes = ["AXI-E", "AXI-A"]
    pid_list = [pid for pid in pid_list if not any(pid.endswith(suffix) for suffix in rm_suffixes)]
    # Modify known wrong basePIDs to match API requirements
    # The software package suffic -A or -E can be removed as the newer basePID don't have this anymore
    # -> Makes the API calls more stable
    chg_suffixes = ["-A", "-E"]
    pid_list = [pid[:-2] if any(pid.endswith(suffix) for suffix in chg_suffixes) else pid for pid in pid_list]

    # Remove duplicated entries in the final pid_list
    pid_list = list(set(pid_list))

    ss = SS(*api_creds)

    # Create a dictionary with the key "pid" to fill with the API response chunks
    suggested_release = {}
    suggested_release["pid"] = []

    # Loop over a list with all serial numbers with a step incrementation of MAX_SR_NO
    for index in range(0, len(list(pid_list)), MAX_PID):

        # Part 1: Get the total number of pages for the pid_chunk list
        # Re-try the Cisco support API call with a backoff again in case of an error
        for _ in range(RETRY_ATTEMPTS):
            # Create a chunk list with the maximum allowed elements specified by MAX_SR_NO
            pid_chunk = list(pid_list)[index : index + MAX_PID]

            # Call the Cisco support API for the pid_chunk list to get the total number of pages
            try:
                response = ss.getSuggestedReleasesByProductIDs(productIds=pid_chunk, pageIndex=1)
            except requests.exceptions.JSONDecodeError:
                continue

            # If the pagination details are present
            # Break out of the range() loop if ErrorResponse is not present in the API response
            if "paginationResponseRecord" in response:
                # Get the total number of pages to create API calls for all pages
                num_pages = response["paginationResponseRecord"]["lastIndex"]
                break

            # SLEEP and continue with next range() loop attempt
            time.sleep(SLEEP)
            SLEEP = SLEEP * SLEEP_MULTIPLIER

        # Ending for loop as iterable exhausted
        else:
            cisco_support_exit_error(task_text=task_text, api="ss", api_response=response)

        # Part 2: Get the API data for each page of the pid_chunk list
        # Call the Cisco support API for each page of the pid_chunk list
        for page in range(1, int(num_pages) + 1):
            # Re-try the Cisco support API call with a backoff again in case of an error
            for _ in range(RETRY_ATTEMPTS):
                # Call the Cisco support API for the pid_chunk list
                try:
                    response = ss.getSuggestedReleasesByProductIDs(productIds=pid_chunk, pageIndex=page)
                except requests.exceptions.JSONDecodeError:
                    continue

                # If the pagination details are present
                # Break out of the range() loop if ErrorResponse is not present in the API response
                if "paginationResponseRecord" in response:
                    # Update the suggested_release dict
                    for item in response["productList"]:
                        suggested_release["pid"].append(item)

                    # Check if the initial list and the response list have the same length. This verifies that
                    # there is a response for each pid of the initial list
                    pid_chunk_response = [item["product"]["basePID"] for item in response["productList"]]
                    # Remove duplicated entries in the pid_list
                    pid_chunk_response = list(set(pid_chunk_response))

                    # Exit the script if the length of both pid lists are not identical
                    if len(pid_chunk) != len(pid_chunk_response):
                        cisco_support_exit_error(task_text=task_text, api="ss", api_response=response)

                    # Break out of the for loop as everything was successfull
                    break

                # SLEEP and continue with next range() loop attempt
                time.sleep(SLEEP)
                SLEEP = SLEEP * SLEEP_MULTIPLIER

            # Ending for loop as iterable exhausted
            else:
                cisco_support_exit_error(task_text=task_text, api="ss", api_response=response)

    # Add the suggested software responce for each device to the serial_dict dictionary
    for record in serial_dict.values():
        # Get the pid from the device in the serial_dict
        pid = record["SNIgetCoverageSummaryBySerialNumbers"]["orderable_pid_list"][0]["orderable_pid"]
        # Normalize the pid and remove the software package suffic -A or -E to be identical with the pid_list
        pid = pid[:-2] if any(pid.endswith(suffix) for suffix in chg_suffixes) else pid
        # Each pid can have multiple suggestion records as the mdfId can be different for the same release
        # Therefor a list will be created to fill with multiple dictionaries if needed
        record["SSgetSuggestedReleasesByProductIDs"] = []

        # Loop over the whole suggested software response
        for item in suggested_release["pid"]:
            # If the pid match add the suggestion to the list
            if item["product"]["basePID"] in pid:
                record["SSgetSuggestedReleasesByProductIDs"].append(item)

    return serial_dict


#### Print functions for Cisco Support API call functions in Nornir style ####################################


def print_sni_owner_coverage_by_serial_number(serial_dict: dict, verbose: bool = False) -> None:
    """
    This function prints the result of get_sni_owner_coverage_by_serial_number() in Nornir style to stdout.
    """
    task_text = "CISCO-API get owner coverage status by serial number"
    print_task_name(text=task_text)

    for sr_no, records in serial_dict.items():
        record = records["SNIgetOwnerCoverageStatusBySerialNumbers"]
        host = records["host"] if records["host"] else sr_no
        print(task_host(host=host, changed=False))
        # Verify if the serial number is associated with the CCO ID
        if "YES" in record["sr_no_owner"]:
            print(task_info(text="Verify provided CCO ID", changed=False))
            print(f"'Verify provided CCO ID' -> {success(True)}")
            print("-> Is associated to the provided CCO ID")
        else:
            print(task_error(text="Verify provided CCO ID", changed=False))
            print(f"'Verify provided CCO ID' -> {success(False)}")
            print("-> Is not associated to the provided CCO ID")

        # Verify if the serial is covered by a service contract
        if "YES" in record["is_covered"]:
            print(task_info(text="Verify service contract", changed=False))
            print(f"'Verify service contract' -> {success(True)}")
            print("-> Is covered by a service contract")
            # Verify the end date of the service contract coverage
            if record["coverage_end_date"]:
                print(task_info(text="Verify service contract end date", changed=False))
                print(f"'Verify service contract end date' -> {success(True)}")
                print(f"-> Coverage end date is {record['coverage_end_date']}")
            else:
                print(task_error(text="Verify service contract end date", changed=False))
                print(f"'Verify service contract end date' -> {success(False)}")
                print("-> Coverage end date not available")
        else:
            print(task_error(text="Verify service contract", changed=False))
            print(f"'Verify service contract' -> {success(False)}")
            print("-> Is not covered by a service contract")

        if verbose:
            print("\n" + json.dumps(record, indent=4))


def print_sni_coverage_summary_by_serial_numbers(serial_dict: dict, verbose: bool = False) -> None:
    """
    This function prints the result of get_sni_coverage_summary_by_serial_numbers() in Nornir style to stdout.
    """
    task_text = "CISCO-API get coverage summary data by serial number"
    print_task_name(text=task_text)

    for sr_no, records in serial_dict.items():
        record = records["SNIgetCoverageSummaryBySerialNumbers"]
        host = records["host"] if records["host"] else sr_no
        print(task_host(host=host, changed=False))
        if "ErrorResponse" in record:
            print(task_error(text=task_text, changed=False))
            print(f"'Get SNI data' -> {success(False)}")
            error_response = record["ErrorResponse"]["APIError"]
            print(f"-> {error_response['ErrorDescription']} ({error_response['SuggestedAction']})\n")
        else:
            print(task_info(text=task_text, changed=False))
            print(f"'Get SNI data' -> {success(True)}")
            print(f"-> Orderable pid: {record['orderable_pid_list'][0]['orderable_pid']}")
            print(f"-> Customer name: {record['contract_site_customer_name']}")
            print(f"-> Customer address: {record['contract_site_address1']}")
            print(f"-> Customer city: {record['contract_site_city']}")
            print(f"-> Customer province: {record['contract_site_state_province']}")
            print(f"-> Customer country: {record['contract_site_country']}")
            print(f"-> Is covered by service contract: {record['is_covered']}")
            print(f"-> Covered product line end date: {record['covered_product_line_end_date']}")
            print(f"-> Service contract number: {record['service_contract_number']}")
            print(f"-> Service contract description: {record['service_line_descr']}")
            print(f"-> Warranty end date: {record['warranty_end_date']}")
            print(f"-> Warranty type: {record['warranty_type']}")

        if verbose:
            print("\n" + json.dumps(record, indent=4))


def print_eox_by_serial_numbers(serial_dict: dict, verbose: bool = False) -> None:
    """
    This function prints the result of get_eox_by_serial_numbers() in Nornir style to stdout.
    """
    task_text = "CISCO-API get EoX data by serial number"
    print_task_name(text=task_text)

    for sr_no, records in serial_dict.items():
        record = records["EOXgetBySerialNumbers"]
        host = records["host"] if records["host"] else sr_no
        print(task_host(host=host, changed=False))
        if "EOXError" in record:
            if "No product IDs were found" in record["EOXError"]["ErrorDescription"]:
                print(task_error(text=task_text, changed=False))
                print(f"'Get EoX data' -> {success(False)}")
                print(f"-> {record['EOXError']['ErrorDescription']} (Serial number does not exist)\n")
            elif "EOX information does not exist" in record["EOXError"]["ErrorDescription"]:
                print(task_info(text=task_text, changed=False))
                print(f"'Get EoX data' -> {success(True)}")
                print(f"-> {record['EOXError']['ErrorDescription']}")
        else:
            print(task_info(text=task_text, changed=False))
            print(f"'Get EoX data (Last updated {record['UpdatedTimeStamp']['value']})' -> {success(True)}")
            print(f"-> EoL product ID: {record['EOLProductID']}")
            print(f"-> Product ID description: {record['ProductIDDescription']}")
            print(f"-> EoL announcement date: {record['EOXExternalAnnouncementDate']['value']}")
            print(f"-> End of sale date: {record['EndOfSaleDate']['value']}")
            print(f"-> End of maintenance release: {record['EndOfSWMaintenanceReleases']['value']}")
            print(f"-> End of vulnerability support: {record['EndOfSecurityVulSupportDate']['value']}")
            print(f"-> Last day of support: {record['LastDateOfSupport']['value']}")

        if verbose:
            print("\n" + json.dumps(record, indent=4))


def print_get_ss_suggested_release_by_pid(serial_dict: dict, verbose: bool = False) -> None:
    """
    This function prints the result of get_ss_suggested_release_by_pid() in Nornir style to stdout.
    """
    task_text = "CISCO-API get suggested release data by pid"
    print_task_name(text=task_text)

    for sr_no, records in serial_dict.items():
        record = records["SSgetSuggestedReleasesByProductIDs"]
        host = records["host"] if records["host"] else sr_no
        # A Task error should not be possible as get_ss_suggested_release_by_pid() have error verification
        # and exits the script in case of an error
        print(task_host(host=host, changed=False))
        print(task_info(text=task_text, changed=False))
        print(f"'Get SS data' -> {success(True)}")
        # As there can be multiple suggestions with the same ID and release, but only with different mdfId,
        # the print_no_duplicates will be created to eliminate duplicate IDs and release information.
        print_no_duplicates = []
        for item in record:
            for idx, suggestion in enumerate(item["suggestions"]):
                print_no_duplicates.append({})
                for key, value in suggestion.items():
                    if value not in print_no_duplicates[idx].values():
                        print_no_duplicates[idx][key] = value
        # Delete all empty dicts that could be in the list
        print_no_duplicates = [item for item in print_no_duplicates if item]
        # Print all software release suggestions as there can be multiple suggestions
        for item in print_no_duplicates:
            print(f"-> ID: {item['id']}, Release: {item['releaseFormat1']}")

        if verbose:
            print("\n" + json.dumps(record, indent=4))
