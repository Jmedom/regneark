import numpy as np
from fpdf import FPDF
from fpdf.fonts import FontFace

mindste_tal_1 = 1
største_tal_1 = 99
mindste_tal_2 = 1
største_tal_2 = 99


n_samples = 15
decimaler = 0
hele_svar = True       #Til division, uden rest
positive_svar = True   #Til subtraktion

kolonner = 3
font_size = 14
row_height = font_size*3


operator = u"\u2022" # dot
operator = u"\u00D7" # x
#operator = "/"
# operator = "+"
#operator = "-"


operator_text = {"/":"division",
                 "+":"addition",
                 "-":"subtraktion",
                 "*":"multiplikation",
                 u"\u2022":"multiplikation",
                 u"\u00D7":"multiplikation"}


class PDF(FPDF):
    def header(self):
        # Rendering logo:
        # self.image("../docs/fpdf2-logo.png", 10, 8, 33)
        # Setting font: helvetica bold 15
        self.set_font("helvetica", style="B", size=15)
        # Moving cursor to the right:
        self.cell(70)
        # Printing title:
        self.cell(65, 10, "Regneark "+operator_text[operator], border=1, align="C")
        # Performing a line break:
        self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", style="I", size=8)
        # Printing page number:
        self.cell(0, 10, f"Side {self.page_no()}/{{nb}}", align="C")




# Instantiation of inherited class
pdf = PDF()
pdf.add_page()
pdf.set_font("Times", size=12)

# cifre = [len(str(mindste_tal_1)),len(str(mindste_tal_1))]
first_val = np.round(np.random.uniform(mindste_tal_1,største_tal_1,n_samples),decimaler)
second_val = np.round(np.random.uniform(mindste_tal_2,største_tal_2,n_samples),decimaler)

if (operator == "/") and (hele_svar is True):
    results = first_val/second_val
    for ii, val in enumerate(results):
        first_val[ii] = round(round(val,decimaler) * second_val[ii],decimaler)

counter = 0
list_regnestykker = []
with pdf.table(borders_layout="None",line_height=row_height,headings_style=FontFace(emphasis="")) as table:
    for ii, data_row in enumerate(first_val):
        row = table.row()
        for jj in range(kolonner):
            val_1 = first_val[counter]
            val_2 = second_val[counter]

            if (positive_svar is True) and (operator == "-") and (val_1<val_2): #Hvis positive svar er True ved subtraktion
                first_val[counter] = val_2
                second_val[counter] = val_1
                val_1 = first_val[counter]
                val_2 = second_val[counter]
            if decimaler == 0:
                val_1 = int(val_1)
                val_2 = int(val_2)

            if (val_1, val_2) in list_regnestykker: # Tjek hvis regnestykket eksisterer i forvejen
                # print(list_regnestykker)
                # print((val_1, val_2)," is in regnestykker")
                while True:
                    val_1 = np.round(np.random.uniform(mindste_tal_1,største_tal_1,1),decimaler)[0] #Generer nyt tal
                    val_2 = np.round(np.random.uniform(mindste_tal_2,største_tal_2,1),decimaler)[0]
                    if (positive_svar is True) and (operator == "-") and (val_1<val_2): #Hvis positive svar er True ved subtraktion
                        first_val[counter] = val_2
                        second_val[counter] = val_1
                        val_1 = first_val[counter]
                        val_2 = second_val[counter]
                    if decimaler == 0:
                        val_1 = int(val_1)
                        val_2 = int(val_2)

                    if (val_1, val_2) not in list_regnestykker:
                        break

            list_regnestykker.append((val_1,val_2))
            val_1 = str(val_1).replace('.', ',')
            val_2 = str(val_2).replace('.', ',')
            row.cell(val_1+operator+val_2+" = ","C")
            counter += 1
            if counter >= n_samples:
                break
        if counter >= n_samples:
            break


pdf.output("Regneark_"+operator_text[operator]+".pdf")

pdf = PDF()
pdf.add_page()
pdf.set_font("Times", size=12)

counter = 0
with pdf.table(line_height=row_height,headings_style=FontFace(emphasis="")) as table:
    for ii, data_row in enumerate(first_val):
        row = table.row()
        for jj in range(kolonner):
            val_1, val_2 = list_regnestykker[counter]
            if (operator == u"\u2022") or (operator == u"\u00D7"):
                result = val_1*val_2
            elif operator == "+":
                result = val_1+val_2
            elif operator == "-":
                result = val_1-val_2
            elif operator == "/":
                result = val_1/val_2

            result = round(result,decimaler)
            if decimaler == 0:
                result = int(result)
            val_1 = str(val_1).replace('.', ',')
            val_2 = str(val_2).replace('.', ',')
            result = str(result).replace('.', ',')
            row.cell(val_1+operator+val_2+" = "+result,"C")
            counter += 1
            if counter >= n_samples:
                break
        if counter >= n_samples:
            break

pdf.output("Regneark_"+operator_text[operator]+"_svarark"+".pdf")

import os
os.startfile("Regneark_"+operator_text[operator]+"_svarark"+".pdf")