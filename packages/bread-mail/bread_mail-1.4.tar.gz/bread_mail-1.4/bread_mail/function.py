from asyncio.windows_events import NULL
import os
import pandas
import webbrowser
from tkinter import filedialog
from tkinter import messagebox
from pyisemail import is_email
import yagmail


def getFilePath(is_import):
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Downloads')

    if is_import:
        filePath = filedialog.askopenfilename(initialdir=desktop,
                                              title='Select desired file',
                                              filetypes=[('Excel files (xlsx, xls, csv)', '.xlsx .xls .csv'),
                                                         ('All files', '*.*')])
    else:
        filePath = filedialog.askopenfilename(initialdir=desktop,
                                              title='Select desired file',
                                              filetypes=[('All files', '*.*'),
                                                         ('Excel files (xlsx, xls, csv)',
                                                          '.xlsx .xls .csv'),
                                                         ('Document files (pdf, doc, docx)',
                                                          '.pdf .doc .docx'),
                                                         ('Image files (png, jpeg, gif)', '.png .jpeg .gif')])

    if (filePath == ''):
        return '-'
    return filePath


def getFileName(filePath):
    fileName = filePath.split('/')[len(filePath.split('/'))-1]
    return fileName


def validEmail(email):
    return is_email(email, check_dns=True)


def getColumn(filePath):
    file = pandas.read_csv(filePath)
    return sorted(file)


def getReceivers(filePath, column):
    file = pandas.read_csv(filePath)
    return (file[column].values.tolist())


def validateReceiver(receiverList):

    invalidReceiverList = []
    validReceiverList = []

    for receiver in receiverList:
        if(validEmail(receiver)):
            validReceiverList.append(receiver)
        else:
            invalidReceiverList.append(receiver)

    return validReceiverList, invalidReceiverList


def sendEmail(senderEmail, senderPassword, validReceiverList, mailSubject, mailMessage, mailAttachment):
    yag = yagmail.SMTP(senderEmail, senderPassword)

    try:
        yag.send(to=senderEmail, cc=validReceiverList,
                 subject=mailSubject, contents=mailMessage, attachments=mailAttachment)
        messagebox.showinfo(title='Email sent',
                            message='Email sent successfully.')
        webbrowser.open("https://www.youtube.com/watch?v=bdqj0T6F5HU")

    except:
        messagebox.showerror(title='Email Error',
                             message='Something wrong when sending email.')
