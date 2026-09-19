from pyDbModuleGen import Ui_MainWindow
from PySide6 import QtWidgets,QtGui
import json
import sys

def nettoyage(chaine:str)->str:
    resu=''
    for c in chaine:
        if c in ' ,?;.:/$^![]()':
            resu+='_'
        elif c in 'éèêë':
            resu+='e'
        elif c in 'àäâ':
            resu+='a'
        elif c=='ç':
            resu+='c'
        elif not c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_µ£@&²³':
            resu+='X'
        else:
            resu+=c
        resu=resu.strip()

    return resu

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)


        # Dico pour la structure DB à enregistrer : 
        self.database={'driver':'QSQLITE','name':'my_database','tables':[]}
        try:
            with open('GenDbConfig.txt',"rt") as myFile:
                dbName=myFile.read().strip()
                self.database['name']=dbName
                self.ui.EdDatabaseName.setText(dbName)
        except:
            pass
        # Connecter les events :
        self.ui.EdTableName.textChanged.connect(self.EdTableNameChange)
        self.ui.BtAddTable.clicked.connect(self.BtAddTable)
        self.ui.BtDeleteTable.clicked.connect(self.BtDeleteTable)
        self.ui.EdDbDriver.textChanged.connect(self.EdDriverChange)
        self.ui.EdDatabaseName.textChanged.connect(self.EdDBNameChange)
        self.ui.BtOpenJson.clicked.connect(self.BtOpenJson)
        self.ui.listTable.currentItemChanged.connect(self.LbTableChange)
        self.ui.BtGenerate.clicked.connect(self.BtGenerate)
        self.ui.BtSaveJson.clicked.connect(self.BtSaveJson)

        for icompo in range(len(self.ui.compo)):
            self.ui.compo[icompo]['Auto'].checkStateChanged.connect(self.CbAutoChange)
            self.ui.compo[icompo]['PK'].checkStateChanged.connect(self.CbPKChange)
            self.ui.compo[icompo]['FieldName'].textChanged.connect(self.EdFieldNameChange)
            if icompo>0:
                self.ui.compo[icompo]['BtUp'].clicked.connect(self.BtUpClick)
            self.ui.compo[icompo]['FieldLength'].textChanged.connect(self.EdFieldLengthChange)
            self.ui.compo[icompo]['FieldType'].currentTextChanged.connect(self.CbxFieldTypeChange)
            self.ui.compo[icompo]['Unique'].checkStateChanged.connect(self.CbUniqueChange)
            self.ui.compo[icompo]['NotNull'].checkStateChanged.connect(self.CbNotNullChange)
            self.ui.compo[icompo]['FKTable'].currentTextChanged.connect(self.CbxFKTableChange)
            self.ui.compo[icompo]['FKField'].currentTextChanged.connect(self.CbxFKFieldChange)
        self.TableChangeInProgress=False
        # Cacher les fields
        for icompo in range(len(self.ui.compo)):
            self.setFieldLineVisible(icompo,False,False)

    # find the position of sender in the components dictionary list
    def FindCompoIndex(self,sender,Column):
        print('FindCompoIndex DEB')
        index=0
        for icompo in range(len(self.ui.compo)):
            if Column!='BtUp' or icompo>0: # BtUp commence à 1 et pas à 0 !!!
                if (self.ui.compo)[icompo][Column]==sender:
                    index=icompo 
                    break
        print('FindCompoIndex FIN')
        return index

    # return the fields list of the selected table in listTable from self.database dictionary        
    def getCurrentFieldsList(self):
        tablesList=self.database['tables']
        if len(tablesList)==0 :
            return None
        if self.ui.listTable.currentRow()>=0:
            tableName=self.ui.listTable.currentItem().text().strip()
            return tablesList[self.ui.listTable.currentRow()][tableName]
        else:
            return None
        
    # get field dictionary by number from database dictionary
    def moveFieldUp(self,Number):
        fieldList=self.getCurrentFieldsList()
        temp=fieldList[Number]
        fieldList.insert(Number-1,temp)
        fieldList.pop(Number+1)


    # return the list of PK fields from à table whith a filter on field type
    def getPKList(self,tableName,FieldType):
        result=['']
        for dicotable in self.database['tables']:
            for table in dicotable.keys():
                if table==tableName:
                    for dicofield in dicotable[table]:
                        if dicofield['PK'] and dicofield['FieldType']==FieldType:
                            result.append(dicofield['FieldName'])
        return result
    
    #show or hide à field line on screen
    def setFieldLineVisible(self,num,LineVisible,FieldNameVisible):
        self.ui.compo[num]['Auto'].setVisible(False)
        self.ui.compo[num]['PK'].setVisible(LineVisible)
        self.ui.compo[num]['FieldName'].setVisible(LineVisible or FieldNameVisible)
        if num>0:
            self.ui.compo[num]['BtUp'].setVisible(LineVisible)
        self.ui.compo[num]['FieldType'].setVisible(LineVisible)
        # self.ui.compo[num]['FieldLength'].setVisible(LineVisible)
        self.ui.compo[num]['Unique'].setVisible(LineVisible)
        self.ui.compo[num]['NotNull'].setVisible(LineVisible)
        self.ui.compo[num]['FKTable'].setVisible(LineVisible)
        self.ui.compo[num]['FKField'].setVisible(self.ui.compo[num]['FKTable'].currentText() !='')
        # if self.ui.compo[num]['PK'].isVisible():
        #     self.sender=self.ui.compo[num]['PK']
        self.checkAuto()

    # Vérifier visibilité des cases Auto ...
    def checkAuto(self):
            nbPKChecked=[]
            for icompo in range(len(self.ui.compo)):
                if self.ui.compo[icompo]['PK'].isChecked():
                    nbPKChecked.append(icompo)
            self.ui.lbAuto.setVisible(False)
            if len(nbPKChecked)==1: # un seul PK Coché => si FieldType=Integer : AutoIncrement visible
                for icompo in range(len(self.ui.compo)):
                    if self.ui.compo[icompo]['PK'].isChecked() and self.ui.compo[icompo]['FieldType'].currentText()=='INTEGER':
                        self.ui.compo[icompo]['Auto'].setVisible(True)
                        self.ui.lbAuto.setVisible(True)
                    else:    
                        self.ui.compo[icompo]['Auto'].setChecked(False)
                        self.ui.compo[icompo]['Auto'].setVisible(False)

            if len(nbPKChecked)>1 or len(nbPKChecked)==0: # pas de PK ou PK composée => pas de clé AutoIncrementale
                for icompo in range(len(self.ui.compo)):
                    self.ui.compo[icompo]['Auto'].setChecked(False)
                    self.ui.compo[icompo]['Auto'].setVisible(False)
            # Maj des champs Auto dans dico database
            fieldsList=self.getCurrentFieldsList()
            if fieldsList != None:
                for icompo in range(len(fieldsList)):
                    try:
                        fieldsList[icompo]['Auto']=self.ui.compo[icompo]['Auto'].isChecked()
                    except:
                        pass


    def EdTableNameChange(self):
        self.ui.EdTableName.setText(nettoyage(self.ui.EdTableName.text()))
        

    def BtAddTable(self):
        if self.ui.EdTableName.text().strip()!='':
            self.ui.EdTableName.setText(nettoyage(self.ui.EdTableName.text()))
            self.ui.listTable.addItem(self.ui.EdTableName.text().strip())
            self.ui.listTable.setCurrentRow(self.ui.listTable.count()-1)
            self.database['tables'].append({self.ui.EdTableName.text().strip():[]})
            # create list entries for the fields
            FieldsList=self.database['tables'][len(self.database['tables'])-1][self.ui.EdTableName.text().strip()]
            for i in range(10):
                FieldsList.append({})
                FieldsList[i]['Auto']=False
                FieldsList[i]['PK']=False
                FieldsList[i]['FieldName']=''
                FieldsList[i]['FieldType']=self.ui.SqQLiteDataType[0]
                FieldsList[i]['FieldLength']=''
                FieldsList[i]['Unique']=False
                FieldsList[i]['NotNull']=False
                FieldsList[i]['FKTable']=''
                FieldsList[i]['FKField']=''
                if i==0:
                    self.setFieldLineVisible(i,False,True)
                else:
                    self.setFieldLineVisible(i,False,False)
            self.ui.EdTableName.clear()
            self.ui.listTable.setCurrentRow(self.ui.listTable.count()-1)
            # maj combo FKTable
            listFKTable=['']
            for i in range(self.ui.listTable.count()-1):
                listFKTable.append(self.ui.listTable.item(i).text())
            for icompo in range(len(self.ui.compo)):
                self.ui.compo[icompo]['FKTable'].clear()    
                self.ui.compo[icompo]['FKTable'].addItems(listFKTable)


    def BtDeleteTable(self):
        # get Item
        item=self.ui.listTable.item(self.ui.listTable.currentRow())
        # remove key from dictionary
        idb=0
        for idb in range(len(self.database['tables'])):
            if item.text() in self.database['tables'][idb]:
                self.database['tables'].pop(idb)
                break
        # remove item from tables listBox
        self.ui.listTable.takeItem(self.ui.listTable.currentRow())

    def EdDriverChange(self):
        self.database['driver']=self.ui.EdDbDriver.text().strip()

    def EdDBNameChange(self):
        self.ui.EdDatabaseName.setText(nettoyage(self.ui.EdDatabaseName.text()))
        self.database['name']=self.ui.EdDatabaseName.text().strip()
        self.ui.BtSaveJson.setText(f'Save this config as {self.ui.EdDatabaseName.text().strip()}.json')
        self.ui.BtGenerate.setText(f'Generate {self.ui.EdDatabaseName.text().strip()}.py')
        try:
            with open('GenDbConfig.txt',"wt") as myFile:
                myFile.write(self.ui.EdDatabaseName.text().strip())
        except:
            pass    
    
    def BtOpenJson(self):
        fileName=self.ui.EdDatabaseName.text().strip()
        if fileName != '':
            self.ui.listTable.clear()
            try:
                with open(fileName+'.json') as jsonFile:
                    self.database=json.loads(jsonFile.read())
                for nomTable in self.database['tables']:
                    for nt in nomTable.keys():
                        self.ui.listTable.addItem(nt)
                if self.ui.listTable.count()>0:
                    self.ui.listTable.setCurrentRow(0)
            except:
                print(f'Erreur de lecture de [{fileName}.json]')

        
    
    def LbTableChange(self):
        self.TableChangeInProgress=True
        if self.ui.listTable.count()>0:
            fieldsList=self.getCurrentFieldsList()
            if fieldsList != None :
                nbPKChecked=0
                for icompo in range(len(self.ui.compo)):
                    self.ui.compo[icompo]['Auto'].setChecked(fieldsList[icompo]['Auto'])
                    self.ui.compo[icompo]['PK'].setChecked(fieldsList[icompo]['PK'])
                    self.ui.compo[icompo]['FieldName'].setText(fieldsList[icompo]['FieldName'])
                    self.ui.compo[icompo]['FieldType'].setCurrentText(fieldsList[icompo]['FieldType'])
                    self.ui.compo[icompo]['FieldLength'].setText(fieldsList[icompo]['FieldLength'])
                    self.ui.compo[icompo]['Unique'].setChecked(fieldsList[icompo]['Unique'])
                    self.ui.compo[icompo]['NotNull'].setChecked(fieldsList[icompo]['NotNull'])
                    tableList=['']
                    for itable in range(self.ui.listTable.count()):
                        if itable != self.ui.listTable.currentRow():
                            tableList.append(self.ui.listTable.item(itable).text())
                    self.ui.compo[icompo]['FKTable'].clear()
                    self.ui.compo[icompo]['FKTable'].addItems(tableList)
                    self.ui.compo[icompo]['FKTable'].setCurrentText(fieldsList[icompo]['FKTable'])
                    # FKField Visible si FKTable choisie
                    self.ui.compo[icompo]['FKField'].setVisible(self.ui.compo[icompo]['FKTable'].currentText()!='')
                    self.ui.compo[icompo]['FKField'].clear()
                    self.ui.compo[icompo]['FKField'].addItems(self.getPKList(self.ui.compo[icompo]['FKTable'].currentText(),self.ui.compo[icompo]['FieldType'].currentText()))
                    self.ui.compo[icompo]['FKField'].setCurrentText(fieldsList[icompo]['FKField'])
                    if fieldsList[icompo]['PK']:
                        nbPKChecked+=1
                    if icompo>0:
                        self.setFieldLineVisible(icompo,fieldsList[icompo]['FieldName'].strip()!='',fieldsList[icompo-1]['FieldName'].strip()!='')
                    else: # ligne 0 => fieldName tj visible
                        self.setFieldLineVisible(icompo,fieldsList[icompo]['FieldName'].strip()!='',True)
                    
                if nbPKChecked>1:
                    self.ui.lbAuto.setVisible(False)
                    for icompo in range(len(self.ui.compo)):
                        self.ui.compo[icompo]['Auto'].setChecked(False)
                        self.ui.compo[icompo]['Auto'].setVisible(False)
                        fieldsList[icompo]['Auto']=False
                else:
                    self.ui.lbAuto.setVisible(True)
                    if self.ui.compo[icompo]['PK'].isChecked() and self.ui.compo[icompo]['FieldType'].currentText()=='INTEGER':
                        self.ui.compo[icompo]['Auto'].setVisible(True)
        self.TableChangeInProgress=False



    def CbAutoChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'Auto')
            # get the compo value
            compoValue=self.ui.compo[index]['Auto'].isChecked()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['Auto']=compoValue


    def CbPKChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'PK')
            # get the compo value
            compoValue=self.ui.compo[index]['PK'].isChecked()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['PK']=compoValue
            self.checkAuto()


    def EdFieldNameChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            print(self.sender)
            index=self.FindCompoIndex(self.sender(),'FieldName')
            print( index)
            # get the compo value
            self.ui.compo[index]['FieldName'].setText(nettoyage(self.ui.compo[index]['FieldName'].text()))
            compoValue=self.ui.compo[index]['FieldName'].text().strip()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['FieldName']=compoValue
            # si dernièreligne avec FieldName non vide => ligne suivante visible
            # if self.ui.compo[index]['FieldName'].text()!='' and self.ui.compo[index+1]['FieldName'].text()=='':
            #     self.setFieldLineVisible(index+1,False,True)
            if index<9:
                self.setFieldLineVisible(index+1,self.ui.compo[index+1]['FieldName'].text().strip()!='',self.ui.compo[index]['FieldName'].text().strip()!='')
            self.setFieldLineVisible(index,self.ui.compo[index]['FieldName'].text().strip()!='',self.ui.compo[index]['FieldName'].text().strip()=='')

    def BtUpClick(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'BtUp')
            self.moveFieldUp(index)
            self.LbTableChange()
                    

    def CbxFieldTypeChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'FieldType')
            # get the compo value
            compoValue=self.ui.compo[index]['FieldType'].currentText()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['FieldType']=compoValue
            #verif si <> integer et PK => autoincrement interdit
            if self.ui.compo[index]['PK'].isChecked() and self.ui.compo[index]['FieldType'].currentText()!='INTEGER':
                if self.ui.compo[index]['Auto'].isChecked():
                    self.ui.compo[index]['Auto'].setChecked(False)
                    fieldsList[index]['Auto']=False
                    self.ui.lbAuto.setVisible(False)
       
        
    def EdFieldLengthChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'FieldLength')
            # get the compo value
            compoValue=str(int(self.ui.compo[index]['FieldLength'].text().strip()))
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['FieldLength']=compoValue


    def CbUniqueChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'Unique')
            # get the compo value
            compoValue=self.ui.compo[index]['Unique'].isChecked()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['Unique']=compoValue

    def CbNotNullChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'NotNull')
            # get the compo value
            compoValue=self.ui.compo[index]['NotNull'].isChecked()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['NotNull']=compoValue

    def CbxFKTableChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'FKTable')
            # get the compo value
            compoValue=self.ui.compo[index]['FKTable'].currentText()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['FKTable']=compoValue
            # Remplissage comboBox FKField sur base des champs de la FKTable choisie (PK)
            self.ui.compo[index]['FKField'].clear()
            self.ui.compo[index]['FKField'].addItems(self.getPKList(compoValue,self.ui.compo[index]['FieldType'].currentText()))
            self.ui.compo[index]['FKField'].setVisible(self.ui.compo[index]['FKTable'].currentText()!='')    
            self.ui.compo[index]['FKField'].setCurrentText(fieldsList[index]['FKField'])


    def CbxFKFieldChange(self):
        if not self.TableChangeInProgress:
            # get the compo index
            index=self.FindCompoIndex(self.sender(),'FKField')
            # get the compo value
            compoValue=self.ui.compo[index]['FKField'].currentText()
            # get the table field list
            fieldsList=self.getCurrentFieldsList()
            # update database dictionary
            fieldsList[index]['FKField']=compoValue
    
    def BtSaveJson(self):
        txt=json.dumps(self.database, indent=8)
        self.ui.EdResults.setPlainText(txt)
        fileName=self.ui.EdDatabaseName.text().strip()
        if fileName !='': # nom database non vide => sauver
            try:
                with open(f'{fileName}.json','w', encoding='utf8') as jsonFile:
                    jsonFile.write(txt)
            except:
                print(f'Problème pour sauvegarder [{fileName}.json]')    
    def findTable(self,nomTable,listTable):
        for nt in listTable:
            if nomTable in nt.keys():
                return nt[nomTable] # liste des dico fields
    
    def fieldListStr(self,tableName,autoIncrement):
        result=''
        for table in self.database['tables']:
            for tName in table.keys():
                if tName==tableName:
                    for field in table[tName]:
                        if field['FieldName'].strip()!='':
                            if autoIncrement or not field['Auto']:
                                result+=field['FieldName']+','
                    break
        return result[0:-1]
    
    def quotedStr(self,pStr):
        return "'"+pStr+"'"
    
    def fieldValueStr(self,tableName,autoIncrement):
        result=''
        for table in self.database['tables']:
            for tName in table.keys():
                if tName==tableName:
                    for field in table[tName]:
                        if field['FieldName'].strip()!='':
                            if autoIncrement or not field['Auto']:
                                if field['FieldType']in self.ui.SqQLiteStrDataType: # si chaine de catractère, il faut des apostrophes 
                                    result+=self.quotedStr('{'+field['FieldName']+'}')+','
                                else:
                                    result+='{'+field['FieldName']+'},'
                break
        return result[0:-1]
    
    def fieldNameValueStr(self,tableName,autoIncrement):
        result=''
        for table in self.database['tables']:
            for tName in table.keys():
                if tName==tableName:
                    for field in table[tName]:
                        if field['FieldName'].strip()!='':
                            if autoIncrement or not field['Auto']:
                                if field['FieldType']in self.ui.SqQLiteStrDataType: # si chaine de catractère, il faut des apostrophes 
                                    result+=field['FieldName']+'='+self.quotedStr('{'+field['FieldName']+'}')+','
                                else:
                                    result+=field['FieldName']+' = '+'{'+field['FieldName']+'},'
                break
        return result[0:-1]

    def listeTableFK(self):
        listTables=[] # liste des tables avec liste des foreign tables
        for dicotable in self.database['tables']:
            for table in dicotable.keys():
                if table.strip() !='':
                    listTables.append({'tableName':table,'FKTables':[]})
                    for dicofield in dicotable[table]:
                        if dicofield['FKTable'].strip() != '':
                            listTables[len(listTables)-1]['FKTables'].append(dicofield['FKTable'].strip())
        return listTables


    def txtCreateTable(self,nomTable,dicoTable):
        pkList=[]
        resu= '\n\t\t\tCREATE TABLE IF NOT EXISTS '+nomTable
        resu+='\n\t\t\t('
        # Liste des champs avec propriétés 
        for field in dicoTable:
            if field['FieldName'].strip() !='':
                resu+='\n\t\t\t\t'+field['FieldName']+' '+field['FieldType']
                if field['PK']:
                    if field['Auto']:
                        resu+=' PRIMARY KEY AUTOINCREMENT'
                    else:
                        resu+=' NOT NULL'
                        pkList.append(field['FieldName'].strip())
                else:
                    if field['Unique']:
                        resu+=' UNIQUE'
                    if field['NotNull']:
                        resu+=' NOT NULL'
                resu+=','
        # PRIMARY KEY si nécessaire
        if len(pkList)>0: # pas clé auto increment
            stPK=pkList[0]
            for i in range(1,len(pkList)):
                stPK+=', '+pkList[i]
            resu+='\n\t\t\t\t'+'PRIMARY KEY ('+stPK+'),'


        # Liste des Foregn Key
        for field in dicoTable:
            if field['FieldName'].strip() !='':
                if field['FKTable'].strip() !='': # It's a foreign key
                    resu+='\n\t\t\t\tFOREIGN KEY ('+field['FieldName']+') REFERENCES '+field['FKTable']+'('+field['FKField']+'),'
        # enlever la dernière virgule :
        resu=resu[0:-1]
        # fermer la parenthèse
        resu+='\n\t\t\t)'
        return resu

    def BtGenerate(self):
        # définir l'ordre de création des tables en fonction des Foreign Key
        #===================================================================
        listTables=self.listeTableFK() 
        # Trier la liste des tables
        if len(listTables)==0:
            return 0
        OrderedTables=[]
        nb=0
        while nb<=len(listTables) and len(OrderedTables)<len(listTables):
            for dicotable in listTables:
                table = dicotable['tableName']
                if table not in OrderedTables:
                    if len(dicotable['FKTables'])==0: # pas de table référencée
                        OrderedTables.insert(0,dicotable['tableName'])
                    else:
                        ok=True
                        for fk in dicotable['FKTables']:
                            if not fk in OrderedTables:
                                ok=False
                        if ok:
                            OrderedTables.append(dicotable['tableName'])
            nb+=1
        if nb>=len(listTables):
            print('=================================================')
            print(f'Référence circulaire ? Vérifiez vos foreign key \n{json.dumps(listTables,indent=4)}')
            print('=================================================')
            exit()

        # Ordre des Créations de tables défini par OrderedTables. On peut créer la procédure de création des tables
# =============================

#     AJOUTER TRY FINALLY !!!!!

# =============================
        # Entête du module .py
        # =====================
        result ='# Module généré par GenDB.py\n'
        result+='#===========================\n'
        result+='import sqlite3\n'
        result+='import pandas as pd\n\n'

        # CREATE ALL TABLES
        # =================
        result+='def createAllTables():\n'
        if self.database['driver']=='QSQLITE':
            result+='\tconn = sqlite3.connect("'+self.database['name'].strip()+'.db")\n'
        else:
            result+='\tconn = ??????.connect("'+self.database['name'].strip()+'.db")\n'
        result+='\tcur = conn.cursor()'

        for table in OrderedTables:
            result+="\n\t# "+table
            result+="\n\tcur.execute('''"
            result+= self.txtCreateTable(table,self.findTable(table,self.database['tables']))
            result+="\n\t\t\t''')\n"
        result+='\tconn.commit()\n'
        result+='\tconn.close()\n\n'

        # CREATE TABLE Table par table
        #==============================
        for table in OrderedTables:
            result+='def createTables_'+table+'():\n'
            if self.database['driver']=='QSQLITE':
                result+='\tconn = sqlite3.connect("'+self.database['name'].strip()+'.db")\n'
            else:
                result+='\tconn = ??????.connect("'+self.database['name'].strip()+'.db")\n'
            result+='\tcur = conn.cursor()'
            result+="\n\t# "+table
            result+="\n\tcur.execute('''"
            result+= self.txtCreateTable(table,self.findTable(table,self.database['tables']))
            result+="\n\t\t\t''')"
            result+='\n\tconn.commit()'
            result+='\n\tconn.close()\n\n'

        # INSERT Fonction pour l'insertion de donnée dans les tables
        # ==========================================================
        for table in OrderedTables:
            # str liste des champs
            paramFName=self.fieldListStr(table,False)
            fieldsValues=self.fieldValueStr(table,False)
               
            # generer la fonction 
            result+='# INSERT INTO '+table+'\n'
            result+='def insert_'+table+'('
            result+=paramFName            
            result+='):\n'
            if self.database['driver']=='QSQLITE':
                result+='\tconn = sqlite3.connect("'+self.database['name'].strip()+'.db")\n'
            else:
                result+='\tconn = ??????.connect("'+self.database['name'].strip()+'.db")\n'
            result+='\tcur = conn.cursor()'
            result+='\n\tsqlQuery="INSERT OR IGNORE INTO '+table+' ('+paramFName+') "'
            result+='\n\tsqlQuery+=f"VALUES ('+fieldsValues+')"'
            result+='\n\tcur.execute(sqlQuery)'
            result+='\n\tlastId = cur.lastrowid'
            result+='\n\tconn.commit()'
            result+='\n\tconn.close()'
            result+='\n\treturn lastId\n\n'

        # SELECT Fonctions d'extraction de données dans les tables
        # =========================================================
        for table in OrderedTables:
            # str liste des champs
            paramFName=self.fieldListStr(table,True)
            fieldsValues=self.fieldValueStr(table,True)
               
            # generer la fonction 
            result+='# SELECT fields FROM '+table+' WHERE condition\n'
            result+='def select_'+table+'(WHERE=""):\n'
            if self.database['driver']=='QSQLITE':
                result+='\tconn = sqlite3.connect("'+self.database['name'].strip()+'.db")\n'
            else:
                result+='\tconn = ??????.connect("'+self.database['name'].strip()+'.db")\n'
            result+='\tsqlQuery="SELECT '+paramFName+' FROM '+table+'"'
            result+='\n\tif WHERE.strip()!="":'
            result+='\n\t\tsqlQuery+=f" WHERE {WHERE}"'
            result+='\n\tdf = pd.read_sql_query(sqlQuery, conn)'
            result+='\n\tconn.close()'
            result+='\n\treturn df\n\n'

        # UPDATE Fonctions de modification de données existantes dans une table
        # =====================================================================
        for table in OrderedTables:
            # str liste des champs
            paramFName=self.fieldListStr(table,True)
            fieldsNameValues=self.fieldNameValueStr(table,True)
               
            # generer la fonction 
            result+='# UPDATE '+table+' SET fields=value WHERE condition\n'
            result+='def update_'+table+'('
            result+=paramFName            
            result+=',WHERE):\n'
            if self.database['driver']=='QSQLITE':
                result+='\tconn = sqlite3.connect("'+self.database['name'].strip()+'.db")\n'
            else:
                result+='\tconn = ??????.connect("'+self.database['name'].strip()+'.db")\n'
            result+='\tcur = conn.cursor()'
            result+='\n\tsqlQuery=f"UPDATE '+table+' SET '+fieldsNameValues+'"'
            result+='\n\tif WHERE.strip()!="":'
            result+='\n\t\tsqlQuery+=f" WHERE {WHERE}"'
            result+='\n\tcur.execute(sqlQuery)'
            result+='\n\tconn.commit()'
            result+='\n\tconn.close()\n\n'
            
        # DELETE Fonctions pour effacer des données existantes dans une table
        # =====================================================================
        for table in OrderedTables:
            # generer la fonction 
            result+='# DELETE FROM '+table+' WHERE condition \n'
            result+='# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!\n'
            result+='def delete_'+table+'(WHERE):\n'
            if self.database['driver']=='QSQLITE':
                result+='\tconn = sqlite3.connect("'+self.database['name'].strip()+'.db")\n'
            else:
                result+='\tconn = ??????.connect("'+self.database['name'].strip()+'.db")\n'
            result+='\tcur = conn.cursor()'
            result+='\n\tsqlQuery="DELETE FROM '+table+'"'
            result+='\n\tif WHERE.strip()!="":'
            result+='\n\t\tsqlQuery+=f" WHERE {WHERE}"'
            result+='\n\tcur.execute(sqlQuery)'
            result+='\n\tconn.commit()'
            result+='\n\tconn.close()\n\n'


        # DROP TABLE Fonctions pour détruire une table
        # =============================================
        for table in OrderedTables:
            # generer la fonction 
            result+='# DROP TABLE '+table+'\n'
            result+='# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée\n'
            result+='def drop_'+table+'():\n'
            if self.database['driver']=='QSQLITE':
                result+='\tconn = sqlite3.connect("'+self.database['name'].strip()+'.db")\n'
            else:
                result+='\tconn = ??????.connect("'+self.database['name'].strip()+'.db")\n'
            result+='\tcur = conn.cursor()'
            result+='\n\tsqlQuery="DROP TABLE '+table+'"'
            result+='\n\tcur.execute(sqlQuery)'
            result+='\n\tconn.commit()'
            result+='\n\tconn.close()\n\n'
            

        # ── Bloc Voodoo : fonctions supplementaires ─────────────────────────────
        dbName = self.database['name'].strip()

        # Lire les champs de la table machines (hors id/Auto)
        machineFields = []
        machineFieldTypes = {}
        for dicotable in self.database['tables']:
            if 'machines' in dicotable:
                for f in dicotable['machines']:
                    if f['FieldName'].strip() != '' and not f['Auto']:
                        machineFields.append(f['FieldName'].strip())
                        machineFieldTypes[f['FieldName'].strip()] = f['FieldType']

        result += '# ── Fonctions supplementaires Voodoo ──\n\n'

        result += 'def init_db():\n'
        result += '\tcreateAllTables()\n\n'

        result += 'def sauvegarder_prix(prix_series, date_str):\n'
        result += '\tconn = sqlite3.connect("' + dbName + '.db")\n'
        result += '\tcur = conn.cursor()\n'
        result += '\tcur.execute("DELETE FROM prix_electricite WHERE date = ?", (date_str,))\n'
        result += '\tfor timestamp, prix in zip(prix_series.index, prix_series.values):\n'
        result += '\t\theure_str = timestamp.strftime("%H:%M")\n'
        result += '\t\tcur.execute(\n'
        result += '\t\t\t"INSERT INTO prix_electricite (date, heure, prix) VALUES (?, ?, ?)",\n'
        result += '\t\t\t(date_str, heure_str, float(prix))\n'
        result += '\t\t)\n'
        result += '\tconn.commit()\n'
        result += '\tconn.close()\n\n'

        result += 'def charger_prix_db(date_str):\n'
        result += '\tconn = sqlite3.connect("' + dbName + '.db")\n'
        result += '\tdf = pd.read_sql_query(\n'
        result += '\t\t"SELECT heure, prix FROM prix_electricite WHERE date = ? ORDER BY heure",\n'
        result += '\t\tconn, params=(date_str,)\n'
        result += '\t)\n'
        result += '\tconn.close()\n'
        result += '\tif df.empty:\n'
        result += '\t\treturn None\n'
        result += '\treturn pd.Series(df["prix"].values, index=df["heure"].values)\n\n'

        # ajouter_machine : signature dynamique selon les champs reels de machines
        if machineFields:
            sigParts = []
            for f in machineFields:
                if machineFieldTypes.get(f) == 'INTEGER':
                    sigParts.append(f + '=0')
                else:
                    sigParts.append(f)
            sig  = ', '.join(sigParts)
            args = ', '.join(machineFields)
            result += 'def ajouter_machine(' + sig + '):\n'
            result += '\tinsert_machines(' + args + ')\n\n'
        else:
            result += 'def ajouter_machine(nom, operateur, email):\n'
            result += '\tinsert_machines(nom, operateur, email)\n\n'

        result += 'def ajouter_produit(nom, description):\n'
        result += '\treturn insert_produits(nom, description)\n\n'

        result += 'def ajouter_tache(produit_id, machine_id, puissance, duree, ordre):\n'
        result += '\tinsert_taches(produit_id, machine_id, puissance, duree, ordre)\n\n'

        result += 'def ajouter_commande(produit_id, heure_depart, cout_total, date):\n'
        result += '\treturn insert_commandes(produit_id, heure_depart, cout_total, date)\n\n'

        result += 'def get_machines():\n'
        result += '\treturn select_machines()\n\n'

        result += 'def get_produits():\n'
        result += '\treturn select_produits()\n\n'

        result += 'def select_taches(WHERE=""):\n'
        result += '\tconn = sqlite3.connect("' + dbName + '.db")\n'
        result += '\tsqlQuery = ("SELECT t.id, t.ordre, t.puissance, t.duree, "\n'
        result += '             "m.nom AS machine, m.operateur, m.email "\n'
        result += '             "FROM taches t "\n'
        result += '             "JOIN machines m ON t.machine_id = m.id")\n'
        result += '\tif WHERE.strip() != "":\n'
        result += '\t\tsqlQuery += f" WHERE {WHERE}"\n'
        result += '\tsqlQuery += " ORDER BY t.ordre"\n'
        result += '\tdf = pd.read_sql_query(sqlQuery, conn)\n'
        result += '\tconn.close()\n'
        result += '\treturn df\n\n'

        result += 'def get_taches_produit(produit_id):\n'
        result += '\treturn select_taches(f"t.produit_id = {produit_id}")\n\n'

        result += 'def select_commandes(WHERE=""):\n'
        result += '\tconn = sqlite3.connect("' + dbName + '.db")\n'
        result += '\tsqlQuery = ("SELECT c.id, p.nom AS produit, c.heure_depart, c.cout_total, c.date "\n'
        result += '             "FROM commandes c "\n'
        result += '             "JOIN produits p ON c.produit_id = p.id")\n'
        result += '\tif WHERE.strip() != "":\n'
        result += '\t\tsqlQuery += f" WHERE {WHERE}"\n'
        result += '\tsqlQuery += " ORDER BY c.heure_depart"\n'
        result += '\tdf = pd.read_sql_query(sqlQuery, conn)\n'
        result += '\tconn.close()\n'
        result += '\treturn df\n\n'

        result += 'def get_commandes():\n'
        result += '\treturn select_commandes()\n\n'

        result += 'def get_produit_by_id(produit_id):\n'
        result += '\tconn = sqlite3.connect("' + dbName + '.db")\n'
        result += '\tcur = conn.cursor()\n'
        result += '\tcur.execute("SELECT * FROM produits WHERE id = ?", (produit_id,))\n'
        result += '\trow = cur.fetchone()\n'
        result += '\tconn.close()\n'
        result += '\treturn row\n\n'

        result += 'def supprimer_commandes_jour(date):\n'
        result += '\tdelete_commandes("date = \'" + date + "\'")\n\n'

        result += 'def get_all_taches():\n'
        result += '\tconn = sqlite3.connect("' + dbName + '.db")\n'
        result += '\tsqlQuery = ("SELECT t.id, t.ordre, t.puissance, t.duree, "\n'
        result += '             "m.nom AS machine, m.operateur, "\n'
        result += '             "p.nom AS produit "\n'
        result += '             "FROM taches t "\n'
        result += '             "JOIN machines m ON t.machine_id = m.id "\n'
        result += '             "JOIN produits p ON t.produit_id = p.id "\n'
        result += '             "ORDER BY p.nom, t.ordre")\n'
        result += '\tdf = pd.read_sql_query(sqlQuery, conn)\n'
        result += '\tconn.close()\n'
        result += '\treturn df\n'

        # Mettre le texte python généré dans l'onglet Résults
        self.ui.EdResults.clear()
        self.ui.EdResults.setPlainText(result)
        # Enregidtrer le module python généré.
        try:
            with open(self.database['name']+'.py','wt') as myFile:
                myFile.write(result)
        except:
            print('problème d''enregistrement du fichier '+self.database['name']+'.py')
            print('Le code python généré se trouve dans l''onglet [Résults] !!')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())