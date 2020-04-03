# coding:utf8
import sys
import datetime
import xlwt
import MySQLdb
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib

# reload(sys)
# sys.setdefaultencoding('utf8')


def get_datas(sql):
    # 一个传入sql导出数据的函数
    # 跟数据库建立连接
    conn = MySQLdb.connect('localhost', 'root', 'mysql', 'healthy', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cur = conn.cursor()
    # 使用 execute() 方法执行 SQL
    cur.execute(sql)
    # 获取所需要的数据
    datas = cur.fetchall()
    # 关闭连接
    cur.close()
    # 返回所需的数据
    return datas


def get_fields(sql):
    # 一个传入sql导出字段的函数
    conn = MySQLdb.connect('localhost', 'root', 'mysql', 'healthy', charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    # 获取所需要的字段名称
    fields = cur.description
    cur.close()
    return fields


def get_excel(data, field, file):
    # 将数据和字段名写入excel的函数
    # 新建一个工作薄对象
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)

    # 写上字段信息
    for col in range(0, len(field)):
        sheet.write(0, col, field[col][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(data) + 1):
        for col in range(0, len(field)):
            sheet.write(row, col, u'%s' % data[row - 1][col])

    newworkbook = workbook.save(file)
    return newworkbook


def GetToday():
    # 获取当前日期
    today = datetime.date.today()
    return today


def create_email(email_from, email_to, email_subject, email_text, annex_path, annex_name):
    # 输入发件人昵称、收件人昵称、主题，正文，附件地址,附件名称生成一封邮件
    # 生成一个空的带附件的邮件实例
    message = MIMEMultipart()
    # 将正文以text的形式插入邮件中
    message.attach(MIMEText(email_text, 'plain', 'utf-8'))
    # 生成发件人名称（这个跟发送的邮件没有关系）
    message['From'] = Header(email_from, 'utf-8')
    # 生成收件人名称（这个跟接收的邮件也没有关系）
    message['To'] = Header(email_to, 'utf-8')
    # 生成邮件主题
    message['Subject'] = Header(email_subject, 'utf-8')
    # 读取附件的内容
    att1 = MIMEText(open(annex_path, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 生成附件的名称
    att1["Content-Disposition"] = 'attachment; filename=' + annex_name
    # 将附件内容插入邮件中
    message.attach(att1)
    # 返回邮件
    return message


def send_email(sender, password, receiver, msg):
    # 一个输入邮箱、密码、收件人、邮件内容发送邮件的函数
    try:
        # 找到你的发送邮箱的服务器地址，已加密的形式发送
        server = smtplib.SMTP_SSL("smtp.tom.com", 465)  # 发件人邮箱中的SMTP服务器
        server.ehlo()
        # 登录你的账号
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        # 发送邮件
        server.sendmail(sender, receiver, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号（是一个列表）、邮件内容
        print("邮件发送成功")
        server.quit()  # 关闭连接
    except Exception:
        print("邮件发送失败")


def main():
    my_sql = sql = 'select body,count(body),time ' \
                   'from tb_health ' \
                   'where to_days(time)=to_days(now()) ' \
                   'group by body,time ' \
                   'order by body'

    # 生成数据
    my_data = get_datas(my_sql)
    # 生成字段名称
    my_field = get_fields(my_sql)
    # 得到日期
    todaystr = GetToday()
    # 文件名称
    my_file_name = str(todaystr) + '.xlsx'
    # 文件路径
    file_path = 'G:/PycharmProjects/django_mjj/' + my_file_name
    # 生成excel
    get_excel(my_data, my_field, file_path)

    my_email_from = '本人'
    my_email_to = '公司'
    # 邮件标题
    my_email_subject = str(todaystr)
    # 邮件正文
    my_email_text = "Dear all,\n\t附件为每天数据，请查收! "
    # 附件地址
    my_annex_path = file_path
    # 附件名称
    my_annex_name = my_file_name
    # 生成邮件
    my_msg = create_email(my_email_from, my_email_to, my_email_subject,
                          my_email_text, my_annex_path, my_annex_name)
    my_sender = 'mengjunjie@tom.com'
    my_password = '密码'
    my_receiver = ['1046853595@qq.com']  # 接收人邮箱列表
    # 发送邮件
    send_email(my_sender, my_password, my_receiver, my_msg)
    print(datetime.datetime.now())


if __name__ == '__main__':
    main()
