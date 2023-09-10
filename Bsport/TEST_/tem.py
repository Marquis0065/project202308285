import xlwings as xw
app = xw.App(visible=False,add_book=False)
book = app.books.open(r'C:\Users\User\Desktop\SEO\12-18\今日数据(py接口).xlsx')
sheet1 = book.sheets['网站概况']
sheet1.range('A2:E2').expand('down').clear_contents()
sheet_qishu = book.sheets['趋势分析']
sheet_qishu.range('A2:F2').expand('down').clear_contents()
book.save()
book.close()
app.quit()