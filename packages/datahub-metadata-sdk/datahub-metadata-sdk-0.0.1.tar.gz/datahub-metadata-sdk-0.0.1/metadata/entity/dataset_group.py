
class DatasetGroup():

    def __init__(self,
                 name: str,
                 namespace: str = None,
                 auto_fix: bool = True):
        if auto_fix:
            self.name = name + "-" + get_auto_name()
        else:
            self.name = name
        if namespace is not None:
            self.name = namespace + "." + self.name

    def properties(self, key: str, value: str):
        if hasattr(self, "_properties"):
            self._properties[key] = value
        else:
            self._properties = {key: value}
        return self

    def get_urn(self):
        if hasattr(self, "urn"):
            return self.urn
        self.urn = builder.make_container_urn(guid=uuid.uuid1())
        return self.urn