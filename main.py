from openpyxl import load_workbook


class Workbook():
    def __init__(self, workbook_name: str) -> None:
        self.workbook_path = f"assets/{workbook_name}"
        self.workbook = load_workbook(self.workbook_path)

    def load_workbook(self, clone_name: str):
        try:
            if cloned_workbook := load_workbook(f"assets/{clone_name}.xlsx"):
                return cloned_workbook
        except FileNotFoundError:
            self.workbook.save(f"assets/{clone_name}.xlsx")
            cloned_workbook = load_workbook(f"assets/{clone_name}.xlsx")
            return cloned_workbook

    def sort_paths(list_of_paths):
        pass

    @staticmethod
    def str_to_float(string) -> float:
        return float(string.replace(".", "").replace(",", "."))
    
    def write(self, folders_list: list, resumed: bool = False):
        def return_last_empty_row(spreadsheet):
            for row in spreadsheet.iter_rows(min_row=3, min_col=2, max_col=2):
                if row[0].value is None:
                    return row[0].row

        for representative in folders_list.keys():
            for pdf in folders_list[representative]:
                workbook = self.load_workbook(representative)
                spreadsheet = workbook.active    
                last_empty_row = return_last_empty_row(spreadsheet)
                for i, analysis in enumerate(pdf.analysis):
                    row = last_empty_row + i

                    spreadsheet.cell(row, 2).value = pdf.date
                    spreadsheet.cell(row, 3).value = pdf.representative
                    spreadsheet.cell(row, 4).value = pdf.buyer
                    spreadsheet.cell(row, 5).value = pdf.buyer_cpf
                    spreadsheet.cell(row, 6).value = self.str_to_float(analysis["kg"])
                    spreadsheet.cell(row, 7).value = self.str_to_float(analysis["pd"])
                    spreadsheet.cell(row, 8).value = self.str_to_float(analysis["pt"])
                    spreadsheet.cell(row, 9).value = self.str_to_float(analysis["rh"])
                    spreadsheet.cell(row, 10).value = self.str_to_float(analysis["unitary_value"])
                    spreadsheet.cell(row, 11).value = self.str_to_float(analysis["total_value"])

                    workbook.save(f"assets/{representative}.xlsx")

import pdf

pdfs = pdf.load()
wb = Workbook("resumo.xlsx")
wb.write(pdfs)
