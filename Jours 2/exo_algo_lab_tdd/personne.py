class Personne:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not isinstance(value, str):
            raise ValueError('Name must be a non-empty string')
        self._name = value.strip()

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError('Age must be non-negative integer')
        self._age = value
