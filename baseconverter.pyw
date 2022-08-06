import subprocess
import math
import time
import tkinter as tk

# Program made By Jefik
# Link on GitHub: https://github.com/Jefik37/base-converter

def tentobase(numog, base):
    erro=False
    num=[] #lista para guardar os valores inteiros
    if numog[0]=='-':
        numog=numog[1:len(numog)]
        negativo=True
    decimais1=[] #lista para guardar os valores decimais, esta linha serve somente para não dar erro no return
    if '.' in numog: #checar decimais
        numseparado=numog.split('.') #separar inteiros e decimais
        numog=numseparado[0] #definir inteiros
        decimais=int(numseparado[1])/10**(len(numseparado[1])) #definir decimais e separar casas em lista
        decimais1=['.'] #lista para guardar os valores decimais
        while decimais!=int(decimais) and len(decimais1)<17: #calcular os decimais
            decimais*=base
            decimais1.append(str(math.floor(decimais))) #adicionar o valor inteiro da multiplicação na lista
            if decimais!=int(decimais): #se ainda tiver algum decimal:
                decimais-=math.floor(decimais) #remover a parte inteira do número
        for i in range (1, len(decimais1)): #converter números maiores que 10 em letras e depois em string
            if int(decimais1[i])>=10:
                decimais1[i]=chr(int(decimais1[i])+55)
            decimais1[i]=str(decimais1[i])
        decimais1=''.join(decimais1) #transformar a lista em uma string

    try:
        numog=int(numog)
    except:
        erro=True
    if not erro:
        if numog==int(numog):
            while numog//base!=0: #calcular os inteiros
                num.append(numog%base) #adicionar o resto na lista de inteiros
                numog=numog//base
            num.append(numog%base)
            for i in range (0, len(num)): #converter números maiores que 10 em letras e inverter a lista
                if num[i]>=10:
                    num[i]=chr(num[i]+55)
                num[i]=str(num[i])
            if negativo:
                num.append('-')
            num=''.join(num[::-1]) #transformar a lista em uma string


        if decimais1!=[]:
            return f'{num}{decimais1}'
        elif not erro:
            return num
    else:
        return 'Valor inválido.'



def basetoten(numog, base):
    erro=False
    newnum=0 #criar variável para o resultado
    num1=numog.lower() #deixar tudo em minúsculo
    if num1[0]=='-':
        negativo=True
        num1=num1[1:len(num1)]
    if '.' in num1: #checar decimais
        numseparado=num1.split('.') #separar inteiros e decimais
        num1=numseparado[0] #definir inteiros
        decimais=list(numseparado[1]) #definir decimais e separar casas em lista

        for i in range (0, len(decimais)): #converter decimais em base 10
            if not decimais[i].isdigit(): #se for letra:
                decimais[i]=str(ord(decimais[i])-87) #converter em número
            if int(decimais[i])>=base: #caso tenha alguma letra inválida:
                erro=True
            newnum+=float(decimais[i])*base**(-i-1) #valor+=dígito*(a sua posição). ex 0.a(base 12)=0.10*12^-1(base 10)
    num=list(num1) #separar casas da parte inteira em lista

    for i in range (0, len(num)): #calcular os inteiros
        if not num[i].isdigit(): #se for letra:
            num[i]=str(ord(num[i])-87) #converter em número
        if int(num[i])>=base: #caso tenha alguma letra inválida:
            erro=True
        newnum+=int(num[i])*base**(len(num)-i-1) #valor+=dígito*(a sua posição). ex b(base 12)=11*12^0(base 10)
    if negativo:
        newnum*=(-1)
    if not erro:
        return str(newnum)
    else:
        return 'Valor inválido.'



def calcular():
    copiarbtn['text']='Copiar'
    baseorigem=int(ent_baseog.get())
    basefinal=int(ent_basefinal.get())
    num=(nmr.get()).replace(' ', '')
    if num!='':
        if baseorigem==10 and basefinal!=10: #caso a base origem for 10
            nmr2['text']=tentobase(num, basefinal)
        elif baseorigem!=10 and basefinal==10: #caso a base final for 10
            nmr2['text']=basetoten(num, baseorigem)
        elif baseorigem!=10 and basefinal!=10: #caso nenhuma das bases for 10, o que exige um passo extra
            numto10=basetoten(num, baseorigem)
            if numto10!='Valor inválido.':
                nmr2['text']=tentobase(numto10, basefinal)
            else:
                nmr2['text']=numto10

def inverterbase():
    base1=ent_baseog.get()
    base2=ent_basefinal.get()
    ent_baseog.delete(0, tk.END)
    ent_basefinal.delete(0, tk.END)
    ent_baseog.insert(0, base2)
    ent_basefinal.insert(0, base1)

def inverterval():
    if nmr2['text']!='Valor inválido.' or (nmr.get()=='' and nmr2['text']==''):
        nmr.delete(0, tk.END)
        nmr.insert(0, nmr2['text'])
        nmr2['text']=''

def inverter():
    inverterbase()
    inverterval()
    calcular()

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def copiar():
    if nmr2['text']!='' and nmr2['text']!='Valor inválido.':
        numero=nmr2['text']
        copy2clip(numero)
        nmr2['text']='Copiado!'
        window.update()
        time.sleep(1)
        nmr2['text']=numero

def enter(x):
    if(x.char)=='\r':
        calcular()

cor="#303030" #padrão: #f0f0f0
cortexto='#989898'
corfonte='white'
window=tk.Tk()
window.title("Conversor de Bases")
window.resizable(False, False)
window.config(bg = cor)
window.bind("<Key>", enter)

for i in range(0,9):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)
window.rowconfigure(9, weight=1, minsize=15)



lbl_baseog = tk.Label(text="Base original:")
ent_baseog = tk.Entry(width=7)
lbl_baseog.grid(row=0, column=0, sticky='e', padx=(15, 0))
ent_baseog.grid(row=0, column=1, sticky='w')
lbl_baseog.config(bg = cor, fg= corfonte)


lbl_basefinal = tk.Label(text="Base final:")
ent_basefinal = tk.Entry(width=7)
lbl_basefinal.grid(row=0, column=1, sticky='e', padx=(80, 0))
ent_basefinal.grid(row=0, column=2, sticky='w', padx=(0, 15))
lbl_basefinal.config(bg = cor, fg= corfonte)


nmrlbl = tk.Label(text='Número original:')
nmr = tk.Entry(width=43)
nmrlbl.grid(row=6, column=0, columnspan=5, sticky='w', padx=(15, 0))
nmr.grid(row=7, column=0, columnspan=5, sticky='w', padx=(15, 0))
nmrlbl.config(bg = cor, fg= corfonte)


nmr2lbl = tk.Label(text='Número convertido:')
nmr2 = tk.Label(relief=tk.SUNKEN, width=28, bg='white')
nmr2lbl.grid(row=8, column=0, columnspan=5, sticky='w', padx=(15, 0))
nmr2.grid(row=9, column=0, columnspan=5, sticky='w', padx=(15, 0))
nmr2lbl.config(bg = cor, fg= corfonte)


btn = tk.Button(text='CONVERTER', height=4, width=15, command=calcular, font=60)
btn.grid(row=11, column=0, columnspan=5, sticky='e', pady=(5, 15), padx=15)
btn.config(bg = cortexto)


copiarbtn = tk.Button(text='Copiar', command=copiar, width='7')
copiarbtn.grid(row=9, column=0, columnspan=5, sticky='e', padx=15)
copiarbtn.config(bg = cortexto)


txtinv = tk.Label(text='Inverter:')
txtinv.grid(row=10, column=0, columnspan=5, sticky='nw', padx=15)
txtinv.config(bg = cor, fg= corfonte)


btn4 = tk.Button(text='Tudo', height=1, width=7, command=inverter)
btn4.grid(row=11, column=0, sticky='nw', padx=15, pady=(5,0))
btn4.config(bg = cortexto)


btn2 = tk.Button(text='Bases', height=1, width=7, command=inverterbase)
btn2.grid(row=11, column=0, sticky='w', pady=(0, 10), padx=15)
btn2.config(bg = cortexto)



btn3 = tk.Button(text='Números', height=1, command=inverterval)
btn3.grid(row=11, column=0, sticky='sw', pady=(0, 15), padx=15)
btn3.config(bg = cortexto)



window.mainloop()
