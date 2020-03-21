from selenium import webdriver
import os
import time
os.mkdir('ogp')

##フォントのダウンロードとインストール
import urllib.request
import sys
import re
import shutil

FONTNAME="Roboto"
csspath = FONTNAME + ".css"
fontpath = FONTNAME + ".ttf"

#for Mac
#INSTALL_PATH = os.path.expanduser('~') + "/Library/Fonts/"
#for ubuntu
INSTALL_PATH = os.path.expanduser('~') + "/.local/share/fonts"

PATTERN  = r"url\(([\w/:%#\$&\?\(\)~\.=\+\-]+)\)"

#CSSのダウンロード
urllib.request.urlretrieve("http://fonts.googleapis.com/css?family="+FONTNAME,"{0}".format(csspath))

with open(csspath) as f:
    s = f.read()
match = re.findall(PATTERN, s)
print("Font File:" + match[0])
#Font本体のダウンロード
urllib.request.urlretrieve(match[0],"{0}".format(fontpath))
shutil.copy2(fontpath, INSTALL_PATH+fontpath)

PATHS = {
    '/?dummy': [959,500],
    '/cards/details-of-confirmed-cases': [959,500],
    '/cards/number-of-confirmed-cases': [959,500],
    '/cards/attributes-of-confirmed-cases': [959,480],
    '/cards/number-of-tested': [959,540],
    '/cards/number-of-reports-to-covid19-telephone-advisory-center': [959,500],
    '/cards/number-of-reports-to-covid19-consultation-desk': [959,500],
    '/cards/predicted-number-of-toei-subway-passengers': [959,750],
    '/cards/agency': [959,730],
    '/cards/details-of-tested-cases': [959, 500],
    '/cards/number-of-inspection-persons': [959, 600]
}

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--hide-scrollbars")

driver = webdriver.Chrome(options=options)

for lang in ['ja', 'en', 'zh-cn', 'zh-tw', 'ko', 'ja-basic']:
    os.mkdir('ogp/'+lang)
    for path, size in PATHS.items():
        print(lang+":"+path)
        driver.set_window_size(size[0], size[1])
        if lang == 'ja':
            driver.get("http://localhost:8000"+path+"?ogp=true")
            driver.save_screenshot('ogp/'+path.replace('/cards/', '').replace('/', '_')+'.png')
        else:
            driver.get("http://localhost:8000/"+lang+path+"?ogp=true")
            driver.save_screenshot('ogp/'+lang+'/'+path.replace('/cards/', '').replace('/', '_')+'.png')

driver.close()
driver.quit()
