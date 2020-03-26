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

	conectivos_binarios=["V","&","->","<->"]
	formula=[]
	
	for cchh in A:
		if cchh in letrasProposicionales:
			formula.append(Tree(cchh, None, None))
		elif cchh == "-":
			formula.append(Tree(cchh,None,formula[-1]))
			del formula[-1]
		elif cchh in conectivos_binarios:
			formula.append(Tree(cchh, formula[-1],formula[-2]))
			del formula[-1]
			del formula[-1]
		return formula[-1]

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
	
	#Crear lista de labels literales
	literales=[]
	for literal in l:
		if literal.get_label()=="-":
			literales.append("-"+(lteral.right).get_label())
		else:
			literales.append(literal.get_-label())
		
	#Verificar que hay pares complementarios
	lista= literales
	lit=lista[0]
	lista_aux=[]
	for i in range(1,len(lista)):
		lista_aux.append(lista[i])
	if lit[0]!="-":
		if "-"+lit in ista_aux:
			return True
		else:
			l=lista_aux
			par_complementario(l)
	else:
		if lit[-1] in lista_aux:
			return True
		else:
			l=lista_aux
			par_complementario(l)
	return False

def es_literal(f):
	# Esta función determina si el árbol f es un literal
	# Input: f, una fórmula como árbol
	# Output: True/False
	for i in f:
		if i.right==None:
			return True
		elif i.label=="-":
			if i.right.right==None:
				return True
			else:
				return False
		else:
			return False

def no_literales(l):
	# Esta función determina si una lista de fórmulas contiene
	# solo literales
	# Input: l, una lista de fórmulas como árboles
	# Output: None/f, tal que f no es literal
	for j in l:
		for es_literal(j)==False:
			return False
		else:
			return True

def clasifica_y_extiende(f):
	# clasifica una fórmula como alfa o beta y extiende listaHojas
	# de acuerdo a la regla respectiva
	# Input: f, una fórmula como árbol
	# Output: no tiene output, pues modifica la variable global listaHojas
	global listaHojas

def Tableaux(f):

	# Algoritmo de creacion de tableau a partir de lista_hojas
	# Imput: - f, una fórmula como string en notación polaca inversa
	# Output: interpretaciones: lista de listas de literales que hacen
	#		 verdadera a f
	global listaHojas
	global listaInterpsVerdaderas

	A = string2Tree(f)
	listaHojas = [[A]]

	return listaInterpsVerdaderas
