import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QRegExpValidator, QColor, QFont, QPainter, QPalette
from PyQt5.QtCore import Qt, QRegExp, QRect


class TranslationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.dna_label = QLabel("DNA:")
        self.dna_input = QLineEdit()
        self.mrna_label = QLabel("mRNA:")
        self.mrna_input = QLineEdit()
        self.protein_label = QLabel("Protein:")
        self.protein_input = QLineEdit()
        self.protein_input.setReadOnly(True)
        self.protein_input.setStyleSheet("QLineEdit { background-color: #F0F0F0; }")  # Set background color

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_sequence)

        self.translation_layout = QVBoxLayout()
        self.translation_layout.addWidget(self.dna_label)
        self.translation_layout.addWidget(self.dna_input)
        self.translation_layout.addWidget(self.mrna_label)
        self.translation_layout.addWidget(self.mrna_input)
        self.translation_layout.addWidget(self.protein_label)
        self.translation_layout.addWidget(self.protein_input)
        self.translation_layout.addWidget(self.convert_button)

        self.setLayout(self.translation_layout)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        # Set the opacity for examples
        painter.setOpacity(0.4)

        # Draw examples on DNA input field
        dna_example_rect = QRect(self.dna_input.geometry().topLeft(), self.dna_input.geometry().size())
        painter.drawText(dna_example_rect, Qt.AlignCenter, "Example: AGCT")

        # Draw examples on mRNA input field
        mrna_example_rect = QRect(self.mrna_input.geometry().topLeft(), self.mrna_input.geometry().size())
        painter.drawText(mrna_example_rect, Qt.AlignCenter, "Example: ACGU")

        # Add design to the protein input field
        protein_rect = QRect(self.protein_input.geometry().topLeft(), self.protein_input.geometry().size())
        painter.setBrush(QColor(255, 204, 204))  # Set the background color for the protein input field
        painter.setPen(Qt.NoPen)
        painter.drawRect(protein_rect)
    def convert_sequence(self):
        dna_sequence = self.dna_input.text().upper()
        mrna_sequence = self.mrna_input.text().upper()

        if dna_sequence and not mrna_sequence:
            self.dna_input.setText(dna_sequence)
            self.mrna_input.setText(self.dna_to_mrna(dna_sequence))
            self.protein_input.setText(self.mrna_to_protein(self.dna_to_mrna(dna_sequence)))
        elif mrna_sequence and not dna_sequence:
            self.mrna_input.setText(mrna_sequence)
            self.dna_input.setText(self.mrna_to_dna(mrna_sequence))
            self.protein_input.setText(self.mrna_to_protein(mrna_sequence))
        else:
            self.clear_outputs()
            self.show_error_dialog("Please enter only one sequence (DNA or mRNA).")

    def show_error_dialog(self, message):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowTitle("Error")
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setStyleSheet("QLabel{ color: red; font-weight: bold; font-size: 12px; }")
        dialog.exec_()



class StudyMateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudyMate")
        self.setWindowIcon(QIcon('rasm.png'))
        self.resize(400, 300)

        self.dna_label = QLabel("DNA:")
        self.dna_label.setStyleSheet("QLabel { font-weight: bold; font-size: 14px; color: blue; }")  # Set label style
        self.dna_input = QLineEdit()
        self.dna_input.setStyleSheet("QLineEdit { background-color: #f0fff0; }")  # Set input field style

        self.mrna_label = QLabel("mRNA:")
        self.mrna_label.setStyleSheet("QLabel { font-weight: bold; font-size: 14px; color: blue; }")  # Set label style
        self.mrna_input = QLineEdit()
        self.mrna_input.setStyleSheet("QLineEdit { background-color: #f0f0ff; }")  # Set input field style

        self.protein_label = QLabel("Protein:")
        self.protein_input = QLineEdit()
        self.protein_input.setStyleSheet("QLineEdit { background-color: #FFF0F0; }")  # Set background color
        self.protein_label.setStyleSheet("QLabel { font-weight: bold; font-size: 14px; color: blue; }")
        self.protein_input.setReadOnly(True)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_sequence)

        self.translation_layout = QVBoxLayout()
        self.translation_layout.addWidget(self.dna_label)
        self.translation_layout.addWidget(self.dna_input)
        self.translation_layout.addWidget(self.mrna_label)
        self.translation_layout.addWidget(self.mrna_input)
        self.translation_layout.addWidget(self.protein_label)
        self.translation_layout.addWidget(self.protein_input)
        self.translation_layout.addWidget(self.convert_button)

        self.translation_widget = QWidget()
        self.translation_widget.setLayout(self.translation_layout)
        self.setCentralWidget(self.translation_widget)

        self.text_label = QLabel("This application helps students to learn translation and transcription.\nFill only one of the DNA or mRNA with uppercase letters that are appropriate to get a result.\nUse upper letters\n? means last few didn't have at least three letters.")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("QLabel { font-size: 12px; font-weight: bold;color: green;}")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_label)
        main_layout.addWidget(self.translation_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        
        self.menu = self.menuBar()
        self.organization_menu = self.menu.addMenu("Our Organization")
        self.website_action = QAction("Visit Website", self)
        self.website_action.triggered.connect(self.open_website)
        self.organization_menu.addAction(self.website_action)

        self.setup_input_validators()

    def setup_input_validators(self):
        dna_validator = QRegExpValidator(QRegExp("[ACGT]+"), self.dna_input)
        self.dna_input.setValidator(dna_validator)

        mrna_validator = QRegExpValidator(QRegExp("[AUGC]+"), self.mrna_input)
        self.mrna_input.setValidator(mrna_validator)

    def convert_sequence(self):
        dna_sequence = self.dna_input.text().upper()
        mrna_sequence = self.mrna_input.text().upper()

        if dna_sequence and not mrna_sequence:
            self.dna_input.setText(dna_sequence)
            self.mrna_input.setText(self.dna_to_mrna(dna_sequence))
            self.protein_input.setText(self.mrna_to_protein(self.dna_to_mrna(dna_sequence)))
        elif mrna_sequence and not dna_sequence:
            self.mrna_input.setText(mrna_sequence)
            self.dna_input.setText(self.mrna_to_dna(mrna_sequence))
            self.protein_input.setText(self.mrna_to_protein(mrna_sequence))
        else:
            self.clear_outputs()
            self.show_error_dialog("Please enter only one sequence (DNA or mRNA).")

    def dna_to_mrna(self, dna_sequence):
        changed = ''
        for i in dna_sequence:
            if i == 'G':
                changed+='C'
            elif i == 'C':
                changed += 'G'
            elif i == 'A':
                changed += 'U'
            elif i == 'T':
                changed += 'A'
        return changed

    def mrna_to_dna(self, mrna_sequence):
        changed = ''
        for i in mrna_sequence:
            if i == 'C':
                changed+='G'
            elif i == 'G':
                changed += 'C'
            elif i == 'U':
                changed += 'A'
            elif i == 'A':
                changed += 'T'
        return changed

    def mrna_to_protein(self, mrna_sequence):
        codon_table = {
        "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
        "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
        "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
        "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",
        "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
        "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
        "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
        "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
        "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
        "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
        "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
        "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
        "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
        }
        change = ''
        for i in range(0, len(mrna_sequence), 3):
            codon = mrna_sequence[i:i + 3]
            if codon in codon_table:
                change += codon_table[codon]
            else:
                change += '?'
        return change


    def open_website(self):
        import webbrowser
        webbrowser.open("https://matestudy.netlify.app")

    def clear_outputs(self):
        self.protein_input.setText("")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.4)  # Set the opacity for examples
        painter.drawText(self.dna_input.rect(), Qt.AlignCenter, "Example: AGCT")
        painter.drawText(self.mrna_input.rect(), Qt.AlignCenter, "Example: ACGU")

    def show_error_dialog(self, message):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowTitle("Error")
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setStyleSheet(
            "QLabel{ color: red; font-weight: bold; font-size: 12px; }"  # Set the text color, font weight, and font size
            "QPushButton{ background-color: #ffcccc; }"  # Set the background color of the button
        )
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyMateApp()
    window.show()
    sys.exit(app.exec_())
