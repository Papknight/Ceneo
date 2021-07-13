import re

if __name__ == '__main__':
    # url = 'https://euro.com.pl/telewizory-led-lcd-plazmowe/lg-oled65cx-tv-oled-uhd-4k.bhtml?from=ceneo&p=8099.00&cr=0&t=20210503-0939&utm_source=ceneo&utm_medium=referral'
    # pattern = 'https?://(www.)?([0-9a-zA-Z]+)\..'
    # s = re.search(pattern, url)
    # for group in s.groups():
    #     print(group)

    text = 'Opinie o emaga.com'
    pattern = 'Opinie o ([a-zA-Z0-9 ]+)'
    s = re.search(pattern, text)
    print(s.groups()[0])
    # for group in s.groups():
    #     print(group)

