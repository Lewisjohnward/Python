''' 
'''

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import operator
import os
import sys
import getpass


class Editor(QWidget):
    def __init__(self, title, text):
        super().__init__()

        # Title edit
        label_title = QLabel("Title")
        label_title.setStyleSheet("font-size: 20px;")
        self.title = QLineEdit(title)
        self.title.textChanged.connect(self.title_changed)
        self.title.setStyleSheet("font-size: 15px;")

        # Text edit
        label_text = QLabel("Text")
        label_text.setStyleSheet("font-size: 20px;")
        self.text = QTextEdit(text)
        self.text.textChanged.connect(self.text_changed)
        self.text.setStyleSheet("font-size: 15px;")

        l = QVBoxLayout()
        l.addWidget(label_title)
        l.addWidget(self.title)
        l.addWidget(label_text)
        l.addWidget(self.text)
        h = QHBoxLayout()
        save_btn = QPushButton("save")
        h.addStretch()
        h.addWidget(save_btn)
        l.addLayout(h)
        self.setLayout(l)

    def title_changed(self):
        print(self.title.text())

    def text_changed(self):
        print(self.text.toPlainText())

    def change_clipping(self, title, text):
        self.title.setText(title)
        self.text.setText(text)

class MyTableModel(QAbstractTableModel):
    # mylist is data, header is headers
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        return len(self.mylist[0])
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))

    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self.mylist[index.row()][index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.mylist[index.row()][index.column()] = value
            return True


class Table(QTableView):
    def __init__(self, data_list, header, editor, undo):
        super().__init__()
        self.selected_row = 0
        self.editor = editor
        self.undo = undo

        self.deleted_rows = []

        self.draw_table()

    def draw_table(self):
        table_model = MyTableModel(self, data_list, header)
        self.setModel(table_model)
        self.clicked.connect(self.handle_click)
        self.resizeColumnsToContents()
        self.setSortingEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.selectRow(self.selected_row)
        self.editor.change_clipping(data_list[0][0], data_list[0][1])


    def handle_click(self, item):
        row = item.row()
        print(row)
        self.selected_row = row
        self.editor.change_clipping(data_list[row][0], data_list[row][1])

    def delete_selected_row(self):
        self.deleted_rows.insert(0, [data_list[self.selected_row][0], data_list[self.selected_row][1]])
        if len(self.deleted_rows):
            self.undo.setEnabled(True)

        data_list.pop(self.selected_row)
        self.draw_table()

    def undo_delete(self):
        data_list.insert(0, [self.deleted_rows[0][0], self.deleted_rows[0][1]])
        self.deleted_rows.pop(0)
        if not len(self.deleted_rows):
            self.undo.setDisabled(True)
            self.redo.setEnabled(True)
        self.draw_table()



class MyWindow(QMainWindow):
    def __init__(self, data_list, header, *args):
        super().__init__()


        # Menu bar
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # Toolbar
        deleteEntryAction = QAction(QIcon("./icons/table-delete-row.png"), '&Delete', self)
        deleteEntryAction.triggered.connect(self.handleDelete)

        # Undo
        self.undoDeleteAction = QAction(QIcon("./icons/arrow-circle-225.png"), '&Undo', self)
        self.undoDeleteAction.setEnabled(False)
        self.undoDeleteAction.triggered.connect(self.handleUndo)

        # Redo
        self.redoDeleteAction = QAction(QIcon("./icons/arrow-circle-225-left.png"), '&Redo', self)
        self.redoDeleteAction.setEnabled(False)
        self.redoDeleteAction.triggered.connect(self.handle_redo)

        # Save
        saveAction = QAction(QIcon("./icons/disk.png"), '&Save', self)
        saveAction.triggered.connect(self.save)


        self.toolbar = self.addToolBar('Delete')
        self.toolbar.addAction(deleteEntryAction)
        self.toolbar.setMovable(False)
        self.toolbar = self.addToolBar('Undo')
        self.toolbar.addAction(self.undoDeleteAction)
        self.toolbar.setMovable(False)
        self.toolbar.addAction(saveAction)


        # Editor
        self.editor = Editor(data_list[0][0], data_list[0][1])
        # Table
        self.table = Table(data_list, header, self.editor, self.undoDeleteAction)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.editor)
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)


    def handleDelete(self):
        self.table.delete_selected_row()

    def handleUndo(self):
        self.table.undo_delete()

    def handle_redo(self):
        self.table.redo_delete()

    def save(self):
        print("saving!")


# the solvent data ...
header = ["Source", "Clipping"]
# use numbers for numeric data to sort properly
data_list = [
["Il Banchetto Dei Corvi (George R.R.Martin)", "Il prete era magro e alto, anche se non quanto Victarion. Il naso sporgeva dal volto ossuto come la pinna di"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Il prete era magro e alto, anche se non quanto Victarion."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Il prete era magro e alto, anche se non quanto Victarion. Il naso sporgeva dal volto ossuto come la pinna di uno squalo, gli occhi sembravano d???acciaio. La barba gli scendeva fino alla vita. Quando soffiava il vento, i capelli simili a funi attorcigliate sbattevano contro la parte posteriore delle cosce."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Un Volmark diede una pacca sulla schiena a Victarion, due Sparr lo obbligarono a prendere un otre di vino. Victarion bevve a lungo, si asciug?? la bocca e lasci?? che lo guidassero ai loro bivacchi, per ascoltarli discutere di guerra, corone, razzie, della gloria e della libert?? del suo regno."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Asha sedette su uno sgabello e si serv?? del vino di Nute il Barbiere senza chiederglielo. Nute non fece obiezioni, aveva alzato un po??? troppo il gomito e aveva perso conoscenza."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Spero che tu non sia venuta per avanzare una pretesa al Trono del Mare.?? Lo punzecchi?? con un sorriso. ??E se cos?? fosse??? ??Ci sono uomini che ricordano quando eri una ragazzina e nuotavi nuda in mare giocando con le bambole.?? ??Giocavo anche con le asce.?? ???? vero?? dovette ammettere Victarion ??ma una donna ha bisogno di un marito, non di una corona. Quando sar?? re, te ne procurer?? uno.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "ninnolo ai pirati di Lys. Tornata a casa, scoprii che Euron"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Dona loro la saggezza di riconoscere il vero re quando si paleser?? di fronte a loro, e concedi loro la forza di respingere il falso re.??? Preg?? tutta la notte, poich?? quando il dio era in lui Aeron Greyjoy non aveva bisogno di dormire, come del resto le onde o i pesci del mare. Nuvole scure si rincorrevano"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Dona loro la saggezza di riconoscere il vero re quando si paleser?? di fronte a loro, e concedi loro la forza di respingere il falso re.??? Preg?? tutta la notte, poich?? quando il dio era in lui Aeron Greyjoy non aveva bisogno di dormire, come del resto le onde o i pesci del mare."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Victarion attese che si acquietassero. ??Voi tutti mi conoscete?? disse. ??Se volete udire discorsi suadenti, andate da qualcun altro. Io non sono un incantatore. Ho un???ascia e queste.?? Sollev?? le enormi mani coperte di maglia di ferro per farle vedere e Nute il Barbiere mostr?? l???ascia, un impressionante pezzo d???acciaio."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Asha ne infilz?? una con la sua daga. ??Harmund Sharp?? grid?? ??tuo figlio Harrag ?? morto a Grande Inverno per questo!?? Tolse la rapa dalla lama e gliela lanci??. ??Credo che tu abbia altri figli. Se vuoi barattare la loro vita per delle rape, non esitare: invoca il nome di mio zio!??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Costerebbe meno se dividessimo tutti lo stesso letto, milady?? ripeteva Dick lo Svelto. ??Puoi mettere la tua spada fra noi. Il vecchio Dick ?? un tipo innocuo. Leale quanto un cavaliere e onesto fino al midollo.?? ??E se invece tu fossi uno smidollato??? chiese retoricamente Brienne. ??Pu?? darsi. Se non ti fidi a farmi dormire nel letto, posso rannicchiarmi sul pavimento, milady.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Dick Crabb mostr?? la sua vera natura il giorno seguente, quando si fermarono ad abbeverare i cavalli. Brienne and?? dietro un cespuglio per svuotare la vescica. Mentre si stava accucciando, ud?? Podrick dire: ??Cosa stai facendo? Allontanati da l????. Fin?? quello che doveva fare, si tir?? su le brache e ritorn?? sulla strada. Trov?? Dick lo Svelto che si puliva le dita dalla farina. ??Non troverai dragoni nelle mie bisacce?? gli disse Brienne. ??L???oro me lo tengo addosso.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Quando non cantava, Dick lo Svelto parlava, intrattenendoli con storie su Punta della Chela Spezzata. Tutte le valli pi?? lugubri avevano un loro lord, diceva, ed erano accomunate solo dalla diffidenza nei confronti degli estranei. Nelle loro vene, il sangue dei primi uomini scorreva scuro e forte."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Dicono che una volta l???abbia usata per uccidere un drago.?? Dick lo Svelto non rimase per nulla impressionato."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??E stanotte piover??!?? continu?? Dick. ??Una fredda notte di pioggia. Tu e Pods ve ne state l?? a dormire al caldo e il vecchio Dick qua sotto da solo a tremare.?? Scosse la testa, mugugnando, mentre si preparava un giaciglio su un mucchio di fieno."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Alcuni dicono che i primi uomini li hanno uccisi tutti, ma ?? meglio non crederci. I fangostri arrivano di notte e portano via i bambini cattivi. E quando si muovono con i piedi palmati fanno un rumore tipo ciac-ciac. Le bambine, le tengono per fare figli, i maschi invece li mangiano, strappando le carni con quei denti verdi e aguzzi.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Sognando un pasto caldo, addent?? una striscia di carne di manzo salata. Dick lo Svelto raccontava della volta in cui ser Clarence Crabb aveva lottato contro il re dei fangostri. ????? un bravo narratore??? dovette ammettere ???ma anche Mark Mullendore era divertente, con la sua scimmietta.???"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Mentre salivano, Dick lo Svelto ne indic?? alcune. ??Quella ?? la testa di un orco, vedete??? Brienne sorrise quando la individu??. ??E l?? c????? un drago di pietra. L???altra ala ?? caduta quando il mio babbo era un ragazzino. Sopra, ci sono le tette che penzolano, come quelle delle vecchie.?? Lanci?? un???occhiata al seno di Brienne."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "???? brutto qui?? disse Podrick. ???? un brutto posto.?? Brienne aveva la stessa sensazione, ma ammetterlo non sarebbe servito a niente. ??Una foresta di pini ?? un luogo lugubre, ma in fondo sono soltanto pini. Non c????? nulla da temere qui.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "???Nelle braccia hai la forza di un uomo??? le aveva detto pi?? di una volta ser Goodwin ???ma il tuo cuore ?? delicato come quello di qualsiasi altra fanciulla. Una cosa ?? esercitarsi nel cortile con una spada dalla punta smussata, un???altra infilzare trenta centimetri di acciaio nel ventre di un uomo e vedere la luce che si spegne nei suoi occhi.??? Per renderla pi?? risoluta, ser Goodwin era solito mandarla dal macellaio di suo padre a sgozzare agnelli e porcellini. I piccoli suini strillavano, gli agnelli gridavano come bambini terrorizzati. Finita la macellazione, Brienne era accecata dalle lacrime versate e gli abiti erano talmente intrisi di sangue che doveva consegnarli alla sua serva perch?? li bruciasse. Ma ser Goodwin continuava ad avere dubbi."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Un momento erano nel fitto in mezzo al bosco, con intorno solo una infinita distesa di pini, poi aggirarono un masso tondeggiante e di fronte a loro si apr?? un varco. Un miglio pi?? avanti, la foresta terminava d???improvviso. Si ritrovarono al cospetto del cielo, del mare e di un antico castello diroccato, abbandonato, invaso dalle erbacce, sul limitare della scogliera. ??I Sussurri?? disse Dick lo Svelto. ??Ascoltate. Riuscite a sentire le teste???"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Non mi interessa che cosa volevi fare. Da dove si entra??? ??Dall???altro lato.?? Dick esit??. ??Il tipo, il fesso che stai cercando, ?? uno che se la prende??? chiese nervosamente. ??Voglio dire, ieri notte ho cominciato a pensare che magari ?? arrabbiato con il vecchio Dick, per quella mappa che gli ho venduto e che non gli ho mica detto che i contrabbandieri qua non ci vengono pi??.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Shagwell piomb?? gi?? dall???albero-diga con una stridente risata. Era l???orrido giullare dei Guitti Sanguinari di Vargo Hoat. Indossava gli abiti multicolori dei giullari, ma cos?? scoloriti e macchiati che sembravano tutti marrone pi?? che grigio o rosa. Impugnava una mazza da guerra, tre sfere irte di rostri attaccate a un manico di legno. Vortic?? la sua arma, in diagonale e verso il basso. Una delle ginocchia di Dick Crabb esplose in un???eruzione di ossa e sangue."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Shags, come sei cattivo?? disse l???uomo spuntato dal pozzo. Rise nel riconoscere Brienne. ??Ancora tu, donna? Che cosa sei venuta a fare qui, a darci la caccia? O magari ti mancavano le nostre simpatiche facce??? ???? venuta per me.?? Shagwell spostava il peso del corpo da un piede all???altro, facendo roteare la mazza. ??Mi sogna tutte le notti, quando si infila le dita nella fica. Mi vuole, gente! Questa vacca sente la mancanza delle mie scopate! Me la inculo e la riempio di seme di giullare, fino a che non caccia fuori un altro piccolo Shagwell!??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Sotto il sole rovente di Dorne, la ricchezza era misurata sia in acqua sia in oro, per cui tutti i pozzi erano sorvegliati con grande attenzione. Il pozzo di Shandystone per?? si era prosciugato cento anni prima e le sentinelle si erano spostate verso un luogo pi?? umido, abbandonando il loro modesto fortilizio dalle colonne scanalate e le triple arcate. Alla fine, le sabbie avevano ripreso possesso di ci?? che era sempre stato loro."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Non ci aveva fatto caso prima, ma pareva un buon auspicio. ???Sette cavalieri sulla strada della gloria. Un giorno i cantastorie ci renderanno immortali.??? Drey avrebbe preferito un gruppo pi?? numeroso, ma avrebbe potuto attirare attenzioni indesiderate e ogni uomo in pi?? raddoppiava il rischio di tradimento."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Le barche con le pertiche avevano il tetto basso ed erano molto larghe, ma praticamente non avevano pescaggio."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Il portello della barca si apr?? di schianto. Areo Hotah, comandante delle guardie del principe Doran, emerse alla luce del sole con l???ascia lunga in mano. Garin si blocc??. Arianne ebbe come l???impressione di ricevere un colpo di mannaia allo stomaco. ???Non doveva finire cos??. Non doveva succedere una cosa del genere.???"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Il portello della barca si apr?? di schianto. Areo Hotah, comandante delle guardie del principe Doran, emerse alla luce del sole con l???ascia lunga in mano. Garin si blocc??. Arianne ebbe come l???impressione di ricevere un colpo di mannaia allo stomaco. ???Non doveva finire cos??. Non doveva succedere una cosa del genere.??? Quando ud?? Drey dire: ???? l???ultima faccia che speravo di vedere?? cap?? di dover intervenire. ??Via!?? grid??, voltandosi"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Il portello della barca si apr?? di schianto. Areo Hotah, comandante delle guardie del principe Doran, emerse alla luce del sole con l???ascia lunga in mano. Garin si blocc??. Arianne ebbe come l???impressione di ricevere un colpo di mannaia allo stomaco. ???Non doveva finire cos??. Non doveva succedere una cosa del genere.??? Quando ud?? Drey dire: ???? l???ultima faccia che speravo di vedere?? cap?? di dover intervenire. ??Via!?? grid??, voltandosi indietro. ??Arys, proteggi la principessa?????"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Senza un linguaggio comune, Arya non poteva comunicare con gli altri. Per?? li ascoltava e, mentre lavorava, ripeteva tra s?? e s?? le parole che udiva. Sebbene il novizio pi?? giovane fosse cieco, doveva occuparsi delle candele. Si aggirava per il tempio con le sue pantofole felpate, circondato dai mormorii delle donne anziane che venivano ogni giorno a pregare."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Senza un linguaggio comune, Arya non poteva comunicare con gli altri. Per?? li ascoltava e, mentre lavorava, ripeteva tra s?? e s?? le parole che udiva. Sebbene il novizio pi?? giovane fosse cieco, doveva occuparsi delle candele. Si aggirava per il tempio con le sue pantofole felpate, circondato dai mormorii delle donne anziane che venivano ogni giorno a pregare. Anche senza occhi, sapeva sempre quali candele si erano esaurite. ??Lo guida l???olfatto?? le spieg?? l???uomo gentile ??e nella zona dove brucia una candela l???aria ?? pi?? calda.?? Disse ad Arya di chiudere gli occhi e di tentare di fare lo stesso."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Trov?? una stanza piena di armi e armature: elmi ornati, curiosi vecchi pettorali, spade lunghe, pugnali, daghe, balestre e alte lance con punte a forma di foglia."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Andava abbastanza d???accordo con la cuoca. Le sbatteva un coltello in mano, indicava una cipolla e Arya l???affettava. Oppure la spingeva verso un grosso impasto e Arya lo lavorava fino a quando la cuoca non diceva ???basta??? (era la prima parola in braavosiano che aveva imparato)."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "I molluschi e le noci di mare abbondavano in quelle zone, c???erano cozze e pesci palla, rane e tartarughe, granchi del limo, granchi maculati e granchi scalatori, anguille rosse, anguille nere, anguille striate, lamprede e ostriche. Tutti questi animali facevano spesso la loro comparsa sui tavoli in legno dove i servitori del Dio dai Mille Volti consumavano i pasti."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Oltre ad aiutare Umma, Arya aveva anche altri compiti. Spazzava il pavimento del tempio, serviva i pasti, faceva la cernita degli abiti di chi era morto, svuotava le loro borse e contava pile di strane monete. Tutte le mattine camminava a fianco dell???uomo gentile mentre lui faceva il giro del tempio a raccogliere i cadaveri."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Sebbene i compiti che le avevano assegnato le lasciassero poco tempo per l???arte della spada, appena poteva si esercitava, duellando con la sua ombra alla luce di una candela blu. Una sera, l???orfana si ritrov?? a passare di l?? e vide Arya mentre si allenava. La ragazza non disse niente, ma il giorno successivo l???uomo gentile accompagn?? Arya alla sua cella."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Era la prima volta che si ritrovava all???aperto da quando era entrata nel tempio. Il cielo era nuvoloso e la nebbia ricopriva la terra come un grigio lenzuolo sfilacciato. Alla sua destra, sent?? un rumore di pagaie provenire dal canale. ???Braavos, la Citt?? Segreta??? pens??."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Era la prima volta che si ritrovava all???aperto da quando era entrata nel tempio. Il cielo era nuvoloso e la nebbia ricopriva la terra come un grigio lenzuolo sfilacciato. Alla sua destra, sent?? un rumore di pagaie provenire dal canale. ???Braavos, la Citt?? Segreta??? pens??. Il nome le pareva pi?? che calzante."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "???Anche cucire era pi?? divertente che studiare le lingue straniere??? si disse Arya, dopo una sera in cui aveva dimenticato met?? delle parole che pensava di sapere e aveva pronunciato le restanti cos?? male che l???orfana non aveva potuto far altro che ridere."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Arya si morse il labbro. ??Diventer?? come lei??? ??No?? rispose l???uomo gentile ??a meno che tu non lo voglia."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Arya si morse il labbro. ??Diventer?? come lei??? ??No?? rispose l???uomo gentile ??a meno che tu non lo voglia. Sono i veleni ad averla resa cos?? com?????.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Quando non versi da bere devi stare immobile come fossi scolpita nella pietra?? la istru?? l???uomo gentile. ??Ce la farai??? ??Certo.?? ???Prima di imparare a muoversi bisogna imparare a stare fermi??? le aveva insegnato Syrio Forel tanto tempo prima ad Approdo del Re, e cos?? Arya aveva fatto. Era stata la coppiera di Roose Bolton ad Harrenhal e, se rovesciavi il vino, il Lord Sanguisuga ti frustava."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Tutte le magie hanno un prezzo, bambina. Sono necessari anni di preghiera, di sacrifici e di studio per elaborare un incantesimo.?? ??Anni??? ripet?? Arya, in preda allo sgomento. ??Se fosse facile, tutti gli uomini lo farebbero. Bisogna imparare a camminare prima di mettersi a correre. Perch?? usare un incantesimo, quando bastano i trucchi dei giullari???"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Benissimo. Tuo padre era capo dei rematori su una galea. Quando tua madre ?? morta, lui ti ha portato in mare con s??. Poi anche lui ?? morto, il suo comandante non sapeva che farsene di te, cos?? ti ha scaricato a Braavos. E il nome della nave qual era???"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Lady Lysa gli dava il seno ogni volta che era sovreccitato. L???arcimaestro Ebrose sostiene che il latte materno abbia molte ottime propriet??.?? ???? questo il tuo consiglio, maestro? Che troviamo una nutrice per il lord di Nido dell???Aquila e Protettore della Valle? E quando lo svezziamo? Il giorno del suo matrimonio? Cos?? passerebbe direttamente dai capezzoli della balia a quelli della moglie!?? La"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Si occup?? del vino caldo, trov?? una forma presentabile di formaggio bianco forte e ordin?? alla cuoca di cucinare pane per venti persone, qualora i lord alfieri arrivassero con pi?? uomini del previsto."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Quando Gretchel le diede lo specchio argentato di Lysa, vide che il colore si intonava perfettamente ai folti capelli castano scuro di Alayne. ???Lord Royce non mi riconoscer?? mai??? pens??. ???Io stessa faccio fatica.???"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "pi?? anziani, scelsero di essere trasportati dal verricello,"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Lord Redfort e lady Waynwood, i lord alfieri pi?? anziani, scelsero di essere trasportati dal verricello, dopo di che il cesto fu calato un???altra volta per il grasso lord Belmore. Gli altri optarono per l???arrampicata."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Le guance e il naso di Hunter erano rossi come mele, rivelando una certa inclinazione per il succo d???uva. Alayne fece in modo di riempirgli la coppa ogni volta che era vuota."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "I capelli di lady Waynwood si stavano ingrigendo, aveva zampe di gallina attorno agli occhi e la pelle del collo rilasciata, ma la sua aura di nobilt?? era inconfondibile."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "scale di marmo che passava vicino alle cripte, ai dongioni"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Pi?? tardi, ci fu una sorta di banchetto, anche se Petyr dovette scusarsi per il vitto modesto. Robert venne condotto alla loro presenza, abbigliato con un farsetto color crema e azzurro, e"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Pi?? tardi, ci fu una sorta di banchetto, anche se Petyr dovette scusarsi per il vitto modesto. Robert venne condotto alla loro presenza, abbigliato con un farsetto color crema e azzurro, e recit?? abbastanza bene la parte del piccolo lord."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Il re teneva il broncio. ??Voglio sedere sul Trono di Spade?? piagnucol??. ??A Joff glielo permettevi.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Waters aveva scelto per comandare i nuovi dromoni"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Negli ultimi tempi, il gran maestro era stato particolarmente petulante. Durante l???ultima seduta del concilio ristretto si era lamentato con amarezza degli uomini che Aurane Waters aveva scelto per comandare i nuovi dromoni della regina."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Vostra grazia, liete novelle?? annunci??. ??Wyman Manderly ha obbedito al tuo comando e ha decapitato ser Davos, il Cavaliere delle Cipolle di lord Stannis.?? ??Ne abbiamo la certezza??? ??La testa e le mani di ser Davos sono state esposte sulle mura di Porto Bianco. Lord Wyman lo dichiara apertamente e i Frey confermano. Hanno visto la testa con i loro occhi, aveva una cipolla in bocca. E anche le mani, una delle quali ?? riconoscibile dalle dita mozze.?? ??Ottimo?? comment?? Cersei. ??Inviate un corvo messaggero a Manderly. Ora che la sua lealt?? ?? dimostrata, informatelo che suo figlio gli sar?? restituito immediatamente.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Il sette ?? un numero sacro alle nostre divinit??.?? ??Vedo che vostra grazia ama le burle.?? ??Le mie burle sono sempre accompagnate dal sorriso. Sto per caso sorridendo? Senti delle risa? Ti assicuro che, quando faccio delle battute, la gente ride.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Ho aiutato sua grazia a indossare l???armatura e gli ho mostrato come mettere la lancia in resta?? rispose ser Loras. ??Quel cavallo ?? troppo grande per lui. E se fosse caduto? E se la sacca di sabbia gli avesse sfondato la testa??? ??I lividi e le labbra spaccate si addicono a un cavaliere.??"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "??Sono stata negligente. Con un regno da governare, una guerra da combattere e un padre di cui onorare il lutto, ho tralasciato la fondamentale questione di nominare un nuovo maestro d???armi. Rimedier?? al pi?? presto.?? Ser Loras si scost?? un ricciolo ribelle dalla fronte. ??Sua maest?? non trover?? un uomo che abbia nemmeno la met?? delle mie capacit?? con la spada e la lancia.?? ???Che umilt??!???"],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Lo lasci?? sul ponte levatoio che attraversava il fossato asciutto, con il suo fondo irto di punte di ferro."],
["Il Banchetto Dei Corvi (George R.R.Martin)", "Quando Cersei entr?? nel solarium, vi trov?? lord Qyburn che leggeva accanto a una delle finestre. ??Compiacendo vostra grazia, ho notizie.?? ??Altri complotti e tradimenti??? domand?? la regina. ??Ho avuto una giornata lunga e faticosa. Cerchiamo di fare presto.??"],
]
app = QApplication([])
win = MyWindow(data_list, header)
win.show()
app.exec()
