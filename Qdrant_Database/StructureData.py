import json
json_file_path = 'News/last.json'

with open(json_file_path, 'r') as json_file:
    # Load the JSON data from the file
    data = json.load(json_file)

class StructureData:
    def __init__(self,data):
        self.data = data
        self.data_list = zip(data[-1]["hrefs"], data[-1]["headings"], data[-1]["images"], data[-1]["time"], data[-1]["text"][:-1])

    def get_lenghts(self):
        text_length = len(self.data[-1]["text"][:-1])
        hrefs_length = len(self.data[-1]["hrefs"])
        images_length = len(self.data[-1]["images"])
        headings_length = len(self.data[-1]["headings"])
        return text_length,hrefs_length,images_length,headings_length

    def get_final_data(self):
        final_data = [
            {"href": href,"heading": heading, "image": image, "time": tm, "text": txt}
            for href, heading, image, tm, txt in self.data_list
            ]

        final_data_dict = {
            i: item
            for i, item in enumerate(final_data)
        }
        return final_data_dict


StructuredData =StructureData(data)
final_data =StructuredData.get_final_data()
# print(final_data)
# StructuredData.get_lenghts()
# print(final_data[2])
# print(final_data[0])
# print(StructuredData.get_lenghts())
