import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDyear(self):
        years = self._model.getYears()
        self._view.ddyear.options.clear()
        for a in years:
            self._view.ddyear.options.append(ft.dropdown.Option(a))
        self._view.update_page()

    def fillDDshape(self, e):
        shape = self._model.getShapeYear(int(self._view.ddyear.value))
        self._view.ddshape.options.clear()
        for s in shape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
            self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result1.controls.clear()
        if self._view.ddyear.value is None or self._view.ddshape.value is None:
            self._view.create_alert("Attenzione: selezionare anno e shape per costruire il grafo!")
            self._view.update_page()
            return
        year = int(self._view.ddyear.value)
        shape = self._view.ddshape.value
        self._model.buildGraph(year, shape)
        numNodi, numArchi = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {numNodi}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {numArchi}"))

        numCCdeboli = self._model.getInfoConnesseDeboli()
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha {numCCdeboli} componenti connesse deboli"))
        largestConnessaDebole = self._model.getLargestConnessaDebole()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da {len(largestConnessaDebole)} nodi:"))
        for n in largestConnessaDebole:
            self._view.txt_result1.controls.append(ft.Text(n))

        self._view.btn_path.disabled = False
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        path, score = self._model.getOptimalPath()
        self._view.txt_result2.controls.append(ft.Text(f"Percorso ottimo trovato con score={score}"))
        self._view.txt_result2.controls.append(ft.Text(f"I nodi attraversati sono {len(path)}:"))
        for p in path:
            self._view.txt_result2.controls.append(ft.Text(p.str2()))
        self._view.update_page()
