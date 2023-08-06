from docplex.mp.model import Model
from svf_package.grid.svf_grid import SVF_GRID
from svf_package.svf import SVF
from svf_package.svf_solution import SVFSolution


class SSVF(SVF):

    """Clase del modelo SVF Simplificado
    """

    def __init__(self, method, inputs, outputs, data, C, eps, d):
        """Constructor de la clase SSVF

        Args:
            method (string): Método SVF que se quiere utilizar
            inputs (list): Inputs a evaluar en el conjunto de dato
            outputs (list): Outputs a evaluar en el conjunto de datos
            data (pandas.DataFrame): Conjunto de datos a evaluar
            C (float): Valores del hiperparámetro C del modelo
            eps (float): Valores del hiperparámetro épsilon del modelo
            d (int): Valor del hiperparámetro d del modelo
        """
        super().__init__(method, inputs, outputs, data, C, eps, d)

    def train(self):
        """Metodo que entrena un modelo SSVF
        """

        y_df = self.data.filter(self.outputs)
        y = y_df.values.tolist()

        # Numero de dimensiones y del problema
        n_dim_y = len(y_df.columns)
        # Numero de observaciones del problema
        n_obs = len(y)

        #######################################################################
        # Crear el grid
        self.grid = SVF_GRID(self.data, self.inputs, self.d)
        self.grid.create_grid()

        # Numero de variables w
        n_var = len(self.grid.df_grid.phi[0])

        #######################################################################

        # Variable w
        # name_w: (i,j)-> i:es el indice de la columna de la matriz phi;j: es el indice de la dimension de y
        name_w = [(i, j) for i in range(0, n_dim_y) for j in range(0, n_var)]
        w = {}
        w = w.fromkeys(name_w, 1)

        # Variable Xi
        name_xi = [(i, j) for i in range(0, n_dim_y) for j in range(0, n_obs)]
        xi = {}
        xi = xi.fromkeys(name_xi, self.C)

        mdl = Model("SSVF C:" + str(self.C) + ", eps:" + str(self.eps) + ", d:" + str(self.d))
        mdl.context.cplex_parameters.threads = 1

        # Variable w
        w_var = mdl.continuous_var_dict(name_w, ub=1e+33, lb=0, name='w')
        # Variable xi
        xi_var = mdl.continuous_var_dict(name_xi, ub=1e+33, lb=0, name='xi')

        # Funcion objetivo
        mdl.minimize(mdl.sum(w_var[i] * w_var[i] * w[i] for i in name_w) + mdl.sum(xi_var[i] * xi[i] for i in name_xi))

        # Restricciones
        for i in range(0, n_obs):
            for dim_y in range(0, n_dim_y):
                left_side = y[i][dim_y] - mdl.sum(w_var[dim_y, j] * self.grid.df_grid.phi[i][j] for j in range(0, n_var))
                # (1)
                mdl.add_constraint(
                    left_side <= 0,
                    ctname='c1_' + str(i) + "_" + str(dim_y)
                )
                # (2)
                mdl.add_constraint(
                    -left_side <= self.eps + xi_var[dim_y, i],
                    ctname='c2_' + str(i) + "_" + str(dim_y)
                )
        self.model = mdl

    def modify_model(self, c, eps):
        """Método que se utiliza para modificar el valor de C y las restricciones de un modelo
        Args:
            c (float): Valores del hiperparámetro C del modelo_
            eps (float): Valores del hiperparámetro épsilon del modelo

        Returns:
            docplex.mp.model.Model: modelo SVF modificado
        """
        n_obs = len(self.data)
        model = self.model.copy()
        name_var = model.iter_variables()
        name_w = list()
        name_xi = list()
        for var in name_var:
            name = var.get_name()
            if name.find("w") == -1:
                name_xi.append(name)
            else:
                name_w.append(name)
        # Variable w
        w = {}
        w = w.fromkeys(name_w, 1)

        # Variable Xi
        xi = {}
        xi = xi.fromkeys(name_xi, c)

        a = [model.get_var_by_name(i) * model.get_var_by_name(i) * w[i] for i in name_w]
        b = [model.get_var_by_name(i) * xi[i] for i in name_xi]
        # Funcion objetivo
        model.minimize(model.sum(a) + model.sum(b))
        # Modificar restricciones
        for i in range(0, n_obs):
            for r in range(len(self.outputs)):
                const_name = 'c2_' + str(i) + "_" + str(r)
                rest = model.get_constraint_by_name(const_name)
                rest.rhs += eps
        return model

    def solve(self):
        """Solución de un modelo SVF
        """
        n_dim_y = len(self.outputs)
        self.model.solve()
        name_var = self.model.iter_variables()
        sol_w = list()
        sol_xi = list()
        for var in name_var:
            name = var.get_name()
            sol = self.model.solution[name]
            if name.find("w") == -1:
                sol_xi.append(sol)
            else:
                sol_w.append(sol)
        # Numero de ws por dimension
        n_w_dim = int(len(sol_w) / n_dim_y)
        mat_w = [[] for _ in range(0, n_dim_y)]
        cont = 0
        for i in range(0, n_dim_y):
            for j in range(0, n_w_dim):
                mat_w[i].append(round(sol_w[cont], 6))
                cont += 1
        self.solution = SVFSolution(mat_w, sol_xi)

