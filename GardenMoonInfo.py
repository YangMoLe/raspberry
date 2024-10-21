from collections import defaultdict
import re


def convert_month_names(text):
    """
    Convert German month names to English in the given text.
    """
    month_map = {
        "Januar": "January",
        "Februar": "February",
        "Maerz": "March",
        "April": "April",
        "Mai": "May",
        "Juni": "June",
        "Juli": "July",
        "August": "August",
        "September": "September",
        "Oktober": "October",
        "November": "November",
        "Dezember": "December"
    }
    # Create a regular expression pattern to match German month names
    pattern = "|".join(month_map.keys())
    # Use a lambda function with re.sub to perform the conversion
    converted_text = re.sub(pattern, lambda match: month_map[match.group()], text)
    return converted_text


def convert_umlauts(text):
    """
    Convert umlauts (ä, ö, ü) to their respective character sequences.
    """
    umlaut_map = {"ä": "ae", "ö": "oe", "ü": "ue"}
    for umlaut, replacement in umlaut_map.items():
        text = text.replace(umlaut, replacement)
    return text

def create_measure_dict(text):
    lines = text.split("\n")
    measure_dict = defaultdict(list)
    for line in lines[1:]:
        if line.strip():  # Check if the line is not empty
            parts = line.split("\t")
            measure = parts[0]
            dates = re.findall(r"([A-Za-z]+):\s*(.*?)\s*(?=[A-Za-z]+:|$)", parts[2])
            for month, date_range in dates:
                # Convert umlauts
                month = convert_umlauts(month)
                # Extract individual date ranges and individual days
                date_ranges = re.findall(r"(\d+)\.?\w*-(\d+)\.?\w*|(\d+)", date_range)
                for date_range in date_ranges:
                    if date_range[0] and date_range[1]:  # Date range
                        start, end = int(date_range[0]), int(date_range[1])
                        measure_dict[month].append((start, end, measure))
                    elif date_range[2]:  # Single day
                        day = int(date_range[2])
                        measure_dict[month].append((day, day, measure))
    return measure_dict




text = """Säen oder setzen von Pflanzen, deren Früchte genutzt werden	Generell bei zunehmendem Mond! Dann am besten in Feuerzeichen	März: 11.-24., 11.-12., 20.-21. April: 9.-23., 9.v, 16.-18.n. Mai: 9.-22., 13.n-15. Juni: 7.-21., 10.-11., 20.-21. Juli: 7.-20., 7.-9.n, 17.-18. August: 5.-18., 5., 1
Säen oder setzen von Pflanzen, deren Blätter genutzt werden 	Arten, die zum „Schießen“ neigen: Generell bei abnehmendem Mond! Dann am besten in Wasserzeichen. Nie aber bei Mondstand in Jungfrau.	März: 1.-9., 26.-31., 1.-2.v, 9., 27.n-29. April: 1.-7., 25.-30., 5.n-7.v, 25. Mai: 1.-7., 24.-31., 3.-4., 30.-31. Juni: 1.-5., 23.-30., 26.-27. Juli: 1.-5., 22.-31., 5., 23.n.-25.n August: 1.-3., 20.-31., 1.-3.v, 20.-21., 28.n-30. September:1.,19.-29.v., 25.-26.
Säen oder setzen von Pflanzen, deren Blüten genutzt werden 	Generell bei zunehmendem Mond! Dann am besten in Luftzeichen	März: 11.-24., 15.-17.v April: 9.-23., 12.-13., 21.-23.n Mai: 9.-22., 9.-10., 18.n-20. Juni: 7.-21., 7.v, 15.-16. Juli: 7.-20., 12.-14.n August: 5.-18., 8.n-10., 18. September: 4.-17., 5.-6.,
Gießen und Bewässern	Generell bei Mondstand in Wasserzeichen	März: 1.-2.v, 9., 17.n-19., 27.n-29. April: 5.n-7.v, 14.-15., 25. Mai: 3.-4., 11.-13v, 21.-22., 30.-31. Juni: 7.n-9., 17.n-19., 26.-27. Juli: 5., 15.-16., 23.n.-25.n August: 1.-3.v, 11.-12., 20.-21., 28.n-30. September: 7.-9., 16.n-17., 25.-26. Oktober: 4.n-6., 14.-15., 22.-23.
Düngen von Gemüse, Obst	Generell bei abnehmendem Mond und bei Vollmond. Dann am besten in Feuerzeichen	März: 1.-9., 25.-31., 2.n-4., 30.-31. April: 1.-7., 24.-30., 7.n, 26.-28.v Mai: 1.-7., 23.-31., 5.-6., 23.-25. Juni: 1.-5., 22.-30., 1.-2., 28.n-30. Juli: 1.-5., 21.-31., 26.-27. August: 1.-3., 19.-31., 3.n, 22.-23., 31. September: 1.-2., 18.-30., 1., 18.-20.v, 27.-29.v Oktober: 1.,17.-31., 24.-26"""


# Update Calendar
#text = convert_umlauts(text)
#text = convert_month_names(text)
#measure_dict = create_measure_dict(text)

#measures = ["Saeen oder setzen von Pflanzen, deren Blaetter genutzt werden", "Saeen oder setzen von Pflanzen, deren Blueten genutzt werden", "Gießen und Bewaessern", "Duengen von Gemuese, Obst"]


class GardenMoonInfo:
    measures_names = ['Saeen oder setzen Blaetter', 'Saeen oder setzen Fruechte', 'Gießen und Bewaessern', 'Duengen']
    measure_dict = {"March": [(1, 9, 0), (26, 31, 0), (1, 2, 0), (9, 9, 0), (27, 29, 0), (11, 24, 1), (15, 17, 1), (1, 2, 2), (9, 9, 2), (17, 19, 2), (27, 29, 2), (1, 9, 2), (25, 31, 2), (2, 4, 2), (30, 31, 2)],
        "April": [(1, 7, 0), (25, 30, 0), (5, 7, 0), (25, 25, 0), (9, 23, 1), (12, 13, 1), (21, 23, 1), (5, 7, 2), (14, 15, 2), (25, 25, 2), (1, 7, 2), (24, 30, 2), (7, 7, 2), (26, 28, 2)],
        "May": [(1, 7, 0), (24, 31, 0), (3, 4, 0), (30, 31, 0), (9, 22, 1), (9, 10, 1), (18, 20, 1), (3, 4, 2), (11, 13, 2), (21, 22, 2), (30, 31, 2), (1, 7, 2), (23, 31, 2), (5, 6, 2), (23, 25, 2)],
        "June": [(1, 5, 0), (23, 30, 0), (26, 27, 0), (7, 21, 1), (7, 7, 1), (15, 16, 1), (7, 9, 2), (17, 19, 2), (26, 27, 2), (1, 5, 2), (22, 30, 2), (1, 2, 2), (28, 30, 2)],
        "July": [(1, 5, 0), (22, 31, 0), (5, 5, 0), (23, 23, 0), (25, 25, 0), (7, 20, 1), (12, 14, 1), (5, 5, 2), (15, 16, 2), (23, 23, 2), (25, 25, 2), (1, 5, 2), (21, 31, 2), (26, 27, 2)],
        "August": [(1, 3, 0), (20, 31, 0), (1, 3, 0), (20, 21, 0), (28, 30, 0), (5, 18, 1), (8, 10, 1), (18, 18, 1), (1, 3, 2), (11, 12, 2), (20, 21, 2), (28, 30, 2), (1, 3, 2), (19, 31, 2), (3, 3, 2), (22, 23, 2), (31, 31, 2)],
        "September": [(1, 1, 0), (19, 29, 0), (25, 26, 0), (4, 17, 1), (5, 6, 1), (7, 9, 2), (16, 17, 2), (25, 26, 2), (1, 2, 2), (18, 30, 2), (1, 1, 2), (18, 20, 2), (27, 29, 2)],
        "October": [(4, 6, 2), (14, 15, 2), (22, 23, 2), (1, 1, 2), (17, 31, 2), (24, 26, 2)]}

    def __init__(self, desired_date):
        self.desired_date = desired_date
        self.measures = self.get_measures_at_date(desired_date)

    def get_measures_at_date(self, desired_date):
        month, day = desired_date.split()
        day = int(day)
        # Convert umlauts
        month = convert_umlauts(month)
        measures = self.measure_dict.get(month, [])
        matching_measures = []
        for start, end, measure in measures:
            if start <= day <= end and measure not in matching_measures:
                matching_measures.append(measure)
        if matching_measures:
            return matching_measures
        return ["Kannst chillen."]

    def fetch_content(self):
        return self.measures

    def parse_content(self, content):
        translated_measures = []
        for meas_index in content:
            translated_measures.append(self.measures_names[meas_index])
        return f"{', '.join(translated_measures)}"

if __name__ == "__main__":
    # Example usage
    import datetime
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%B %d")
    garden_info = GardenMoonInfo(formatted_date)
    print(garden_info.parse_content(garden_info.fetch_content()))