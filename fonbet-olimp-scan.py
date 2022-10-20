from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as WDE
import time
import datetime

# User-agent
user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"
print(user_agent)

# Логин
login_olimp = "######"
print("Логин: ", login_olimp)

login_fonbet = "########"

# Банк
bank = float(10)
print("Начальная ставка: ", str(bank))

# Ограничение по коэффициентам поиска
search_lower_coefficient = float(1.30)
print("Нижний коэффициент поиска", str(search_lower_coefficient))
search_upper_coefficient = float(1.44)
print("Верхний коэффициент поиска", str(search_upper_coefficient))

# Ограничение по разности
input_lower_difference = float(1.04)
print("Нижний порог разности: ", str(input_lower_difference))
input_upper_difference = float(7.00)
print("Верхний порог разности: ", str(input_upper_difference))

input_coefficient_exception = [1.85]
print("Коэффициенты исключения: ", str(input_coefficient_exception))

def scan():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(user_agent)
    chrome_options.add_argument("user-data-dir=C:/cookie/{}".format(login_fonbet))
    driver1 = webdriver.Chrome(options=chrome_options)
    driver1.get("https://www.fonbet.ru/live/table-tennis/")
    driver1.implicitly_wait(21600)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(user_agent)
    chrome_options.add_argument("user-data-dir=C:/cookie/{}".format(login_olimp))
    driver2 = webdriver.Chrome(options=chrome_options)
    driver2.get("https://www.olimp.bet/live/40")
    driver2.implicitly_wait(21600)

    quantity_rate = int(0)
    quantity_not_successful = int(0)

    # Поставленные
    staged_list = []

    status = True

    while status:

        try:

            driver2.implicitly_wait(0.2)

            # Проверка купона олимп
            try:

                driver2.find_element_by_xpath("//*[contains(@class,'basket active')]")

            except WDE:

                try:

                    print("Купон олимпа закрыт")
                    driver2.find_element_by_xpath("//*[contains(@class,'basket')]").click()

                except WDE:

                    status = True

            driver1.implicitly_wait(300)
            driver2.implicitly_wait(300)

            # Поиск и добавление названия события на фонбет             
            fon_match_name_elements = driver1.find_elements_by_xpath("//*[contains(@class,'table-component-factor-value_single--6nfox _compact')][1]/parent::div//*[@class='table-component-text--5BmeJ sport-event__name--HefZL _clickable--G5cwQ _event-view--7J8rE _compact--7BwYe']")

            # Добавление имени первого игрока фон
            fon_first_player_list = []
            element = True

            try:

                i = 0

                while element:

                    fon_first_player = str(fon_match_name_elements[i].text)
                    fon_first_player = str(fon_first_player.split("—")[0])
                    fon_first_player = fon_first_player.strip()
                    fon_first_player_list.append(fon_first_player)
                    i += 1

            except IndexError:

                element = False
                #fon_first_player_list.pop(0)
                i = 0

            # Добавление второго игрока фонбет
            fon_second_player_list = []
            element = True

            try:

                i = 0

                while element:

                    fon_second_player = str(fon_match_name_elements[i].text)
                    fon_second_player = str(fon_second_player.split("—")[1])
                    fon_second_player = fon_second_player.strip()
                    fon_second_player_list.append(fon_second_player)
                    i += 1

            except IndexError:

                element = False
                i = 0

            # Сформированный список имен игроков фонбет
            fon_formed_player = []
            fon_formed_player = fon_first_player_list + fon_second_player_list
            # print("___________________________________")
            # print("Фонбет")
            # print(fon_formed_player)

            # Поиск и добавление первого коэффициента фонбет
            fon_first_coefficient_elements = driver1.find_elements_by_xpath("//*[@class='table-component-text--5BmeJ sport-event__name--HefZL _clickable--G5cwQ _event-view--7J8rE _compact--7BwYe']/parent::div/parent::div/parent::div//*[contains(@class,'table-component-factor-value_single--6nfox _compact')][1]")
            fon_first_coefficient_list = []
            element = True

            try:

                i = 0

                while element:

                    fon_first_coefficient_list.append(fon_first_coefficient_elements[i].text)
                    i += 1

            except IndexError:

                element = False
                i = 0

            # Поиск и добавление второго коэффициента фонбет
            fon_second_coefficient_elements = driver1.find_elements_by_xpath("//*[@class='table-component-text--5BmeJ sport-event__name--HefZL _clickable--G5cwQ _event-view--7J8rE _compact--7BwYe']/parent::div/parent::div/parent::div//*[contains(@class,'table-component-factor-value_single--6nfox _compact')][2]")
            fon_second_coefficient_list = []
            element = True

            try:

                i = 0

                while element:

                    fon_second_coefficient_list.append(fon_second_coefficient_elements[i].text)
                    i += 1

            except IndexError:

                element = False
                i = 0

            # Сформированный список коэффициентов фонбет
            fon_formed_coefficient = fon_first_coefficient_list + fon_second_coefficient_list
            # print(fon_formed_coefficient)

            # Поиск и добавление имени события на олимп
            olimp_match_name_elements = driver2.find_elements_by_xpath("//*[contains(@class,'contained')][1]/parent::div/parent::div/parent::div//*[contains(@class,'colLeft')]//a")


            # Добавление имени первого игрока олимп
            olimp_first_player_list = []
            element = True

            try:

                i = 0

                while element:

                    olimp_first_player = str(olimp_match_name_elements[i].text)
                    olimp_first_player = str(olimp_first_player.split("-")[0])
                    olimp_first_player = olimp_first_player.replace(".", "")
                    olimp_first_player = olimp_first_player.strip()
                    olimp_first_player_list.append(olimp_first_player)
                    i += 1

            except IndexError:

                element = False
                i = 0

            # Добавление имени второго игрока олимп
            olimp_second_player_list = []
            element = True

            try:

                i = 0

                while element:

                    olimp_second_player = str(olimp_match_name_elements[i].text)
                    olimp_second_player = str(olimp_second_player.split("-")[1])
                    olimp_second_player = olimp_second_player.replace(".", "")
                    olimp_second_player = olimp_second_player.strip()
                    olimp_second_player_list.append(olimp_second_player)
                    i += 1

            except IndexError:

                element = False
                i = 0

            # Сформированный список имен игроков олимп
            olimp_formed_player = []
            olimp_formed_player = olimp_first_player_list + olimp_second_player_list
            # print("___________________________________")
            # print("Олимп")
            # print(olimp_formed_player)

            # Поиск и добавление первого коэффициента олимп
            olimp_first_coefficient_elements = driver2.find_elements_by_xpath("//*[contains(@class,'colLeft')]//a/parent::div/parent::div/parent::div//*[contains(@class,'contained')][1]")
            olimp_first_coefficient_list = []
            element = True

            try:

                i = 0

                while element:

                    olimp_first_coefficient_list.append(olimp_first_coefficient_elements[i].text)

                    i += 1

            except IndexError:

                element = False
                i = 0

            # Поиск и добавление второго коэффициента олимп
            olimp_second_coefficient_elements = driver2.find_elements_by_xpath("//*[contains(@class,'colLeft')]//a/parent::div/parent::div/parent::div//*[contains(@class,'contained')][2]")
            olimp_second_coefficient_list = []
            element = True

            try:

                i = 0

                while element:

                    olimp_second_coefficient_list.append(olimp_second_coefficient_elements[i].text)
                    i += 1

            except IndexError:

                element = False
                i = 0

            # Сформированный список коэффициентов олимп
            olimp_formed_coefficient = olimp_first_coefficient_list + olimp_second_coefficient_list
            # print(olimp_formed_coefficient)
            # print(len(olimp_formed_player))
            # print(len(olimp_formed_coefficient))

            enumeration = True

            olimp_index = 0

            # Обработка и простановка
            while enumeration:

                try:

                    fon_index = fon_formed_player.index(olimp_formed_player[olimp_index])
                    # print("Игрок: ", str(olimp_formed_player[olimp_index]), "состыкован")
                    fon_coefficient = float(fon_formed_coefficient[fon_index])
                    olimp_coefficient = float(olimp_formed_coefficient[olimp_index])
                    difference_rate_subtraction = olimp_coefficient - fon_coefficient
                    difference_rate_division = olimp_coefficient / fon_coefficient

                    # Ограничение по коэффициентам разности
                    if input_lower_difference <= difference_rate_division <= input_upper_difference:

                        # Ограничение коэффициента поиска
                        if search_lower_coefficient <= olimp_coefficient <= search_upper_coefficient:

                            # Проверка на коэффициенты исключения
                            if olimp_coefficient not in input_coefficient_exception:

                                # Проверка коэффициента фонбет
                                driver1.implicitly_wait(0.2)
                                staged_event_fonbet = driver1.find_element_by_xpath("//*[contains(text(),'" + str(olimp_formed_player[olimp_index]) + "')]")
                                staged_event_fonbet = str(staged_event_fonbet.text)
                                staged_event_fonbet = staged_event_fonbet.strip()
                                staged_event_fonbet_first_player = staged_event_fonbet.split("—")[0]
                                staged_event_fonbet_first_player = staged_event_fonbet_first_player.strip()
                                staged_event_fonbet_second_player = staged_event_fonbet.split("—")[1]
                                staged_event_fonbet_second_player = staged_event_fonbet_second_player.strip()

                                if olimp_formed_player[olimp_index] == staged_event_fonbet_first_player:

                                    index_coefficient = 1
                                    #print("Первый Игрок")

                                if olimp_formed_player[olimp_index] == staged_event_fonbet_second_player:

                                    index_coefficient = 2
                                    #print("Второй Игрок")

                                coefficient_checking = driver1.find_element_by_xpath("//*[contains(text(),'" + str(olimp_formed_player[olimp_index]) + "')]/parent::div/parent::div/parent::div//*[contains(@class,'table-component-factor-value_single--6nfox _compact')][" + str(index_coefficient) + "]")
                                coefficient_checking = float(coefficient_checking.text)

                                if coefficient_checking <= fon_coefficient:

                                    # Поиск события, для добавления в список поставленных
                                    driver2.implicitly_wait(0.2)
                                    staged_event = driver2.find_element_by_xpath("//*[contains(text(),'" + str(olimp_formed_player[olimp_index]) + "')]")
                                    staged_event = str(staged_event.text)

                                    # Проверка на поставленные ставки
                                    if staged_event not in staged_list:

                                        # Попытка поиска кнопки коэффициента
                                        try:
                                            driver2.implicitly_wait(0.2)
                                            coefficient_player = olimp_formed_coefficient[olimp_index]
                                            coefficient_player = float(coefficient_player)
                                            coefficient_button = driver2.find_element_by_xpath("//*[contains(text(),'" +str(olimp_formed_player[olimp_index]) + "')]/parent::div/parent::div/parent::div//*[contains(text(),'" + str(coefficient_player) +"')]")
                                            coefficient_button.click()

                                            # Попытка проверка на тип матча
                                            try:

                                                driver2.implicitly_wait(2)

                                                if driver2.find_element_by_xpath("//*[contains(@class,'column')]//*[contains(text(),'Основные. По')]"):

                                                    # Проверка коэффициента из купона
                                                    coupon_coefficient = driver2.find_element_by_xpath("//*[contains(@class,'flex-column')]//*[contains(@class,'flex-row')]//span")
                                                    coupon_coefficient = str(coupon_coefficient.text)
                                                    coupon_coefficient = float(coupon_coefficient)

                                                    if coupon_coefficient >= coefficient_player:

                                                        rate = float(bank * difference_rate_division)

                                                        rate = int(rate)

                                                        # Попытка простановки
                                                        try:

                                                            enumeration = False
                                                            print("Попытка простановки: ", str(rate))
                                                            panel_element = driver2.find_element_by_xpath("//*[@placeholder='Введите сумму']")
                                                            panel_element.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b")
                                                            panel_element.send_keys(str(rate))
                                                            driver2.find_element_by_xpath("//*[contains(text(),'Сделать ставку')]").click()
                                                            driver2.implicitly_wait(18)

                                                            if driver2.find_element_by_xpath("//*[contains(text(),'Ваша ставка успешно принята')]"):

                                                                print("___________________________________")
                                                                print("Поставленно: ", rate, "на коэффициент: ", coefficient_player)
                                                                print("Игрок: ", str(olimp_formed_player[olimp_index]))
                                                                print("Коэффициент Фонбета: ", str(coefficient_checking))
                                                                print("Коэфццициент Олимпа: ", str(olimp_formed_coefficient[olimp_index]))
                                                                print("Разность: ", str(difference_rate_subtraction))
                                                                print("Разность деления: ", str(difference_rate_division))
                 
                                                                # Добавление события в список поставленных
                                                                staged_list.append(staged_event)
                                                                print("Поставленные: ", str(staged_list))

                                                                # Запись статистики
                                                                file = open("file.txt", "a")
                                                                file.write(str(rate) + " ")
                                                                file = open("file.txt", "a")
                                                                file.write(str(olimp_formed_coefficient[olimp_index]) + " ")
                                                                file = open("file.txt", "a")
                                                                file.write(str(round(difference_rate_division, 2)) + "\n")

                                                                quantity_rate += 1
                                                                print("Количество ставок: ", str(quantity_rate))
                                                                
                                                        # Попытка простановки
                                                        except WDE:

                                                            enumeration = False
                                                            quantity_not_successful += 1
                                                            print("Количество не удачных попыток: ", str(quantity_not_successful))
                                                            driver2.execute_script("window.scrollTo(0, 0)")
                                                            driver2.implicitly_wait(1)

                                                            # Закрытие открытых купонов
                                                            try:

                                                                driver2.find_element_by_xpath("//*[text()='Очистить все']").click()

                                                            except WDE:

                                                                status = True
            
                                                    # Проверка коэффициента из купона
                                                    else:

                                                        print("Коэффициент Олимпа изменился")
                                                        olimp_index += 1
                                                        driver2.execute_script("window.scrollTo(0, 0)")
                                                        driver2.implicitly_wait(1)

                                                        # Закрытие открытых купонов
                                                        try:

                                                            driver2.find_element_by_xpath("//*[text()='Очистить все']").click()

                                                        except WDE:

                                                            status = True

                                            # Попытка проверка на тип матча
                                            except WDE:

                                                print("Ошибка WDE: Проверка на тип матча")
                                                olimp_index += 1 
                                                driver2.execute_script("window.scrollTo(0, 0)")
                                                driver2.implicitly_wait(1)

                                                # Закрытие открытых купонов
                                                try:

                                                    driver2.find_element_by_xpath("//*[text()='Очистить все']").click()

                                                except WDE:

                                                    status = True

                                        # Попытка поиска кнопки коэффициента
                                        except WDE:

                                            print("Ошибка WDE: Поиска кнопки коэффициента")
                                            driver2.execute_script("window.scrollTo(0, 0)")
                                            olimp_index += 1

                                    # Проверка на поставленные ставки
                                    else:

                                        #print("На найденное событие уже ставили")
                                        olimp_index += 1

                                # Проверка коэффициент фонбета
                                else:

                                    print("Коэффициент Фонбета изменился")
                                    olimp_index += 1

                            # Проверка на коэффициенты исключения
                            else:

                                print("Найденный коэффициент в списке исключения")
                                olimp_index += 1
                                
                        # Ограничение коэффициента поиска
                        else:

                            #print("Найденный коэффициент: не подходит условиям поиска")
                            olimp_index += 1

                    # Ограничение коэффициента разности
                    else:

                        #print("Найденный коэффициент: не подходит условиям разности")
                        olimp_index += 1

                except ValueError:

                    olimp_index += 1

                except IndexError:

                    #print("Все игроки из списка сверены")
                    enumeration = False

        # Ошибка WDE главного цикла
        except WDE:

            print("Ошибка WDE: Главного цикла")
            enumeration = False
            driver2.implicitly_wait(1)

            # Закрытие открытых купонов
            try:

                driver2.find_element_by_xpath("//*[text()='Очистить все']").click()

            except WDE:

                status = True

            driver1.get("https://www.fonbet.ru/live/table-tennis/")
            driver2.get("https://www.olimp.bet/live/40")

        except AttributeError:

            status = True

        except IndexError:

            print("Ошибка IndexError: Главного цикла")

scan()
