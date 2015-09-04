#!/usr/bin/env python2.7
# Author: Alison Mukoma
# Proffessional: Proffessional Software Programming and Security Engineering
# Email: alisonmuko@metaCode.net
# written: 3rd September 2015: From: 03Am...
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

    def sendmessage():
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


    def msgnum(command):
        try:
            return int(command.split()[1])
        except:
            return -1 # assume this is Bad

    helptext = """
    Available commands:
    i    - index display
    l n? - list all messages (or just message n)
    d n? - mark all messages for deletion (or just message n)
    s n? - save all messages to a file (or just message n)
    m
    - compose and send a new mail message
    q
    - quit pymail
    ?
    - display this help text

    """

    def interact(msgList, mailfile):
        showindex(msgList)
        toDelete = []
        while True:
            try:
                command = input('[Pymail] Action? (i, l, d, s, m, q, ?)')
            except EOFError:
                command = 'q'
            if not command:
                command = '*'

            # quit
            if command == 'q':
                break

            # index
            elif command[0] == 'i':
                showu=index(msgList)

            # list
            elif command[0] == 'l':
                if len(commad) == 1:
                    for i in range(1, len(msgList)+1):
                        showmessage(i, msgList)
                else:
                    showmessage(msgnum(command), msgList)

            # save
            elif command[0] == 's':
                if len(command) == 1:
                    for i in range(1, len(msgList)+1):
                        savemessage(i, mailfile, msgList)
                else:
                    savemessage(msgnum(command), mailfile, msgList)

            # delete
            elif command[0] == 'd':
                if len(command) == 1:   # delete all later
                    toDelete = list(range1, len(msgList)+1) # 3.x requires list
                else:
                    delnum = msgnum(command)
                    if(1 <= len(msgList)) and (delnum not in toDelete):
                        toDelete.append(delnum)
                    else:
                        print('Bad message number')



                    # toDelete = list(range(1, length(msgList)) and (delnum not in toDelete)):
            # mail
        elif command[0] == 'm': # send a new mail via SMTP
            sendmessage()
            #execfile('smtpmail.py', {})    # alt: run file in own namespace
        elif command[0] == '?':
            print(helptext)
        else:
            print('what? -- type "?" for command help')
    return toDelete

if __name__=="__main__":
    import getpass
    import mailconfig
    mailserver = mailconfig.popservername   # ex: 'pop.rmi.net'
    mailuser = mailconfig.popusername   # ex: 'Alison'
    mailfile = mailconfig.savemailfile  # ex: r'c:\stuffsavemail'
    mailpswd = getpass.getpass('Password for %s?' % mailserver)
    print(['Pymail emailclient'])
    msgList = loadmessages(mailserver, mailuser, mailpaswd) # load all
    toDelete   = interact(msgList, mailfile)
    if toDelete:
        deleteMessages(mailserver, mailuser, mailpswd, toDelete)
    print("BYE.")
