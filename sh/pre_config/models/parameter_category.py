import yaql


class ParameterCategory:

    def __init__(self, name, data=None):
        self.engine = yaql.language.factory.YaqlFactory().create()
        self.name = name
        self.data = data
        self.evaluated_object = {}
        self.evaluated_array = []
        self.param_query_pairs = {}

    def get(self):
        self.evaluate_all_queries()
        for key in self.evaluated_object:
            string_value = self.generate_condor_output(key, self.evaluated_object[key])
            self.evaluated_array.append(string_value)
        return self.evaluated_array

    def add_key_value(self, key, value):
        self.evaluated_object[key] = value

    def add_key_value_query(self, param, query):
        self.param_query_pairs[param] = query

    def add(self, value):
        self.evaluated_array.append(value)

    def generate_condor_output(self, key, value):
        condor_knob = "{key} = {value}\n".format(key=key.upper(), value=value)
        return condor_knob

    def generate_yaim_output(self, key, value):
        env_variable = key.upper() + "=\"" + str(value) + "\"\n"
        return env_variable

    def evaluate_query(self, parameter):
        query = self.param_query_pairs[parameter]
        expression = self.engine(query)
        return expression.evaluate(self.data)

    def evaluate_all_queries(self):
        for parameter in self.param_query_pairs:
            value = self.evaluate_query(parameter)
            self.evaluated_object[parameter] = value