import logging
import re
import os
import paramiko
import psycopg2

from dotenv import load_dotenv
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
load_dotenv()
token = os.getenv('TOKEN')
host = os.getenv('RM_HOST')
port = os.getenv('RM_PORT')
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
database = os.getenv('DB_DATABASE')
# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def ssh_connect(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username, password=password)
    return ssh

def execute_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    return output

def get_release(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        release_info = execute_command(ssh, "lsb_release -a")
        update.message.reply_text(release_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_uname(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        uname_info = execute_command(ssh, 'uname -a')
        update.message.reply_text(uname_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_uptime(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        uptime_info = execute_command(ssh, "uptime")
        update.message.reply_text(uptime_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_df(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        df_info = execute_command(ssh, 'df')
        update.message.reply_text(df_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")
def get_free(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        free_info = execute_command(ssh, 'free')
        update.message.reply_text(free_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_mpstat(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        mpstat_info = execute_command(ssh, 'mpstat')
        update.message.reply_text(mpstat_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")
def get_w(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        w_info = execute_command(ssh, 'w')
        update.message.reply_text(w_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_auths(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        auths_info = execute_command(ssh, 'last -n 10')
        update.message.reply_text(auths_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_critical(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        critical_info = execute_command(ssh, 'dmesg | grep -i "error" | tail -n 5')
        update.message.reply_text(critical_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_critical(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        critical_info = execute_command(ssh, 'dmesg | grep -i "error" | tail -n 5')
        update.message.reply_text(critical_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")
def send_long_message(update, text):
    max_len = 4096
    sms_bot = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    for chunk in sms_bot:
        update.message.reply_text(chunk)

def get_ps(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        ps_info = execute_command(ssh, 'ps aux')
        send_long_message(update, ps_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")
def get_ss(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        ss_info = execute_command(ssh, 'netstat -tulp')
        send_long_message(update, ss_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")
def get_apt_list(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        args = context.args

        if args:
            package_name = " ".join(args)
            command = f"dpkg -l | grep {package_name}"
            package_info = execute_command(ssh, command)
            if package_info:
                send_long_message(update, package_info)
            else:
                update.message.reply_text(f"Пакет '{package_name}' не найден")
        else:
            command = "dpkg -l"
            apt_list = execute_command(ssh, command)
            send_long_message(update, apt_list)

        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")
def get_services(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        services_info = execute_command(ssh, 'systemctl list-units --type=service')
        send_long_message(update, services_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_repl_logs(update: Update, context):
    try:
        ssh = ssh_connect(host, port, username, password)
        log_info = execute_command(ssh, 'cat /var/log/postgresql/postgresql-15-main.log | grep replication')
        send_long_message(update, log_info)
        ssh.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_emails(update: Update, context):
    try:
        db_connection = psycopg2.connect(user=db_user,
                                         dbname=database,
                                         password=db_password,
                                         host=db_host,
                                         port=db_port)
        cursor = db_connection.cursor()
        cursor.execute("SELECT email FROM emails;")
        emails = cursor.fetchall()
        if emails:
            email_list = '\n'.join([email[0] for email in emails])
            update.message.reply_text(email_list)
        else:
            update.message.reply_text("В базе нет email-адресов")
        cursor.close()
        db_connection.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def get_phone_numbers(update: Update, context):
    try:
        db_connection = psycopg2.connect(user=db_user,
                                         dbname=database,
                                         password=db_password,
                                         host=db_host,
                                         port=db_port)
        cursor = db_connection.cursor()
        cursor.execute("SELECT phone_number FROM phone_nubers;")
        numbers = cursor.fetchall()
        if numbers:
            number_list = '\n'.join([number[0] for number in numbers])
            update.message.reply_text(number_list)
        else:
            update.message.reply_text("В базе нет телефонный номеров")
        cursor.close()
        db_connection.close()
    except Exception as e:
        update.message.reply_text(f"Ошибка: {e}")

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Help!')


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_numbers'

def findEmailaCommand(update: Update, context):
    update.message.reply_text('Введите текст для поискат адресов (email)')

    return 'find_email'

def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки его сложности')

    return 'verify_password'

def find_phone_numbers(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(?:\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}')  # формат 8 (000) 000-00-00

    phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов

    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return  # Завершаем выполнение функции

    phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'  # Записываем очередной номер

    update.message.reply_text(phoneNumbers)# Отправляем сообщение пользователю
    context.user_data['phone_nubers'] = phoneNumberList
    keyboard = [['Да', 'Нет']]
    update.message.reply_text("Хотите записать найденные номера в БД?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return 'recordPhoneNumbers'  # Завершаем работу обработчика диалога

def recordPhoneNumbers(update: Update, context):
    response = update.message.text

    phoneNumberList = context.user_data.get('phone_nubers', [])
    if response == 'Да':
        try:
            db_connection = psycopg2.connect(user=db_user,
                                             dbname=database,
                                             password=db_password,
                                             host=db_host,
                                             port=db_port)
            coursor = db_connection.cursor()

            for phone_number in phoneNumberList:
                coursor.execute("INSERT INTO phone_nubers (phone_number) values (%s);", (phone_number,))

            db_connection.commit()
            update.message.reply_text("Телефонные номера записаны в БД")

            coursor.close()
            db_connection.close()
        except Exception as e:
            update.message.reply_text(f"Ошибка при записи в БД: {e}")
    else:
        update.message.reply_text("Телефонные номера не записаны в БД")
    return ConversationHandler.END
def find_email(update: Update, context):
    user_input = update.message.text

    emailReg = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-z0-9.-]+\.[a-zA-Z]{2,}')
    emailList = emailReg.findall(user_input)

    if not emailList:
        update.message.reply_text('Email-адресов не найдено')
        return ConversationHandler.END

    emails = ''
    for i in range(len(emailList)):
        emails += f'{i + 1}. {emailList[i]}\n'

    update.message.reply_text(emails)
    context.user_data['email'] = emailList
    keyboard = [['Да', 'Нет']]
    update.message.reply_text("Хотите записать найденные email-адреса в БД?",
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return 'recordEmails'  # Завершаем работу обработчика диалога
def recordEmails(update: Update, context):
    response = update.message.text

    emailList = context.user_data.get('email', [])
    if response == 'Да':
        try:
            db_connection = psycopg2.connect(user=db_user,
                                             dbname=database,
                                             password=db_password,
                                             host=db_host,
                                             port=db_port)
            coursor = db_connection.cursor()

            for email in emailList:
                coursor.execute("INSERT INTO emails (email) values (%s);", (email,))

            db_connection.commit()
            update.message.reply_text("Email-адреса записаны в БД")

            coursor.close()
            db_connection.close()
        except Exception as e:
            update.message.reply_text(f"Ошибка при записи в БД: {e}")
    else:
        update.message.reply_text("Email-адреса не записаны в БД")
    return ConversationHandler.END

def verify_password(update: Update, context):
    user_input = update.message.text

    passwordRe = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#S%^$*()])[A-Za-z\d!@#S%^$*()]{8,}$')
    if passwordRe.match(user_input):
        update.message.reply_text('Пароль сложный')
    else:
        update.message.reply_text('Пароль простой')
    return ConversationHandler.END
def echo(update: Update, context):
    update.message.reply_text(update.message.text)


def main():
    updater = Updater(token, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_numbers', findPhoneNumbersCommand)],
        states={
            'find_phone_numbers': [MessageHandler(Filters.text & ~Filters.command, find_phone_numbers)],
            'recordPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, recordPhoneNumbers)]
        },
        fallbacks=[]
    )
    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailaCommand)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, find_email)],
            'recordEmails': [MessageHandler(Filters.text & ~Filters.command, recordEmails)]
        },
        fallbacks=[]
    )
    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_w", get_w))
    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))
    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(CommandHandler("get_apt_list", get_apt_list))
    dp.add_handler(CommandHandler("get_services", get_services))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))
    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_phone_numbers",get_phone_numbers))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerVerifyPassword)

    # Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
