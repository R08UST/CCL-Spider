import csv
from selenium import webdriver
import urllib
import time
f=open('./means.csv','w')
writer=csv.writer(f)
writer.writerow(['文件名','上文','当前句','下文'])
mark='意思'
bs=webdriver.Firefox()
code=urllib.parse.quote(mark)
bs.get("http://ccl.pku.edu.cn:8080/ccl_corpus/search?q="+code+"&start=0&num=50&index=FullIndex&outputFormat=HTML&encoding=UTF-8&maxLeftLength=30&maxRightLength=30&orderStyle=score&LastQuery=&dir=xiandai&scopestr=")
while(True):
    #print(bs.page_source)
    #http=urllib.request.urlopen("http://ccl.pku.edu.cn:8080/ccl_corpus/search?q="+code+"&start=0&num=50&index=FullIndex&outputFormat=HTML&encoding=UTF-8&maxLeftLength=30&maxRightLength=30&orderStyle=score&LastQuery=&dir=xiandai&scopestr=")
    #bs=BeautifulSoup(http,"lxml")
    '''for rec in (bs.find_all('tr',style='padding:2px 5%')):
        print(rec.find('a'))'''
    buttons=[x.find_elements_by_tag_name('td')[-1] for x in bs.find_elements_by_tag_name('table')[-1].find_elements_by_tag_name('tr')] # find the context button
    for button in buttons:
        try:
            #time.sleep(0.5)
            button.click()
           # time.sleep(0.5)
            words=bs.find_element_by_id('info').find_elements_by_tag_name('tr')
            if words:
                where=words[0]
                pre=words[1]
                current=words[2]
                post=words[3]
                writer.writerow([where.text[3:],pre.text[2:],current.text[3:],post.text[2:]])
                #bs.find_element_by_class_name('ui-dialog-buttonset').click()
            else:
                words=bs.find_element_by_id('info').find_elements_by_tag_name('tr')    
        except:
            print('error')
            continue
    try:
        if bs.find_element_by_tag_name('p').find_elements_by_tag_name('a')[-1].text=='下一页':
            bs.find_element_by_tag_name('p').find_elements_by_tag_name('a')[-1].click()
            bs.current_url
        else:
            break
    except:
        a=bs.current_url
        start=str(int(a[a.find('start')+6:a.find('&num')])+50)
        bs.get("http://ccl.pku.edu.cn:8080/ccl_corpus/search?q="+code+"&start="+start+"&num=50&index=FullIndex&outputFormat=HTML&encoding=UTF-8&maxLeftLength=30&maxRightLength=30&orderStyle=score&LastQuery=&dir=xiandai&scopestr=")

bs.close()