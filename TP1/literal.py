class Literal:
	def __init__(self, name, verite):
		self._name = name
		self._verite = verite
	
	def __str__(self):
		if not(self._verite):
			return f"!{self._name}"
		else:
			return self._name

	def __hash__(self):
		return hash((self._name, self._verite)) # Hash le nom ou le nom+1 si la negation

	def __eq__(self, other) -> bool:
		return (self._name == other._name) and (self._verite == other._verite)
	
	def __invert__(self):
		return Literal(self._name, not(self._verite))