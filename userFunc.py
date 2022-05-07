from shema import allShema

def selectRelationShema(self):
        selected = int(input("Unesite shemu koju zelite: "))
        relationShema = self.shema.get(selected)
        self.r = relationShema[0]
        self.fr = relationShema[1]
        self.keyCandidates.clear()

def printRelations(self):
    print("Relacije:", end=" ")
    for r in self.r:
        print(r, end=" ")
    print()

def printFR(self):
    print("Funkcionalne Ovisnosti:")
    for k,v in self.fr.items():
        for el in v:
            print(k, "-->", el)

def printAllShema(self):
    for key, value in self.shema.items():
        print("shema ", key, ":", end="\n")
        print("relations: ", value[0])
        print("dependencies: ", value[1])
    

def addAttribute(self):
    numAttributes = int(input("Unesite zeljeni broj atributa: "))
    for i in range(numAttributes):
        attribute = input("Unesite atribut "+ str(i+1) + " :")
        if attribute not in self.r:
            self.r.extend(attribute)
        else:
            print("Atribut vec postoji u relaciji")

    self.r = list(dict.fromkeys(self.r))
    self.r.sort()

def eraseAttribute(self):
    numOfAttributes = int(input("Koliko atributa zelite izbrisati: "))
    for i in range(numOfAttributes):
        printRelations()
        attribute = input("Koji atribut zelite izbrisati: ")
        if attribute in self.r:
            self.r.remove(attribute)
        else:
            print("Atribut ne postoji u relaciji")

#dodat jednu funkciju koja provjerava jeli funkcionalna ovisnost dobra
def addFR(self):
    numOfFR = int(input("Koliko funkcionalnih ovisnosti zelite: "))
    for i in range(numOfFR):
        newfr = input("Unesite funkcijsku ovisnost  _ -> _ : ")
        newfr = newfr.split(" -> ")
        if(newfr[0] in self.fr.keys()):
            self.fr[newfr[0]].append(newfr[1])
        else:
            lista = []
            lista.append(newfr[1])
            self.fr[newfr[0]] = lista
    
def eraseFR(self):
    numOfFR = int(input("Koliko funkcionalnih ovisnosti zelite izbrisati: "))
    for i in range(numOfFR):
        self.printFR()
        delFr = input("Koju funkcionalnu ovisnost zelite izbrisati _ -> _ : ")
        delFr = delFr.split(" -> ")
        if(delFr[0] in self.fr.keys()):
            #na mjesu odabranog kljuca brisemo unesenu relaciju
            self.fr[delFr[0]].remove(delFr[1])
        else:
            print("Pogresan Unos")

    self.printFR()

def printKeyCandidates(self):
    self.addIfNotInFR()
    self.findKeys()
    print("Minimalni Kljucevi: ", self.findMinimalKeys())


def printMenu(self):
        print("Odaberite opciju koju zelite: ")
        print("1) Odabir relacijske sheme")
        print("2) Ispis relacijskih shema")
        print("3) Ispis atributa")
        print("4) Ispis funkcionalnih ovisnosti")
        print("5) Ispis trenutne relacijske sheme")
        print("6) Dodavanje atributa")
        print("7) Brisanje atributa")
        print("8) Dodavanje funkcionalnih ovisnosti")
        print("9) Brisanje funkcionalnih ovisnosti")
        print("10) Ispis kljuceva kandidata")
        print("11) 3. Normalna forma")
        print("12) BC forma") 
        print("13) Prestanak rada")
       