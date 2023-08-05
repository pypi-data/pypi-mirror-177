# Documento inicial
# https://github.com/gabrielbdornas/projetos-antigos-testes/blob/main/vpn-fhemig/app/controllers/contracheque_importations_controller.rb
from meu_contracheque.time_reader import find_last_month, find_today, find_last_period
import os
import shutil
import sys
import click
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pathlib import Path
from dotenv import load_dotenv
import csv
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import unidecode
import time
load_dotenv(dotenv_path=Path('.', '.env'))

def clean_full_process():
  os.system('rm -rf .temp/')
  os.system('rm -rf contracheques.csv')

def clean_process():
  os.system('rm -rf .temp/')

def scraping_process_begin(headless):
  try:
    driver = driver_initiate(headless)
    today = find_today()
    last_month = find_last_month(today)
    period = get_period(last_month)
  except:
    click.echo('Não foi possível iniciar o processo de busca de contracheque.')
    sys.exit(1)
  return driver, period

def driver_initiate(headless):
  try:
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.headless = headless
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(3)
    driver.get('https://www.portaldoservidor.mg.gov.br/broker2/?controle=LoginInicial')
  except:
    click.echo('Não foi possível iniciar o driver. Tente acesso mais tarde pois portal pode estar fora do ar.')
    sys.exit(1)
  return driver

def scraping_login_process(driver, period, masp, senha):
  try:
    cpf_field = driver.find_element(By.NAME, 'j_username')
    pwd_field = driver.find_element(By.NAME, 'j_password')
    cpf_field.send_keys(masp)
    pwd_field.send_keys(senha)
    # Clica no botão para entrar e selecionar o mês desejado
    button = driver.find_elements(By.XPATH, "//button")[1]
    button.click()
  except:
    click.echo('Não foi possível realizar login para busca do contracheque')
    sys.exit(1)

def scraping_full_process(driver, period, headless):
  doc_type = ''
  driver.implicitly_wait(3)
  contracheque = driver.find_element(By.XPATH, "/html/body/js-placeholder/div[1]/main/section[2]/div[1]/div[1]/a") 
  driver.execute_script("arguments[0].setAttribute('target','_self')", contracheque)
  contracheque.click()
  #enter iframe before select month input field
  driver.get('https://www.portaldoservidor.mg.gov.br/fcrh-portal/area-restrita/?menu=contracheques')
  month_input = driver.find_element_by_class_name('z-textbox')
  month_input.send_keys(period)
  contracheque_button = driver.find_element(By.XPATH, "//div/div/button")
  contracheque_button.click()
  time.sleep(10)
  lines = driver.find_elements(By.XPATH, "//tr[@class='z-listitem']")
  # import ipdb; ipdb.set_trace(context=10)
  for line in lines:
    doc_type = line.find_elements(By.XPATH, "//div[@class='z-listcell-content']")[1].text
    doc_type = format_doc_type(doc_type)
    get_pdf(driver, period, doc_type, headless)
    exibir_button = driver.find_element(By.XPATH, "//button[text()='Exibir']")
    exibir_button.click()
    get_page_source(driver, period, doc_type)

def format_doc_type(doc_type):
  unaccented_string = unidecode.unidecode(doc_type)
  return unaccented_string.lower().replace(' ', '_')  

def get_page_source(driver, period, doc_type):
  if not os.path.isdir('.temp'):
    os.system('mkdir .temp')
  page_source = driver.page_source
  file_path = page_source_file_path(period, doc_type)
  write_page_source = open(file_path, 'w', encoding='utf-8')
  write_page_source.write(page_source)
  write_page_source.close()
  driver.find_element(By.XPATH, "//button[text()='Voltar']").click()

def get_pdf(driver, period, doc_type, headless):
  if not os.path.isdir('contracheques'):
    os.system('mkdir contracheques')
  period_list = period.split('/')
  mes = period_list[0]
  ano = period_list[1]
  downloads_path = str(Path.home() / "Downloads")
  file_path = ''
  new_file_path = f'contracheques/{ano}{mes}_contracheque_{doc_type}.pdf'
  if headless:
    file_path = f'Contracheque-{ano}{mes}.pdf'
  else:
    file_path = f'{downloads_path}/Contracheque-{ano}{mes}.pdf' 
  if os.path.isfile(file_path):
    os.remove(file_path)
  click.echo(f'Baixando pdf do contracheque {doc_type} {period}')
  driver.find_element(By.XPATH, "//button[text()='Baixar']").click()
  if os.path.isfile(new_file_path):
    os.remove(new_file_path)
  time.sleep(10)
  download_completed = False
  shutil.move(file_path, new_file_path)

def page_source_file_path(period, doc_type):
  period = period.split('/')
  month = period[0]
  year = period[1]
  file_path = f".temp/{year}_{month}_{doc_type}_page_source.html"
  return file_path

def csv_register():
  for file in os.listdir('.temp'):
    position = os.listdir('.temp').index(file) + 1
    files_len = len(os.listdir('.temp'))
    split_file = file.split('_')
    year = split_file[0]
    month = split_file[1]
    doc_type = split_file[2]
    period = f'{month}/{year}'
    click.echo(f'Registrando csv {position} de {files_len} contraqueche(s) - {period}')
    # csv header
    fieldnames = ['periodo', 'mes', 'ano', 'masp', 'tipo_contracheque', 'cpf','nome', 'cargo', 'orgao_exercicio', 'unidade_exercicio', 'verba', 'valor', 'previdencia']
    rows = find_contracheque_values(period, doc_type)
    file_path = 'contracheques.csv'
    file_exist = os.path.isfile(file_path)
    with open(file_path, 'a', encoding='utf-8', newline='') as f:
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      if not file_exist:
        writer.writeheader()
      writer.writerows(rows)

def find_contracheque_values(period, doc_type):
  rows = []
  file_path = page_source_file_path(period, doc_type)
  file = open(file_path, 'r', encoding='utf-8').read()
  soup = BeautifulSoup(file, 'html5lib')
  value_table = soup.findAll("tbody")[8]
  lines = value_table.findAll("tr") # linhas da tabela
  for line in lines:
    row = find_contracheque_fix_information(period, doc_type)
    if lines.index(line) != 0: # Pula a primeira linha da tabela que é o cabeçalho
      columns = line.findAll("td") # colunas da tabela por linha
      for column in columns:
        if columns.index(column) == 2: # coluna da descrição da despesa
          text = column.findAll("small")
          if len(text) != 0:
            text = text[0].text.strip()
            row['verba'] = text
        elif columns.index(column) == 4:
          value = column.findAll("small")
          if len(value) != 0:
            value = float(value[0].text.strip()[3:].replace('.', '').replace(',', '.'))
            row['valor'] = value
        elif columns.index(column) == 5:
          value = column.findAll("small")
          if len(value) != 0:
            value = float(value[0].text.strip()[3:].replace('.', '').replace(',', '.')) * -1
            row['valor'] = value
    if 'verba' in row.keys() and 'valor' in row.keys():
      rows.append(row)
  return rows

def find_contracheque_fix_information(period, doc_type):
  file_path = page_source_file_path(period, doc_type)
  file = open(file_path, 'r', encoding='utf-8').read()
  soup = BeautifulSoup(file, 'html5lib')
  elements = soup.findAll("small")
  row = {
      'periodo': period,
      'mes': int(period.split('/')[0]),
      'ano': int(period.split('/')[1]),
      'masp': elements[23].get_text(strip=True),
      'tipo_contracheque': doc_type,
      'cpf': elements[59].get_text(strip=True),
      'nome': elements[26].get_text(strip=True),
      'cargo': elements[80].get_text(strip=True),
      'orgao_exercicio': elements[104].get_text(strip=True),
      'unidade_exercicio': elements[113].get_text(strip=True)
    }
  return row

def get_period(last_month):
  return f'{last_month.month}/{last_month.year}'

def normalize_period(period):
  split_period = period.split('/')
  month = str(split_period[0])
  if len(month) == 1:
    month = f'0{month}'
  year = split_period[1]
  period = f'{month}/{year}'
  return period



  # contracheque = driver.find_element(By.XPATH, "/html/body/js-placeholder/div[1]/nav[3]/div[1]/ul[2]/li/div/ul/li[3]/a")
  # while found_period:
  #   mes = driver.find_element(By.ID, 'mesAno')
  #   # Seleciona o mês desejada e clica no botão consultar
  #   period = normalize_period(period)
  #   mes.send_keys(period)
  #   driver.find_element(By.XPATH, "//input[@type='submit' and @value='Consultar']").click()
  #   try:
  #     driver.find_element(By.XPATH, f"//b[text()='Nao possui contracheque no mes/ano {period}']")
  #     if stop_period == None:
  #       found_period = False
  #       click.echo(f'Fim da busca. Nao possui contracheque no mes/ano {period}.')
  #     elif stop_period == period:
  #       found_period = False
  #       click.echo(f'Fim da busca no período {period} desejado.')
  #     else:
  #       period = get_period(find_last_period(period))
  #       click.echo(f'Nao possui contracheque no mes/ano {period}.')
  #       voltar = driver.find_element(By.XPATH, "//a[@class='botao' and text()='VOLTAR']")
  #       voltar.click()
  #       found_period = (True, False)[last_period] # para execução se desejado for último período
  #   except NoSuchElementException:
  #     try:
  #       voltar = driver.find_element(By.XPATH, "//a[@class='botao' and text()='VOLTAR']")
  #       click.echo(f'Baixando informações contracheque {period}')
  #       get_page_source(driver, period, 'normal', pdf)
  #       period = get_period(find_last_period(period))
  #       voltar.click()
  #       found_period = (True, False)[last_period] # para execução se desejado for último período
  #     except NoSuchElementException:
  #       driver.find_element(By.XPATH, "//input[@type='submit' and @value='Consultar']").click()
  #       click.echo(f'Baixando informações contracheque {period}')
  #       get_page_source(driver, period, 'normal', pdf)
  #       driver.find_element(By.XPATH, "//a[@class='botao' and text()='VOLTAR']").click()
  #       mes = driver.find_element(By.ID, 'mesAno')
  #       mes.send_keys(period)
  #       driver.find_element(By.XPATH, "//input[@type='submit' and @value='Consultar']").click()
  #       driver.find_element(By.XPATH, "//input[@id='folha1']").click()
  #       driver.find_element(By.XPATH, "//input[@type='submit' and @value='Consultar']").click()
  #       click.echo(f'Baixando informações contracheque gratificação {period}')
  #       get_page_source(driver, period, 'gratificacao', pdf)
  #       period = get_period(find_last_period(period))
  #       voltar = driver.find_element(By.XPATH, "//a[@class='botao' and text()='VOLTAR']")
  #       voltar.click()
  #       found_period = (True, False)[last_period] # para execução se desejado for último período
  # driver.quit()