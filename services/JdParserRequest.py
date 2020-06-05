import json


class JdParserRequest():

    def _init_(self):
        self.skills = self.skills
        self.jdString = self.jdString
        self.function = self.function
        self.companyId = self.companyId
        self.skillFlag = self.skillFlag
        self.capabilityFlag = self.capabilityFlag

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

