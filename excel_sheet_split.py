#  Split one excel file with multiple sheets into several excel files
from openpyxl import load_workbook,Workbook


wb = load_workbook("D:/20200708/csv/123.xlsx")
sheetnames = wb.sheetnames
#print (sheetnames)
for k in range(0,len(sheetnames)):
    #print (sheetnames[k])
    ws = wb.worksheets[k]
    print(ws)
    # create new Excel
    wb2 = Workbook()
    # get sheet detail
    ws2 = wb2.active
    #get all details in excel by using for function
    for i,row in enumerate(ws.iter_rows()):
        for j,cell in enumerate(row):
            # write into new Excel
            ws2.cell(row=i+1, column=j+1, value=cell.value)
            # set new sheet name
            ws2.title = sheetnames[k]

    wb2.save(sheetnames[k] + ".xlsx")
