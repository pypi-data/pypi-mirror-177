import numpy as np
import FINITO_TOOLBOX.FINITO_COMMON_LIBRARY as FINITO_CL

def GET_VALUE_FROM_TXT_MEF1D_FINITO(FILENAME):
    """
    This function reads data from .txt file.
    
    Input:
    FILENAME              | Structural dataset                                     | .txt extension

    Output: 
    TYPE_ELEMENT          | Type element in Finito algorithm                       | Integer 
                          |     0 - Frame bar element                              |
    TYPE_SOLUTION         | Solution of the system of equations                    | Integer
                          |    0 - Condense procedure                              |
                          |    1 - Zero and One algorithm                          |
    N_NODES               | Number of nodes                                        | Integer
    N_MATERIALS           | Number of materials                                    | Integer
    N_SECTIONS            | Number of sections                                     | Integer
    N_ELEMENTS            | Number of frame elements                               | Integer
    N_DOFPRESCRIPTIONS    | Number of DOF displacement control                     | Integer
    N_DOFLOADED           | Number of DOF forces                                   | Integer
    N_ELEMENTSLOADED      | Number of elements loaded                              | Integer
    N_DOFSPRINGS          | Number of DOF spring elements                          | Integer
    COORDINATES           | Coordinates properties                                 | Py Numpy array
                          |    Node, x, y                                          |
    ELEMENTS              | Elements properties                                    | Py Numpy array
                          |    Node 0 ... Node (N_NODES - 1), Material ID,         | 
                          |    Geometry ID, Hinge ID node 0, Hinge ID node 1       |
    MATERIALS             | Materials properties                                   | Py Numpy array
                          |    Young, Poisson, Density, Thermal coefficient        |
    SECTIONS              | Sections properties                                    | Py Numpy array
                          |    Area, Inertia 1, Inertia Frame bar, X GC, Y GC      |
    PRESCRIPTIONS         | Prescribed DOF displacement properties                 | Py Numpy array              
                          |    Node, Direction (X = 0, Y = 1, Z = 2), Value        | 
    NODAL_LOAD            | Nodal DOF force properties                             | Py Numpy array              
                          |    Node, Direction (X = 0, Y = 1, Z = 2), Value        |
    SPRINGS               | Nodal DOF spring properties                            | Py Numpy array              
                          |    Node, Direction (X = 0, Y = 1, Z = 2), Value        |
    """
    # Open file and read dataset
    FILE = open(FILENAME, "r")
    DATASET = FILE.read().split("\n")
    TYPE_ELEMENT = int(DATASET.pop(0).split(':')[1])
    TYPE_SOLUTION = int(DATASET.pop(0).split(':')[1])
    N_NODES = int(DATASET.pop(0).split(':')[1])
    N_MATERIALS = int(DATASET.pop(0).split(':')[1])
    N_SECTIONS = int(DATASET.pop(0).split(':')[1])
    N_ELEMENTS = int(DATASET.pop(0).split(':')[1])
    N_ELEMENTSLOADED = int(DATASET.pop(0).split(':')[1])
    N_DOFPRESCRIPTIONS = int(DATASET.pop(0).split(':')[1])
    N_DOFLOADED  = int(DATASET.pop(0).split(':')[1]) 
    N_DOFSPRINGS = int(DATASET.pop(0).split(':')[1])
    DATASET.pop(0)
    DATASET.pop(0)
    
    # Read coordinates
    COORDINATES = np.zeros((N_NODES, 2))
    for I_COUNT in range(N_NODES):
        VALUES = DATASET.pop(0).split(',')
        COORDINATES[int(VALUES[0]),0] = float(VALUES[1])
        COORDINATES[int(VALUES[0]),1] = float(VALUES[2])
    DATASET.pop(0)
    DATASET.pop(0)
    
    # Read elements
    ELEMENTS = np.zeros((N_ELEMENTS, 6))
    for J_COUNT in range(N_ELEMENTS):
        VALUES = DATASET.pop(0).split(',')
        ELEMENTS[int(VALUES[0]),0] = int(VALUES[1])
        ELEMENTS[int(VALUES[0]),1] = int(VALUES[2])    
        ELEMENTS[int(VALUES[0]),2] = int(VALUES[3])
        ELEMENTS[int(VALUES[0]),3] = int(VALUES[4])
        ELEMENTS[int(VALUES[0]),4] = int(VALUES[5])
        ELEMENTS[int(VALUES[0]),5] = int(VALUES[6])
    DATASET.pop(0)
    DATASET.pop(0)
    
    # Read materials
    MATERIALS = np.zeros((N_MATERIALS, 4))
    for K_COUNT in range(N_MATERIALS):
        VALUES = DATASET.pop(0).split(',')
        MATERIALS[int(VALUES[0]),0] = float(VALUES[1])
        MATERIALS[int(VALUES[0]),1] = float(VALUES[2])    
        MATERIALS[int(VALUES[0]),2] = float(VALUES[3])
        MATERIALS[int(VALUES[0]),3] = float(VALUES[4])
    DATASET.pop(0)
    DATASET.pop(0)
    
    # Read sections
    SECTIONS = np.zeros((N_SECTIONS, 5))
    for L_COUNT in range(N_SECTIONS):
        VALUES = DATASET.pop(0).split(',')
        SECTIONS[int(VALUES[0]),0] = float(VALUES[1])
        SECTIONS[int(VALUES[0]),1] = float(VALUES[2])    
        SECTIONS[int(VALUES[0]),2] = float(VALUES[3])
        SECTIONS[int(VALUES[0]),3] = float(VALUES[4])
        SECTIONS[int(VALUES[0]),4] = float(VALUES[5])
    DATASET.pop(0)
    DATASET.pop(0)
    
    # Prescribed DOF displacements
    PRESCRIPTIONS = np.zeros((N_DOFPRESCRIPTIONS, 3))
    for M_COUNT in range(N_DOFPRESCRIPTIONS):
        VALUES = DATASET.pop(0).split(',')
        PRESCRIPTIONS[int(VALUES[0]),0] = int(VALUES[1])
        PRESCRIPTIONS[int(VALUES[0]),1] = int(VALUES[2])
        PRESCRIPTIONS[int(VALUES[0]),2] = float(VALUES[3]) 
    DATASET.pop(0)
    DATASET.pop(0)

    # Read element load
    if N_ELEMENTSLOADED == 0:
        DATASET.pop(0)
        ELEMENT_EXTERNAL_LOAD = "null"
    else:
        ELEMENT_EXTERNAL_LOAD = np.zeros((N_ELEMENTSLOADED, 4))
        for N_COUNT in range(N_ELEMENTSLOADED):
            VALUES = DATASET.pop(0).split(',')
            ELEMENT_EXTERNAL_LOAD[int(VALUES[0]),0] = float(VALUES[1])
            ELEMENT_EXTERNAL_LOAD[int(VALUES[0]),1] = float(VALUES[2])    
            ELEMENT_EXTERNAL_LOAD[int(VALUES[0]),2] = float(VALUES[3])
            ELEMENT_EXTERNAL_LOAD[int(VALUES[0]),3] = float(VALUES[4])
    DATASET.pop(0)
    DATASET.pop(0)
    
    # Read nodal DOF load
    NODAL_LOAD = np.zeros((N_DOFLOADED, 3))
    for O_COUNT in range(N_DOFLOADED):
        VALUES = DATASET.pop(0).split(',')
        NODAL_LOAD[int(VALUES[0]),0] = float(VALUES[1])
        NODAL_LOAD[int(VALUES[0]),1] = float(VALUES[2]) 
        NODAL_LOAD[int(VALUES[0]),2] = float(VALUES[3]) 
    DATASET.pop(0)
    DATASET.pop(0)
    
    # Read spring DOF elements
    if N_DOFSPRINGS == 0:
        DATASET.pop(0)
        SPRINGS = "null"
    else:
        SPRINGS = np.zeros((N_DOFSPRINGS, 3))
        for P_COUNT in range(N_DOFSPRINGS):
            VALUES = DATASET.pop(0).split(',')
            SPRINGS[int(VALUES[0]),0] = int(VALUES[1])
            SPRINGS[int(VALUES[0]),1] = int(VALUES[2])
            SPRINGS[int(VALUES[0]),2] = float(VALUES[3]) 
    return TYPE_SOLUTION, TYPE_ELEMENT, N_NODES, N_MATERIALS, N_SECTIONS, N_ELEMENTS, N_DOFPRESCRIPTIONS, N_ELEMENTSLOADED, N_DOFLOADED, N_DOFSPRINGS, COORDINATES, ELEMENTS, MATERIALS, SECTIONS, PRESCRIPTIONS, ELEMENT_EXTERNAL_LOAD, NODAL_LOAD, SPRINGS

def GET_VALUE_FROM_DICT_MEF1D_FINITO(DICTIONARY):
    """
    This function reads data from dictionary.

    Input:
    DICTIONARY            | Structural dataset                                     | Py dictionary

    Output: 
    TYPE_ELEMENT          | Type element in Finito algorithm                       | Integer 
                          |     0 - Frame bar element                              |
    TYPE_SOLUTION         | Solution of the system of equations                    | Integer
                          |    0 - Condense procedure                              |
                          |    1 - Zero and One algorithm                          |
    N_NODES               | Number of nodes                                        | Integer
    N_MATERIALS           | Number of materials                                    | Integer
    N_SECTIONS            | Number of sections                                     | Integer
    N_ELEMENTS            | Number of frame elements                               | Integer
    N_DOFPRESCRIPTIONS    | Number of DOF displacement control                     | Integer
    N_DOFLOADED           | Number of DOF forces                                   | Integer
    N_ELEMENTSLOADED      | Number of elements loaded                              | Integer
    N_DOFSPRINGS          | Number of DOF spring elements                          | Integer
    COORDINATES           | Coordinates properties                                 | Py Numpy array
                          |    Node, x, y                                          |
    ELEMENTS              | Elements properties                                    | Py Numpy array
                          |    Node 0 ... Node (N_NODES - 1), Material ID,         | 
                          |    Geometry ID, Hinge ID node 0, Hinge ID node 1       |
    MATERIALS             | Materials properties                                   | Py Numpy array
                          |    Young, Poisson, Density, Thermal coefficient        |
    SECTIONS              | Sections properties                                    | Py Numpy array
                          |    Area, Inertia 1, Inertia Frame bar, X GC, Y GC      |
    PRESCRIPTIONS         | Prescribed DOF displacement properties                 | Py Numpy array              
                          |    Node, Direction (X = 0, Y = 1, Z = 2), Value        | 
    NODAL_LOAD            | Nodal DOF force properties                             | Py Numpy array              
                          |    Node, Direction (X = 0, Y = 1, Z = 2), Value        |
    SPRINGS               | Nodal DOF spring properties                            | Py Numpy array              
                          |    Node, Direction (X = 0, Y = 1, Z = 2), Value        |
    """
    # Read dataset
    TYPE_ELEMENT = DICTIONARY["TYPE_ELEMENT"]
    TYPE_SOLUTION = DICTIONARY["TYPE_SOLUTION"]
    N_NODES = DICTIONARY["N_NODES"]
    N_MATERIALS = DICTIONARY["N_MATERIALS"]
    N_SECTIONS = DICTIONARY["N_SECTIONS"]
    N_ELEMENTS = DICTIONARY["N_ELEMENTS"]
    N_DOFPRESCRIPTIONS = DICTIONARY["N_DOFPRESCRIPTIONS"]
    N_DOFLOADED = DICTIONARY["N_DOFLOADED"]
    N_ELEMENTSLOADED = DICTIONARY["N_ELEMENTSLOADED"]
    N_DOFSPRINGS = DICTIONARY["N_DOFSPRINGS"]
    COORDINATES = DICTIONARY["COORDINATES"]
    ELEMENTS = DICTIONARY["ELEMENTS"]
    MATERIALS = DICTIONARY["MATERIALS"]
    SECTIONS = DICTIONARY["SECTIONS"]
    PRESCRIPTIONS = DICTIONARY["PRESCRIBED DISPLACEMENTS"]
    ELEMENT_EXTERNAL_LOAD = DICTIONARY["ELEMENT LOADS"]
    NODAL_LOAD = DICTIONARY["NODAL LOADS"]
    SPRINGS = DICTIONARY["SPRINGS"]
    return TYPE_SOLUTION, TYPE_ELEMENT, N_NODES, N_MATERIALS, N_SECTIONS, N_ELEMENTS, N_DOFPRESCRIPTIONS, N_ELEMENTSLOADED, N_DOFLOADED, N_DOFSPRINGS, COORDINATES, ELEMENTS, MATERIALS, SECTIONS, PRESCRIPTIONS, ELEMENT_EXTERNAL_LOAD, NODAL_LOAD, SPRINGS

def MATERIALS_PROPERTIES_0(ELEMENTS, MATERIALS, I_ELEMENT, AUX_1):
    """
    This function creates a vector with the material information of the I_ELEMENT element TYPE_ELEMENT = 0 (Frame element).

    Input:
    ELEMENTS           | Elements properties                                   | Py Numpy array
                       |    ID, Node 0 ... Node (N_NODES - 1), Material ID ,   |
                       |    Geometry ID, Hinge ID node 1, Hinge ID node 2      |
    MATERIALS          | Materials properties                                  | Py Numpy array
                       |     ID, Young, Poisson, Density, Thermal coefficient  |
    I_ELEMENT          | i element in looping                                  | Integer
    AUX_1              | ID material                                           | Integer
    
    Output:
    MATERIAL_IELEMENT  | Material I_ELEMENT properties                         | Py list[5]
                       |     [0] - Young                                       |
                       |     [1] - Shear modulus                               |
                       |     [2] - Poisson                                     |
                       |     [3] - Thermal coefficient                         |
                       |     [4] - Density                                     |
    """
    MATERIAL_ID = int(ELEMENTS[I_ELEMENT, AUX_1])
    E = MATERIALS[MATERIAL_ID, 0]
    NU = MATERIALS[MATERIAL_ID, 1]
    PHO = MATERIALS[MATERIAL_ID, 2]
    ALPHA = MATERIALS[MATERIAL_ID, 3]
    G = E / (2 * (1 + NU))
    MATERIAL_IELEMENT = [E, G, NU, ALPHA, PHO]
    return MATERIAL_IELEMENT

def GEOMETRIC_PROPERTIES_0(COORDINATES, ELEMENTS, SECTIONS, I_ELEMENT, AUX_2):
    """ 
    This function assigns the bar element's geometric propertiest of the I_ELEMENT element TYPE_ELEMENT = 0 (Frame element).

    Input:
    COORDINATES        | Coordinates properties                                | Py Numpy array
                       |     Node, x, y                                        |
    ELEMENTS           | Elements properties                                   | Py Numpy array
                       |    Node 0 ... Node (N_NODES - 1), Material ID,        |
                       |    Geometry ID, Hinge ID node 1, Hinge ID node 2      | 
    SECTIONS           | Sections properties                                   | Py Numpy array
                       |    Area, Inertia 1, Inertia Frame bar, X GC, Y GC     |
    I_ELEMENT          | i element in looping                                  | Integer
    AUX_2              | ID section                                            | Integer

    Output:
    SECTION_IELEMENT   | Section I_ELEMENT properties                          | Py list[6]
                       |     [0] - Length                                      |
                       |     [1] - Sine                                        |
                       |     [2] - Cosine                                      |
                       |     [3] - Area                                        |
                       |     [4] - Inertia auxiliar                            |
                       |     [5] - Inertia frame element                       |
    """
    NODE_1 = int(ELEMENTS[I_ELEMENT, 0])
    NODE_2 = int(ELEMENTS[I_ELEMENT, 1])
    X_NODE1 = COORDINATES[NODE_1, 0]
    Y_NODE1 = COORDINATES[NODE_1, 1]
    X_NODE2 = COORDINATES[NODE_2, 0]
    Y_NODE2 = COORDINATES[NODE_2, 1]
    DELTA_X = X_NODE2 - X_NODE1
    DELTA_Y = Y_NODE2 - Y_NODE1
    L = ((DELTA_X) ** 2 + (DELTA_Y) ** 2) ** 0.50
    COS = DELTA_X / L
    SIN = DELTA_Y / L
    SECTION_ID = int(ELEMENTS[I_ELEMENT, AUX_2])
    A = SECTIONS[SECTION_ID, 0]
    I_1 = SECTIONS[SECTION_ID, 1]
    I_2 = SECTIONS[SECTION_ID, 2]
    SECTION_IELEMENT = [L, SIN, COS, A, I_1, I_2]
    return SECTION_IELEMENT

# VETOR COMPLETO DE FORÇAS EQUIVALENTES DO ELEMENTO POR DOF
def CONTRBUITION_ELEMENT_EXTERNAL_LOAD(TYPE_ELEMENT, N_ELEMENTSLOADED, ELEMENT_EXTERNAL_LOAD, DOF_GLOBALNODAL, ELEMENTS, COORDINATES, SECTIONS, AUX_2, N_DOFSELEMENT, N_DOFSGLOBAL, N_NODESELEMENT, N_DOFSNODE):
    """
    This function builds the external charges vector at the level of freedom concerned the element load. 
  
    Input:
    TYPE_ELEMENT           | Type element in Finito algorithm                   | Integer
                           |        0 - Frame bar element                       |
                           |        1 - CST surface element                     |
    N_ELEMENTSLOADED       | Number of elements loaded                          | Integer
    ELEMENT_EXTERNAL_LOAD  | Element load properties                            | Py Numpy array [ELEMENT_EXTERNAL_LOAD x 4]
                           |    Element, Coordinate system (local = 0,          |
                           |    global system = 1), Axial load Value,           |
                           |    Transversal load Value                          |
    DOF_GLOBALNODAL        | ID global DOF per node                             | Py Numpy array[N_NODES x ??]
                           |    ?? = [3] -> TYPE_ELEMENT = 0                    |
                           |    ?? = [2] -> TYPE_ELEMENT = 1                    |
    ELEMENTS               | Elements properties                                | Py Numpy array
                           |   Node 0 ... Node (N_NODES - 1), Material ID,      |
                           |    Geometry ID, Hinge ID node 0, Hinge ID node 1   |
    COORDINATES            | Coordinates properties                             | Py Numpy array
                           |    Node, x, y                                      |
    SECTIONS               | Sections properties                                | Py Numpy array
                           |    Area, Inertia 1, Inertia Frame bar, X GC, Y GC  |
    AUX_2                  | Geometry or Thickness ID in ELEMENTS               | Integer
                           |       Geometry  -> TYPE_ELEMENT = 0                |
                           |       Thickness -> TYPE_ELEMENT = 1                |
    N_DOFSELEMENT          | Number of degress of freedom per element           | Integer
    N_DOFSGLOBAL           | Total of degrees of freedom                        | Integer
    N_NODESELEMENT         | Number of nodes per element                        | Integer
    N_DOFSNODE             | Number of degress of freedom per node              | Integer

    Output:
    DOF_ELEMENTFORCE       | Force per DOF from element load                    | Py Numpy array[N_DOFSGLOBAL x 1]
    """
    
    DOF_ELEMENTFORCE = np.zeros((N_DOFSGLOBAL, 1))
    
    # Element iteration
    for I_COUNT in range(N_ELEMENTSLOADED):
        
        # Section properties in I element
        ID_ELEMENT = ELEMENT_EXTERNAL_LOAD[I_COUNT, 0]
        SECTION_IELEMENT = GEOMETRIC_PROPERTIES_0(COORDINATES, ELEMENTS, SECTIONS, ID_ELEMENT, AUX_2)
        L = SECTION_IELEMENT[0]
        SIN = SECTION_IELEMENT[1]
        COS = SECTION_IELEMENT[2]
        
        # Load properties
        IDSIST = ELEMENT_EXTERNAL_LOAD[I_COUNT, 1]
        Q_X = ELEMENT_EXTERNAL_LOAD[I_COUNT, 2]
        Q_Y = ELEMENT_EXTERNAL_LOAD[I_COUNT, 3]

        # Equivalent nodal force 
        if TYPE_ELEMENT == 0:
            if IDSIST == 0:
                F_EQ = np.array([[Q_X * L / 2], [Q_Y * L / 2], [Q_Y * L ** 2 / 12], [Q_X * L / 2], [Q_Y * L / 2], [- Q_Y * L ** 2 / 12]])
            elif IDSIST == 1:
                Q_XX = Q_X * COS + Q_Y * SIN
                Q_YY = - Q_X * SIN + Q_Y * COS
                F_EQ = np.array([[Q_XX * L / 2], [Q_YY * L / 2], [Q_YY * L ** 2 / 12], [Q_XX * L / 2], [Q_YY * L / 2], [- Q_YY * L ** 2 / 12]])
        
        # System rotation
        R_IELEMENT = ELEMENT_ROTATION(TYPE_ELEMENT, SECTION_IELEMENT)
        GLOBAL_ELEMENT_EQUIVALENT_FORCE = np.dot(np.transpose(R_IELEMENT), F_EQ)
        
        # Global DOF in element
        DOF_GLOBALIELEMENT = FINITO_CL.GLOBAL_DOF_ELEMENT(N_NODESELEMENT, N_DOFSNODE, DOF_GLOBALNODAL, ELEMENTS, ID_ELEMENT)

        # Global DOF in structure
        for J_COUNT in range(N_DOFSELEMENT):
            AUX_3 = DOF_GLOBALIELEMENT[J_COUNT]
            DOF_ELEMENTFORCE[AUX_3, 0] += GLOBAL_ELEMENT_EQUIVALENT_FORCE[J_COUNT, 0]
    return DOF_ELEMENTFORCE

def HINGED_PROPERTIES(ELEMENTS):
    """
    This function creates an array with the hinge properties per node.

    Input
    ELEMENTS  | Elements properties                                | Py Numpy array
              |     Node 0 ... Node (N_NODES - 1), Material ID,    | 
              |     Geometry ID, Hinge ID node 1, Hinge ID node 2  |
    
    Output:
    HINGES    | Hinge properties per node                          | Py Numpy array[N_NODES x 2]
              |     0 - No hinge                                   |
              |     1 - Yes hinge                                  |
    """
    HINGES = ELEMENTS[:, 4:]
    return HINGES

def ELEMENT_STIFFNESS_0(TYPE_ELEMENT, SECTION_IELEMENT, MATERIAL_IELEMENT, HINGES_IELEMENT):
    """ 
    This function creates the element stiffness matrix of the I_ELEMENT. 
    
    Input:
    TYPE_ELEMENT       | Type element in Finito algorithm                      | Integer 
                       |     0 - Frame bar element                             |        
    SECTION_IELEMENT   | Section I_ELEMENT properties                          | Py list[6]
                       |     [0] - Length                                      |
                       |     [1] - Sine                                        |
                       |     [2] - Cosine                                      |
                       |     [3] - Area                                        |
                       |     [4] - Inertia auxiliar                            |
                       |     [5] - Inertia frame element                       |
    MATERIAL_IELEMENT  | Material I_ELEMENT properties                         | Py list[5]
                       |     [0] - Young                                       |
                       |     [1] - Shear modulus                               |
                       |     [2] - Poisson                                     |
                       |     [3] - Thermal coefficient                         |
                       |     [4] - Density                                     |   
    HINGES             | Hinge properties per node                             | Py Numpy array[N_NODES x 2]
                       |     0 - No hinge                                      |
                       |     1 - Yes hinge                                     |
    
    Output:
    K_IELEMENT         | Local stiffness matrix I_ELEMENT                      | Py Numpy array [N_DOFSELEMENT x N_DOFSELEMENT]
    """
    if (TYPE_ELEMENT == 0 and HINGES_IELEMENT[0] == 0 and HINGES_IELEMENT[1] == 0):
        L = SECTION_IELEMENT[0]
        A = SECTION_IELEMENT[3]
        I = SECTION_IELEMENT[5]
        E = MATERIAL_IELEMENT[0]
        C1 = A * E / L
        C2 = E * I / (L ** 3)
        K_IELEMENT = np.array([[C1, 0, 0, -C1, 0, 0],
                               [0, 12 * C2, 6 * C2 * L, 0, -12 * C2, 6 * C2 * L],
                               [0, 6 * C2 * L, 4 * C2 * L ** 2, 0, -6 * C2 * L, 2 * C2 * L ** 2],
                               [-C1, 0, 0, C1, 0, 0],
                               [0, -12 * C2, -6 * C2 * L, 0, 12 * C2, -6 * C2 * L],
                               [0, 6 * C2 * L, 2 * C2 * L ** 2, 0, -6 * C2 * L, 4 * C2 * L **2]])
    elif (TYPE_ELEMENT == 0 and HINGES_IELEMENT[0] == 0 and HINGES_IELEMENT[1] == 1):
        L = SECTION_IELEMENT[0]
        A = SECTION_IELEMENT[3]
        I = SECTION_IELEMENT[5]
        E = MATERIAL_IELEMENT[0]
        C1 = A * E / L
        C2 = E * I / (L ** 3)
        K_IELEMENT = np.array([[C1, 0, 0, -C1, 0, 0],
                               [0, 3 * C2, 3 * C2 * L, 0, -3 * C2, 0],
                               [0, 3 * C2 * L, 3 * C2 * L ** 2, 0, -3 * C2 * L, 0],
                               [-C1, 0, 0, C1, 0, 0],
                               [0, -3 * C2, -6 * C2 * L, 0, 3 * C2, 0],
                               [0, 0, 0, 0, 0, 0]])    
    elif (TYPE_ELEMENT == 0 and HINGES_IELEMENT[0] == 1 and HINGES_IELEMENT[1] == 0):
        L = SECTION_IELEMENT[0]
        A = SECTION_IELEMENT[3]
        I = SECTION_IELEMENT[5]
        E = MATERIAL_IELEMENT[0]
        C1 = A * E / L
        C2 = E * I / (L ** 3)
        K_IELEMENT = np.array([[C1, 0, 0, -C1, 0, 0],
                               [0, 3 * C2, 0, 0, -3 * C2, 3 * C2 * L],
                               [0, 0, 0, 0, 0, 0],
                               [-C1, 0, 0, C1, 0, 0],
                               [0, -3 * C2, 0, 0, 3 * C2, -3 * C2 * L],
                               [0, 3 * C2 * L, 0, 0, -3 * C2 * L, 3 * C2 * L **2]])     
    elif (TYPE_ELEMENT == 0 and HINGES_IELEMENT[0] == 1 and HINGES_IELEMENT[1] == 1):
        L = SECTION_IELEMENT[0]
        A = SECTION_IELEMENT[3]
        I = SECTION_IELEMENT[5]
        E = MATERIAL_IELEMENT[0]
        C1 = A * E / L
        C2 = E * I / (L ** 3)
        K_IELEMENT = np.array([[C1, 0, 0, -C1, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [-C1, 0, 0, C1, 0, 0],
                              [0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0]])
    return K_IELEMENT

def ELEMENT_ROTATION(TYPE_ELEMENT, SECTION_IELEMENT):
    """ 
    This function creates the rotation matrix of the I_ELEMENT element.

    Input:
    TYPE_ELEMENT       | Type element in Finito algorithm                      | Integer 
                       |     0 - Frame bar element                             |
    SECTION_IELEMENT   | Section I_ELEMENT properties                          | Py list[6]
                       |     [0] - Length                                      |
                       |     [1] - Sine                                        |
                       |     [2] - Cosine                                      |
                       |     [3] - Area                                        |
                       |     [4] - Inertia auxiliar                            |
                       |     [5] - Inertia frame element                       |  
    Output:
    R_IELEMENT         | Rotation matrix  I_ELEMENT                            | Py Numpy array [N_DOFSELEMENT x N_DOFSELEMENT]
    """
    SIN = SECTION_IELEMENT[1]
    COS = SECTION_IELEMENT[2]
    if TYPE_ELEMENT == 0:
        R_IELEMENT = np.array([[COS, SIN, 0, 0, 0, 0],
                               [-SIN, COS, 0, 0, 0, 0],
                               [0, 0, 1, 0, 0, 0],
                               [0, 0, 0, COS, SIN, 0],
                               [0, 0, 0, -SIN, COS, 0],
                               [0, 0, 0, 0, 0, 1]])
    return R_IELEMENT                                                                                                                                                                                                                                                                                                                                                             