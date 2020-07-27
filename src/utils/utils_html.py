from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
import time


class ValidacionesHtml:

    @staticmethod
    def verificar_ventana_archivo_duplicado(webdriver_test_ux: WebDriver):

        try:
            WebDriverWait(webdriver_test_ux, 20).until(
                EC.presence_of_element_located((By.ID, 'oc-dialog-fileexists-content')))

            check_sustituir_archivos = WebDriverWait(webdriver_test_ux, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//label[@for="checkbox-allnewfiles"][text()="Archivos Nuevos"]')))

            check_sustituir_archivos.click()

            btn_continuar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="continue"][text()="Continuar"]')))

            btn_continuar.click()

        except ElementNotInteractableException:
            pass
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass
        #
        # id
        # oc - dialog - fileexists - content
        #
        # id
        # checkbox - allnewfiles
        #
        # < button
        #
        # class ="continue" disabled="" > Continuar < / button >
        #
        # class = up-file-actions isDone
