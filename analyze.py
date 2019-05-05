import sys
import pandas as pd

"""
Parsing the file path
"""
EMPTY_STRING = ""
SPACE = " "

"""
Parsing the given date:
The pandas library add 00:00:00 (h:m:s) to the date 
in the file so I uses the length of the day which is 11 
in the format YYYY-MM-DD
"""
DATE_LEN = 11

"""
Columns names in the data.
"""
INSTALLS_COL = "Installs"
COST_COL = "Cost"
DATE_COL = "Date"
CAMPAIGN_COL = "Campaign"

"""
Informative messages
"""
# --- FOR THE BY-DAY-REPORT ---
DATE_MSG = "Date: "
TOT_INSTALLS_MSG = " ,Total installs for this date: "
TOT_COST_MSG = " ,Total cost for this date: "
# --- FOR THE TOTALS REPORT ---
TOTAL_INSTALLS_MSG = "Total installs in this report: "
TOTAL_COST_MSG = "Total cost in this report: "
TOTAL_ANDROID_MSG = "Total number of Android downloads "
TOTAL_IOS_MSG = "Total number of iOS downloads "
DOLLAR_SIGN = "$"

"""
Brands names :
"""
ANDROID_BIG_LET = "Android"
ANDROID_SMALL_LET = "android"
IOS_BIG_LET = "iOS"
IOS_SMALL_LET = "ios"

"""
Redundant lines in the file :
The first two lines doesn't include any important data but just
some titles
"""
REDUNDANT_LINES = [0, 1]


def create_full_path(path):
    full_path = EMPTY_STRING
    for partial_string in path:
        full_path += partial_string + SPACE
    return full_path.strip()


def find_total_installs(downloads):
    downloads_counter = 0
    for download in downloads:
        if download is not None:
            downloads_counter += download
    return downloads_counter


def find_total_cost(costs):
    total_cost = 0
    for cost in costs:
        total_cost += cost
    return total_cost


def change_date_to_format(date):
    date_substring = str(date)
    date_substring = date_substring[:DATE_LEN]
    return date_substring


def analyze_by_day(data):
    all_dates_in_data = data.Date.unique()
    for date in all_dates_in_data:
        sub_data = data[data.Date == date]
        total_installs_for_day = find_total_installs(sub_data[INSTALLS_COL])
        total_cost_for_day = find_total_cost(sub_data[COST_COL])
        print(DATE_MSG + change_date_to_format(date) + TOT_INSTALLS_MSG + str(
            total_installs_for_day) + TOT_COST_MSG + str(total_cost_for_day))
    return None


def is_android(campaign):
    if campaign is None:
        return False
    return (ANDROID_BIG_LET in campaign) or (ANDROID_SMALL_LET in campaign)


def is_ios(campaign):
    if campaign is None:
        return False
    return (IOS_BIG_LET in campaign) or (IOS_SMALL_LET in campaign)


def find_total_android_and_ios_downloads(campaign_col, installs_col):
    android_downloads_counter, ios_downloads_counter = 0, 0
    for i in range(len(campaign_col)):
        if campaign_col.iloc[i] is not None:
            if is_android(campaign_col.iloc[i]) and not is_ios(campaign_col.iloc[i]):
                android_downloads_counter += installs_col.iloc[i]
            if not is_android(campaign_col.iloc[i]) and is_ios(campaign_col.iloc[i]):
                ios_downloads_counter += installs_col.iloc[i]
    return android_downloads_counter, ios_downloads_counter
    # HERE THE CHANGES CAN BE SEEN:
    # for download in campaign_col:
    #     if download is not None:
    #         if is_android(download) and not is_ios(download):
    #             android_downloads_counter += 1
    #         if not is_android(download) and is_ios(download):
    #             ios_downloads_counter += 1
    # return android_downloads_counter, ios_downloads_counter


def main():
    # --- Data editing ---
    path = sys.argv[1:]
    path = create_full_path(path)
    data = pd.read_excel(path)
    data = data.drop(REDUNDANT_LINES, axis=0)
    data = data.dropna(0)  # drop lines with nan from the table
    data.columns = data.iloc[0]  # changed the first line "Date Campaign ..." the be the columns titles
    data = data.drop([2])  # removing the line which now became the columns name
    data = data.sort_values([DATE_COL])

    total_installs = find_total_installs(data[INSTALLS_COL])
    total_cost = find_total_cost(data[COST_COL])
    android_downloads, ios_downloads = find_total_android_and_ios_downloads(data[CAMPAIGN_COL], data[INSTALLS_COL])

    print(TOTAL_INSTALLS_MSG + str(total_installs))
    print(TOTAL_COST_MSG + str(total_cost) + DOLLAR_SIGN)
    print(TOTAL_ANDROID_MSG + str(android_downloads))
    print(TOTAL_IOS_MSG + str(ios_downloads))
    analyze_by_day(data)


if __name__ == '__main__':
    main()
