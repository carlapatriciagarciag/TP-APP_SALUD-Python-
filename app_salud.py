import requests


class SistemaSalud():
    def __init__(self):
        self.registros = {}
        self.metas = { }


    def traducir(self, texto):
        #no se toca 
        url = "https://api.mymemory.translated.net/get"
        #no se toca 
        datos = {
            "q": texto,
            "langpair": "es|en"
        }
        response = requests.get(url, params=datos)
        data = response.json()
        return data["responseData"]["translatedText"]
    
    def obtener_calorias(self, comida):
        #la url tampoco se toca
        url = "https://api.edamam.com/api/nutrition-data"

        #datos (ESTO NO SE TOCA NI SE PRUEBA!)

        datos = {
            "app_id": "68618447",
            "app_key": "1df8535ef66be41812589c3d39f3792d",
            "ingr": comida
        }
        # el response en su (url, params = datos) es que yo le digo que params va a ser igual al diccionario del nombre datos (ASI QUE NO SE TOCA!)
        response = requests.get(url, params=datos)
        data = response.json()

       #get es el tipo 
        calorias = data.get("calories", 0)
        #para que no de 0 en calorias si se coloca una comida no valida en la API
        if calorias == 0:
            return 100
        return calorias 


       

    def cargar_datos(self):
        total_calorias = 0
        comidas = []
        self.mes = input("mes: ").lower().strip()
        #isalpha te termine verificar si es str o no te duelve true o false
        #strip para que permite colocar espacios porque isalpha colca false con cualquier caracter que no sea str

        while not self.mes.isalpha():
            print("solo letras, no numeros")
            self.mes = input("mes: ").lower().strip()
        while True:
            #esto hace q si no lo hace bien, vuelve a pedir
            try:
                self.dia = int(input("dia: "))
                if 1 <= self.dia <= 31:
                    break  
                else:
                    print("dia invalido")
            except:
                print("ingrese un numero")
       
        sueño = input("Horas de sueño: ")

        while not sueño.isdigit():
            print("Ingrese un número válido de horas")
            sueño = input("Horas de sueño: ")

        sueño = int(sueño)

        if sueño > 24:
            print("Tu límite para dormir son 24 horas")
            return
        
        while True:
            ejercicio = input("Horas de ejercicio: ")

            if ejercicio.isdigit():
                ejercicio = int(ejercicio)
                if 0 <= ejercicio <= 24:
                    break
                else:
                    print("Debe estar entre 0 y 24 horas")
            else:
                print("Ingrese un número válido")
        while True:
            comida = input("que comiste: (fin para terminar) ")
            if comida.lower() == "fin":
                break
            if comida.isdigit():
                print("No ingreses números, solo texto")
                continue
            
            comida_en = self.traducir(comida)
            print("Resultado:", comida_en)
            #Llama a calorias para que me diga
            calorias = self.obtener_calorias(comida_en)
            if calorias is None:
                print("comida no valida, escribalo correctamente o cambie.")
                comida = input("que comiste: ")
           
            else:
                comidas.append(comida)
                total_calorias+=calorias
                print("calorias:", calorias)

            registro = {
                "sueño": sueño,
                "ejercicio": ejercicio,
                #aca no se puede cambiar si va en mayuscula o minuscula ya que estamos usando una API entonces hay que ser especificos
                #de como lo escribimos. para probarlo podes colocar: 1 manzana grande 
                # si queres otros alimentos escribime y vemos la documentacion de la API, asi que la interfaz debe colocar los reglamentos para escribirlo correctamente.
                "comida": comidas,
                "calorias": total_calorias
            }
       
            if self.mes not in self.registros:
                self.registros[self.mes] = {}
            self.registros[self.mes][self.dia] = registro
       
    




    def modificar_datos(self):
        print("¿Qué quieres cambiar?")
        while True:
            mes = input("Ingrese mes: ").lower()
            if mes.isalpha():
                break
            print("El mes debe ser texto")

        while True:
            dia = input("Ingrese día: ")
            if dia.isdigit():
                dia = int(dia)
                break
            print("El día debe ser un número")

        if mes in self.registros and dia in self.registros[mes]:
            registro = self.registros[mes][dia]
            print("Registro actual:", registro)

            print("\nCampos disponibles: sueño, ejercicio, comida")
            campo = input("¿Qué deseas modificar?: ").lower()

            if campo == "sueño":
                nuevo = int(input("Nuevas horas de sueño: "))
                registro["sueño"] = nuevo

            elif campo == "ejercicio":
                nuevo = int(input("Nuevas horas de ejercicio: "))
                registro["ejercicio"] = nuevo

            elif campo == "comida":
                print("¿Qué quieres hacer con la comida?")
                print("1. Reemplazar")
                print("2. Agregar")
                print("3. Eliminar")
                opcion = input("Ingrese el numero que desea: ")

                if opcion == "1":
                    comida = input("Nueva comida: ")
                    comida_en = self.traducir(comida)
                    calorias = self.obtener_calorias(comida_en)
                    registro["comida"] = comida
                    registro["calorias"] = calorias

                elif opcion == "2":
                    comida_nueva = input("Comida a agregar: ")
                    registro["comida"].append(comida_nueva)

                    comida_en = self.traducir(registro["comida"])
                    registro["calorias"] += self.obtener_calorias(comida_en)

                elif opcion == "3":
                    comida_eliminar = input("Comida a eliminar: ")
                    comidas = registro["comida"].split(", ")

                    if comida_eliminar in comidas:
                        comidas.remove(comida_eliminar)
                        registro["comida"] = ", ".join(comidas)

                        comida_en = self.traducir(registro["comida"])
                        registro["calorias"] = self.obtener_calorias(comida_en)
                    else:
                        print("Esa comida no está en el registro")

            else:
                print("Campo inválido")

            print("Registro actualizado:", registro)

        else:
            print("No existe ese mes ni día")
           
    
    def eliminar_registro(self):
        mes = input("ingrese mes: ").lower()
        dia = int(input("ingrese dia: "))
        if mes in self.registros and dia in self.registros[mes]:
            del self.registros[mes][dia]
            del self.registros[mes]
            print("registro eliminado")
        else:
            print("no existen datos en esa fecha")
    
    def mostrar_registro(self):
        if not self.registros:
            print("no hay registros")
        else: 
            for mes, dias in self.registros.items():
                print(" ", mes)
                for dia, datos in dias.items():
                    print(" dia", dia, datos)
            
        

    
    def agregar_metas(self):
        clave = input("que meta queres agregar hoy? ejercicio/calorias a digeridas/sueño: ").lower()
        if clave == "ejercicio":
            valor = int(input("agregue el objetivo en horas: "))
        elif clave == "sueño":
            valor = int(input("agregue el objetivo en horas: "))
        elif clave == "calorias":
            valor = int(input("agregue el objetivo en calorias: "))

        
        
        self.metas[clave] = valor
        
    
    def modificar_metas(self):
        clave = input("que meta vas a modificar?").lower()
        if clave in self.metas:
            nuevo_valor = int(input("agregar el nuevo valor: "))
            self.metas[clave] = nuevo_valor
            return True 
        else: 
            return False 
        
    def eliminar_metas(self):
        clave = input("que meta vas a eliminar? ")
        if clave in self.metas:
            del self.metas[clave]
            print("se ha eliminado")
        else: 
            print("no existe esa meta")

    
   
    def mostrar_metas(self):
        if not self.metas:
            print("no hay metas ")
            return False
        for clave, valor in self.metas.items():
            print(f"{clave}: {valor}")   
        

class Menu:

    def __init__(self):
        self.sistema = SistemaSalud()
       
    def ejecutar(self):
        while True:
            print("1: agregar datos, 2: modificar datos, 3:eliminar datos, 4: mostrar datos, 5: agregar metas, 6: modificar metas, 7: eliminar metas, 8: mostrar metas, 9: cerrar sesion")
            opcion = int(input("opcion: "))
            match opcion:
                case 1:
                    self.sistema.cargar_datos()
                case 2:
                    self.sistema.modificar_datos()
                case 3:
                    self.sistema.eliminar_registro()
                case 4:
                    self.sistema.mostrar_registro()
                case 5:
                    self.sistema.agregar_metas()
                case 6:
                    self.sistema.modificar_metas()
                case 7:
                    self.sistema.eliminar_metas()
                case 8:
                    self.sistema.mostrar_metas()
                case 9:
                    exit()
menu = Menu()
menu.ejecutar()