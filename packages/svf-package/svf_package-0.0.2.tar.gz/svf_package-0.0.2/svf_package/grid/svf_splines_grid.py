from itertools import product
from numpy import arange
from pandas import DataFrame

from svf_package.grid.grid import GRID


class SVF_SPLINES_GRID(GRID):

    def __init__(self, data, inputs, d):
        """
            Constructor de la clase SVF_SPLINES_GRID
        Args:
            data (pandas.DataFrame): conjunto de datos sobre los que se construye el grid
            inputs (list): listado de inputs
            d (int): número de particiones en las que se divide el grid
        """
        super().__init__(data, inputs, d)

    def create_grid(self):
        """
            Función que crea un grid en base a unos datos e hiperparámetro d
        """
        self.df_grid = DataFrame(columns=["id_cell", "value", "phi"])
        x = self.data.filter(self.inputs)
        # Numero de columnas x
        n_dim = len(x.columns)
        # Lista de listas de knot
        knot_list = list()
        # Lista de indices (posiciones) para crear el vector de subind
        knot_index = list()
        for col in range(0, n_dim):
            # knots de la dimension col
            knot = [0]
            knot_max = x.iloc[:, col].max()
            knot_min = x.iloc[:, col].min()
            amplitud = (knot_max - knot_min) / self.d
            for i in range(0, self.d + 1):
                knot_i = knot_min + i * amplitud
                knot.append(knot_i)
            knot_list.append(knot)
            knot_index.append(arange(0, len(knot)))
        self.df_grid["id_cell"] = list(product(*knot_index))
        self.df_grid["value"] = list(product(*knot_list))
        self.knot_list = knot_list
        self.calculate_df_grid_phi()

    def calculate_phi_observation(self, dmu):
        """
            Función que calcula el valor de la transformación (phi) de una observación en el grid.
        Args:
            dmu (list): Observación a evaluar

        Returns:
            list: Vector de 1 0 con la transformación del vector en base al grid
        """
        phi_list = []
        n_dim = len(dmu)
        for j in range(0, n_dim):
            phi = [1]
            for i in range(0, len(self.knot_list[j])):
                if dmu[j] >= self.knot_list[j][i]:
                    value = dmu[j] - self.knot_list[j][i]
                else:
                    value = 0
                phi.append(value)
            phi_list.append(phi)
        return phi_list

    def calculate_df_grid_phi(self):
        """Método para añadir al dataframe grid el valor de la transformada de cada observación
        """
        x = self.df_grid["value"]
        x_list = x.values.tolist()
        phi_list = list()
        for dmu in x_list:
            phi = self.calculate_phi_observation(dmu)
            phi_list.append(phi)
        self.df_grid["phi"] = phi_list
