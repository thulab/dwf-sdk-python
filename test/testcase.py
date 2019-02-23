class TestCase:
    def __init__(self, name, desc, data, template, judgements):
        self.name = name
        self.desc = desc
        self.data = data
        self.template = template
        self.judgements = judgements

    def __repr__(self):
        print('Test Case of %s \n Content: %s \n Template: %s ' % (self.name, self.desc, self.template))
