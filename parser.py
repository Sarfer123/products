import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.webdriver import WebDriver

ser: Service = Service("/opt/homebrew/bin/geckodriver")
op: Options = webdriver.FirefoxOptions()
op.set_preference('dom.webdriver.enabled', False)
op.set_preference('dom.webnotfications.enabled', False)
op.set_preference('media.volume_scale', '0.0')
op.set_preference('general.useragent.override', 'matvey')
op.headless = True
browser: WebDriver = webdriver.Firefox(service=ser, options=op)

id = 0
x = 0
z = 1
column_number = 1
con = sqlite3.connect('products.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS products(id INT PRIMARY KEY,
names TEXT,
calories REAL,
proteins REAL,
fats REAL,
carbohydrates REAL);""")
con.commit()

for i in range(10000):
	id = id + 1
	cur.execute(f"INSERT INTO products(id) VALUES ({id});")
	con.commit()

id = 0

browser.get('https://calorizator.ru/product/all')

name = browser.find_element(By.CSS_SELECTOR, f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr.odd.views-row-first > td.views-field.views-field-title.active > a').get_attribute('textContent')
kcal = browser.find_element(By.CSS_SELECTOR, f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr.odd.views-row-first > td.views-field.views-field-field-kcal-value').get_attribute('textContent')
fat = browser.find_element(By.CSS_SELECTOR, f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr.odd.views-row-first > td.views-field.views-field-field-fat-value').get_attribute('textContent')
carbohydrate = browser.find_element(By.CSS_SELECTOR, f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr.odd.views-row-first > td.views-field.views-field-field-carbohydrate-value').get_attribute('textContent')
protein = browser.find_element(By.CSS_SELECTOR, f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr.odd.views-row-first > td.views-field.views-field-field-protein-value').get_attribute('textContent')

cur.execute(f"UPDATE products SET names = '{name}' WHERE id = '{column_number}';")
cur.execute(f"UPDATE products SET fats = '{fat}' WHERE id = '{column_number}';")
cur.execute(f"UPDATE products SET calories = '{kcal}' WHERE id = '{column_number}';")
cur.execute(f"UPDATE products SET proteins = '{protein}' WHERE id = '{column_number}';")
cur.execute(f"UPDATE products SET carbohydrates = '{carbohydrate}' WHERE id = '{column_number}';")
con.commit()

column_number = column_number + 80

for i in range(79):
	id = id + 1
	x = x + 1

	name = browser.find_element(By.CSS_SELECTOR,
	f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-title.active > a')\
	.get_attribute('textContent')
	kcal = browser.find_element(By.CSS_SELECTOR,
	f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-kcal-value')\
	.get_attribute('textContent')
	fat = browser.find_element(By.CSS_SELECTOR,
	f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-fat-value')\
	.get_attribute('textContent')
	carbohydrate = browser.find_element(By.CSS_SELECTOR, f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-carbohydrate-value').get_attribute('textContent')
	protein = browser.find_element(By.CSS_SELECTOR, f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-protein-value').get_attribute('textContent')

	cur.execute(f"UPDATE products SET names = '{name}' WHERE id = '{id}';")
	cur.execute(f"UPDATE products SET fats = '{fat}' WHERE id = '{id}';")
	cur.execute(f"UPDATE products SET calories = '{kcal}' WHERE id = '{id}';")
	cur.execute(f"UPDATE products SET proteins = '{protein}' WHERE id = '{id}';")
	cur.execute(f"UPDATE products SET carbohydrates = '{carbohydrate}' WHERE id = '{id}';")
	con.commit()
x = 0

for i in range(77):
	browser.get(f'https://calorizator.ru/product/all?page={z}')
	z = z + 1
	cur.execute(f"UPDATE products SET names = '{name}' WHERE id = '{column_number}';")
	cur.execute(f"UPDATE products SET fats = '{fat}' WHERE id = '{column_number}';")
	cur.execute(f"UPDATE products SET calories = '{kcal}' WHERE id = '{column_number}';")
	cur.execute(f"UPDATE products SET proteins = '{protein}' WHERE id = '{column_number}';")
	cur.execute(f"UPDATE products SET carbohydrates = '{carbohydrate}' WHERE id = '{column_number}';")
	con.commit()

	for i in range(78):
		id = id + 1
		x = x + 1

		name = browser.find_element(By.CSS_SELECTOR,
		f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-title.active > a')\
		.get_attribute('textContent')
		kcal = browser.find_element(By.CSS_SELECTOR,
		f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-kcal-value')\
		.get_attribute('textContent')
		fat = browser.find_element(By.CSS_SELECTOR,
		f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-fat-value')\
		.get_attribute('textContent')
		carbohydrate = browser.find_element(By.CSS_SELECTOR,
											f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-carbohydrate-value').get_attribute(
			'textContent')
		protein = browser.find_element(By.CSS_SELECTOR,
									   f'#main-content > div > div.view-content > table.views-table.sticky-enabled.cols-6.sticky-table > tbody > tr:nth-child({x}) > td.views-field.views-field-field-protein-value').get_attribute(
			'textContent')

		cur.execute(f"""UPDATE products SET names = "{name}" WHERE id = '{id}';""")
		con.commit()
		cur.execute(f"UPDATE products SET fats = '{fat}' WHERE id = '{id}';")
		con.commit()
		cur.execute(f"UPDATE products SET calories = '{kcal}' WHERE id = '{id}';")
		con.commit()
		cur.execute(f"UPDATE products SET proteins = '{protein}' WHERE id = '{id}';")
		con.commit()
		cur.execute(f"UPDATE products SET carbohydrates = '{carbohydrate}' WHERE id = '{id}';")
		con.commit()
	column_number = column_number + 80
	x = 0
