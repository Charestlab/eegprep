

class Configuration(object):

    def __init__(self):
        self.inner = {}

    def setDefaults(self, confDict):
        self.inner.update(confDict)

    def updateFromString(self, confString):
        lines = confString.splitlines()
        for line in lines:
            keyVal = line.split('=')
            if len(keyVal) == 2:
                key, value = [seg.strip('') for seg in keyVal]
                if key in self.inner:
                    if str(self.inner[key]).isdigit():
                        self.inner[key] = int(value)
                    else:
                        self.inner[key] = value

    def __getitem__(self, key):
        return self.inner[key]

    def __str__(self):
        lines = ['{}={}'.format(*i) for i in self.inner.items()]
        return '\n'+'\n'.join(lines)+'\n'
