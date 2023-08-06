"""
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░▒▒▒▒▒░░░░░░░░░░▒▒▒▒░░░░░░░░░░░▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░▒▓▓▓▓▓▓▓▒░░░░░░▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░▓▓▓▓▓▓▓▓▓░░░░░░▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░▓▓▓▓▓▓▓░░░░░░░▒▒▒▒▒▒▒░░░░░░░░▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░██▓▓▓▓▒░░░░░░░▒█▒░░░░░░░░▓█▓░░░░██░░░░░░░░░█▒░░░░░░░▒▓▓▓█▓▓▓░░░░░░░░▒▓▓▓▓▓▓▓░░░░░░
░░░░░█▓░░░░░░░░░░░░▒█▒░░░░░░░░▓█▓█▒░░██░░░░░░░░░█▒░░░░░░░░░░▒█░░░░░░░░░░▒█▒░░░░░▒█▒░░░░
░░░░░██▓▓▓▓░░░░░░░░▒█▒░░░░░░░░▓▓░▒█▓░██░░░░░░░░░█▒░░░░░░░░░░▒█░░░░░░░░░░▓█░░░░░░░█▓░░░░
░░░░░█▓░░░░░░░░░░░░▒█▒░░░░░░░░▓▓░░░▓▓██░░░░░░░░░█▒░░░░░░░░░░▒█░░░░░░░░░░▒█▓░░░░░▓█░░░░░
░░░░░▓▓░░░░░░░░░░░░▒▓░░░░░░░░░▓▓░░░░▒▓▓░░░░░░░░░▓▒░░░░░░░░░░▒▓░░░░░░░░░░░░▒▓▓▓▓▓▒░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
"""
################################################################################
# UNIVERSIDADE FEDERAL DE CATALÃO (UFCAT)
# WANDERLEI MALAQUIAS PEREIRA JUNIOR,                  ENG. CIVIL / PROF (UFCAT)
# MARCOS NAPOLEÃO RABELO,                              ENG. CIVIL / PROF (UFCAT)
# DAVIDSON DE OLIVEIRA FRANÇA JUNIOR,                    ENG. CIVIL / PROF (UNA)
# GABRIEL BERNARDES CARVALHO,                                 ENG. CIVIL (UFCAT)
# JOSÉ VITOR CARVALHO SILVA,                                  ENG. CIVIL (UFCAT)
# MURILO CARNEIRO RODRIGUES,                                  ENG. CIVIL (UFCAT)
################################################################################

################################################################################
# DESCRIÇÃO ALGORITMO:
# BIBLIOTECA FINITO PARA FUNÇÕES DO ALGORITMO MEF2D DESENVOLVIDA PELO GRUPO DE 
# PESQUISA E ESTUDOS EM ENGENHARIA (GPEE)
################################################################################

################################################################################
# BIBLIOTECAS NATIVAS PYTHON
import numpy as np

################################################################################
# BIBLIOTECAS DESENVOLVEDORES GPEE
    
def GET_VALUE_FROM_DICT_MEF2D_FINITO(DICTIONARY):
    """
    This function read input data from dictionary.

    Input:
    FILENAME             | Structural dataset                                     | Py dictionary

    Output: 
    N_NODES              | Number of nodes                                        | Integer
    N_MATERIALS          | Number of materials                                    | Integer
    N_THICKNESS          | Number of thicness                                     | Integer
    N_ELEMENTS           | Number of CST element                                  | Integer
    N_FORCES             | Number of nodal forces                                 | Integer
    N_PRESSURES          | Number of element pressures                            | Integer
    N_DISPLACEMENTS      | Number of nodal displacement control                   | Integer
    TYPE_PLANE           | Type of analysis in the plan                           | String
                         |      'EPT' - Plane Stress                              |
                         |      'EPD' - Plane Strain                              |
    TYPE_ELEMENT         | Type element in Finito algorithm                       | Integer 
                         |      0 - Frame bar element                             |
                         |      1 - CST surface element                           |
    TYPE_SOLUTION        | Solution of the system of equations                    | Integer
                         |      0 - Condense procedure                            |
                         |      1 - 0 and 1 algorithm                             |
    TYPE_INTEGRATION     | Type numerical integration                             | String
                         |      1 - Hammer 12 points integration                  |
    COORDINATES          | Coordinates properties                                 | Py Numpy array
                         |      Node, X, Y                                        |
    MATERIALS            | Materials properties                                   | Py Numpy array
                         |      ID, Young, Poisson, Density                       |
    THICKNESS            | Thickness properties                                   | Py Numpy array
                         |      ID, Thickness                                     |
    ELEMENTS             | Elements properties                                    | Py Numpy array
                         |      ID, Node 0 ... Node (N_DODES - 1), Material ID,   |
                         |      Thickness ID                                      |
    NODAL_EXTERNAL_LOAD  | Nodal force properties                                 | Py Numpy array              
                               ID, node ID, FX value, FY value 
    # # # # # # # # # # # # # # # # # # # # # # # # #

    PRESSURES: Under development 
    
    # # # # # # # # # # # # # # # # # # # # # # # # #
    PRESCRIPTIONS:       | Displacement properties                                | Py Numpy array  
                         |  ID, Node ID, Direction ('X', Y' and 'BOTH'), Displa-  |
                         |  cement value                                          |
    """
    N_NODES = DICTIONARY["N_NODES"]
    N_MATERIALS = DICTIONARY["N_MATERIALS"]
    N_THICKNESS = DICTIONARY["N_THICKNESS"]
    N_ELEMENTS = DICTIONARY["N_ELEMENTST3"]
    N_ELEMENTST6 = DICTIONARY["N_ELEMENTST6"]
    N_ELEMENTST10 = DICTIONARY["N_ELEMENTST10"]
    N_FORCES = DICTIONARY["N_FORCES"]
    N_PRESSURES = DICTIONARY["N_PRESSURES"]
    N_DISPLACEMENTS = DICTIONARY["N_DISCPLACEMENTS"]
    TYPE_PLANE = DICTIONARY["TYPE_PLANE"]
    TYPE_ELEMENT = DICTIONARY["TYPE_ELEMENT"]
    TYPE_SOLUTION = DICTIONARY["TYPE_SOLUTION"]
    GRAU_INT = DICTIONARY["GRAU_INT"]
    COORDINATES = DICTIONARY["COORDINATES"]
    MATERIALS = DICTIONARY["MATERIALS"]
    THICKNESS = DICTIONARY["THICKNESS"]
    ELEMENTS = DICTIONARY["ELEMENTS"]
    NODAL_EXTERNAL_LOAD = DICTIONARY["EXTERNAL LOADS"]
    PRESCRIPTIONS = DICTIONARY["PRESCRIBED DISPLACEMENTS"]
    return N_NODES, N_MATERIALS, N_THICKNESS, N_ELEMENTS, N_ELEMENTST6, N_ELEMENTST10, N_FORCES, N_PRESSURES, N_DISPLACEMENTS, N_DISPLACEMENTS, TYPE_PLANE, TYPE_ELEMENT, TYPE_SOLUTION, GRAU_INT, COORDINATES, MATERIALS, THICKNESS, ELEMENTS, NODAL_EXTERNAL_LOAD, PRESCRIPTIONS

def GET_VALUE_FROM_TXT_MEF2D_FINITO(FILENAME):
    """
    This function read input data from .txt file.

    Input:
    FILENAME             | Structural dataset                                     | .txt extension

    Output: 
    N_NODES              | Number of nodes                                        | Integer
    N_MATERIALS          | Number of materials                                    | Integer
    N_THICKNESS          | Number of thicness                                     | Integer
    N_ELEMENTS           | Number of CST element                                  | Integer
    N_FORCES             | Number of nodal forces                                 | Integer
    N_PRESSURES          | Number of element pressures                            | Integer
    N_DISPLACEMENTS      | Number of nodal displacement control                   | Integer
    TYPE_PLANE           | Type of analysis in the plan                           | String
                         |      'EPT' - Plane Stress                              |
                         |      'EPD' - Plane Strain                              |
    TYPE_ELEMENT         | Type element in Finito algorithm                       | Integer 
                         |      0 - Frame bar element                             |
                         |      1 - CST surface element                           |
    TYPE_SOLUTION        | Solution of the system of equations                    | Integer
                         |      0 - Condense procedure                            |
                         |      1 - 0 and 1 algorithm                             |
    TYPE_INTEGRATION     | Type numerical integration                             | String
                         |      1 - Hammer 12 points integration                  |
    COORDINATES          | Coordinates properties                                 | Py Numpy array
                         |      Node, X, Y                                        |
    MATERIALS            | Materials properties                                   | Py Numpy array
                         |      ID, Young, Poisson, Density                       |
    THICKNESS            | Thickness properties                                   | Py Numpy array
                         |      ID, Thickness                                     |
    ELEMENTS             | Elements properties                                    | Py Numpy array
                         |      ID, Node 0 ... Node (N_DODES - 1), Material ID,   |
                         |      Thickness ID                                      |
    NODAL_EXTERNAL_LOAD  | Nodal force properties                                 | Py Numpy array              
                               ID, node ID, FX value, FY value 
    # # # # # # # # # # # # # # # # # # # # # # # # #

    PRESSURES: Under development 
    
    # # # # # # # # # # # # # # # # # # # # # # # # #
    PRESCRIPTIONS:       | Displacement properties                                | Py Numpy array  
                         |  ID, Node ID, Direction ('X', Y' and 'BOTH'), Displa-  |
                         |  cement value                                          |
    """
    # Read input file general properties
    FILE = open(FILENAME, "r")
    DATASET = FILE.read().split("\n")
    N_NODES = int(DATASET.pop(0).split(':')[1])
    N_MATERIALS = int(DATASET.pop(0).split(':')[1])
    N_THICKNESS = int(DATASET.pop(0).split(':')[1])
    N_ELEMENTS = int(DATASET.pop(0).split(':')[1])
    N_ELEMENTST6 = int(DATASET.pop(0).split(':')[1])
    N_ELEMENTST10 = int(DATASET.pop(0).split(':')[1])
    N_FORCES = int(DATASET.pop(0).split(':')[1])
    N_PRESSURES = int(DATASET.pop(0).split(':')[1])
    N_DISPLACEMENTS = int(DATASET.pop(0).split(':')[1])
    TYPE_PLANE = int(DATASET.pop(0).split(':')[1])
    TYPE_ELEMENT = int(DATASET.pop(0).split(':')[1])
    TYPE_SOLUTION = int(DATASET.pop(0).split(':')[1])
    TYPE_INTEGRATION = int(DATASET.pop(0).split(':')[1])
    # Read coordinates 
    DATASET.pop(0)
    DATASET.pop(0)   
    COORDINATES = np.zeros((N_NODES, 2))
    for I_COUNT in range(N_NODES):
        VALUES = DATASET.pop(0).split(',')
        COORDINATES[int(VALUES[0]), 0] = float(VALUES[1])
        COORDINATES[int(VALUES[0]), 1] = float(VALUES[2])
    # Read materials
    DATASET.pop(0)
    DATASET.pop(0)
    MATERIALS = np.zeros((N_MATERIALS, 3))
    for J_COUNT in range(N_MATERIALS):
        VALUES1 = DATASET.pop(0).split(',')
        MATERIALS[int(VALUES1[0]), 0] = float(VALUES1[1])
        MATERIALS[int(VALUES1[0]), 1] = float(VALUES1[2])
    # Read thickness
    DATASET.pop(0)
    DATASET.pop(0)
    THICKNESS = np.zeros((N_THICKNESS, 1))
    for K_COUNT in range(N_THICKNESS):
        VALUES2 = DATASET.pop(0).split(',')
        THICKNESS[int(VALUES2[0]), 0] = float(VALUES2[1])
    # Read Elements
    DATASET.pop(0)
    DATASET.pop(0)
    # COLOCAR AQUI UM IF PARA DIZER QUE ESSA LEITURA É SÓ DO T3
    ELEMENTS = np.zeros((N_ELEMENTS, 5))
    for L_COUNT in range(N_ELEMENTS):
        VALUES3 = DATASET.pop(0).split(',')
        ELEMENTS[int(VALUES3[0]), 0] = int(VALUES3[1])
        ELEMENTS[int(VALUES3[0]), 1] = int(VALUES3[2])
        ELEMENTS[int(VALUES3[0]), 2] = int(VALUES3[3])
        ELEMENTS[int(VALUES3[0]), 3] = int(VALUES3[4])
        ELEMENTS[int(VALUES3[0]), 4] = int(VALUES3[5])
    # Read nodal forces
    DATASET.pop(0)
    DATASET.pop(0)
    NODAL_EXTERNAL_LOAD = np.zeros((N_FORCES, 3))
    for M_COUNT in range(N_FORCES):
        VALUES4 = DATASET.pop(0).split(',')
        NODAL_EXTERNAL_LOAD[int(VALUES4[0]), 0] = float(VALUES4[1])  # Nó
        if float(VALUES4[2]) != 0:
            NODAL_EXTERNAL_LOAD[int(VALUES4[0]), 2] = float(VALUES4[2])
            NODAL_EXTERNAL_LOAD[int(VALUES4[0]), 1] = 0
        elif float(VALUES4[3]) != 0:
            NODAL_EXTERNAL_LOAD[int(VALUES4[0]), 2] = float(VALUES4[3])
            NODAL_EXTERNAL_LOAD[int(VALUES4[0]), 1] = 1
    # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # Under development Pressure read
    
    # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Read displacement
    DATASET.pop(0)
    DATASET.pop(0)
    COUNT = 0
    for K_COUNT in range(N_DISPLACEMENTS):
        VALUES5 = DATASET[K_COUNT].split(',')

        if VALUES5[2] == "'BOTH'":
            COUNT += 2

        else:
            COUNT += 1
    PRESCRIPTIONS = np.zeros((COUNT, 3))
    COUNT = 0
    for w in range(N_DISPLACEMENTS):
        VALUES6 = DATASET.pop(0).split(',')
        if VALUES6[2] == "'X'":
            PRESCRIPTIONS[COUNT, 0] = int(VALUES6[1])
            PRESCRIPTIONS[COUNT, 1] = 0
            PRESCRIPTIONS[COUNT, 2] = float(VALUES6[3])
            COUNT += 1
        elif VALUES6[2] == "'Y'":
            PRESCRIPTIONS[COUNT, 0] = int(VALUES6[1])
            PRESCRIPTIONS[COUNT, 1] = 1
            PRESCRIPTIONS[COUNT, 2] = float(VALUES6[3])
            COUNT += 1
        else:
            PRESCRIPTIONS[COUNT, 0] = int(VALUES6[1])
            PRESCRIPTIONS[COUNT, 1] = 0
            PRESCRIPTIONS[COUNT, 2] = float(VALUES6[3])
            COUNT += 1
            PRESCRIPTIONS[COUNT, 0] = int(VALUES6[1])
            PRESCRIPTIONS[COUNT, 1] = 1
            PRESCRIPTIONS[COUNT, 2] = float(VALUES6[3])
            COUNT += 1
    return N_NODES, N_MATERIALS, N_THICKNESS, N_ELEMENTS, N_ELEMENTST6, N_ELEMENTST10, N_FORCES, N_PRESSURES, N_DISPLACEMENTS, TYPE_PLANE, TYPE_ELEMENT, TYPE_SOLUTION, TYPE_INTEGRATION, COORDINATES, MATERIALS, THICKNESS, ELEMENTS, NODAL_EXTERNAL_LOAD, PRESCRIPTIONS

# ORGANIZAÇÃO DAS PROPRIEDADES GEOMÉTRICAS DO ELEMENTO I TIPO PLANO
def GEOMETRIC_PROPERTIES_1(COORDINATES, ELEMENTS, I_ELEMENT, THICKNESS, AUX_2):
    """ 
    This function assigns the surface element's geometric propertiest of the I_ELEMENT element TYPE_ELEMENT = 1 (CST element).
    
    Input:
    COORDINATES        | Coordinates properties                                | Py Numpy array
                       |    Node, x, y                                         |
    ELEMENTS           | Elements properties                                   | Py Numpy array
                       |    Node 0 ... Node (N_NODES - 1), Material ID,        |
                       |    Thickness ID                                       |
    THICKNESS          | Thickness properties                                  | Py Numpy array
                       |    Thickness                                          |
    I_ELEMENT          | ID i element in looping for                           | Integer
    AUX_2              | ID thickness                                          | Integer

    Output: 
    SECTION_IELEMENT   | Section I_ELEMENT properties                          | Py dictionary
                       |     ['X_E']       - Elements coordinates              |                                   
                       |     ['THICKNESS'] - Sine                              |
    """
    NODE_0 = int(ELEMENTS[I_ELEMENT, 0])
    X0, Y0 = COORDINATES[NODE_0, 0], COORDINATES[NODE_0, 1]
    NODE_1 = int(ELEMENTS[I_ELEMENT, 1])
    X1, Y1 = COORDINATES[NODE_1, 0], COORDINATES[NODE_1, 1]
    NODE_2 = int(ELEMENTS[I_ELEMENT, 2])
    X2, Y2 = COORDINATES[NODE_2, 0], COORDINATES[NODE_2, 1]
    THICK_ID = int(ELEMENTS[I_ELEMENT, AUX_2])
    THICK = THICKNESS[THICK_ID, 0]
    SECTION_IELEMENT = {'X_E': np.array([[X0, Y0], [X1, Y1], [X2, Y2]]), 'THICKNESS': THICK}
    return SECTION_IELEMENT

# MATRIZ CONSTITUTIVA DO ELEMENTO TIPO PLANO
def CONSTITUTIVE_C(TYPE_PLANE, MATERIALS, ELEMENTS, I_ELEMENT):
    """
    This function determines the matrix responsible for establishing the constitutive relationship between stress and strain according to the choosen analysis.

    Input:
    TYPE_PLANE  | Type of analysis in the plan                           | String
                |      'EPT' - Plane Stress                              |
                |      'EPD' - Plane Strain                              |
    MATERIALS   | Materials properties                                   | Py Numpy array
                |      ID, Young, Poisson, Density                       |
    ELEMENTS    | Elements properties                                    | Py Numpy array
                |    Node 0 ... Node (N_NODES - 1), Material ID,         |
                |    Thickness ID                                        |
    I_ELEMENT   | ID i element in looping for                            | Integer

    Output:
    C           | Constitutive matrix                                    | Py Numpy array[3 x 3]
    """
    MATERIAL_ID = int(ELEMENTS[I_ELEMENT, 4])
    E = MATERIALS[MATERIAL_ID, 0]
    NU = MATERIALS[MATERIAL_ID, 1]
    # Plane stress
    if TYPE_PLANE == 0:
        C11 = 1
        C12 = NU
        C21 = C12
        C22 = 1
        C33 = 0.5 * (1 - NU)
        AUX_1 = E / (1 - NU ** 2)
        AUX_2 = np.array([[C11, C12, 0], [C21, C22, 0], [0, 0, C33]])
    # Plane strain
    elif TYPE_PLANE == 1:
        C11 = 1 - NU
        C12 = NU
        C21 = NU
        C22 = 1 - NU
        C33 = 0.5 - NU
        AUX_1 = E/((1 + NU)*(1 - 2*NU))
        AUX_2 = np.array([[C11, C12, 0],[C21, C22, 0],[0, 0, C33]])
    C = AUX_1 * AUX_2
    return C

def SHAPE_FUNCTIONS(TYPE_ELEMENT, N_NODESELEMENT, ISO_COORDINATES):
    """
    This function creates the matrix of the derivatives of the shape functions

    Input:
    TYPE_ELEMENT         | Type element in Finito algorithm                       | Integer 
                         |      0 - Frame bar element                             |
                         |      1 - CST surface element                           |
    N_NODESELEMENT: Number of nodes per element (integer);
    ISO_COORDINATES: Isoparametric coordinates (Python dictionary);

    Output:
    ND_DIFF: ND derivatives matrix (Python Numpy array);
    NX_DIFF: NX derivatives matrix (Python Numpy array);
    """
    if TYPE_ELEMENT == 1:
        # Derivative shape functions 
        DIFF_KSI = [-1, 1, 0]
        DIFF_ETA = [-1, 0, 1]
        # ND e NX assembly
        NX_DIFF = np.array([DIFF_KSI, DIFF_ETA])
        ND_DIFF = DND_ASSEMBLY(N_NODESELEMENT, NX_DIFF)
    return ND_DIFF, NX_DIFF

def DND_ASSEMBLY(N_NODESELEMENT, NX_DIFF):
    """
    This function assembles the derived matrix ND

    Input:
    N_NODESELEMENT: Number of nodes per element (integer);
    NX_DIFF: NX derivatives matrix (Python Numpy array);
    
    Output:
    ND_DIFF: ND derivatives matrix (Python Numpy array);
    """
    ND_DIFF_1 = np.zeros((2, 2 * N_NODESELEMENT))
    ND_DIFF_2 = np.zeros((2, 2 * N_NODESELEMENT))
    # Automatic assembly 
    for I_COUNT in range(2):
        COUNT_1 = 0
        COUNT_2 = 0
        for J_COUNT in range(0, 2 * N_NODESELEMENT, 2):
            ND_DIFF_1[I_COUNT, J_COUNT] = NX_DIFF[I_COUNT, COUNT_1]
            COUNT_1 += 1
        for K_COUNT in range(1, 2 * N_NODESELEMENT, 2):
            ND_DIFF_2[I_COUNT, K_COUNT] = NX_DIFF[I_COUNT, COUNT_2]
            COUNT_2 += 1
    ND_DIFF = np.vstack((ND_DIFF_1, ND_DIFF_2))
    return ND_DIFF

def STIFFNESS(NX_DIFF, ND_DIFF, C, X_E, THICK):
    """
    This function assembles the element's stiffness matrix to a Gaussian point

    Input:
    NX_DIFF: NX derivatives matrix (Python Numpy array);
    ND_DIFF: ND derivatives matrix (Python Numpy array);
    C: Constitutive matrix in formulation (Python Numpy array); 
    X_E: i element coordinates (Python Numpy array);

    Output:
    K_I: i element stiffness matrix (Python Numpy array);
    """

    # Jacobian matrix
    J = np.dot(NX_DIFF, X_E)
    # Determinant of the Jacobian matrix
    DET_J = np.linalg.det(J)
    # Gamma and Gamma U matrix
    GAMMA = np.linalg.inv(J)
    GAMMA_00 = GAMMA[0, 0]
    GAMMA_01 = GAMMA[0, 1]
    GAMMA_10 = GAMMA[1, 0]
    GAMMA_11 = GAMMA[1, 1]
    GAMMA_U = np.array([[GAMMA_00, GAMMA_01, 0, 0],
                        [GAMMA_10, GAMMA_11, 0, 0],
                        [0, 0, GAMMA_00, GAMMA_01],
                        [0, 0, GAMMA_10, GAMMA_11]])
    H = np.array([[1, 0, 0, 0],
                    [0, 0, 0, 1],
                    [0, 1, 1, 0]])
    B = np.dot(np.dot(H, GAMMA_U), ND_DIFF)
    # i element stiffness matrix
    K_I = THICK * (np.dot(np.dot(B.transpose(), C), np.dot(B, DET_J)))
    return K_I

def NUMERICAL_INTEGRATION(TYPE_INTEGRATION):
    """
    This function creates the parameters for numerical integration
    
    Input:
    TYPE_INTEGRATION: Type numerical integration (string);

    Output:
    NUM_INT: Setup numerical integration (Python dictionary);
    """
    # Hammer 12 points
    # if TYPE_INTEGRATION == 'HAMMER-12':
    if TYPE_INTEGRATION == 1:
        W = [0.116786275726379/2.0, 0.116786275726379/2.0, 0.116786275726379/2.0,
                            0.050844906370207/2.0, 0.050844906370207/2.0, 0.050844906370207/2.0,
                            0.082851075618374/2.0, 0.082851075618374/2.0, 0.082851075618374/2.0,
                            0.082851075618374/2.0, 0.082851075618374/2.0, 0.082851075618374/2.0]
        KSI = [0.501426509658179, 0.249286745170910, 0.249286745170910,
                               0.873821971016996, 0.063089014491502, 0.063089014491502,
                               0.053145049844816, 0.310352451033785, 0.636502499121399,
                               0.310352451033785, 0.636502499121399, 0.053145049844816]
        ETA = [0.249286745170910, 0.249286745170910, 0.501426509658179,
                               0.063089014491502, 0.063089014491502, 0.873821971016996,
                               0.310352451033785, 0.636502499121399, 0.053145049844816,
                               0.053145049844816, 0.310352451033785, 0.636502499121399]
        # N_POINTS = W.shape[1] - shape não funciona em lista
        N_POINTS = len(W)
    NUM_INT = {'W': W, 'KSI': KSI, 'ETA': ETA, 'N': N_POINTS}
    return NUM_INT

def ELEMENT_STIFFNESS_1(NUM_INT, N_DOFSELEMENT, TYPE_ELEMENT, N_NODESELEMENT, C_IELEMENT, SECTION_IELEMENT):
    """
    This function calculates the stiffness matrix of the isoparametric element

    Input:
    NUM_INT: Setup numerical integration (Python dictionary);
    N_DOFSELEMENT: Number of degress of freedom per element (integer);
    TYPE_ELEMENT: Type element in Finito algorithm (integer); 
            0 - Frame bar element
            1 - CST surface element
    N_NODESELEMENT: Number of nodes per element (integer);
    C_IELEMENT: i element constitutive matrix in formulation (Python Numpy array); 
    SECTION_IELEMENT: i element geometric properties (Python dictionary);

    Output:
    K_IELEMENT: Complete i element stiffness matrix
    """
    POINTS = NUM_INT['N']
    K_IELEMENT = np.zeros((N_DOFSELEMENT, N_DOFSELEMENT))
    for I_COUNT in range(POINTS):
        ISO_COORDINATES = {'KSI': NUM_INT['KSI'][I_COUNT], 'ETA': NUM_INT['ETA'][I_COUNT]}
        [ND_DIFF, NX_DIFF] = SHAPE_FUNCTIONS(TYPE_ELEMENT, N_NODESELEMENT, ISO_COORDINATES)
        X_E = SECTION_IELEMENT['X_E']
        THICK = SECTION_IELEMENT['THICKNESS']
        K_I = STIFFNESS(NX_DIFF, ND_DIFF, C_IELEMENT, X_E, THICK)
        WEIGHT = NUM_INT['W'][I_COUNT]
        K_IELEMENT += K_I * WEIGHT
    return K_IELEMENT

#  /$$$$$$$$ /$$$$$$ /$$   /$$ /$$$$$$ /$$$$$$$$  /$$$$$$        /$$$$$$$$  /$$$$$$   /$$$$$$  /$$       /$$$$$$$   /$$$$$$  /$$   /$$                                
# | $$_____/|_  $$_/| $$$ | $$|_  $$_/|__  $$__/ /$$__  $$      |__  $$__/ /$$__  $$ /$$__  $$| $$      | $$__  $$ /$$__  $$| $$  / $$                                
# | $$        | $$  | $$$$| $$  | $$     | $$   | $$  \ $$         | $$   | $$  \ $$| $$  \ $$| $$      | $$  \ $$| $$  \ $$|  $$/ $$/                                
# | $$$$$     | $$  | $$ $$ $$  | $$     | $$   | $$  | $$         | $$   | $$  | $$| $$  | $$| $$      | $$$$$$$ | $$  | $$ \  $$$$/                                 
# | $$__/     | $$  | $$  $$$$  | $$     | $$   | $$  | $$         | $$   | $$  | $$| $$  | $$| $$      | $$__  $$| $$  | $$  >$$  $$                                 
# | $$        | $$  | $$\  $$$  | $$     | $$   | $$  | $$         | $$   | $$  | $$| $$  | $$| $$      | $$  \ $$| $$  | $$ /$$/\  $$                                
# | $$       /$$$$$$| $$ \  $$ /$$$$$$   | $$   |  $$$$$$/         | $$   |  $$$$$$/|  $$$$$$/| $$$$$$$$| $$$$$$$/|  $$$$$$/| $$  \ $$                                
# |__/      |______/|__/  \__/|______/   |__/    \______/          |__/    \______/  \______/ |________/|_______/  \______/ |__/  |__/                                                                                                                                                                                                                                                                                                                                                                   
                                                                                                                                                                    
#   /$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$$       /$$$$$$$$ /$$$$$$$$  /$$$$$$  /$$   /$$ /$$   /$$  /$$$$$$  /$$        /$$$$$$   /$$$$$$  /$$$$$$ /$$$$$$$$  /$$$$$$ 
#  /$$__  $$| $$__  $$| $$_____/| $$_____/      |__  $$__/| $$_____/ /$$__  $$| $$  | $$| $$$ | $$ /$$__  $$| $$       /$$__  $$ /$$__  $$|_  $$_/| $$_____/ /$$__  $$
# | $$  \__/| $$  \ $$| $$      | $$               | $$   | $$      | $$  \__/| $$  | $$| $$$$| $$| $$  \ $$| $$      | $$  \ $$| $$  \__/  | $$  | $$      | $$  \__/
# | $$ /$$$$| $$$$$$$/| $$$$$   | $$$$$            | $$   | $$$$$   | $$      | $$$$$$$$| $$ $$ $$| $$  | $$| $$      | $$  | $$| $$ /$$$$  | $$  | $$$$$   |  $$$$$$ 
# | $$|_  $$| $$____/ | $$__/   | $$__/            | $$   | $$__/   | $$      | $$__  $$| $$  $$$$| $$  | $$| $$      | $$  | $$| $$|_  $$  | $$  | $$__/    \____  $$
# | $$  \ $$| $$      | $$      | $$               | $$   | $$      | $$    $$| $$  | $$| $$\  $$$| $$  | $$| $$      | $$  | $$| $$  \ $$  | $$  | $$       /$$  \ $$
# |  $$$$$$/| $$      | $$$$$$$$| $$$$$$$$         | $$   | $$$$$$$$|  $$$$$$/| $$  | $$| $$ \  $$|  $$$$$$/| $$$$$$$$|  $$$$$$/|  $$$$$$/ /$$$$$$| $$$$$$$$|  $$$$$$/
#  \______/ |__/      |________/|________/         |__/   |________/ \______/ |__/  |__/|__/  \__/ \______/ |________/ \______/  \______/ |______/|________/ \______/ 