# fastmaillib.py
# LICENSE: MIT
# VERSION: v0.2.1
"""
说明:
更加方便地使用 Python 收邮件
部分基于 Liao Xuefeng 的代码, 并进行了封装操作
此代码为 Python 3.x 而设计, 但理论上兼容 Python 2.x(2.7)
"""
"""
日志:
v0.2.3:
    修复 Get.get 函数中 num 参数不可用问题
"""

import email, smtplib
from email.mime.text import MIMEText
from email.parser import Parser
import poplib
from email.header import decode_header
from email.utils import parseaddr

class Get:
    def connect(mail, user, password, pop3_host):
        """Connect to mail server"""
        try:
            obj = poplib.POP3_SSL(pop3_host)
            obj.user(user)
            obj.pass_(password)
            return obj
        except Exception as e:
            return e
    def num(obj):
        """Get the number of messages on hand"""
        try:
            resp, mails, octets = obj.list()
            return len(mails)
        except Exception as e:
            return e
    def get(obj, num):
        """Get mail's content"""
        try:
            resp, mails, octets = obj.list()
            index = len(mails)
            resp, lines, octets = obj.retr(num)
            message_content = b'\r\n'.join(lines).decode('utf-8')
            message = Parser().parsestr(message_content)
            info = Get.print_info(message)
            return info
        except Exception as e:
            return e
    def quit(obj):
        """Break connection"""
        try:
            obj.quit()
            return True
        except Exception as e:
            return e
    def print_info(msg, indent=0):
        """Convert mail object to content"""
        total = {}
        if indent == 0:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header == 'Subject':
                        value = Get.decode_str(value)
                        total["subject"] = value
                    else:
                        hdr, addr = parseaddr(value)
                        name = Get.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                        if not("name" in total):
                            total["name"] = name
                            total["addr"] = addr
        if msg.is_multipart():
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                total["message"] = part
                # print_info(part, indent + 1)
        else:
            content_type = msg.get_content_type()
            if content_type == 'text/plain' or content_type == 'text/html':
                content = msg.get_payload(decode=True)
                charset = guess_charset(msg)
                if charset:
                    content = content.decode(charset)
        return total
    def decode_str(s):
        """Decode mail objects"""
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value
    def guess_charset(msg):
        """Guess charset"""
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset