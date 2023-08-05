import sys
import click
from meu_contracheque.time_reader import find_last_period
from meu_contracheque.scraping_mg import (scraping_process_begin,
                                         scraping_login_process,
                                         scraping_full_process,
                                         csv_register,
                                         clean_full_process,
                                         clean_process)


def scraping_mg_last_period(masp, senha, headless, pdf):
  """
  Função responsável pela busca de informações do último contracheque dos servidores do Estado de Minas Gerais.
  Parâmetros:
  -------
  masp: string
    Masp do servidor do Estado de Minas Gerais
  senha: string
    Senha de acesso ao Portal do servidor do Estado de Minas Gerais
  Retorna:
  -------
  Arquivo "contracheques.csv" atualizado com as informações do último contracheque disponível no Portal do Servidor.
  """
  try:
    click.echo('Iniciando processo de extração do último contracheque...')
    clean_full_process()
    start = scraping_process_begin(headless)
    driver = start[0]
    period = start[1]
    scraping_login_process(driver, period, masp, senha)
    scraping_full_process(driver, period, headless)
    # csv_register()
    # clean_process()
    click.echo('Processo de extração do último contracheque finalizado com sucesso.')
  except:
    click.echo('Não foi possível finalizar o processo de busca do contracheque mais recente.')
    sys.exit(1)

@click.command(name='mais-recente')
@click.pass_context
def scraping_mg_last_period_cli(ctx):
  """
  Função CLI responsável pela busca de informações do último contracheque dos servidores do Estado de Minas Gerais.
  Por padrão, função buscará masp e senha nas variáveis de ambiente MASP e PORTAL_PWD cadastradas na máquina ou
  em arquivo .env.
  Parâmetros:
  ----------
  masp: string
      Masp do servidor do Estado de Minas Gerais
    senha: string
      Senha de acesso ao Portal do servidor do Estado de Minas Gerais
    Retorna:
    -------
    Arquivo "contracheques.csv" atualizado com as informações do último contracheque disponível no Portal do Servidor.
  """
  scraping_mg_last_period(ctx.obj['masp'], ctx.obj['senha'], ctx.obj['headless'], ctx.obj['pdf'])
