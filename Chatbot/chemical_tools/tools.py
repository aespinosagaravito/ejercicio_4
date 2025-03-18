from docxtpl import DocxTemplate
import json


def collect_product_info():
    # Se crea el diccionario base con las claves requeridas.
    doc = DocxTemplate("input/cualicuantitativa.docx")
    product_dict = {}

    product_dict["codigo"] = input("Ingrese el código del producto: ")
    product_dict["producto"] = input("Ingrese el nombre del producto: ")
    product_dict["peso_dosificacion"] = input("Ingrese el peso/dosificación : ")
    product_dict["nombre_generico"] = input("Ingrese el nombre genérico: ")
    product_dict["color"] = input("Ingrese el color: ")
    product_dict["lote_estandar"] = input("Ingrese el lote estándar: ")
    product_dict["forma_farmaceutica"] = input("Ingrese la forma farmacéutica: ")
    product_dict["unidad_medida_del_producto"] = input(
        "Ingrese la unidad de medida del producto : "
    )
    product_dict["molde"] = input("Ingrese el molde del producto: ")

    materiales = []
    try:
        num_materiales = int(input("Ingrese la cantidad de materiales a agregar: "))
    except ValueError:
        print("Cantidad no válida. Se asigna 0 materiales.")
        num_materiales = 0

    for i in range(num_materiales):
        print(f"\n--- Material {i+1} ---")
        material = {}
        material["codigo_sap"] = input("Ingrese el código SAP: ")
        material["descripcion"] = input("Ingrese la descripción: ")
        material["funcion"] = input("Ingrese la función: ")
        material["cantidad"] = input("Ingrese la cantidad: ")
        material["exceso"] = input("Ingrese el exceso: ")
        materiales.append(material)

    product_dict["materiales"] = materiales

    doc.render(product_dict)
    doc.save("output/cualicuantitativa.docx")
    print("documento_generado_con_exito")
