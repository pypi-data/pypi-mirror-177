# -#- coding: utf-8 -#-
from facturacion_electronica import facturacion_electronica as fe
from facturacion_electronica.firma import Firma
import json
from lxml import etree
import unittest


class TestEjemploEstadoEnvio(unittest.TestCase):
    """
    Test Consulta Envío
    """
    def test_consulta_certificado_vencido(self):
        """
        Test Consulta de estado  con certificado vencido
        """
        print("Se inicia test consulta estado envío")
        f = open("facturacion_electronica/ejemplos/ejemplo_estado_envio.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.consulta_estado_envio(ejemplo)
        errores = result.get('errores', [])
        x = 'No hay Token en consulta envío'
        if x in errores :
            errores.remove(x)
        self.assertFalse(errores)
        self.assertEqual(result.get('glosa', ''), 'TOKEN NO EXISTE')

    """
    Test Consulta Envío Cesión
    """
    def test_consulta_envio_cesion_certificado_vencido(self):
        """
        Test Consulta Envío Cesión
        """
        print("Se inicia test consulta envío cesión")
        f = open("facturacion_electronica/ejemplos/ejemplo_estado_envio_cesion.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.consulta_estado_envio(ejemplo)
        errores = result.get('errores', [])
        x = 'No hay Token en consulta envío'
        if x in errores:
            errores.remove(x)
        self.assertFalse(errores)
        self.assertEqual(result.get('glosa', ''), 'Token no existe')

    """
    Test REenvío Correo Envío
    """
    def test_reenvio_correo_envio(self):
        """
        Test Reenvío Correo de envío
        """
        print("Se inicia test reenvio Correo de envio")
        f = open("facturacion_electronica/ejemplos/ejemplo_reenvio_correo_envio.json")
        txt_json = f.read()
        f.close()
        ejemplo = json.loads(txt_json)
        firma_electronica = ejemplo['firma_electronica'].copy()
        result = fe.reenvio_correo_envio(ejemplo)
        errores = result.get('errores', [])
        x = 'No hay Token en reenvío correo'
        if x in errores :
            errores.remove(x)
        self.assertFalse(errores)
        self.assertEqual(result.get('glosa', ''), 'Token no existe')

if __name__ == '__main__':
    unittest.main()
