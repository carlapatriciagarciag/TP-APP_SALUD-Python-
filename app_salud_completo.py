import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import calendar
from datetime import date

# Crear un entorno virtual para cada proyecto desde la terminal
#  python3 -m venv venv

# Luego de creado se debe activar con este comnado desde la terminla
# source venv/bin/activate

# Desde la terminal se debe ver algo asi:
# (venv) carlagarcia@MacBook-Air-de-Carla Testing 2026 % 
print("ARRANCÓ EL PROGRAMA")

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
                total_calorias += calorias
                print("calorias:", calorias)

        # BUG CORREGIDO: el registro se guarda UNA vez, DESPUÉS del loop de comidas
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
                    registro["comida"] = [comida]
                    registro["calorias"] = calorias

                elif opcion == "2":
                    comida_nueva = input("Comida a agregar: ")
                    registro["comida"].append(comida_nueva)
                    # BUG CORREGIDO: traducir recibe un string, no la lista completa
                    comida_en = self.traducir(comida_nueva)
                    registro["calorias"] += self.obtener_calorias(comida_en)

                elif opcion == "3":
                    comida_eliminar = input("Comida a eliminar: ")
                    # BUG CORREGIDO: comida ya es una lista, no hay que hacer .split()
                    if comida_eliminar in registro["comida"]:
                        registro["comida"].remove(comida_eliminar)
                        # Recalcula las calorias totales con las comidas restantes
                        total = 0
                        for c in registro["comida"]:
                            c_en = self.traducir(c)
                            total += self.obtener_calorias(c_en)
                        registro["calorias"] = total
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
            # BUG CORREGIDO: solo borra el mes si quedó vacío, no siempre
            if not self.registros[mes]:
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
        else:
            print("meta no reconocida")
            return

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


    def verificar_metas(self, sueño, ejercicio, calorias):
        # BUG CORREGIDO: usa .get() para no crashear si falta alguna meta
        meta_sueño = self.metas.get("sueño")
        meta_ejercicio = self.metas.get("ejercicio")
        meta_calorias = self.metas.get("calorias")

        cumplio_sueño = sueño >= meta_sueño if meta_sueño is not None else None
        cumplio_ejercicio = ejercicio >= meta_ejercicio if meta_ejercicio is not None else None
        cumplio_calorias = calorias <= meta_calorias if meta_calorias is not None else None

        return cumplio_calorias, cumplio_ejercicio, cumplio_sueño

    def mostrar_metas(self):
        if not self.metas:
            print("no hay metas ")
            return False
        for clave, valor in self.metas.items():
            print(f"{clave}: {valor}")


    # ─────────────────────────────────────────────────────────────────────────
    # MÉTODO AUXILIAR: pide mes y devuelve (nombre_mes, numero_mes, año_actual)
    # Lo usan los cuatro métodos de gráfico para no repetir el mismo código
    # ─────────────────────────────────────────────────────────────────────────
    def _pedir_mes_con_registros(self):
        if not self.registros:
            print("No hay registros cargados todavía.")
            return None, None, None

        print("Meses con registros:", ", ".join(self.registros.keys()))
        mes_elegido = input("Ingrese el nombre del mes a graficar: ").lower().strip()

        if mes_elegido not in self.registros:
            print(f"No hay registros para '{mes_elegido}'.")
            return None, None, None

        # Intentar detectar el número de mes (inglés y español)
        numero_mes = None
        año_actual = date.today().year
        for i in range(1, 13):
            if calendar.month_name[i].lower() == mes_elegido:
                numero_mes = i
                break

        meses_es = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }
        if numero_mes is None:
            numero_mes = meses_es.get(mes_elegido)

        if numero_mes is None:
            while True:
                try:
                    numero_mes = int(input(f"No reconocí '{mes_elegido}' como mes. Ingrese el número (1-12): "))
                    if 1 <= numero_mes <= 12:
                        break
                    else:
                        print("Debe estar entre 1 y 12.")
                except ValueError:
                    print("Ingrese un número válido.")

        return mes_elegido, numero_mes, año_actual


    # ─────────────────────────────────────────────
    # GRÁFICO DE HORAS DE SUEÑO (integrado desde horasdesueño.py)
    # Usa los datos reales cargados en self.registros
    # ─────────────────────────────────────────────
    def graficar_sueño(self):
        print(" Gráfico de Horas de Sueño Diarias ")

        mes_elegido, numero_mes, año_actual = self._pedir_mes_con_registros()
        if mes_elegido is None:
            return

        dias_registrados = self.registros[mes_elegido]

        fechas = []
        horas_sueño = []

        for dia, datos in sorted(dias_registrados.items()):
            try:
                fecha = date(año_actual, numero_mes, dia)
                fechas.append(fecha)
                horas_sueño.append(datos["sueño"])
            except ValueError:
                # Día inválido para ese mes (ej: día 31 en abril) — se omite
                continue

        if not fechas:
            print("No se pudieron construir fechas válidas con los registros de ese mes.")
            return

        umbral_horas_sueño = 7.0

        colores = ['green' if horas >= umbral_horas_sueño else 'red' for horas in horas_sueño]

        plt.figure(figsize=(15, 7))

        barras = plt.bar(fechas, horas_sueño, color=colores)

        # Leyenda manual ya que usamos un único plt.bar()
        from matplotlib.patches import Patch
        leyenda = [
            Patch(color='green', label='Sueño suficiente (>=7h)'),
            Patch(color='red', label='Sueño insuficiente (<7h)')
        ]
        plt.legend(handles=leyenda, loc='best')

        plt.xlabel('Días del Mes')
        plt.ylabel('Horas de Sueño')
        plt.title(f'Horas de Sueño Diarias para {mes_elegido.capitalize()} de {año_actual}', fontsize=16)

        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))

        cantidad_dias = len(fechas)
        if cantidad_dias > 20:
            plt.xticks(rotation=45, ha='right', fontsize=8)
        else:
            plt.xticks(fontsize=10)

        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()


    # ─────────────────────────────────────────────
    # GRÁFICO DE CALORÍAS (integrado desde caloriias.py)
    # Usa los datos reales cargados en self.registros
    # ─────────────────────────────────────────────
    def graficar_calorias(self):
        print(" Gráfico de Calorías Diarias ")

        mes_elegido, numero_mes, año_actual = self._pedir_mes_con_registros()
        if mes_elegido is None:
            return

        dias_registrados = self.registros[mes_elegido]

        fechas = []
        calorias = []

        for dia, datos in sorted(dias_registrados.items()):
            try:
                fecha = date(año_actual, numero_mes, dia)
                fechas.append(fecha)
                calorias.append(datos["calorias"])
            except ValueError:
                # Día inválido para ese mes — se omite
                continue

        if not fechas:
            print("No se pudieron construir fechas válidas con los registros de ese mes.")
            return

        umbral_de_calorias = 2000

        fechas_calorias_bajas = []
        valores_calorias_bajas = []
        fechas_calorias_altas = []
        valores_calorias_altas = []

        for i, valor_caloria in enumerate(calorias):
            if valor_caloria < umbral_de_calorias:
                fechas_calorias_bajas.append(fechas[i])
                valores_calorias_bajas.append(valor_caloria)
            else:
                fechas_calorias_altas.append(fechas[i])
                valores_calorias_altas.append(valor_caloria)

        plt.figure(figsize=(15, 7))

        if fechas_calorias_bajas:
            plt.bar(fechas_calorias_bajas, valores_calorias_bajas, color='green', label='Calorías dentro de objetivo (<2000 kcal)')
        
        if fechas_calorias_altas:
            plt.bar(fechas_calorias_altas, valores_calorias_altas, color='red', label='Calorías fuera de objetivo (>=2000 kcal)')

        plt.xlabel('Días del Mes')
        plt.ylabel('Calorías (kcal)')
        plt.title(f'Calorías Diarias para {mes_elegido.capitalize()} de {año_actual}', fontsize=16)

        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))

        cantidad_dias = len(fechas)
        if cantidad_dias > 20:
            plt.xticks(rotation=45, ha='right', fontsize=8)
        else:
            plt.xticks(fontsize=10)

        plt.yticks(fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=2)
        plt.tight_layout(rect=[0, 0.05, 1, 1])
        plt.show()


    # ─────────────────────────────────────────────
    # GRÁFICO DE DÍAS DE EJERCICIO (integrado desde ejercio.py)
    # Usa los datos reales cargados en self.registros
    # ─────────────────────────────────────────────
    def graficar_ejercicio(self):
        print(" Gráfico de Días de Ejercicio")

        mes_elegido, numero_mes, año_actual = self._pedir_mes_con_registros()
        if mes_elegido is None:
            return

        dias_registrados = self.registros[mes_elegido]

        fechas_del_mes = []
        estado_ejercicio_por_dia = []

        for dia, datos in sorted(dias_registrados.items()):
            try:
                fecha = date(año_actual, numero_mes, dia)
                fechas_del_mes.append(fecha)
                # 1 si registró alguna hora de ejercicio, 0 si no hizo nada
                estado_ejercicio_por_dia.append(1 if datos["ejercicio"] > 0 else 0)
            except ValueError:
                # Día inválido para ese mes — se omite
                continue

        if not fechas_del_mes:
            print("No se pudieron construir fechas válidas con los registros de ese mes.")
            return

        plt.figure(figsize=(15, 7))

        fechas_con_ejercicio = []
        fechas_sin_ejercicio = []

        altura_si_ejercicio = 1.0
        altura_no_ejercicio = 0.0

        for i, dia_ejercicio_estado in enumerate(estado_ejercicio_por_dia):
            if dia_ejercicio_estado == 1:
                fechas_con_ejercicio.append(fechas_del_mes[i])
            else:
                fechas_sin_ejercicio.append(fechas_del_mes[i])

        if fechas_con_ejercicio:
            plt.scatter(fechas_con_ejercicio, [altura_si_ejercicio] * len(fechas_con_ejercicio),
                        color='green', s=150, zorder=2, label='Sí Ejercicio', marker='o')

        if fechas_sin_ejercicio:
            plt.scatter(fechas_sin_ejercicio, [altura_no_ejercicio] * len(fechas_sin_ejercicio),
                        color='red', s=150, zorder=2, label='No Ejercicio', marker='o')

        plt.xlabel('Días del Mes')
        plt.ylabel('Estado del Ejercicio')
        plt.title(f'Días de Ejercicio para {mes_elegido.capitalize()} de {año_actual}', fontsize=16)

        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))

        cantidad_dias = len(fechas_del_mes)
        if cantidad_dias > 20:
            plt.xticks(rotation=45, ha='right', fontsize=8)
        else:
            plt.xticks(fontsize=10)

        plt.yticks([altura_no_ejercicio, altura_si_ejercicio], ['No', 'Sí'], fontsize=12)
        plt.ylim(-0.5, 1.5)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.legend(loc='upper right') # Esta línea añade la leyenda
        plt.tight_layout()
        plt.show()


    # ─────────────────────────────────────────────────────────────────────────
    # GRÁFICO GENERAL DE HÁBITOS (integrado desde general (1).py)
    # Calcula puntuaciones reales a partir de self.registros en vez de simular
    # ─────────────────────────────────────────────────────────────────────────
    def graficar_general(self):
        print("--- Gráfico General de Hábitos Mensual ---")

        mes_elegido, numero_mes, año_actual = self._pedir_mes_con_registros()
        if mes_elegido is None:
            return

        dias_registrados = self.registros[mes_elegido]
        num_dias_mes = len(dias_registrados)

        # Recolectar datos reales del mes
        lista_calorias = [datos["calorias"] for datos in dias_registrados.values()]
        lista_sueño = [datos["sueño"] for datos in dias_registrados.values()]
        # Cuenta días en que hubo al menos 1 hora de ejercicio
        total_dias_ejercicio = sum(1 for datos in dias_registrados.values() if datos["ejercicio"] > 0)

        prom_calorias = sum(lista_calorias) / num_dias_mes
        prom_sueño = sum(lista_sueño) / num_dias_mes

        # Calcular puntuaciones (misma lógica que general (1).py — no se toca)
        objetivo_calorias_ideal = 2100
        rango_calorias_aceptable = 200
        objetivo_horas_sueno = 8.0
        objetivo_ejercicio_semanal = 4
        objetivo_ejercicio_mensual = (objetivo_ejercicio_semanal / 7) * num_dias_mes

        puntuacion_calorias = min(100, (prom_calorias / objetivo_calorias_ideal) * 100)

        puntuacion_sueño = (prom_sueño / objetivo_horas_sueno) * 100
        puntuacion_sueño = min(100, puntuacion_sueño)

        puntuacion_ejercicio = (total_dias_ejercicio / objetivo_ejercicio_mensual) * 100
        puntuacion_ejercicio = min(100, puntuacion_ejercicio)

        puntuacion_calorias = max(0, min(100, puntuacion_calorias))

        categorias = ['Calorías', 'Horas de Sueño', 'Días de Ejercicio']
        valores = [puntuacion_calorias, puntuacion_sueño, puntuacion_ejercicio]
        colores = ['#4CAF50', '#2196F3', '#FF9800']

        fig, ax = plt.subplots(figsize=(10, 6))

        y_pos = np.arange(len(categorias))

        ax.barh(y_pos, valores, color=colores)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(categorias, fontsize=12)
        ax.set_xlim(0, 100)
        ax.set_xlabel('Porcentaje de Cumplimiento del Objetivo (%)', fontsize=12)
        ax.set_title(f'Cumplimiento de Hábitos para {mes_elegido.capitalize()} de {año_actual}', fontsize=16)

        for i, v in enumerate(valores):
            ax.text(v + 2, i, f"{int(v)}%", color='black', va='center', ha='left', fontsize=10)

        ax.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()


class Menu:

    def __init__(self):
        self.sistema = SistemaSalud()
       
    def ejecutar(self):
        while True:
            print("\n1: agregar datos")
            print("2: modificar datos")
            print("3: eliminar datos")
            print("4: mostrar datos")
            print("5: agregar metas")
            print("6: modificar metas")
            print("7: eliminar metas")
            print("8: mostrar metas")
            print("9: cerrar sesion")
            print("── Gráficos ──")
            print("10: gráfico de sueño")
            print("11: gráfico de calorías")
            print("12: gráfico de ejercicio")
            print("13: gráfico general de hábitos")

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
                case 10:
                    self.sistema.graficar_sueño()
                case 11:
                    self.sistema.graficar_calorias()
                case 12:
                    self.sistema.graficar_ejercicio()
                case 13:
                    self.sistema.graficar_general()

menu = Menu()
menu.ejecutar()
