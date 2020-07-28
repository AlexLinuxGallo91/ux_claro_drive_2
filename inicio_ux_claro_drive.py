from src.webdriver_config.config_webdriver import ConfiguracionWebDriver
from selenium import webdriver
from src.validaciones_json.json_evaluacion_base import GeneradorJsonBaseEvaluacion
from os import path
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.utils_temporizador import Temporizador
from src.utils.utils_format import FormatUtils
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from src.utils.utils_html import ValidacionesHtml
import src.validaciones_json.constantes_json as jsonConst
import time
import sys
import json


def inicio_sesion_claro_drive(webdriver_test_ux: webdriver, jsonEval, jsonArgs):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:
        webdriver_test_ux.get('https://www.clarodrive.com/')
        btn_inicio_sesion = WebDriverWait(webdriver_test_ux, 6).until(EC.presence_of_element_located((By.ID, 'login')))
        btn_inicio_sesion.click()

        input_email = WebDriverWait(webdriver_test_ux, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'InputEmail')))
        input_email.send_keys(jsonArgs['user'])

        input_password = WebDriverWait(webdriver_test_ux, 6).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'InputPassword')))
        input_password.send_keys(jsonArgs['password'])

        btn_ingreso_cuenta = WebDriverWait(webdriver_test_ux, 6).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="INICIAR SESI\u00D3N"]')))
        btn_ingreso_cuenta.click()

        WebDriverWait(webdriver_test_ux, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Folder "][@class="name-without-extension"]')))

        jsonEval["steps"][0]["output"][0]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][0]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][0]["output"][0]["output"] = 'Se ingresa correctamente al portal Claro Drive'

    except ElementNotInteractableException as e:
        jsonEval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar al portal Claro Drive'
    except NoSuchElementException as e:
        jsonEval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar al portal Claro Drive'
    except TimeoutException as e:
        jsonEval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar al portal Claro Drive'

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    jsonEval["steps"][0]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    jsonEval["steps"][0]["start"] = fecha_inicio
    jsonEval["steps"][0]["end"] = fecha_fin

    return jsonEval


def carga_archivo_claro_drive(webdriver_test_ux: webdriver, path_archivo_carga: str, nombre_archivo_sin_ext: str,
                              jsonEval):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:
        carpeta_folder = WebDriverWait(webdriver_test_ux, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Folder "][@class="name-without-extension"]')))
        carpeta_folder.click()

        WebDriverWait(webdriver_test_ux, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()=" Folder "][@class="last"]')))

        input_file = WebDriverWait(webdriver_test_ux, 10).until(
            EC.presence_of_element_located((By.ID, 'file_upload_start')))

        input_file.send_keys(path_archivo_carga)

        ValidacionesHtml.verificar_ventana_archivo_duplicado(webdriver_test_ux)

        WebDriverWait(webdriver_test_ux, 720).until(EC.presence_of_element_located(
            (By.XPATH, '//span[@class="name-without-extension"][text()="{} "]'.format(nombre_archivo_sin_ext))))

        jsonEval["steps"][1]["output"][0]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][1]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][1]["output"][0]["output"] = 'Se realiza correctamente la carga del archivo'

    except NoSuchElementException:
        jsonEval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][1]["status"] = jsonConst.FAILED
        jsonEval["steps"][1]["output"][0]["output"] = 'No fue posible realizar la carga del archivo'

    except ElementClickInterceptedException:
        jsonEval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][1]["status"] = jsonConst.FAILED
        jsonEval["steps"][1]["output"][0]["output"] = 'No fue posible realizar la carga del archivo'

    except TimeoutException:
        jsonEval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][1]["status"] = jsonConst.FAILED
        jsonEval["steps"][1]["output"][0]["output"] = 'No fue posible realizar la carga del archivo'

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    jsonEval["steps"][1]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    jsonEval["steps"][1]["start"] = fecha_inicio
    jsonEval["steps"][1]["end"] = fecha_fin

    return jsonEval


def descarga_archivo_claro_drive(webdriver_test_ux: webdriver, nombre_archivo_sin_ext: str, jsonEval, ext_archivo: str):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:

        webdriver_test_ux.refresh()

        archivo_a_descargar = WebDriverWait(webdriver_test_ux, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[@class="name-without-extension"][text()="{} "]'.format(nombre_archivo_sin_ext))))

        archivo_a_descargar.click()

        btn_descarga = WebDriverWait(webdriver_test_ux, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@type="button"][@class="menuItem svg downloadImage icon-download icon-32"]')))

        btn_descarga.click()

        jsonEval["steps"][2]["output"][0]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][2]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][2]["output"][0]["output"] = 'Se realiza la descarga del archivo correctamente'
    except NoSuchElementException as e:
        jsonEval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][2]["status"] = jsonConst.FAILED
        jsonEval["steps"][2]["output"][0][
            "output"] = 'No fue posible realizar la descarga del archivo correctamente: {}'.format(e)
    except ElementClickInterceptedException as e:
        jsonEval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][2]["status"] = jsonConst.FAILED
        jsonEval["steps"][2]["output"][0][
            "output"] = 'No fue posible realizar la descarga del archivo correctamente: {}'.format(e)
    except TimeoutException as e:
        jsonEval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][2]["status"] = jsonConst.FAILED
        jsonEval["steps"][2]["output"][0][
            "output"] = 'No fue posible realizar la descarga del archivo correctamente: {}'.format(e)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    jsonEval["steps"][2]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    jsonEval["steps"][2]["start"] = fecha_inicio
    jsonEval["steps"][2]["end"] = fecha_fin

    return jsonEval


def borrar_archivo_claro_drive(webdriver_test_ux: webdriver, jsonEval, nombre_archivo_sin_ext: str, ext_archivo: str):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:

        webdriver_test_ux.refresh()

        archivo_por_eliminar = WebDriverWait(webdriver_test_ux, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[@class="name-without-extension"][text()="{} "]'.format(nombre_archivo_sin_ext))))

        archivo_por_eliminar.click()

        btn_borrar = WebDriverWait(webdriver_test_ux, 20).until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@type="button"][@class="menuItem svg deleteImage icon-delete icon-32"]')))

        btn_borrar.click()

        jsonEval["steps"][3]["output"][0]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][3]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][3]["output"][0]["output"] = 'Se realiza el borrado del archivo correctamente'
    except NoSuchElementException as e:
        jsonEval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][3]["status"] = jsonConst.FAILED
        jsonEval["steps"][3]["output"][0][
            "output"] = 'No fue posible realizar el borrado del archivo correctamente: {}'.format(e.msg)

    except ElementClickInterceptedException as e:
        jsonEval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][3]["status"] = jsonConst.FAILED
        jsonEval["steps"][3]["output"][0][
            "output"] = 'No fue posible realizar el borrado del archivo correctamente: {}'.format(e.msg)

    except TimeoutException as e:
        jsonEval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][3]["status"] = jsonConst.FAILED
        jsonEval["steps"][3]["output"][0][
            "output"] = 'No fue posible realizar el borrado del archivo correctamente: {}'.format(e.msg)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    jsonEval["steps"][3]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    jsonEval["steps"][3]["start"] = fecha_inicio
    jsonEval["steps"][3]["end"] = fecha_fin

    return jsonEval


def cerrar_sesion_claro_drive(webdriver_test_ux: webdriver, jsonEval):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:
        webdriver_test_ux.refresh()
        boton_ajustes = WebDriverWait(webdriver_test_ux, 10).until(EC.element_to_be_clickable((By.ID, 'expand')))
        boton_ajustes.click()

        boton_cerrar_sesion = WebDriverWait(webdriver_test_ux, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//li[@data-id="logout"]/a')))

        boton_cerrar_sesion.click()
        WebDriverWait(webdriver_test_ux, 10).until(EC.presence_of_element_located((By.ID, 'login')))

        jsonEval["steps"][4]["output"][0]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][4]["status"] = jsonConst.SUCCESS
        jsonEval["steps"][4]["output"][0]["output"] = 'Se cierra sesion correctamente'

    except NoSuchElementException as e:
        jsonEval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(e.msg)

    except ElementClickInterceptedException as e:
        jsonEval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(e.msg)

    except TimeoutException as e:
        jsonEval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(e.msg)

    except ElementNotInteractableException as e:
        jsonEval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["status"] = jsonConst.FAILED
        jsonEval["steps"][4]["output"][0]["output"] = 'No fue posible realizar el cierre de sesion: {}'.format(e.msg)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    jsonEval["steps"][4]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    jsonEval["steps"][4]["start"] = fecha_inicio
    jsonEval["steps"][4]["end"] = fecha_fin

    return jsonEval


def verificacion_estatus_final(json_evaluacion):
    val_paso_1 = True if json_evaluacion["steps"][0]["status"] == jsonConst.SUCCESS else False
    val_paso_2 = True if json_evaluacion["steps"][1]["status"] == jsonConst.SUCCESS else False
    val_paso_3 = True if json_evaluacion["steps"][2]["status"] == jsonConst.SUCCESS else False
    val_paso_4 = True if json_evaluacion["steps"][3]["status"] == jsonConst.SUCCESS else False
    val_paso_5 = True if json_evaluacion["steps"][4]["status"] == jsonConst.SUCCESS else False

    eval_final = val_paso_1 and val_paso_2 and val_paso_3 and val_paso_4 and val_paso_5

    return jsonConst.SUCCESS if eval_final else jsonConst.FAILED


def main():
    file_config = FormatUtils.lector_archivo_ini()

    path_web_driver = file_config.get('Driver', 'ruta')
    web_driver_por_usar = file_config.get('Driver', 'driverPorUtilizar')

    tiempo_inicial_ejecucion_prueba = Temporizador.obtener_tiempo_timer()
    fecha_prueba_inicial = Temporizador.obtener_fecha_tiempo_actual()

    # verifica que el usuario haya establecido el path de la imagen a subir
    args = sys.argv[1:]

    if len(args) == 0:
        print('Favor de establecer el parametro json')
        sys.exit()

    json_args = args[0]

    if not FormatUtils.cadena_a_json_valido(json_args):
        sys.exit()
    else:
        json_args = json.loads(json_args)

    if not FormatUtils.verificar_keys_json(json_args):
        sys.exit()

    if not path.exists(json_args['pathImage']):
        print('La imagen/archivo por cargar no existe o no se localiza, favor de corregir el path del archivo')
        sys.exit()
    elif not path.isfile(json_args['pathImage']):
        print('La ruta establecida no corresponde a un archivo o imagen valido, favor de corregir el path del archivo')
        sys.exit()

    nombre_archivo_imagen_sin_ext = Path(json_args['pathImage']).stem
    nombre_archivo_imagen_con_ext = path.basename(json_args['pathImage'])
    ext_archivo = path.splitext(nombre_archivo_imagen_con_ext)[1]

    # se establece el navegador (por defecto firefox)
    webdriver_config = ConfiguracionWebDriver(path_web_driver, web_driver_por_usar)
    webdriver_ux_test = webdriver_config.configurar_obtencion_web_driver()

    # se genera el json de evaluacion
    json_evaluacion_claro_drive = GeneradorJsonBaseEvaluacion.generar_nuevo_template_json()

    json_evaluacion_claro_drive = inicio_sesion_claro_drive(webdriver_ux_test, json_evaluacion_claro_drive, json_args)

    json_evaluacion_claro_drive = carga_archivo_claro_drive(webdriver_ux_test, json_args['pathImage'],
                                                            nombre_archivo_imagen_sin_ext, json_evaluacion_claro_drive)

    json_evaluacion_claro_drive = descarga_archivo_claro_drive(webdriver_ux_test, nombre_archivo_imagen_sin_ext,
                                                               json_evaluacion_claro_drive, ext_archivo)

    json_evaluacion_claro_drive = borrar_archivo_claro_drive(webdriver_ux_test, json_evaluacion_claro_drive,
                                                             nombre_archivo_imagen_sin_ext, ext_archivo)

    json_evaluacion_claro_drive = cerrar_sesion_claro_drive(webdriver_ux_test, json_evaluacion_claro_drive)

    tiempo_final_ejecucion_prueba = Temporizador.obtener_tiempo_timer() - tiempo_inicial_ejecucion_prueba
    fecha_prueba_final = Temporizador.obtener_fecha_tiempo_actual()

    json_evaluacion_claro_drive['start'] = fecha_prueba_inicial
    json_evaluacion_claro_drive['end'] = fecha_prueba_final
    json_evaluacion_claro_drive['time'] = tiempo_final_ejecucion_prueba
    json_evaluacion_claro_drive['status'] = verificacion_estatus_final(json_evaluacion_claro_drive)

    # json_evaluacion_claro_drive = GeneradorJsonBaseEvaluacion. \
    #    establecer_estructura_principal_json(json_args['user'], json_evaluacion_claro_drive)

    time.sleep(2)

    webdriver_ux_test.close()
    webdriver_ux_test.quit()

    print(json.dumps(json_evaluacion_claro_drive))


main()
