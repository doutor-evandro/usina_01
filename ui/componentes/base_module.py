"""
Classe base para módulos da interface
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class BaseModule(ABC):
    """Classe base para todos os módulos da interface"""

    def __init__(self, parent_frame, sistema, cores=None):
        self.parent_frame = parent_frame
        self.sistema = sistema
        self.cores = cores or self._cores_padrao()
        self.widgets = {}

    def _cores_padrao(self):
        """Cores padrão do sistema"""
        return {
            'primaria': '#2E86AB',
            'secundaria': '#A23B72',
            'sucesso': '#F18F01',
            'fundo': '#F5F5F5',
            'texto': '#2C3E50',
            'sidebar': '#2C3E50',
            'content': '#FFFFFF'
        }

    @abstractmethod
    def criar_interface(self):
        """Método abstrato para criar a interface do módulo"""
        pass

    @abstractmethod
    def atualizar_dados(self):
        """Método abstrato para atualizar os dados do módulo"""
        pass

    def limpar_frame(self):
        """Limpa todos os widgets do frame pai"""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        self.widgets.clear()

    def criar_card(self, parent, titulo, valor, cor, row, col):
        """Cria um card de informação"""
        frame_card = tk.Frame(parent, bg=cor, relief=tk.RAISED, bd=2)
        frame_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        label_titulo = tk.Label(frame_card, text=titulo, bg=cor, fg='white',
                                font=('Arial', 12, 'bold'))
        label_titulo.pack(pady=(10, 5))

        label_valor = tk.Label(frame_card, text=valor, bg=cor, fg='white',
                               font=('Arial', 16, 'bold'))
        label_valor.pack(pady=(0, 10))

        return frame_card, label_valor