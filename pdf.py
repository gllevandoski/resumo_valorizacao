class PDF:
    def __init__(self, file: str) -> None:
        import fitz
        self.pdf = fitz.open(file)
        self.pdf_path = file
        self.properties = self.get_properties()

    def get_properties(self) -> dict:
        # top left coordinates (x0, y0) and bottom right coordinates (x1, y1)
        coordinates = {
                          "representative": (50, 80, 140, 95),
                          "buyer": (150, 80, 360, 95),
                          "date": (350, 80, 415, 100),
                          "buyer_cpf": (150, 110, 250, 120),
                          "buyer_rg": (250, 110, 350, 120),
                          "analysis_average": (110, 150, 150, 200),
                          "analysis": (50, 250, 435, 475),
                          "serial_number": (200, 200, 500, 225)
                      }

        properties = list()

        for page in self.pdf:
            properties.append({
                                   "analysis": self.analysis_to_list(page.get_text("text", coordinates["analysis"])),
                                   "analysis_average": self.analysis_average_to_dict(page.get_text("text", coordinates["analysis_average"])),
                                   "representative": page.get_text("text", coordinates["representative"]).strip(),
                                   "buyer": page.get_text("text", coordinates["buyer"]).strip(),
                                   "date": page.get_text("text", coordinates["date"]).strip(),
                                   "cpf": page.get_text("text", coordinates["buyer_cpf"]).strip(),
                                   "rg": page.get_text("text", coordinates["buyer_rg"]).strip(),
                                   "serial_number": page.get_text("text", coordinates["serial_number"]).strip()
                              })
            
        return properties
            
    @staticmethod
    def analysis_average_to_dict(analysis: list) -> dict:
        analysis_dict = dict()
        analysis = analysis.strip().split("\n")
        analysis_dict["pd"] = analysis[0]
        analysis_dict["pt"] = analysis[1]
        analysis_dict["rh"] = analysis[2]
        analysis_dict["kg"] = analysis[3]

        return analysis_dict

    @staticmethod
    def analysis_to_list(analysis: list) -> list:
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


        analysis_list = cleanse_list(analysis.split("\n"))
        return format_list(analysis_list, column_count=6)


def load() -> dict:
    from glob import glob
    from os import walk

    pdfs = dict()
    for folder in list(walk("valorizacoes"))[0][1]: # gets all the folders immediately bellow the folder
        files = glob(f"valorizacoes/{folder}/*.pdf")
        if files:
            pdfs[folder] = list()

            for file in files:
                pdf = PDF(file)
                pdfs[folder].append(pdf)

    return pdfs


if __name__ == "__main__":
    pdfs = load()

    for pdf in pdfs.values():
        for analysis in pdf:
            for prop in analysis.properties:
                print(prop)
