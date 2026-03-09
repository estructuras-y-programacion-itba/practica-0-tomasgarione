import random
import csv

def inicializar_planilla():
    planilla=[]
    for i in range(10):
        planilla.append(None)
    return planilla

def categorias():
    return ["E","F","P","G","1","2","3","4","5","6"]

def tirar_dados(cantidad):
    dados=[]
    for i in range(cantidad):
        dados.append(random.randint(1,6))
    return dados

def contar_dados(dados):
    conteo=[0,0,0,0,0,0,0]
    for d in dados:
        conteo[d]+=1
    return conteo

def es_generala(conteo):
    for c in conteo:
        if c==5:
            return True
    return False

def es_poker(conteo):
    for c in conteo:
        if c==4:
            return True
    return False

def es_full(conteo):
    tiene3=False
    tiene2=False
    for c in conteo:
        if c==3:
            tiene3=True
        if c==2:
            tiene2=True
    return tiene3 and tiene2

def es_escalera(dados):
    d=dados[:]
    d.sort()
    if d==[1,2,3,4,5]:
        return True
    if d==[2,3,4,5,6]:
        return True
    return False

def calcular_puntos(cat,dados):
    if cat=="E":
        if es_escalera(dados):
            return 20
        return 0
    if cat=="F":
        if es_full(contar_dados(dados)):
            return 30
        return 0
    if cat=="P":
        if es_poker(contar_dados(dados)):
            return 40
        return 0
    if cat=="G":
        if es_generala(contar_dados(dados)):
            return 50
        return 0
    numero=int(cat)
    suma=0
    for d in dados:
        if d==numero:
            suma+=d
    return suma

def guardar_csv(j1,j2):
    cats=categorias()
    archivo=open("jugadas.csv","w",newline="")
    writer=csv.writer(archivo)
    writer.writerow(["jugada","j1","j2"])
    for i in range(len(cats)):
        writer.writerow([cats[i],j1[i],j2[i]])
    archivo.close()

def elegir_dados_guardar(dados):
    print("\nDados actuales:")
    for i in range(len(dados)):
        print(i+1,":",dados[i])
    texto=input("Posiciones de dados a guardar (ej: 1 3 5) o Enter para ninguno: ")
    guardados=[]
    nuevos=[]
    if texto=="":
        return [],dados
    posiciones=texto.split()
    for i in range(len(dados)):
        if str(i+1) in posiciones:
            guardados.append(dados[i])
        else:
            nuevos.append(dados[i])
    return guardados,nuevos

def elegir_categoria(planilla,dados,tirada):
    cats=categorias()
    conteo=contar_dados(dados)
    if es_generala(conteo) and tirada==1:
        print("GENERALA REAL")
        planilla[3]=80
        return True
    print("\nCategorias disponibles:")
    for i in range(len(cats)):
        if planilla[i]==None:
            print(cats[i])
    cat=input("Elegir categoria: ")
    indice=cats.index(cat)
    puntos=calcular_puntos(cat,dados)
    if tirada==1 and cat in ["E","F","P"] and puntos>0:
        puntos+=5
    planilla[indice]=puntos
    return False

def turno(planilla,jugador):
    dados=tirar_dados(5)
    guardados=[]
    tirada=1
    while tirada<=3:
        print("\nJugador",jugador)
        print("Tirada",tirada)
        print("Guardados:",guardados)
        print("Dados:",dados)
        if tirada==3:
            break
        g,dados_restantes=elegir_dados_guardar(dados)
        guardados=guardados+g
        if len(guardados)==5:
            dados=[]
            break
        decision=input("Volver a tirar? (s/n): ")
        if decision=="n":
            dados=dados_restantes
            break
        dados=tirar_dados(5-len(guardados))
        tirada+=1
    dados_finales=guardados+dados
    return elegir_categoria(planilla,dados_finales,tirada)

def fin_del_juego(j1,j2,generala_real):
    if generala_real:
        return True
    for i in range(len(j1)):
        if j1[i]==None or j2[i]==None:
            return False
    return True

def mostrar_ganador(j1,j2):
    p1=0
    p2=0
    for v in j1:
        if v!=None:
            p1+=v
    for v in j2:
        if v!=None:
            p2+=v
    print("\nPuntaje final")
    print("Jugador 1:",p1)
    print("Jugador 2:",p2)
    if p1>p2:
        print("Gana Jugador 1")
    elif p2>p1:
        print("Gana Jugador 2")
    else:
        print("Empate")

def main():
    j1=inicializar_planilla()
    j2=inicializar_planilla()
    generala_real=False
    jugador=1
    while not fin_del_juego(j1,j2,generala_real):
        if jugador==1:
            generala_real=turno(j1,1)
            jugador=2
        else:
            generala_real=turno(j2,2)
            jugador=1
        guardar_csv(j1,j2)
    mostrar_ganador(j1,j2)

# No cambiar a partir de aqui
if __name__ == "__main__":
    main()
