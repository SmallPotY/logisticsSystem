# coding=utf-8
import poplib
import time
import os

from email.parser import Parser

from email.header import decode_header
from jobs.Email.EmaillDownload import download_email_path


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


# 邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# 下载邮件附件
def get_mail_attachment(email_host, email_user, email_pass, key_word):
    # 需要验证的邮件服务
    pop_conn = poplib.POP3_SSL(email_host)
    pop_conn.user(email_user)
    pop_conn.pass_(email_pass)

    num = len(pop_conn.list()[1])  # 邮件总数
    get_file_sucess = 0
    # 倒叙遍历邮件
    for i in range(num, 0, -1):

        resp, lines, octets = pop_conn.retr(i)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)

        receiving_time = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')  # 格式化收件时间
        receiving_time = time.strftime("%Y%m%d%H%M%S", receiving_time)

        # 获取邮件标题和发件人
        email_title, from_name, from_addr = '', '', ''
        for header in ['From', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    subject = decode_str(value)  # 解析邮件标题
                    email_title = '%s' % subject
                # else:
                #     hdr, addr = parseaddr(value)
                # name = decode_str(hdr)
                # from_name = '%s' % name  # 解析发件人名称
                # from_addr = '%s' % addr  # 解析发件人邮箱

        # print('receiving_time', receiving_time)
        # print("email_title", email_title)
        # print("from_name", from_name)
        # print("from_addr", from_addr)

        # print("=======================================")
        if key_word in email_title:
            for part in msg.walk():
                filename = part.get_filename()

                if filename:
                    data = part.get_payload(decode=True)

                    path = download_email_path + '/'
                    file_name = email_title + receiving_time + '.xls'
                    save_path = path + file_name

                    if os.path.exists(save_path):
                        pop_conn.quit()
                        return False, '文件已存在'
                    f_ex = open(save_path, 'wb')
                    f_ex.write(data)
                    f_ex.close()
                    get_file_sucess += 1
                    pop_conn.quit()
                    return True, save_path
                # else:
                #     print('所查找的邮件无附件')
        # else:
        #     print('无匹配邮件!\n')
    if get_file_sucess == 0:
        pop_conn.quit()
        return False, '未找到符合条件的邮件'


if __name__ == '__main__':
    emailhost = "imap.exmail.qq.com"
    emailuser = "jie.yang@hxh-ltd.com"
    emailpass = "Jyang19930621+-*/"
    keywords = "预警编号5372：肇庆圆通出仓数据"
    get_mail_attachment(emailhost, emailuser, emailpass, keywords)
