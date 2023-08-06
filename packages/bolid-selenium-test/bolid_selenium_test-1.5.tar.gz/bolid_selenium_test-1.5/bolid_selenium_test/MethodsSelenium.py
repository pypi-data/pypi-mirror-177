# -*- coding: utf-8 -*-
import time

from selenium.common.exceptions import *
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Methods:
    def __init__(self, app):
        self.app = app

    """
    Проверка перехода на нужный endpoint
    :Args:
        - host: хост приложения пример: 'http://192.168.22.130:8080'
        - endpoint: пример: '/partitions'
        - locator: локатор Xpath пример: '//button[.="Объект"]'
    """

    def pageEndpoint(self, host: str, endpoint: str, locator: str):
        wd = self.app.wd
        if wd.current_url == host + endpoint:
            pass
        else:
            self.click((By.XPATH, locator))
            time.sleep(0.1)
            assert str(wd.current_url) == str(host + endpoint), f" \nОшибка перехода на сраницу! " \
                                                                f"\nОжидаемый адрес:'{host + endpoint}'" \
                                                                f"\nФактический адрес:'{wd.current_url}'"

    """
    Проверка поля ввода на валидацию
    :Args:
        - input: данные которые вводятся в поле
        - expected: данные которые мы ожидаем увидеть
        - locator: локатор Xpath пример: '//button[.="Объект"]'
    """

    def assertEqual(self, input: str, expected: str, locator: str):
        self.inputValues(input, locator)
        self.assertValues(expected, locator)

    """
    Метод ввода значений в поле
    :Args:
        - input: данные которые вводятся в поле
        - locator: локатор Xpath пример: '//button[.="Объект"]'
    """

    def inputValues(self, value: str, locator: str):
        try:
            wd = self.app.wd
            element = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((By.XPATH, ('%s' % locator))))
            element.clear()
            element.send_keys(value)
            # element.click()
        except Exception as e:
            assert e == TimeoutException, f"Ошибка локатор поля ввода '{locator}' - не найден"

    """
    Метод проверки введенных значений
    :Args:
        - value: данные которые ожидаются
        - locator: локатор Xpath пример: '//button[.="Объект"]'
    """

    def assertValues(self, value: str, locator: str):
        try:
            wd = self.app.wd
            element = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((By.XPATH, ('%s' % locator))))
            values = element.get_attribute('value')
            assert str(value) == str(
                values), f"\nОжидаемый результат ввода = '{value}'\nФактическое значение в поле = '{values}'"
        except TimeoutException:
            print(f"Ошибка при проверке локатор поля ввода '{locator}' - не найден")

    """
    Метод получения текста
    :Args:
        - locator: локатор элемента на странице из которого необходимо получить текс Xpath пример: '//button[.="Объект"]'
    """

    def getText(self, locator: str):
        wd = self.app.wd
        return WebDriverWait(wd, 10).until(EC.visibility_of_element_located((By.XPATH, ('%s' % locator)))).text

    """
    Метод проверки текста на странице
    :Args:
        - list_text: список необходимого текста пример '['tex1', 'text2'...]'
        - locator: локатор Xpath пример: '//button[.="Объект"]'
    """

    def assertTextOnPage(self, locator: str, list_text: str):
        info_element = self.getText(locator)
        for x in list_text:
            assert x in info_element, \
                f"\n----------------------\n" \
                f"Ошибка!\nОжидаемый текст: ***{x}*** - отсутствует на странице!\n" \
                f"\n----------------------\n" \
                f"Фактический текст на странице:\n{info_element}" \
                f"\n----------------------"

    """
    Метод проверки отсутствия текста на странице
    :Args:
        - list_text: список необходимого текста пример '['tex1', 'text2'...]'
        - locator: локатор Xpath пример: '//button[.="Объект"]'
    """

    def assertotMissingTextOnPage(self, locator: str, list_text: str):
        info_element = self.getText(locator)
        for x in list_text:
            assert x not in info_element, \
                f"\n----------------------\n" \
                f"Ошибка!\nОжидаемый текст: ***{x}*** - отсутствует на странице!\n" \
                f"\n----------------------\n" \
                f"Фактический текст на странице:\n{info_element}" \
                f"\n----------------------"

    """
    Метод клика по элементу
    :Args:
        - locator: локатор элемента передается с необходимым селектором (xpath/css/id/name...) 
        пример (By.XPATH, '//button[.="Объект"]')
    """

    def click(self, locator: str):
        try:
            wd = self.app.wd
            element = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((locator)))
            element.click()
        except Exception as e:
            assert e == TimeoutException, f"Ошибка! Нет возможности кликнуть по локатору: '{locator}'"

    """
    Метод получения длины необходимых элементов на странице 
    :Args:
        - locator: локатор Xpath пример: '//button[.="Объект"]'
        метод вернет количество найденных элементов по лакатору
    """

    def getElementsLen(self, locator: str):
        wd = self.app.wd
        return len(wd.find_elements(By.XPATH, locator))

    """
    Проверка соответствия элемента ожидаемому классу
    :Args:
        - locator: локатор Xpath пример: '//button[.="Объект"]'
        - className: ожидаемый класс
    """

    def assertStatusElementByClass(self, locator: str, className: str):
        wd = self.app.wd
        element = WebDriverWait(wd, 20).until(
            EC.element_to_be_clickable((By.XPATH, locator)))
        class_button = element.get_property("className")
        assert str(
            class_button) == className, f"Ошибка ожидаемого класса!\nФактический класс: '{class_button}'"

    """
    Метод получения Property
    :Args:
        - locator: локатор Xpath пример: '//button[.="Объект"]'
        - property: необходимый property
        метод вернет запрашиваемые данные по ключу property
    """

    def getProperty(self, locator: str, property: str):
        try:
            wd = self.app.wd
            element = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((By.XPATH, locator)))
            return element.get_property(property)
        except Exception as e:
            assert e == TimeoutException, f"Ошибка! Нет возможности кликнуть по локатору: '{locator}'"

    """
    Метод выборв чек-бокса
    :Args:
        - position: указывается положение чекбокса 
            пример: ON(включение) или OFF(выключение)
        - click: локатор элемента по xpath по которому происходит клик по чек-боксу
            пример: /html/body//label/span
        - status: локатор элемента по xpath по которому происходит выявление текущего статуса
            пример: /html/body//label/input
    """

    def checkBox(self, position: str, click: str, status: str):
        try:
            wd = self.app.wd
            element = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((By.XPATH, click)))
            selected = wd.find_element(By.XPATH, status)
            if position == "ON":
                if selected.is_selected() == True:
                    pass
                else:
                    element.click()
            elif position == "OFF":
                if selected.is_selected() == False:
                    pass
                else:
                    element.click()
        except Exception as exc:
            assert exc == TimeoutException, f"Ошибка! локатор чекбокса: '{click}' не найден"

    """
    Метод проверки положения чек-бокса
    :Args:
        - position: указывается положение чекбокса которое ожидаем
            пример: ON(включен) или OFF(выключен)
        - status: локатор элемента по xpath по которому происходит выявление текущего статуса
            пример: /html/body//label/input
    """

    def assertCheckBox(self, position: str, status: str):
        wd = self.app.wd
        selected = wd.find_element(By.XPATH, status)
        if position == "ON":
            status_check_box = True
        if position == "OFF":
            status_check_box = False
        if selected.is_selected() == False:
            result = 'Не включается'
        if selected.is_selected() == True:
            result = 'Не выключается'
        assert status_check_box == selected.is_selected(), f"Ошибка! Чекбокс: {result}"

    """
     Метод получения статуса кнопки
     :Args:
        - locator: локатор Xpath пример: '//button[.="Объект"]'
        данный метод возвращает статус атрибута 'disabled' - True или False
     """

    def attributeStatusButton(self, locator: str):
        wd = self.app.wd
        selected = wd.find_element(By.XPATH, locator)
        return selected.get_attribute('disabled')

    """
    Метод выбора позиции из выпадающего списка
    :Args:
        - button: указывается локатор кнопки раскрытия списка xpath 
        - position: указывается локатор xpath необходимой позиции для выбора
        В данном методе позиция для выбора указывается по индексу для удобства перебора большого количество значений
    """

    def selectDropdownList(self, button: str, position: str):
        try:
            self.app.method.click((By.XPATH, button))
            self.app.method.click((By.XPATH, position))
        except TimeoutException as exc:
            assert exc == TimeoutException, f"Ошибка!!! Локатор выпадающего списка не найден"

    """
    Метод выбора позиции из выпадающего списка с чек-боксом
    :Args:
        - button: указывается локатор кнопки раскрытия списка xpath 
        - position: указывается локатор xpath необходимой позиции для выбора
        - status: локатор элемента по xpath по которому происходит выявление текущего статуса чек-бокса
        Данный метод раскрывает выпадающий список выбирает необходимый элемент и включает чекбокс рядом с этим элементом
    """

    def selectDropdownListCheckBox(self, button: str, position: str, status: str):
        try:
            wd = self.app.wd
            self.app.method.click((By.XPATH, button))
            selected = wd.find_element(By.XPATH, status)
            if selected.is_selected() == False:
                self.app.method.click((By.XPATH, position))
        except TimeoutException as exc:
            assert exc == TimeoutException, f"Ошибка!!! Локатор выпадающего списка не найден"

    """
    Метод выбора позиции из выпадающего списка по имени
    :Args:
        - button: указывается локатор кнопки раскрытия списка xpath 
        - name: указывается название необходимой позиции
        выбор происходит по xpath
    """

    def selectDropdownListByName(self, button: str, name: str):
        try:
            self.app.method.click((By.XPATH, button))
            self.app.method.click((By.XPATH, f'/html/body//div[@class="option"][.="{name}"]'))
        except TimeoutException as exc:
            assert exc == TimeoutException, f"Ошибка!!! Локатор выпадающего списка не найден"

    """
     Метод проверки выбранной позиции в выпадающем списке
     :Args:
         - values: указывается ожидаемый текст
         - locator: локатор выпадающего списка xpath пример: '//button[.="Объект"]'
     """

    def assertSelectionDropdownList(self, values: str, locator: str):
        try:
            wd = self.app.wd
            element = wd.find_element(By.XPATH, locator).get_property("textContent")
            assert str(element) == str(
                values), f"\nОжидаемое значение в выпадающем списке: '{values}'\nФактическое: '{element}'"
        except TimeoutException as exc:
            assert exc == TimeoutException, f"Ошибка локатор выпадающего списка '{locator}' - не найден"

    """
     Метод проверки выбранной позиции в выпадающем списке через с чек-боксом
     :Args:
         - values: указывается ожидаемый текст
         - locator: локатор выпадающего списка xpath пример: '//button[.="Объект"]'
     """

    def assertSelectionDropdownListCheckBox(self, values: str, locator: str):
        try:
            wd = self.app.wd
            element = wd.find_element(By.XPATH, locator).get_property("outerText")
            assert str(values) in str(
                element), f"\nОжидаемое значение в выпадающем списке: '{values}'\nФактическое: '{element}'"
        except TimeoutException as exc:
            assert exc == TimeoutException, f"Ошибка локатор выпадающего списка '{locator}' - не найден"

    """
     Метод выбора виджета ползунка
     :Args:
         - volum: указывается необходимое положение виджета
         - locator: локатор виджета ползунка xpath пример: '//button[.="Объект"]'
     """

    def sliderWidget(self, volum: str, locator: str):
        try:
            wd = self.app.wd
            slider = wd.find_element(By.XPATH, locator)
            wd.execute_script("arguments[0].value = arguments[1]", slider, "%s" % volum)
        except Exception as exc:
            assert exc == TimeoutException, f"Ошибка локатор виджета {locator} ползунка не найден"

    """
     Метод проверки виджета ползунка
     :Args:
         - volum: указывается ожидаемое положение виджета
         - locator: локатор виджета ползунка xpath пример: '//button[.="Объект"]'
     """

    def assertSliderWidget(self, volum: str, locator: str):
        wd = self.app.wd
        element = wd.find_element(By.XPATH, locator).get_property("value")
        assert int(element) == int(
            volum), f"\n***Неверное положение виджета ползунка!***\nОжидаемое:'{volum}'\nФактическое:'{element}'"

    """
     Метод проверки текста в всплывающей подсказке
     :Args:
         - text: указывается ожидаемый текст
         по умолчанию локатор поиска элемента в котором происходит поиск = '//*[@class="b-tooltip-text"]'
     """

    def assertTooltipText(self, text: str):
        locator = '//*[@class="b-tooltip-text"]'
        actual_text = self.getText(locator)
        assert str(text) == str(
            actual_text), f"\nОшибка при проверке всплывающей подсказки!\nОжидаемый текст: '{text}'\nФактический текст: '{actual_text}'"

    """
     Метод задержки элемента в фокусе
     :Args:
        - locator: локатор виджета ползунка xpath пример: '//button[.="Объект"]'
        Данный метод устанавливает фокус на необходимый элемент
     """

    def elementFocus(self, locator: str):
        try:
            wd = self.app.wd
            element = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((By.XPATH, ('%s' % locator))))
            action = ActionChains(wd)
            action.move_to_element(element).perform()
        except TimeoutException as exc:
            assert exc == TimeoutException, f"Ошибка!!! Локатор '{locator}' не найден"

    """ 
    Сравение количества найденных элементов с зададнным знаением.
    Метод осуществляет поиск всех видимых элементов.
    В аргументе передается 
    :Args:
        -  locator локатор Xpath пример: './/button'
        -  egual количество ожидаемых элементов пример: 5
    """

    def assertList(self, locator: str, equal: int):
        try:
            wd = self.app.wd
            if equal > 0:
                WebDriverWait(wd, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "%s" % locator)))
            x = len(wd.find_elements(By.XPATH, "%s" % locator))
            assert x == equal, f"Ожидаемый результат = {equal}, Фактический = {x}"
        except Exception as e:
            assert e == TimeoutException, f"Ошибка, локатор {locator} - не найден"

    """ 
    Сравнение текста элемента с заданным значением.
    В аргументе передается 
    :Args:
        -  locator локатор Xpath пример: './/button'
        -  text сравниваемое строковое значение  пример: 'Имя'
    """

    def assertElementText(self, locator: str, text: str):
        try:
            wd = self.app.wd
            WebDriverWait(wd, 5).until(
                EC.visibility_of_element_located((By.XPATH, "%s" % locator)))
            element = wd.find_element(By.XPATH, "%s" % locator).text
            assert element == text, f"Ожидаемый результат = {text}, Фактический = {element}"
        except Exception as e:
            assert e == TimeoutException, f"Ошибка, локатор {locator} - не найден"

    """ 
    Ввод скопированного значения в текстовое поле 
    Метод логично использовать после копирования значения по кнопке 
    и вставке в другое поле для сравнения результата.
    В аргументе передается 
    :Args:
        -  locator локатор Xpath пример: './/button'
    """

    def fieldEnterCtrl_v(self, locator: str):
        try:
            wd = self.app.wd
            WebDriverWait(wd, 5).until(
                EC.element_to_be_clickable((By.XPATH, "%s" % locator)))
            wd.find_element(By.CSS_SELECTOR, "%s" % locator).click()
            ActionChains(wd).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        except Exception as e:
            assert e == TimeoutException, f"Ошибка, локатор {locator} - не найден"

    """ 
    Правильное закрытие или переход.
    Метод подтверждает, что после какого-то действия указанный элемент пропал из DOM.
    В аргументе передается 
    :Args:
        -  locator_element локатор Xpath пример: './/input'
        -  locator_action локатор Xpath пример: './/button'
    """

    def checkHideElement(self, locator_element: str, locator_action: str):
        try:
            wd = self.app.wd
            element = WebDriverWait(wd, 9).until(
                EC.visibility_of_element_located((By.XPATH, locator_element)))
            self.app.Elements.click(locator_action)
            WebDriverWait(wd, 10).until(EC.staleness_of(element))
        except Exception as e:
            assert e == TimeoutException, f"Элемент продолжает отображаться"

    """ 
    Сравнение значения атрибута элемента с заданным значением 
    Данный метод логично использовать для проверки кнопки: активна\неактивна, проверка состояния поля и т.д.
    В аргументе передается 
    :Args:
        -  locator локатор Xpath пример: './/input'
        -  param имя нужного атрибута пример 'readonly'
        -  value свравниваемое значение аргумента пример: 'true' (можеть быть и None)
    """

    def asserFieldParam(self, locator: str, param: str, value: str):
        try:
            wd = self.app.wd
            field_value = WebDriverWait(wd, 5).until(
                EC.visibility_of_element_located((By.XPATH, "%s" % locator)))
            assert field_value.get_attribute(
                param) == value, f"Ожидаемый результат = {value}, " \
                                 f"Фактический = {field_value.get_attribute(param)}"
        except Exception as e:
            assert e == TimeoutException, f"Ошибка, локатор {locator} - не найден"
