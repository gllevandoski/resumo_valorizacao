def load_pdfs():
    from glob import glob
    import fitz

    date_rect = (350, 80, 415, 100)
    representative_rect = (50, 80, 140, 95)
    buyer_rect = (150, 80, 360, 95)
    cpf_rect = (150, 110, 250, 120)
    analysis_rect = (50, 250, 435, 475) # top left coordinates (x0, y0) and bottom right coordinates (x1, y1)

    for file in glob("samples/**/*.pdf", recursive=True):
        pdf = fitz.open(file)
        for page in pdf:                
            text = page.get_text("text", analysis_rect)
            representative = page.get_text("text", representative_rect).strip()
            buyer = page.get_text("text", buyer_rect).strip()
            date = page.get_text("text", date_rect).strip()
            cpf = page.get_text("text", cpf_rect).strip()
            dict_list = convert_pdf_to_dict(text, 6)

            return {
                        "date": date, 
                        "representative": representative, 
                        "buyer": buyer, 
                        "cpf": cpf,
                        "analysis": dict_list
                    }


def convert_pdf_to_dict(text: list, column_count: int):
    from string import digits
    from math import ceil

    split_text = text.split("\n")
    list_text = list()

    # cleaning up the split_text list from empty strings, 
    # dashes and non-useful stuff
    for item in split_text:
        for digit in digits:
            if digit in item:
                list_text.append(item)
                break

    formated_text = list()

    for i in range(int(ceil(len(list_text))/column_count)):
        c = (i * column_count)
        kg, pd, pt, rh, valor_un, valor_total = list_text[c:c + column_count]
        formated_text.append(
                                {
                                    "kg": kg,
                                    "pd": pd,
                                    "pt": pt,
                                    "rh": rh,
                                    "valor_un": valor_un,
                                    "valor_total": valor_total
                                }
                            )

    return formated_text

def load_to_excel(pdf_info):
    from openpyxl import load_workbook

    wb = load_workbook("resumo.xlsx")
    spreadsheet = wb.active

    for row in range(len(pdf_info["analysis"])):
        date_cell = spreadsheet.cell(row + 3, 0 + 2)
        representative_cell = spreadsheet.cell(row + 3, 1 + 2)
        buyer_cell = spreadsheet.cell(row + 3, 2 + 2)
        cpf_cell = spreadsheet.cell(row + 3, 3 + 2)
        kg_cell = spreadsheet.cell(row + 3, 4 + 2)
        pd_cell = spreadsheet.cell(row + 3, 5 + 2)
        pt_cell = spreadsheet.cell(row + 3, 6 + 2)
        rh_cell = spreadsheet.cell(row + 3, 7 + 2)
        un_cell = spreadsheet.cell(row + 3, 8 + 2)
        total_cell = spreadsheet.cell(row + 3, 9 + 2)

        date_cell.value = pdf_info["date"]
        representative_cell.value = pdf_info["representative"]
        buyer_cell.value = pdf_info["buyer"]
        cpf_cell.value = pdf_info["cpf"]
        kg_cell.value = float(pdf_info["analysis"][row]["kg"].replace(",", "."))
        pd_cell.value = float(pdf_info["analysis"][row]["pd"].replace(",", "."))
        pt_cell.value = float(pdf_info["analysis"][row]["pt"].replace(",", "."))
        rh_cell.value = float(pdf_info["analysis"][row]["rh"].replace(",", "."))
        un_cell.value = float(pdf_info["analysis"][row]["valor_un"].replace(",", "."))
        total_cell.value = float(pdf_info["analysis"][row]["valor_total"].replace(",", "."))
    wb.save("resumo.xlsx")


pdf_information = load_pdfs()
load_to_excel(pdf_information)
