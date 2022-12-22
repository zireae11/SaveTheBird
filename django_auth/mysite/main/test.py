import pyshorteners

link = url11
s = pyshorteners.Shortener()
print(s.tinyurl.short(link))
