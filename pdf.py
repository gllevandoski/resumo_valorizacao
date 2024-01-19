class Pdf:
    def __init__(self, file_path: str) -> None:
        import fitz
        pdf = fitz.open(file_path)
        self.pages = list()
        for page in pdf:
            self.pages.append(PdfPage(page))

class PdfPage:
    def __init__(self, properties) -> None:
        self.properties = properties
        self.page_number = properties.number
        # top left coordinates (x0, y0) and bottom right coordinates (x1, y1)
        self.coordinates = {
                               "representative": (50, 80, 150, 90),
                               "buyer": (150, 80, 360, 90),
                               "date": (350, 80, 415, 100),
                               "buyer_cpf": (150, 110, 250, 120),
                               "buyer_rg": (250, 110, 350, 120),
                               "analysis_average": (110, 130, 150, 220),
                               "analysis": (50, 250, 440, 475),
                               "serial_number": (200, 200, 500, 225),
                               "analysis_type": (30, 230, 40, 245),
                               "total_value": (390, 500, 460, 530)
                           }
        self.ocr_extract_info()

    def ocr_extract_info(self):
        self.representative = self.properties.get_text("text", self.coordinates["representative"]).strip()
        self.buyer = self.properties.get_text("text", self.coordinates["buyer"]).strip()
        self.date = self.properties.get_text("text", self.coordinates["date"]).strip()

        self.buyer_cpf = self.properties.get_text("text", self.coordinates["buyer_cpf"]).strip()
        self.buyer_rg = self.properties.get_text("text", self.coordinates["buyer_rg"]).strip()
        self.serial_number = self.properties.get_text("text", self.coordinates["serial_number"]).strip()

        try:
            self.analysis_type = int(self.properties.get_text("text", self.coordinates["analysis_type"]).strip())
        except ValueError as VE:
            print(f"page {self.properties.number}", VE)
            self.analysis_type = "erro"

        self.calculate_analysis_lines(self.properties.get_text("text", self.coordinates["analysis"]))
        self.calculate_analysis_average()

    def calculate_analysis_average(self) -> dict:
        from string import ascii_letters
        try:
            analysis = self.properties.get_text("text", self.coordinates["analysis_average"])
            analysis = analysis.strip().split("\n")
            analysis_dict = dict()

            analysis_dict["pd"] = analysis[0]
            analysis_dict["pt"] = analysis[1]
            analysis_dict["rh"] = analysis[2]
            analysis_dict["kg"] = analysis[3]
            analysis_dict["unitary_value"] = "0"
            analysis_dict["total_value"] = self.properties.get_text("text", self.coordinates["total_value"]).strip().strip(ascii_letters).strip("/\\")

            self.analysis_average = analysis_dict
        except IndexError as E:
            self.analysis_average = "erro"
            print(self.properties, E)

    def calculate_analysis_lines(self, dirty_list) -> list:
        def cleanse_list(dirty_list: list) -> list:
            from string import digits
            clean_list = list()

            for item in dirty_list:
                for digit in digits:
                    if digit in item:
                        clean_list.append(item)
                        break

            return clean_list

        def format_list(unformatted_list: list, column_count: int = 6) -> list:
            from math import ceil
            list_lenght = int(ceil(len(unformatted_list)) / column_count)
            formatted_list = list()

            # groups the old list items together in new lists the size of column_count
            for i in range(list_lenght):
                c = (i * column_count)
                kg, pd, pt, rh, unitary_value, total_value = unformatted_list[c:c + column_count]
                formatted_list.append({"kg": kg, "pd": pd, "pt": pt, "rh": rh, "unitary_value": unitary_value, "total_value": total_value})

            return formatted_list

        analysis_list = cleanse_list(dirty_list.split("\n"))
        self.analytics = format_list(analysis_list, column_count=6)

        if self.analytics == []:
            self.analytics.append(f"error on {self.buyer}")


def load() -> list:
    from glob import glob

    pdfs = list()
    files = glob(f"pdf/**/*.pdf", recursive=True)

    for file in files:
        pdf = Pdf(file)
        pdfs.append(pdf)

    return pdfs


if __name__ == "__main__":
    pdfs = load()

    for pdf in pdfs:
        for page in pdf.pages:
            print(page)
