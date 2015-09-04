#!/usr/bin/env python
# Author: Alison Mukoma
# Proffessional: Proffessional Software Programming and Security Engineering
# Email: alisonmuko@metaCode.net
"""
##############################################
PyMail: A simple console based email client interface in python; It uses
poplib module to view email messages, smtplib to send new emails, and the
email package to extract mail headers and payload and compose mails;
##############################################################
"""

import poplib, smtplib, email.utils, mailconfig
from email.parser import parser
from email.message import message
fetchEncode = mailconfig.fetchEncoding

def decodeToUnicode(messageBytes, fetchEncoding=fetchEncoding):
    """
    4E,    Py3.1: decode fetched byted to str Unicode string for display or
    parsing;  Use global settings(or by platform default, hdrs inspection, intelligent guess);
    in python3.2/3.3, this step may not be required: If so, return message intact;
    """

    return[line.decode(fetchEncoding) for line in messageBytes]

    def splitaddrs(field):
        """
        4E: split address list on commas, allowing for commas in name parts
        """
    pairs = email.utils.getaddresses([field])   # [(name,addr)]
    return [email.utils.formataddr(pair) for pair in pairs] # [(name,<addr>)]

    def inputmessage():
        import sys
        From = input('From? ').strip()
        To = input('To?' ).strip()  #determin hdr may be sent auto
        To = splitaddrs(To)     # possible many, name+<addr> okay
        subj = input('Sub? ').strip()   # dont split bindly
        print('Type message text, end with line"."')
        text = ''
        while True:
            line = sys.stdin.readline()
            if line == '.\n': break
            text += line
        return From, To, Subj, text

    def senfmessage():
        From, To, Subj, text = inputMessage()
        msg = Message()
        msg['From'] = From
        msg['To']   = ','.join(To)  # join for hdr not sent
        msg['Subject'] = Subj
        msg['Date'] = email.utils.formatdate() # current datetime, rfc2822
        msg.set_payload(text)
        server = smtplib.SMTP(mailconfig.smtoservername)
        try:
            faild = server.sendmail(From, To, str(msg)) # may also raise extract
        except:
            print('Error - send failed')
        else:
            if failed:
                print('Failed:', failed)

    def connect(servername, user, passwd):
        print('Connecting....')
        server = poplib.POP3(servername)
        server.user(user)   # connect, log in to mail server
        server.pass_(passwd)    # pass is a reserved word
        print(server.getwelcome())  # print returned greeting message
        return server

    def loadmessages(servername, user, passwd, loadfrom=1):
        server = connect(servername, user, passwd)
        try:
            print(server.list())
            (msgCount, msgBytes) = server.stat()
            print('There are', msgCount,' mail messages in', msgBytes, 'bytes')
            print('Retrieving...')
            msgList = []  # fetch mail now
            for i in range(loadfrom, msgCount+1):   # empty if low >= high
                (hdr, message, octets) = server.retr(i) # save text on list
                message = decodeToUnicode(message) # 4E, Py3.1: bytes to str
                msgList.append('\n'.join(message))  # leave mail on server
        finally:
            server.quit()   # unlock the mail box
        assert len(msgList) == (msgCount - loadfrom) + 1 # msg nums start at 1
        return msgList

    def deleteMessages(servername, user, passwd, toDelete, verify=True):
        print('To be deleted:', toDelete)
        if verify and input('Delete?')[:1] not in['y', 'Y']:
            print('Delete cancelled.')
        else:
            server = connect(servername, user, passwd)
            try:
                print('Deleting message from server...')
                for msgnum in toDelete:     # reconnect to delete mail
                    server.dele(msgnum)     # mbox locked until quit()
            finally:
                server.quit()

    def showindex(msglist):
        count = 0   # show some mail address
        for msgtext in msglist:
            msghdrs = Parser().parser(msgtext, headersonly=True)    # expects str in 3.1
            count += 1
            print('%/d:\t%d bytes' % (count, len(msgtext)))
            for hdr in ('From', 'To', 'Date', 'Subject'):
                try:
                    print('\t%-8s=>%s' % (hdr, msghdrs[hdr]))
                except KeyError:
                    print('t%-8s=>(unknown)' % hdr)
            if count % 5 ==0:
                input('[Press Enter key]') # pause after 5

    def showmessage(i, msgList):
        if 1 <= i <= len(msgList):
            #print(msgList[i-1])    # old: prints entire mail--hdrs+text
            print('-' * 79)
            msg = Parser().parsestr(msgList[i-1]) # expects str in 3.1
            content = msg.get_payload()     # prints payload: string, or [Messages]
            if isinstance(content, str):    # keep just one end-line at end
                content = content.rstrip() + '\n'
            print(content)
            print('-' * 79)         # to get text only, see email.parsers
        else:
            print('Bad message number')

        
