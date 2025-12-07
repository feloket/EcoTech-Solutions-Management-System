# menu
"""Sistema de Gestión Ecotech Solutions"""
from conexiondb import Database
from clases import Empleados, Usuario, Departamento, Proyecto, RegistroDeTiempo
from indicadores import IndicadorEconomico
from datetime import datetime, date


def mostrar_menu_principal():
    """Mostrar menú principal"""
    print("\n" + "="*60)
    print("    SISTEMA DE GESTIÓN ECOTECH SOLUTIONS")
    print("="*60)
    print("1.  Gestión de Empleados")
    print("2.  Gestión de Usuarios")
    print("3.  Gestión de Departamentos")
    print("4.  Gestión de Proyectos")
    print("5.  Registro de Tiempo")
    print("6.  Indicadores Económicos")
    print("0.  Salir del Sistema")
    print("="*60)


def menu_empleados(db):
    """Menú de gestión de empleados"""
    while True:
        print("\n" + "="*60)
        print("    GESTIÓN DE EMPLEADOS")
        print("="*60)
        print("1. Registrar nuevo empleado")
        print("2. Listar empleados")
        print("3. Buscar empleado por ID")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("0. Volver al menú principal")
        print("="*60)

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR NUEVO EMPLEADO ---")
            nombre = input("Nombre completo: ").strip()
            direccion = input("Dirección: ").strip()
            telefono = input("Teléfono: ").strip()
            email = input("Email: ").strip()
            salario = float(input("Salario: ").strip())

            emp = Empleados(db, nombre=nombre, direccion=direccion, telefono=telefono,
                            email=email, salario=salario)
            emp.registrar_empleado()

        elif opcion == "2":
            print("\n--- LISTA DE EMPLEADOS ---")
            empleados = Empleados.listar_empleados(db)
            if empleados:
                for emp in empleados:
                    print(f"\n{emp}")
            else:
                print("No hay empleados registrados.")

        elif opcion == "3":
            print("\n--- BUSCAR EMPLEADO ---")
            id_emp = int(input("ID del empleado: ").strip())
            emp = Empleados.buscar_por_id(db, id_emp)
            if emp:
                print(f"\n{emp}")
            else:
                print("Empleado no encontrado.")

        elif opcion == "4":
            print("\n--- ACTUALIZAR EMPLEADO ---")
            id_emp = int(input("ID del empleado a actualizar: ").strip())
            emp = Empleados.buscar_por_id(db, id_emp)

            if emp:
                print(f"\nEmpleado actual: {emp.nombre}")
                print("Deje en blanco para mantener el valor actual")

                nombre = input(f"Nuevo nombre [{emp.nombre}]: ").strip()
                if nombre:
                    emp.nombre = nombre

                direccion = input(
                    f"Nueva dirección [{emp.direccion}]: ").strip()
                if direccion:
                    emp.direccion = direccion

                telefono = input(f"Nuevo teléfono [{emp.telefono}]: ").strip()
                if telefono:
                    emp.telefono = telefono

                email = input(f"Nuevo email [{emp.email}]: ").strip()
                if email:
                    emp.email = email

                salario = input(f"Nuevo salario [{emp.salario}]: ").strip()
                if salario:
                    emp.salario = float(salario)

                emp.actualizar_empleado()
            else:
                print("Empleado no encontrado.")

        elif opcion == "5":
            print("\n--- ELIMINAR EMPLEADO ---")
            id_emp = int(input("ID del empleado a eliminar: ").strip())
            confirmar = input("¿Está seguro? (s/n): ").strip().lower()
            if confirmar == 's':
                Empleados.eliminar_empleado(db, id_emp)
            else:
                print("Operación cancelada.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def menu_usuarios(db):
    """Menú de gestión de usuarios"""
    while True:
        print("\n" + "="*60)
        print("    GESTIÓN DE USUARIOS")
        print("="*60)
        print("1. Registrar nuevo usuario")
        print("2. Listar usuarios")
        print("3. Autenticar usuario")
        print("0. Volver al menú principal")
        print("="*60)

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR NUEVO USUARIO ---")
            nombre_usuario = input("Nombre de usuario: ").strip()
            password = input("Contraseña: ").strip()
            rol = input("Rol (admin/usuario/gerente): ").strip()
            id_empleado = input(
                "ID del empleado (dejar vacío si no aplica): ").strip()
            id_empleado = int(id_empleado) if id_empleado else None

            usuario = Usuario(db, nombre_usuario=nombre_usuario, password=password,
                              rol=rol, id_empleado=id_empleado)
            usuario.registrar_usuario()

        elif opcion == "2":
            print("\n--- LISTA DE USUARIOS ---")
            usuarios = Usuario.listar_usuarios(db)
            if usuarios:
                for usr in usuarios:
                    print(f"ID: {usr['id_usuario']}, Usuario: {usr['nombre_usuario']}, "
                          f"Rol: {usr['rol']}, ID Empleado: {usr['id_empleado']}")
            else:
                print("No hay usuarios registrados.")

        elif opcion == "3":
            print("\n--- AUTENTICAR USUARIO ---")
            nombre_usuario = input("Nombre de usuario: ").strip()
            password = input("Contraseña: ").strip()

            usuario = Usuario(
                db, nombre_usuario=nombre_usuario, password=password)
            if usuario.autenticar():
                print(f"Autenticación exitosa. Rol: {usuario.rol}")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def menu_departamentos(db):
    """Menú de gestión de departamentos"""
    while True:
        print("\n" + "="*60)
        print("    GESTIÓN DE DEPARTAMENTOS")
        print("="*60)
        print("1. Crear departamento")
        print("2. Listar departamentos")
        print("3. Buscar departamento por ID")
        print("4. Actualizar departamento")
        print("5. Eliminar departamento")
        print("0. Volver al menú principal")
        print("="*60)

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- CREAR DEPARTAMENTO ---")
            nombre = input("Nombre del departamento: ").strip()
            gerente = input("Nombre del gerente: ").strip()
            id_empleado = input(
                "ID del empleado responsable (opcional): ").strip()
            id_proyecto = input(
                "ID del proyecto asociado (opcional): ").strip()

            id_empleado = int(id_empleado) if id_empleado else None
            id_proyecto = int(id_proyecto) if id_proyecto else None

            depto = Departamento(db, nombre=nombre, gerente=gerente,
                                 id_empleado=id_empleado, id_proyecto=id_proyecto)
            depto.crear_departamento()

        elif opcion == "2":
            print("\n--- LISTA DE DEPARTAMENTOS ---")
            departamentos = Departamento.listar_departamentos(db)
            if departamentos:
                for dept in departamentos:
                    print(f"ID: {dept['id_departamento']}, Nombre: {dept['nombre']}, "
                          f"Gerente: {dept['gerente']}, ID Empleado: {dept['id_empleado']}, "
                          f"ID Proyecto: {dept['id_proyecto']}")
            else:
                print("No hay departamentos registrados.")

        elif opcion == "3":
            print("\n--- BUSCAR DEPARTAMENTO ---")
            id_dept = int(input("ID del departamento: ").strip())
            dept = Departamento.buscar_por_id(db, id_dept)
            if dept:
                print(f"\n{dept}")
            else:
                print("Departamento no encontrado.")

        elif opcion == "4":
            print("\n--- ACTUALIZAR DEPARTAMENTO ---")
            id_dept = int(input("ID del departamento a actualizar: ").strip())
            dept = Departamento.buscar_por_id(db, id_dept)

            if dept:
                print(f"\nDepartamento actual: {dept.nombre}")
                dept.nombre = input(
                    f"Nuevo nombre [{dept.nombre}]: ").strip() or dept.nombre
                dept.gerente = input(
                    f"Nuevo gerente [{dept.gerente}]: ").strip() or dept.gerente
                dept.actualizar_departamento()
            else:
                print("Departamento no encontrado.")

        elif opcion == "5":
            print("\n--- ELIMINAR DEPARTAMENTO ---")
            id_dept = int(input("ID del departamento a eliminar: ").strip())
            confirmar = input("¿Está seguro? (s/n): ").strip().lower()
            if confirmar == 's':
                Departamento.eliminar_departamento(db, id_dept)
            else:
                print("Operación cancelada.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def menu_proyectos(db):
    """Menú de gestión de proyectos"""
    while True:
        print("\n" + "="*60)
        print("    GESTIÓN DE PROYECTOS")
        print("="*60)
        print("1. Crear proyecto")
        print("2. Listar proyectos")
        print("3. Editar proyecto")
        print("4. Eliminar proyecto")
        print("0. Volver al menú principal")
        print("="*60)

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- CREAR PROYECTO ---")
            nombre = input("Nombre del proyecto: ").strip()
            descripcion = input("Descripción: ").strip()
            fecha_inicio = input("Fecha inicio (YYYY-MM-DD) [hoy]: ").strip()
            fecha_termino = input(
                "Fecha término (YYYY-MM-DD) [opcional]: ").strip()

            fecha_inicio = datetime.strptime(
                fecha_inicio, "%Y-%m-%d").date() if fecha_inicio else date.today()
            fecha_termino = datetime.strptime(
                fecha_termino, "%Y-%m-%d").date() if fecha_termino else None

            proyecto = Proyecto(db, nombre=nombre, descripcion=descripcion,
                                fecha_inicio=fecha_inicio, fecha_termino=fecha_termino)
            proyecto.crear_proyecto()

        elif opcion == "2":
            print("\n--- LISTA DE PROYECTOS ---")
            proyectos = Proyecto.listar_proyectos(db)
            if proyectos:
                for proy in proyectos:
                    print(f"ID: {proy['id_proyecto']}, Nombre: {proy['nombre']}, "
                          f"Inicio: {proy['fecha_inicio']}, Término: {proy['fecha_termino']}")
                    print(f"  Descripción: {proy['descripcion']}\n")
            else:
                print("No hay proyectos registrados.")

        elif opcion == "3":
            print("\n--- EDITAR PROYECTO ---")
            id_proy = int(input("ID del proyecto a editar: ").strip())
            print("Funcionalidad en desarrollo.")

        elif opcion == "4":
            print("\n--- ELIMINAR PROYECTO ---")
            id_proy = int(input("ID del proyecto a eliminar: ").strip())
            confirmar = input("¿Está seguro? (s/n): ").strip().lower()
            if confirmar == 's':
                Proyecto.eliminar_proyecto(db, id_proy)
            else:
                print("Operación cancelada.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def menu_registro_tiempo(db):
    """Menú de registro de tiempo"""
    while True:
        print("\n" + "="*60)
        print("    REGISTRO DE TIEMPO")
        print("="*60)
        print("1. Registrar tiempo")
        print("2. Listar todos los registros")
        print("3. Consultar por empleado")
        print("4. Consultar por proyecto")
        print("0. Volver al menú principal")
        print("="*60)

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- REGISTRAR TIEMPO ---")
            fecha = input("Fecha (YYYY-MM-DD) [hoy]: ").strip()
            horas = int(input("Horas trabajadas: ").strip())
            descripcion = input("Descripción del trabajo: ").strip()
            id_empleado = int(input("ID del empleado: ").strip())
            id_proyecto = int(input("ID del proyecto: ").strip())

            fecha = datetime.strptime(
                fecha, "%Y-%m-%d").date() if fecha else date.today()

            registro = RegistroDeTiempo(db, fecha=fecha, horas=horas,
                                        descripcion=descripcion, id_empleado=id_empleado,
                                        id_proyecto=id_proyecto)
            registro.registrar_tiempo()

        elif opcion == "2":
            print("\n--- TODOS LOS REGISTROS ---")
            registros = RegistroDeTiempo.listar_registros(db)
            if registros:
                for reg in registros:
                    print(f"ID: {reg['id_registro']}, Fecha: {reg['fecha']}, "
                          f"Horas: {reg['horas']}, Empleado: {reg['id_empleado']}, "
                          f"Proyecto: {reg['id_proyecto']}")
                    print(f"  Descripción: {reg['descripcion']}\n")
            else:
                print("No hay registros de tiempo.")

        elif opcion == "3":
            print("\n--- CONSULTAR POR EMPLEADO ---")
            id_empleado = int(input("ID del empleado: ").strip())
            registros = RegistroDeTiempo.consultar_registro(
                db, id_empleado=id_empleado)
            if registros:
                total_horas = sum(r['horas'] for r in registros)
                print(f"\nRegistros del empleado {id_empleado}:")
                for reg in registros:
                    print(
                        f"  {reg['fecha']}: {reg['horas']} horas - Proyecto {reg['id_proyecto']}")
                print(f"\nTotal horas: {total_horas}")
            else:
                print("No hay registros para este empleado.")

        elif opcion == "4":
            print("\n--- CONSULTAR POR PROYECTO ---")
            id_proyecto = int(input("ID del proyecto: ").strip())
            registros = RegistroDeTiempo.consultar_registro(
                db, id_proyecto=id_proyecto)
            if registros:
                total_horas = sum(r['horas'] for r in registros)
                print(f"\nRegistros del proyecto {id_proyecto}:")
                for reg in registros:
                    print(
                        f"  {reg['fecha']}: {reg['horas']} horas - Empleado {reg['id_empleado']}")
                print(f"\nTotal horas: {total_horas}")
            else:
                print("No hay registros para este proyecto.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def menu_indicadores(db, usuario_actual=None):
    """Menú de indicadores económicos"""
    indicador_eco = IndicadorEconomico(db)

    while True:
        print("\n" + "="*60)
        print("    INDICADORES ECONÓMICOS")
        print("="*60)
        print("1. Consultar indicador por fecha")
        print("2. Consultar indicador por periodo")
        print("3. Ver historial de registros")
        print("4. Consultar registros por indicador")
        print("0. Volver al menú principal")
        print("="*60)

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            print("\n--- CONSULTAR INDICADOR POR FECHA ---")
            IndicadorEconomico.mostrar_indicadores()

            opcion_ind = input("\nSeleccione el indicador (1-6): ").strip()

            if opcion_ind not in IndicadorEconomico.INDICADORES:
                print("Opción inválida.")
                continue

            indicador_info = IndicadorEconomico.INDICADORES[opcion_ind]

            fecha_str = input("Ingrese fecha (YYYY-MM-DD) [hoy]: ").strip()
            if fecha_str:
                try:
                    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                except ValueError:
                    print("Formato de fecha inválido.")
                    continue
            else:
                fecha = date.today()

            # Consultar API
            resultado = indicador_eco.consultar_indicador_fecha(
                indicador_info['codigo'],
                fecha
            )

            if resultado:
                print(f"\n{'='*50}")
                print(f"Indicador: {resultado['nombre']}")
                print(f"Fecha: {resultado['fecha']}")
                print(
                    f"Valor: {resultado['valor']} {resultado.get('unidad_medida', '')}")
                print(f"{'='*50}")

                # Preguntar si desea guardar
                guardar = input(
                    "\n¿Desea guardar este registro? (s/n): ").strip().lower()
                if guardar == 's':
                    nombre_usuario = input(
                        "Ingrese su nombre de usuario: ").strip()
                    indicador_eco.registrar_indicador(
                        nombre_indicador=resultado['nombre'],
                        fecha_valor=resultado['fecha'],
                        valor=resultado['valor'],
                        usuario_consulta=nombre_usuario
                    )
            else:
                print("No se pudo obtener el indicador.")

        elif opcion == "2":
            print("\n--- CONSULTAR INDICADOR POR PERIODO ---")
            IndicadorEconomico.mostrar_indicadores()

            opcion_ind = input("\nSeleccione el indicador (1-6): ").strip()

            if opcion_ind not in IndicadorEconomico.INDICADORES:
                print("Opción inválida.")
                continue

            indicador_info = IndicadorEconomico.INDICADORES[opcion_ind]

            try:
                fecha_inicio_str = input("Fecha inicio (YYYY-MM-DD): ").strip()
                fecha_fin_str = input("Fecha fin (YYYY-MM-DD): ").strip()

                fecha_inicio = datetime.strptime(
                    fecha_inicio_str, "%Y-%m-%d").date()
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

                if fecha_inicio > fecha_fin:
                    print("La fecha de inicio debe ser menor que la fecha fin.")
                    continue

                # Consultar periodo
                resultados = indicador_eco.consultar_indicador_periodo(
                    indicador_info['codigo'],
                    fecha_inicio,
                    fecha_fin
                )

                if resultados:
                    print(f"\n{'='*60}")
                    print(f"Indicador: {resultados[0]['nombre']}")
                    print(f"Periodo: {fecha_inicio} a {fecha_fin}")
                    print(f"Total registros: {len(resultados)}")
                    print(f"{'='*60}\n")

                    for res in resultados:
                        fecha_valor = datetime.fromisoformat(
                            res['fecha'].replace('Z', '+00:00'))
                        print(
                            f"{fecha_valor.strftime('%Y-%m-%d')}: {res['valor']} {res.get('unidad_medida', '')}")

                    # Preguntar si desea guardar todos
                    guardar = input(
                        "\n¿Desea guardar estos registros? (s/n): ").strip().lower()
                    if guardar == 's':
                        nombre_usuario = input(
                            "Ingrese su nombre de usuario: ").strip()

                        contador = 0
                        for res in resultados:
                            if indicador_eco.registrar_indicador(
                                nombre_indicador=res['nombre'],
                                fecha_valor=res['fecha'],
                                valor=res['valor'],
                                usuario_consulta=nombre_usuario
                            ):
                                contador += 1

                        print(
                            f"\n✓ Se guardaron {contador} registros exitosamente.")
                else:
                    print("No se encontraron datos para el periodo especificado.")

            except ValueError:
                print("Formato de fecha inválido.")
                continue

        elif opcion == "3":
            print("\n--- HISTORIAL DE REGISTROS ---")
            registros = IndicadorEconomico.listar_registros(db)

            if registros:
                print(f"\nÚltimos {len(registros)} registros:")
                print(f"{'='*80}")
                for reg in registros:
                    print(
                        f"ID: {reg['id_indicador']} | {reg['nombre_indicador']}")
                    print(
                        f"  Fecha valor: {reg['fecha_valor']} | Valor: {reg['valor']}")
                    print(
                        f"  Consultado por: {reg['usuario_consulta']} el {reg['fecha_consulta']}")
                    print(f"  Proveedor: {reg['sitio_proveedor']}")
                    print("-" * 80)
            else:
                print("No hay registros guardados.")

        elif opcion == "4":
            print("\n--- CONSULTAR POR INDICADOR ---")
            nombre_buscar = input(
                "Ingrese nombre del indicador a buscar: ").strip()

            registros = IndicadorEconomico.consultar_por_indicador(
                db, nombre_buscar)

            if registros:
                print(f"\nRegistros encontrados: {len(registros)}")
                print(f"{'='*80}")
                for reg in registros:
                    print(
                        f"Fecha: {reg['fecha_valor']} | Valor: {reg['valor']}")
                    print(
                        f"Consultado por: {reg['usuario_consulta']} el {reg['fecha_consulta']}")
                    print("-" * 80)
            else:
                print("No se encontraron registros.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def main():
    """Función principal del sistema"""
    print("\n" + "="*60)
    print("    INICIANDO SISTEMA ECOTECH SOLUTIONS")
    print("="*60)

    db = Database()

    try:
        connection = db.conectar()

        if connection:
            print("Conexión a la base de datos.")
            db.create_tables()
            print("Esquema de base de datos listo.")

            while True:
                mostrar_menu_principal()
                opcion = input("\nSeleccione una opción: ").strip()

                if opcion == "1":
                    menu_empleados(db)
                elif opcion == "2":
                    menu_usuarios(db)
                elif opcion == "3":
                    menu_departamentos(db)
                elif opcion == "4":
                    menu_proyectos(db)
                elif opcion == "5":
                    menu_registro_tiempo(db)
                elif opcion == "6":
                    menu_indicadores(db)
                elif opcion == "0":
                    print("\n¡Gracias por usar el sistema!")
                    print("Cerrando conexión a la base de datos...")
                    break
                else:
                    print("Opción inválida. Intente nuevamente.")

    except Exception as e:
        print(f"Error fatal: {e}")

    finally:
        db.desconectar()
        print("Conexión cerrada correctamente.")
        print("\n" + "="*60)


if __name__ == "__main__":
    main()
