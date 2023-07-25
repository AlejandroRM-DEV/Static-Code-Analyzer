iris = {}


def add_iris(id_n, species, petal_length, petal_width, **kwargs):
    new_dict = {
        "species": species,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }
    new_dict.update(kwargs)
    iris[id_n] = new_dict

