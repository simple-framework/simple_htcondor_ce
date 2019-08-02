class ConfigFile:
    def __init__(self, output_file, data):
        self.categories = []
        self.evaluated_lines = []
        self.output_file = output_file
        self.data = data


    def add_categories(self, categories):
        for category in categories:
            self.categories.append(category)

    def evaluate_categories(self):
        for category in self.categories:
            evaluated_results = category.get()
            for data_entry in evaluated_results:
                self.evaluated_lines.append(data_entry)

    def generate_output_file(self):
        output_file = open(self.output_file, 'w')
        self.evaluate_categories()
        for line in self.evaluated_lines:
            output_file.write(line)
        output_file.close()