from io import BytesIO

class Pdf:
    def __init__(self, file: BytesIO) -> None:
        import fitz
        pdf = fitz.open(stream=file)
        self.pages = list()

        for page in pdf:
            self.pages.append(PdfPage(page))

class PdfPage:
    def __init__(self, properties) -> None:
        self.properties = properties
        self.page_number = properties.number + 1

        # top left coordinates (x0, y0) and bottom right coordinates (x1, y1)
        # this is measured in points (1 inch = 72 points), you need to get this manually
        self.coordinates = {
                               "representative": (50, 75, 162, 88),
                               "buyer": (162, 75, 338, 88),
                               "date": (360, 75, 450, 88),
                               "buyer_cpf": (162, 105, 270, 118),
                               "buyer_rg": (270, 105, 400, 118),
                               "analysis_average": (110, 130, 160, 195),
                               "analysis": (50, 240, 465, 445),
                               "serial_number": (288, 190, 450, 220),
                               "analysis_type": (36, 225, 50, 245),
                               "total_value": (360, 495, 450, 515),
                               "quotations": (380, 130, 445, 195),
                               "avg_kg_price": (110, 495, 170, 515)
                           }
        self.ocr_extract_info()

    def ocr_extract_info(self):
        self.representative = self.properties.get_text("text", self.coordinates["representative"]).strip()
        self.buyer = self.properties.get_text("text", self.coordinates["buyer"]).strip()
        self.date = self.properties.get_text("text", self.coordinates["date"]).strip()

        self.buyer_cpf = self.properties.get_text("text", self.coordinates["buyer_cpf"]).strip()
        self.buyer_rg = self.properties.get_text("text", self.coordinates["buyer_rg"]).strip()
        self.serial_number = self.properties.get_text("text", self.coordinates["serial_number"]).strip()
        
        self.cleanse_quotations(self.properties.get_text("text", self.coordinates["quotations"]).strip().split("\n"))
        self.calculate_analysis_lines(self.properties.get_text("text", self.coordinates["analysis"]))
        self.calculate_analysis_average()

        try:
            self.analysis_type = int(self.properties.get_text("text", self.coordinates["analysis_type"]).strip())

        except ValueError as VE:
            print(f"page {self.properties.number}", VE)
            self.analysis_type = "erro"

    def cleanse_quotations(self, dirty_quotations):
        from string import digits
        self.quotations = list()

        for item in dirty_quotations:
            for digit in digits:
                if digit in item:
                    self.quotations.append(float(item.replace(".", "").replace(",", ".")))
                    break

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
