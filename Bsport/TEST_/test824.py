import time
import telebot
import xlwings as xw
from PIL import ImageGrab

app = xw.App(visible=False,add_book=False)
book = app.books.open(r'C:\Users\User\Desktop\数据+ip历史-22.xlsx')
sheet_shuju = book.sheets['数据']
sheet_ip =  book.sheets['ip历史']
row_ip = sheet_ip.used_range.last_cell.row
row_shuju = sheet_shuju.used_range.last_cell.row

range_shuju = sheet_shuju.range(f'A{row_shuju+1}:V{row_shuju+9}')
range_shuju.api.CopyPicture()
img_shuju = ImageGrab.grabclipboard()  # 获取剪贴板的图片数据
img_shuju.save(r'C:\Users\User\Desktop\SEO\截图文件\shuju.png')  # 保存图片
time.sleep(2)

range_IP = sheet_shuju.range(f'A{row_ip+1}:V{row_ip+63}')
range_IP.api.CopyPicture()
img_IP = ImageGrab.grabclipboard()  # 获取剪贴板的图片数据
img_IP.save(r'C:\Users\User\Desktop\SEO\截图文件\IP.png')  # 保存图片
time.sleep(2)

bot_DA = telebot.TeleBot("6106076754:AAHjxPSBpyjwpY-lq1iEslUufW46XQvAfr0")
bot_DA.send_photo(-812533282,open(r'C:\Users\User\Desktop\SEO\截图文件\shuju.png','rb'))
bot_DA.send_photo(-812533282,open(r'C:\Users\User\Desktop\SEO\截图文件\IP.png','rb'))
# 关闭机器人实例
bot_DA.stop_polling()

book.close()  # 不保存，直接关闭
app.quit()  # 退出

