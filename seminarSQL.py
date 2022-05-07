import itertools
import userFunc
import os
from shema import allShema

class DataBase:
    def __init__(self):
        self.r =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.fr = {
            "A": ["EF"],
            "F": ["CH"],
            "I": ["DB"],
            "J": ["I"],
            "E": ["CD"]
        }

        self.frCopy = []
        self.expansionCandidates = []
        self.expansionCandidatesBCKP = []
        self.usedForExpansion = []
        self.rightArr = []
        self.leftArr = []
        self.keyCandidates = []
        self.attrNotInFR = []
        self.shema = allShema()
    
    selectRelationShema = userFunc.selectRelationShema 
    printRelations = userFunc.printRelations
    printFR = userFunc.printFR
    addFR = userFunc.addFR
    eraseFR = userFunc.eraseFR
    addAttribute = userFunc.addAttribute
    eraseAttribute = userFunc.eraseAttribute
    printMenu = userFunc.printMenu
    printKeyCandidates = userFunc.printKeyCandidates 
    printAllShema = userFunc.printAllShema

    def switch(self, argument):
        switcher = {
            1 : self.selectRelationShema,
            2: self.printAllShema,
            3: self.printRelations,
            4: self.printFR,
            5: [self.printRelations, self.printFR],
            6: self.addAttribute,
            7: self.eraseAttribute,
            8: self.addFR,
            9: self.eraseFR,
            10: self.printKeyCandidates,
            11: self.norm_form,
            12: self.BC_form,
            13: exit
        }
        (switcher[argument][0]() , switcher[argument][1]()) if(argument == 5) else switcher[argument]()

    def selectionMenu(self):
        self.printMenu()
        selected = int(input(">> "))
        self.switch(selected)

    def sortLRSides(self):
        self.rightArr = list(dict.fromkeys(self.rightArr))
        self.leftArr = list(dict.fromkeys(self.leftArr))
        self.rightArr.sort()
        self.leftArr.sort()
    
    #2 donje funkcije ce nac sve atribute kojih nema u rjecniku 
    def checkIfInFR(self, r):
        for k, v in self.fr.items():
            if r in k:
                return False
            for str in v:
                if r in str:
                    return False
        return True
    
    def addIfNotInFR(self):
        for r in self.r:
            if(self.checkIfInFR(r)):
                self.attrNotInFR.extend(r)

    def addRelNotInFR(self):
        for el in self.attrNotInFR:
            self.leftArr.extend(el)
            self.rightArr.extend(el)

    def makeCopyFR(self):
        copyDict = {}
        for k, v in self.fr.items():
            copyDict[''.join(sorted(k))] = v
        return copyDict

    #ako vise ne postoji ni jedna kombinacija s desne strane medu funkcionalnim ovisnostima prosirujemo
    def expand(self, r):
        self.rightArr.extend(r)
        self.leftArr.extend(r)
        self.sortLRSides()

    #radi kombinacije iz desnog niza i provjerava jesu li u funkcionalnim ovisnostima
    def checkRightSide(self):
        for L in range(0, len(self.rightArr)+1):
            for subset in itertools.combinations(self.rightArr, L):
                komb = ''.join(subset)
                if komb in self.frCopy.keys():
                    return True
        return False

    #puni desni niz atributima kojima prosirujemo 
    def addToRightSide(self,key):
        for k,v in self.fr.items():
            if(key == k or ''.join(sorted(k)) == key):
                if(key in self.frCopy):
                    #ako smo iskoristili funkcionalnu ovisnost onda je brisemo 
                    self.frCopy.pop(key)
                for el in v:
                    self.rightArr.extend(el)
        self.sortLRSides()

    #prosit ce desnu stranu svim kombinacijama iz desne strane tj mogucim funkcionalnim ovisnostima
    def makeAllRelations(self):
        for L in range(0, len(self.rightArr)+1):
            for subset in itertools.combinations(self.rightArr, L):
                komb = ''.join(sorted(subset))
                self.addToRightSide(komb)

    #vraca relacije koje nemamo
    def returnRelationsExp(self):  
        relArr = []
        for el in self.r:
            if el not in self.rightArr: # and el not in self.attrNotInFR:
                relArr.extend(el)
        return relArr
    
    def expansion(self, arr):
        for k in self.frCopy:
            if k in arr:
                return k
        return None

    def checkCandidate(self):
        while(self.rightArr != self.r):
            #provjeri postoji li ikoja kombinacija iz desne  strane s kojom bismo mogli prosirit
            if(self.checkRightSide()):
                self.makeAllRelations()
             
            #ako ne postoji onda prosiri
            else:
                #expansionArr = self.returnRelationsExp()
                expansionArr = self.expansionCandidatesBCKP
                # provjeri sve kandidate za sirenje
                for r in expansionArr:
                    if r not in self.expansionCandidates and r not in self.usedForExpansion:
                        self.expansionCandidates.extend(r)
                
                # ako trenutni kljuc nije kandidat prestajemo s pretragom i brisemo koristene
                if not self.expansionCandidates:
                    return False

                # uzimamo jednog od kandidata, s kojim sirimo
                key = self.expansion(self.expansionCandidates) if(self.expansion(self.expansionCandidates)) else self.expansionCandidates[0]
                
                self.expansionCandidates.remove(key)
                self.usedForExpansion.extend(key)
                
                self.expand(key)

        return True
            
    def findCandidateKey(self):
        #radi dok desna strana nije ista kao relacije, ako ne moze nac vise funkcionalnih ovisnosti vraca false, ako nade kandidata vraca true
        if(self.checkCandidate()):
            stra = ""
            stra = stra.join(self.leftArr)
            if(stra not in self.keyCandidates):
                self.keyCandidates.append(stra)
        #brisi stare relacije i vrati se na pocetno stanje
        self.leftArr.clear()
        self.rightArr.clear()
        self.frCopy.clear()
        self.usedForExpansion.clear()

    def findMinimalKeys(self):
        minimalKeys = []
        minLen = len(min(self.keyCandidates, key=len))
        for key in self.keyCandidates:
            if len(key) == minLen:
                minimalKeys.append(key)
        return minimalKeys

    def findKeys(self):
        for r in self.fr:
            #prosiri livu i desnu stranu sa slovom
            self.expand(r)
            self.addRelNotInFR()
            self.usedForExpansion.clear()
            self.frCopy = self.makeCopyFR()
            #dodaj u desnu stranu sve moguce kombinacije iz funkcionalnih ovisnosti i obrisi iz rezervnog dictionaryja
            self.addToRightSide(r)
            #pronaci sve relacije koje moramo provjeriti
            self.expansionCandidatesBCKP = self.returnRelationsExp()
            #radi dok desna strana nije ista kao relacije ili dok ne moze naci vise kombinacija, kad zavrsi brise livi i desni niz i postavlja novi dict
            self.findCandidateKey()
            #provjerava sve ostale kandidate za prosirenje s trenutnim slovom
            
            while(self.expansionCandidatesBCKP):
                self.frCopy = self.makeCopyFR()
                self.expansionCandidatesBCKP.pop(0)
                self.usedForExpansion.clear()
                self.expand(r)
                self.addRelNotInFR()
                self.addToRightSide(r)
                self.findCandidateKey()
 
    def norm_form(self):
        #kreiramo niz 
        ro =[]
        #petlja kojom prolazimo kroz funkcijske ovisnosti
        for k,v in self.fr.items():
            print("".join(k) + "->" + "".join(v) +" unija ",ro)
            #sljedece 2 linije koda pretvaramo kljuc i vrijednost u string da bi ih u trecoj liniji koda lakse zbrojili
            a = "".join(k)
            b = "".join(v)
            if(len(v) > 1):
                for i in v:
                  c = a + i
                  c = "".join(sorted(c))
                  if(c not in ro):
                     ro.append(c)
            else:
                c = a+b
                c = "".join(sorted(c))
                if c not in ro:
                  ro.append(c)
            #zlatna naredba any :-)...provjerava da li igdje u ro-u postoji c(koji je poveznica dva stringa a i b)
            
        #ukoliko se kljuc ne pojavljuje u ro...dodamo ga
        niz = self.findMinimalKeys()
        d = niz[0]
        if not any(d in f for f in ro):
            ro.append(d)
            print(ro)
        print()
        print("RO: ",ro)
        print()


    def BC_form(self):
        #stvaramo string i u sljedece 2 linije koda spremamo cilu relaciju u jedan string
            rel = ""
            
            for i in self.r:
                rel += i
            
            #sljedece 3 linije koda kao i u prsoloj funkciji
            for k,v in self.fr.items():
                print("".join(k) + "->" + "".join(v) + " unija " + rel)
                a = "".join(k)
                b = "".join(v)
                
                #radimo listu od stringa...odnosno razdvajamo svako slovo za sebe da bi mogli provjerit postoji li cijela desna 
                # strana negde u stringu relacije
                c = list(b)
                
                #ako postoji....mijenjamo ga sa praznim stringom posto je string nepromjenjiv i ne mozemo brisati elemente
                if (b in rel):
                    rel = rel.replace(b, "")
                #sljedeca for petlja provjerava dali cijela desna strana postoji u stringu relacije....ukoliko ne 
                # postoji ne mozemo brisati ta slova iz relacije

                arr = []
                for i in c:
                    if i not in rel:
                        arr.clear()
                        break;
                    else:
                        arr.append(i) 
                

                for i in arr:
                    rel = rel.replace(i,"")
                

                
            print()
            print("REST: ", rel)
            #kada smo dosli do kraja i vise nemamo FO potrebno je projeriti da li u ostatku postoji kombinacija da se nalazi u minimalnim kljucevima
            #zbog toga radimo 2 stringa u jedan spemamo kandidate za provjeru(newstr) a u rest spreammo ona slova koja ne postoje u minimalnim kljucevima
            niz = self.findMinimalKeys()
            newstr = ""
            rest = ""
            f = "".join(niz)
            for e in rel:
                if any(e in s for s in f):
                    newstr += "".join(e)
                if not any(e in s for s in f):
                    rest += "".join(e)
            sr = "".join(sorted(newstr))
            #radimo novi niz gdje sortiramo svaki od minimalnih kljuceva kako bi laske provjerili rjesenje zadatka
            arr2 = []
            for i in niz:
                res = "".join(sorted(i))
                arr2.append(res)
            print()
            #ukoliko postoji rjesenje dobijemo minimalni kljuc koji postoji u min kljucevima koji ce odredivati ostatak(rest)
            if sr in arr2 and rest:
                print("Imamo rjesenje u kljucevima relacije: ", sr + "->" + rest)
            elif sr in arr2:
                print("Imamo rjesenje u kljucevima relacije: ", sr)
            else:
                print("Nemamo rjesenje.")
            print() 
db = DataBase()

while(True):
    db.selectionMenu()
    print()
    os.system("PAUSE")
