from core.models import Partner, Score
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
import email.message
import time
from dotenv import load_dotenv
import os
from django.utils import timezone

def get_score_daily_job():
    driver = webdriver.Chrome()

    driver.get("https://www.livelo.com.br/ganhe-pontos-compre-e-pontue")

    while len(driver.find_elements(By.XPATH, '//*[@id="div-cardsParity"]')) < 1:
        time.sleep(1)

    partner_div = driver.find_element(By.XPATH, '//*[@id="div-cardsParity"]')
    partners = partner_div.find_elements(By.CLASS_NAME, 'parity__card')

    for partner in partners:
        score = None
        score_club = None
        infos = partner.find_element(By.CLASS_NAME, 'parity__card--info')
        try:
            info_value = infos.find_element(By.CLASS_NAME, 'info__value')
            info_club = infos.find_element(By.CLASS_NAME, 'info__club')
            score = parse_score(info_value.find_element(By.CLASS_NAME, 'parity__card--info__text-extended').text, 'default')
            score_club = parse_score(info_club.find_element(By.CLASS_NAME, 'info__club-text').text, 'livelo_club')
        except:
            print('Não tem promoção para o clube')
            try:
                score = int(partner.find_element(By.CSS_SELECTOR, '#div-parityInfo > div.info__value > span:nth-child(4)').text)
                score_club = score
            except:
                print('Seletor não encontrado')
        finally:
            button = partner.find_element(By.CLASS_NAME, 'button__knowmore')
            link = button.find_element(By.TAG_NAME, 'a').get_attribute('href')
            name = link[61:].split('/')[0]
            partner_id = get_partner_id(name)
            id =  partner_id if partner_id else create_partner(name, link)
            create_score(id, score_club, score)
    driver.quit()

def parse_score(text, type):
    if type == 'livelo_club':
        # Exemplo:
        # R$ 1 até 10 pontos
        score = text.split()[3]
    else:
        # Exemplo:
        # ou até 8 Pontos Livelo
        score = text.split()[2]
    return int(score)

def get_partner_id(name):
    try:
        return Partner.objects.get(name = name).id
    except:
        return None

def create_partner(name, link):
    return Partner.objects.create(name=name,
                                  link=link).id
     

def create_score(partner_id, score_club, score):
    Score.objects.create(partner_id=partner_id,
                         score_club=score_club,
                         score=score).id

def send_promotions_notifications():
    today = timezone.now().date()
    scores_today = Score.objects.filter(created_at__date=today)
    for user in User.objects.all:
        followed_partners_ids = user.followed_partners.values_list('id', flat=True)
        promotions_to_send = scores_today.filter(partner_id__in=followed_partners_ids).order_by('-score')
        email_message = create_message(user.username, promotions_to_send)
        send_email(email_message, user.email)

def create_message(username, data):
    email_body = f"""
    <h3>Ei, {username}, essas são as promoções de hoje!</h3>
    """
    for score in data:
        email_body += f"<p><b>{score.partner.name}</b> - {score.score}</p>"
    return email_body

def send_email(message, remittee):
    # Load environment variables from .env file
    load_dotenv()
    msg = email.message.Message()
    msg['Subject'] = "Veja as pontuações de hoje para suas lojas favoritas!"
    msg['From'] = os.getenv('EMAIL')
    msg['To'] = remittee
    password = os.getenv('PASSWORD')
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(message)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')

