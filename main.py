def load_pdfs():
    from glob import glob
    import fitz

    # top left coordinates (x0, y0) and bottom right coordinates (x1, y1)
    date_rect = (350, 80, 415, 100)
    representative_rect = (50, 80, 140, 95)
    buyer_rect = (150, 80, 360, 95)
    cpf_rect = (150, 110, 250, 120)
    analysis_rect = (50, 250, 435, 475)
    pdf_list = list()

    for file in glob("valorizacoes/**/*.pdf", recursive=True):
        pdf = fitz.open(file)

        for page in pdf:                
            analysis = page.get_text("text", analysis_rect)
            analysis_list = analysis_to_list(analysis)

            representative = page.get_text("text", representative_rect).strip()
            buyer = page.get_text("text", buyer_rect).strip()
            date = page.get_text("text", date_rect).strip()
            cpf = page.get_text("text", cpf_rect).strip()

            pdf_list.append({"date": date, "representative": representative, "buyer": buyer, "cpf": cpf, "analysis": analysis_list})

    for pdf in pdf_list:
        kg, pd, pt, rh = 0, 0, 0, 0
        
        for analysis in pdf["analysis"]:
            kg += float(analysis["kg"].replace(".", "").replace(",", "."))
            pd += float(analysis["pd"].replace(".", "").replace(",", ".")) * float(analysis["kg"].replace(".", "").replace(",", "."))
            pt += float(analysis["pt"].replace(".", "").replace(",", ".")) * float(analysis["kg"].replace(".", "").replace(",", "."))
            rh += float(analysis["rh"].replace(".", "").replace(",", ".")) * float(analysis["kg"].replace(".", "").replace(",", "."))

        pd /= kg
        pt /= kg
        rh /= kg
        pdf["summary"] = {"kg": kg, "pd": pd, "pt": pt, "rh": rh}

    return pdf_list


def analysis_to_list(analysis: list):
    def cleanse_list(dirty_list: list):
        from string import digits
        clean_list = list()

        # searches the list for empty strings, dashes and non-useful stuff and removes it
        for item in dirty_list:
            for digit in digits:
                if digit in item:
                    clean_list.append(item)
                    break

        return clean_list

    def format_list(unformatted_list: list):
        from math import ceil
        column_count = 6
        formatted_list = list()
        list_lenght = int(ceil(len(unformatted_list)) / column_count)

        # groups lists together depending on column_count
        for i in range(list_lenght):
            c = (i * column_count)
            kg, pd, pt, rh, valor_un, valor_total = unformatted_list[c:c + column_count]
            formatted_list.append({"kg": kg, "pd": pd, "pt": pt, "rh": rh, "valor_un": valor_un, "valor_total": valor_total})

        return formatted_list


    analysis_list = cleanse_list(analysis.split("\n"))
    return format_list(analysis_list)


def load_to_excel(pdf_info, resumed=False):
    def return_last_empty_row(ss):
        for row in ss.iter_rows(min_row=3, min_col=2, max_col=2):
            if None is row[0].value:
                return row[0].row
    from openpyxl import load_workbook

    wb = load_workbook("resumo.xlsx")
    spreadsheet = wb.active

    if resumed:
        for pdf in pdf_info:
            row = return_last_empty_row(spreadsheet)

            spreadsheet.cell(row, 2).value = pdf["date"]
            spreadsheet.cell(row, 3).value = pdf["representative"]
            spreadsheet.cell(row, 4).value = pdf["buyer"]
            spreadsheet.cell(row, 5).value = pdf["cpf"]
            spreadsheet.cell(row, 6).value = pdf["summary"]["kg"]
            spreadsheet.cell(row, 7).value = pdf["summary"]["pd"]
            spreadsheet.cell(row, 8).value = pdf["summary"]["pt"]
            spreadsheet.cell(row, 9).value = pdf["summary"]["rh"]
            # spreadsheet.cell(row, 10).value = pdf["analysis"]["valor_un"]
            # spreadsheet.cell(row, 11).value = pdf["analysis"]["valor_total"]

    if not resumed:
        for pdf in pdf_info:
            last_empty_row = return_last_empty_row(spreadsheet)
            for i in range(len(pdf["analysis"])):
                row = last_empty_row + i

                spreadsheet.cell(row, 2).value = pdf["date"]
                spreadsheet.cell(row, 3).value = pdf["representative"]
                spreadsheet.cell(row, 4).value = pdf["buyer"]
                spreadsheet.cell(row, 5).value = pdf["cpf"]
                spreadsheet.cell(row, 6).value = float(pdf["analysis"][i]["kg"].replace(".", "").replace(",", "."))
                spreadsheet.cell(row, 7).value = float(pdf["analysis"][i]["pd"].replace(".", "").replace(",", "."))
                spreadsheet.cell(row, 8).value = float(pdf["analysis"][i]["pt"].replace(".", "").replace(",", "."))
                spreadsheet.cell(row, 9).value = float(pdf["analysis"][i]["rh"].replace(".", "").replace(",", "."))
                spreadsheet.cell(row, 10).value = float(pdf["analysis"][i]["valor_un"].replace(".", "").replace(",", "."))
                spreadsheet.cell(row, 11).value = float(pdf["analysis"][i]["valor_total"].replace(".", "").replace(",", "."))

    wb.save("resumo.xlsx")


pdf_information = load_pdfs()
load_to_excel(pdf_information, resumed=True)
