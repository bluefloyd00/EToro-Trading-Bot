import multiprocessing
import time

from random import randint
from selenium import webdriver
from selenium.webdriver.support.ui import Select

manager = multiprocessing.Manager()
stock_names = manager.list()
stock_per_change = manager.list()
stock_volume = manager.list()


class Auto_trading_bot:
    def __init__(self):
        # chrome 86 driver, you might have to install a different file here
        self.bot = webdriver.Chrome(executable_path='./chromedriver')

    def get_tables(self, local_stock_names, local_stock_per_change, local_stock_volume):
        bot = self.bot
        bot.get('https://finance.yahoo.com/most-active')  # reaching the site
        buttons = bot.find_elements_by_tag_name('button')  # getting all the buttons
        for button in buttons:
            if button.get_attribute('value') == 'agree':
                button.click()  # clicking the consent button
                break  # breaking the loop (or the if, I am not sure)
        # clicking twice the % change on the stocks table
        for i in range(2):
            time.sleep(3)  # waiting for the table content to load
            bot.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/'
                                      'div[2]/div[1]/table/thead/tr/th[5]').click()
        time.sleep(5)
        # getting the entire table
        table = bot.find_element_by_tag_name('tbody')
        # getting all the rows
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            # getting the first column for each row, the name of the stock
            # and appending the global list with these names
            local_stock_names.append(row.find_elements_by_tag_name('td')[0].text)
            # doing the same for the % change
            local_stock_per_change.append(row.find_elements_by_tag_name('td')[4].text)
            # once again for the total volume
            local_stock_volume.append(row.find_elements_by_tag_name('td')[5].text)


if __name__ == '__main__':
    bot1 = Auto_trading_bot()
    process1 = multiprocessing.Process(target=bot1.get_tables, args=(stock_names, stock_per_change, stock_volume))
    process1.start()
    process1.join()
    for i in range(25):
        print(str(stock_names[i]) + ' ' + str(stock_per_change[i]) + ' ' + str(stock_volume[i]))
