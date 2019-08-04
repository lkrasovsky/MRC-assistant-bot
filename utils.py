import os
import shutil
import tempfile

import PyPDF2
import telebot
from bs4 import BeautifulSoup as bs
from pdf2image import convert_from_path
from telebot import types

import constants


def create_groups_keyboard():
    types = telebot.types
    groups_keyboard = types.ReplyKeyboardMarkup()

    groups_keyboard.row("8к1191", "8к1591", "8к1391")
    groups_keyboard.row("8к3291", "8к3791")
    groups_keyboard.row("8к2491", "8к2492", "8к2493")
    groups_keyboard.row("8к1111", "8к2411")

    groups_keyboard.row("7к1191", "7к1591", "7к1391")
    groups_keyboard.row("7к3291", "7к3791")
    groups_keyboard.row("7к2491", "7к2492", "7к2493")
    groups_keyboard.row("7к1111", "7к2411")

    groups_keyboard.row("61191", "61591", "61391")
    groups_keyboard.row("63291", "63791")
    groups_keyboard.row("62491", "62492", "62493")

    return groups_keyboard


def create_menu_keyboard():
    menu_keyboard = types.ReplyKeyboardMarkup()

    menu_keyboard.row("Расписание 📋")
    menu_keyboard.row("Номера преподов ☎")
    menu_keyboard.row("Сайт 🌎")
    menu_keyboard.row("Изменить группу")
    menu_keyboard.row("О боте ❔", "Автор 🙇🏼")

    return menu_keyboard


def go_to_website():
    url = "http://www.mrk-bsuir.by/ru"
    request = constants.session.get(url, headers=constants.headers)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        return soup
    else:
        return Exception


def get_schedule():
    download_url = go_to_website().find('a', attrs={'id': 'rasp'})['href']

    rasp_dir = "rasp"

    # save rasp.pdf
    response = constants.session.get(download_url, headers=constants.headers)
    try:
        shutil.rmtree(rasp_dir)
    except:
        pass

    try:
        os.mkdir(rasp_dir)
    except FileExistsError:
        pass
    path = rasp_dir + "/rasp.pdf"
    with open(path, 'wb') as file:
        file.write(response.content)

    # convert pages to .jpg
    pdf = PyPDF2.PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = 'page_{}.jpg'.format(page + 1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        with tempfile.TemporaryDirectory() as path:

            images_from_path = convert_from_path(output_filename, output_folder=path)

        base_filename = os.path.splitext(os.path.basename(output_filename))[0] + '.jpg'

        for page in images_from_path:
            page.save(os.path.join(rasp_dir + "/", base_filename), 'JPEG')

        os.remove(output_filename)
    os.remove(rasp_dir + '/rasp.pdf')


def get_page(message):
    global page
    if message == "8к1191" or message == "8к1591" or message == "8к1391" or message == "8к1111" or \
            message == "7к1191" or message == "7к1591" or message == "7к1391" or message == "61391":
        page = "1"
    elif message == "8к2491" or message == "8к2492" or message == "8к2493" or message == "8к2491" or \
            message == "7к2492" or message == "7к2493" or message == "8к2411":
        page = "2"
    elif message == "8к3791" or message == "8к3291" or message == "7к3791" or message == "7к3291":
        page = "3"
    elif message == "7к1111" or message == "61191" or message == "61591":
        page = "4"
    elif message == "7к2411" or message == "62491" or message == "62492" or message == "62493":
        page = "5"
    elif message == "63791" or message == "63291":
        page = "6"

    try:
        return page
    except NameError:
        return 0


def set_users_page(id, message):
    filename = str("users/" + id + "_rasp_page.txt")
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    try:
        os.mknod(filename)
    except FileExistsError:
        pass

    page = get_page(message)

    file = open(filename, 'r+')
    if page != 0:
        file.write("" + page)
        file.close()
        file = open(filename, 'r+')
        file.read()
        file.close()
        return True
    else:
        return False
