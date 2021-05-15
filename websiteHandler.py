import urllib.request
from datetime import datetime
from urllib.parse import urlparse
import gzip
import shutil
import os
import webbrowser
import difflib
import hashlib
from bs4 import BeautifulSoup


def setVariable(URL):
    global TIME
    global FILENAME
    global WEBSITENAME

    TIME = str(datetime.now())  # Get current time
    TIME = TIME[:-7]  # Make current time look more readable
    WEBSITENAME = urlparse(URL).netloc  # Get the whole domain
    WEBSITENAME = ('.'.join(WEBSITENAME.split('.')[1:]))  # Strips the TLD
    FILENAME = WEBSITENAME + " " + TIME + ".html"  # creates the filename


def downloadWebPage(URL):
    urllib.request.urlretrieve(URL, FILENAME)


def compressWebpage():
    with open(FILENAME, 'rb') as f_in:
        with gzip.open(FILENAME + ".gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def deleteOldWebPage():
    os.remove(FILENAME)


def moveSnapShot():
    shutil.move(FILENAME + ".gz", os.getcwd() + "/Snapshots")


# https://stackoverflow.com/questions/19007383/compare-two-different-files-line-by-line-in-python
def compareTwoFiles(FILECHOICE):
    if isDifferent(FILECHOICE) == 0:

        beautifyTheSoup(FILECHOICE[:-3] + "-Decompressed.html")
        beautifyTheSoup(FILENAME)

        global COMPARISONFILENAME
        COMPARISONFILENAME = "Comparison of " + FILENAME + "-" + FILECHOICE[:-3]
        file1 = open(FILECHOICE[:-3] + "-Decompressed.html", 'r').readlines()
        file2 = open(FILENAME, 'r').readlines()
        htmlDiffer = difflib.HtmlDiff()
        htmldiffs = htmlDiffer.make_file(file1, file2, FILECHOICE[:-3] + "-Decompressed.html", FILENAME)

        with open(COMPARISONFILENAME + ".html", 'w') as outfile:
            outfile.write(htmldiffs)
        return 1
    else:
        return 0


def decompressWebpage(FILECHOICE):
    with gzip.open(FILECHOICE, 'rb') as f_in:
        with open(FILECHOICE[:-3] + "-Decompressed.html", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def beautifyTheSoup(file):
    with open(file) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        html = soup.prettify("utf-8")
        with open(file, "wb") as file:
            file.write(html)


def openDecompressedFile(FILECHOICE):   # No extensions
    webbrowser.open('file://' + os.path.realpath(FILECHOICE))


def openComparisonFile(COMPARISONFILENAME):     # No extensions
    webbrowser.open('file://' + os.path.realpath(COMPARISONFILENAME + ".html"))


def isDifferent(FILECHOICE):        # No extensions
    currentVersion = sha256sum(FILECHOICE[:-3] + "-Decompressed.html")
    snapshotVersion = sha256sum(FILENAME)
    if currentVersion == snapshotVersion:
        return 1
    else:
        return 0


def sha256sum(filename):  # No extensions
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def deleteDecompressedFile(FILECHOICE):  # No nextensions
    os.remove(FILECHOICE)


def deleteComparisonFile(COMPARISONFILENAME):  # No nextensions
    os.remove(COMPARISONFILENAME + ".html", )


def compareSnapshot(URL, FILECHOICE):   # No extensions
    if os.getcwd()[-10:] != "/Snapshots":
        os.chdir(os.getcwd() + "/Snapshots")
    setVariable(URL)
    downloadWebPage(URL)
    decompressWebpage(FILECHOICE)
    if compareTwoFiles(FILECHOICE) == 1:
        openComparisonFile(COMPARISONFILENAME)
        deleteDecompressedFile(FILECHOICE[:-3] + "-Decompressed.html")
        deleteOldWebPage()
        deleteComparisonFile(COMPARISONFILENAME)
        deleteDecompressedFile(FILECHOICE + ".gz")
    else:
        deleteDecompressedFile(FILECHOICE[:-3] + "-Decompressed.html")
        deleteOldWebPage()
        return 0


def compareSnapshotAndSave(URL, FILECHOICE):    # No extensions
    if os.getcwd()[-10:] != "/Snapshots":
        os.chdir(os.getcwd() + "/Snapshots")
    setVariable(URL)
    downloadWebPage(URL)
    decompressWebpage(FILECHOICE)
    if compareTwoFiles(FILECHOICE) == 1:
        openComparisonFile(COMPARISONFILENAME)
        deleteDecompressedFile(FILECHOICE[:-3] + "-Decompressed.html")
        deleteComparisonFile(COMPARISONFILENAME)
        compressWebpage()
        deleteOldWebPage()
    else:
        deleteDecompressedFile(FILECHOICE[:-3] + "-Decompressed.html")
        deleteOldWebPage()
        return 0


def viewSnapshot(FILECHOICE):   # No extensions
    decompressWebpage(FILECHOICE)
    openDecompressedFile(FILECHOICE[:-3] + "-Decompressed.html")
    deleteDecompressedFile(FILECHOICE[:-3] + "-Decompressed.html")


def takeSnapShot(URL):  # No extensions
    setVariable(URL)
    downloadWebPage(URL)
    compressWebpage()
    deleteOldWebPage()
    moveSnapShot()
