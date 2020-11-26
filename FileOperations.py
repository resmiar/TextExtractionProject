import xlsxwriter


def write_file(tags_list):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Tags_list.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    print("Writing to file")

    # Iterate over the data and write it out row by row.
    for attribute in tags_list.keys():
        worksheet.write(row, col, attribute)
        worksheet.write(row+1, col, tags_list[attribute])
        col += 1

    workbook.close()

