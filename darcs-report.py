import os, sys
import xml.etree.ElementTree as etree
import smtplib

if len(sys.argv[1:]) < 1:
    print('no respondents?')
    quit(1)

respondents = ', '.join(sys.argv[1:])

def load_latest_hash():
    try:
        return open('_darcs/prefs/latest.hash', 'r').read().strip()
    except:
        return None

def save_latest_hash(hash):
    with open('_darcs/prefs/latest.hash', 'w') as f:
        f.write("%s\n" % hash)

def getxml(cmd):
    sock = os.popen(cmd)
    tree = etree.fromstringlist(sock.readlines())
    sock.close()
    return tree

def send_report(patchname, author, hash):
    repo = os.path.split(os.getcwd())[-1]
    subject = '[%s] %s' % (repo, patchname)
    msg = "From: %s\nTo: %s\nSubject: %s\n" % (author, respondents, subject)
    sock = os.popen('darcs diff -u --hash "%s"' % hash)
    msg += ''.join(sock.readlines()) + '\n'
    sock.close()
    server = smtplib.SMTP('localhost')
    server.sendmail(author, respondents, msg)
    server.quit()

prevhash = load_latest_hash()
if prevhash is None:
    cmd = 'darcs changes --last 1 --xml-output'
else:
    cmd = 'DARCS_DONT_ESCAPE_ISPRINT=1 darcs changes --from-hash "%s" --xml-output' % prevhash
for el in reversed(getxml(cmd).findall('patch')):
    hash = el.attrib['hash']
    if hash == prevhash:
        continue
    send_report(el.find('name').text, el.attrib['author'], hash)
    save_latest_hash(el.attrib['hash'])
