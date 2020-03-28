#-*-coding: utf-8-*-
from random import choice
##############################################################################
# Variables globales
##############################################################################

# Crea las letras minúsculas a-z
letrasProposicionales = [chr(x) for x in range(97, 123)]
# inicializa la lista de interpretaciones
listaInterpsVerdaderas = []
# inicializa la lista de hojas
listaHojas = []

##############################################################################
# Definición de objeto tree y funciones de árboles
##############################################################################

class Tree(object):
	def __init__(self, label, left, right):
		self.left = left
		self.right = right
		self.label = label
	def get_label(self):
		return self.label
	def __str__(self):
		return "Tree({0},{1},{2})".format( self.label, self.left, self.right)

def Inorder(f):
	# Imprime una formula como cadena dada una formula como arbol
	# Input: tree, que es una formula de logica proposicional
	# Output: string de la formula
	if f.right == None:
		return f.label
	elif f.label == '-':
		return f.label + Inorder(f.right)
	else:
		return "(" + Inorder(f.left) + f.label + Inorder(f.right) + ")"

def StringtoTree(A):
	# Crea una formula como tree dada una formula como cadena escrita en notacion polaca inversa
	# Input: A, lista de caracteres con una formula escrita en notacion polaca inversa
	# letrasProposicionales, lista de letras proposicionales
	# Output: formula como tree

	Conectivos = ['O','Y','>']
	Pila = []
	for c in A:
		if c in letrasProposicionales:
			Pila.append(Tree(c,None,None))
		elif c == '-':
			FormulaAux = Tree (c,None,Pila[-1])
			del Pila[-1]
			Pila.append(FormulaAux)
		elif c in Conectivos:
			FormulaAux = Tree (c, Pila[-1], Pila[-2])
			del Pila[-1]
			del Pila[-1]
			Pila.append(FormulaAux)
	return Pila[-1]

##############################################################################
# Definición de funciones de tableaux
##############################################################################

def imprime_hoja(H):
	cadena = "{"
	primero = True
	for f in H:
		if primero == True:
			primero = False
		else:
			cadena += ", "
		cadena += Inorder(f)
	return cadena + "}"

def par_complementario(l):
	# Esta función determina si una lista de solo literales
	# contiene un par complementario
	# Input: l, una lista de literales
	# Output: True/False

	#Entra de esta manera: lista=[Tree(q,None,None), Tree(-,None,Tree(p,None,None)),Tree(r,None,None)]

	#Hacer una lista de la forma[p,-p,q]
	mi_lista=[]
	for item in l:
		if item.label=='-':
			mi_lista.append('-'+item.right.label)
		else:
			mi_lista.append(item.label)
	#Comprobar si hay pares complementarios

	for elem in mi_lista:
		if elem[0]=='-':
			complementario=elem[1]
			if complementario in mi_lista:
				return True
		else:
			complementario='-'+elem[0]
			if complementario in mi_lista:
				return True
	return False

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
	#El input tiene esta forma: Tree(p,None,None)
	Conectivos = ['O','Y','>']
	if f.label in Conectivos:
		return False
	elif f.label=='-':
		Conectivos.append('-')
		x = f.right
		if x.label in Conectivos:
			return False
		else:
			return True
	return True


def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
	count=1
	for formula in l:
		if es_literal(formula)== False: #Si no es literal
			print(formula)
			break
		else:
			print("Sigo Viva")
	return False



def alfa_beta(f):
	if f.label=='-':
		if (f.right).label=='-': #Doble negación
			return '1ALFA'
		elif (f.right).label=='O': #¬(A1vA2)
			return '3ALFA'
		elif (f.right).label=='>': #¬(A1>A2)
			return '4ALFA'
		elif (f.right).label=='Y': #¬(B1∧B2)
			return '1BETA'
		else:
			return 'HOJA'
	elif f.label=='Y': #(A1∧ A2)
		return '2ALFA'
	elif f.label=='O': #(B1 ∨ B2)
		return '2BETA'
	elif f.label=='>':
		return '3BETA'
	else:
		return 'HOJA'

def clasifica_y_extiende(f):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# Output: no tiene output, pues modifica la variable global listaHojas
	global listaHojas
	listaHojas=[[f]]
	print(imprime_hoja(listaHojas[0]))
	clasificacion = alfa_beta(f)
	if clasificacion=='HOJA':
		listaHojas.remove([f])
		listaHojas.append(f)
	elif clasificacion == '1ALFA':
		hijo=[(f.right).right]
		listaHojas.remove([f])
		listaHojas.append(hijo)
	elif clasificacion=='2ALFA':
	  	hijo_izq=f.left
	  	hijo_der=f.right
	  	listaHojas.remove([f])
	  	lis=[hijo_izq,hijo_der]
	  	listaHojas.append(lis)
	elif clasificacion=='3ALFA':
	  	hijo_izq=Tree('-',None,(f.right).left)
	  	hijo_der=Tree('-',None,(f.right).right)
	  	listaHojas.remove([f])
	  	lis=[hijo_izq,hijo_der]
	  	listaHojas.append(lis)
	elif clasificacion=='4ALFA':
	  	hijo_izq=(f.right).left
	  	hijo_der=Tree('-',None,(f.right).right)
	  	listaHojas.remove([f])
	  	lis=[hijo_izq,hijo_der]
	  	listaHojas.append(lis)
	elif clasificacion=='1BETA':
	  	hijo_izq=[Tree('-',None,(f.right).left)]
	  	hijo_der=[Tree('-',None,(f.right).right)]
	  	listaHojas.remove([f])
	  	listaHojas.append(hijo_izq)
	  	listaHojas.append(hijo_der)
	elif clasificacion=='2BETA':
	  	hijo_izq=[f.left]
	  	hijo_der=[f.right]
	  	listaHojas.remove([f])
	  	listaHojas.append(hijo_izq)
	  	listaHojas.append(hijo_der)
	elif clasificacion=='3BETA':
	  	hijo_izq=[Tree('-', None, f.left)]
	  	hijo_der=[f.right]
	  	listaHojas.remove([f])
	  	listaHojas.append(hijo_izq)
	  	listaHojas.append(hijo_der)
	return listaHojas
def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	# verdadera a f
	A = StringtoTree(f)
	listaHojas = [[A]]
	while len(listaHojas) > 0:
		hojas = choice(listaHojas)
		if not no_literales(hojas):
			for tree in hojas:
				clasifica_y_extiende(tree)
		else:
			if par_complementario(hojas):
				listaHojas.remove(hojas)
			else:
				listaInterpsVerdaderas.append(hojas)
				listaHojas.remove(hojas)
	return listaInterpsVerdaderas

lista=[Tree("q",None,None), Tree("-", None, Tree("-",None,Tree("q",None,None))),Tree("r",None,None)]
a=par_complementario(lista)
print(a)
