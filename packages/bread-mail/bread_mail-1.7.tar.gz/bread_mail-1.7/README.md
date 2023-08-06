# Introduction

This is a simple Python application that is packed and used for sending email to multiple recipients at once.

<br />

## Pre-conditions

Please ensure that these following are installed on your operating system:

1. Python
2. Pip

<br />

## Installation

Use this command to install the package:

> pip install bread-mail

<br />

## How to launch

1. Open your **Command Prompt (CMD)/ Terminal** on your operating system.
2. Enter **python**
3. Enter **from bread_mail import gui**
4. Enter **gui.launch()**
5. It should appear with the GUI now

<br />

## How to use

#### Sender

1. Email will remain the same
2. **Password is different**, **App Password is needed** instead of your original account password
   > Manage your Google Account -> Security -> App Passwords (under section _Signing in to Google_)

_You have to complete 2-Step Verification to see App Passwords_

<br />

#### Receivers

1. Import the CSV file that stores the receivers' email
2. Select the email column
3. Load the email (emails auto-checking will be conducted to find out invalid emails)

<br />

#### Subject

This is the title of the email.

<br />

#### Message

Message of the email
'HTML editor' to create fancy message for the email.

<br />

#### Attachment

'Attach' to add attachment\
'Clear' to clear **all** the attachments
