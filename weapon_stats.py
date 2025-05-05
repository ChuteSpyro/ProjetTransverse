class Arme:
    def __init__(self, nom: str, damages: int, maniability: int):
        self.nom = nom
        self.damages = damages
        self.maniability = maniability

    def __repr__(self):
        return f"Arme(nom={self.nom}, damages={self.damages}, maniability={self.maniability})"

# Exemple d'utilisation :
dagger = Arme(nom="Dagger", damages=25, maniability=70)
axe = Arme(nom="Axe", damages=60, maniability=45)
light_saber = Arme(nom="Hache", damages=40, maniability=55)

print(dagger)
print(axe)
print(light_saber)