import numpy as np

# CRIAÇÃO DOS ÍNDICES INICIAIS PARA EXECUÇÃO DO ALGORITMO
def INDEX_ASSEMBLY(TYPE_ELEMENT):
    """ 
    This function establishes values for the internal variables that are used in the algorithm.
    
    Input:
    TYPE_ELEMENT    | Type element in Finito algorithm           | Integer 
                    |        0 - Frame bar element               |
                    |        1 - CST surface element             |

    Output:
    N_DOFSNODE      | Number of degress of freedom per node      | Integer
    N_NODESELEMENT  | Number of nodes per element                | Integer
    DOFS_LOCAL      | ID local degrees of freedom in element     | Py list[??]
                    |       ?? = [6] -> TYPE_ELEMENT = 0         |
                    |       ?? = [6] -> TYPE_ELEMENT = 1         |
    AUX_1           | Material ID in ELEMENTS                    | Integer
    AUX_2           | Geometry or Thickness ID in ELEMENTS       | Integer
                    |       Geometry  -> TYPE_ELEMENT = 0        |
                    |       Thickness -> TYPE_ELEMENT = 1        |
    N_DOFSELEMENT   | Number of degress of freedom per element   | Integer
    """
    # Frame bar element
    if TYPE_ELEMENT == 0: 
        N_DOFSNODE = 3
        N_NODESELEMENT = 2
        DOFS_LOCAL = [0, 1, 2, 3, 4, 5]
    # CST surface element
    elif TYPE_ELEMENT == 1:
        N_DOFSNODE = 2
        N_NODESELEMENT = 3
        DOFS_LOCAL = [0, 1, 2, 3, 4, 5]
    AUX_1 = N_NODESELEMENT + 0
    AUX_2 = N_NODESELEMENT + 1
    N_DOFSELEMENT = N_DOFSNODE * N_NODESELEMENT
    return N_DOFSNODE, N_NODESELEMENT, DOFS_LOCAL, AUX_1, AUX_2, N_DOFSELEMENT

# DETERMINAÇÃO DOS ID's DOF POR NÓ DA ESTRUTURA
def DOF_GLOBAL_ASSEMBLY(TYPE_ELEMENT, N_DOFSNODE, N_NODES):
    """
    This function determines the value of the degrees of global freedoms by node of the structure.
    
    Input
    TYPE_ELEMENT     | Type element in Finito algorithm           | Integer 
                     |        0 - Frame bar element               |
                     |        1 - CST surface element             |   
    N_DOFSNODE       | Number of degress of freedom per node      | Integer
    N_NODES          | Number of nodes                            | Integer

    Output:
    DOF_GLOBALNODAL  | ID global DOF per node                     | Py Numpy array[N_NODES x ??]
                     |       ?? = [3] -> TYPE_ELEMENT = 0         |
                     |       ?? = [2] -> TYPE_ELEMENT = 1         |
    """
    DOF_GLOBALNODAL = np.zeros((N_NODES, N_DOFSNODE))
    for I_COUNT in range (N_NODES):
        # Frame bar element
        if TYPE_ELEMENT == 0: 
            DOF_GLOBALNODAL[I_COUNT, 0] = int(N_DOFSNODE * I_COUNT + 0)
            DOF_GLOBALNODAL[I_COUNT, 1] = int(N_DOFSNODE * I_COUNT + 1)
            DOF_GLOBALNODAL[I_COUNT, 2] = int(N_DOFSNODE * I_COUNT + 2)
        # CST surface element
        elif TYPE_ELEMENT == 1:
            DOF_GLOBALNODAL[I_COUNT, 0] = int(N_DOFSNODE * I_COUNT + 0)
            DOF_GLOBALNODAL[I_COUNT, 1] = int(N_DOFSNODE * I_COUNT + 1)
    return DOF_GLOBALNODAL

# GRAUS DE LIBERDADE TOTAL
def TOTAL_DEGREE_FREEDOM(N_DOFSNODE, N_NODES):
    """ 
    This function determines the quantity and ID values of the structure's global degrees of freedom.

    Input:
    N_DOFSNODE    | Number of degress of freedom per node  | Integer 
    N_NODES       | Number of nodes                        | Integer 

    Output:
    DOF_GLOBAL    | ID global degree of freedom            | Py list[N_DOFSGLOBAL]
    N_DOFSGLOBAL  | Total of degrees of freedom            | Integer 
    """
    DOF_GLOBAL = []
    N_DOFSGLOBAL = N_NODES * N_DOFSNODE
    for I_COUNT in range (N_DOFSGLOBAL):
        DOF_GLOBAL.append(I_COUNT)
    return DOF_GLOBAL, N_DOFSGLOBAL

# GRAUS DE LIBERDADE RESTRITOS
def PRESCRIPTIONS_DEGREE_FREEDOM(PRESCRIPTIONS, DOF_GLOBALNODAL):
    """
    This function determines the quantity and ID values of the displacements prescribed degrees of freedom. 

    Input: 
    DOF_GLOBALNODAL         | ID global DOF per node                         | Py Numpy array[N_NODES x ??]
                            |       ?? = [3] -> TYPE_ELEMENT = 0             |
                            |       ?? = [2] -> TYPE_ELEMENT = 1             |
    PRESCRIPTIONS           | Prescribed DOF displacement properties         | Py Numpy array              
                            |   Node, Direction (X = 0, Y = 1, Z = 2), Value | 

    Output:
    DOF_PRESCRIPTIONS       | ID prescribed degree of freedom                | Py list[N_DOFSPRESCRIPTIONS]
    DOF_PRESCRIPTIONSVALUE  | Value prescribed degree of freedom             | Py list[N_DOFSPRESCRIPTIONS]
    N_DOFSPRESCRIPTIONS     | Total number of prescribed degrees of freedom  | Integer
    """
    DOF_PRESCRIPTIONS = []
    DOF_PRESCRIPTIONSVALUE = []
    N_DOFSPRESCRIPTIONS = PRESCRIPTIONS.shape[0]
    for I_COUNT in range (N_DOFSPRESCRIPTIONS):
        NODE = int(PRESCRIPTIONS[I_COUNT, 0])
        INDEX_DOF = int(PRESCRIPTIONS[I_COUNT, 1])
        DOF_VALUE = int(DOF_GLOBALNODAL[NODE, INDEX_DOF])
        DOF_PRESCRIPTIONS.append(DOF_VALUE)
        PRESCRIBED_VALUE = PRESCRIPTIONS[I_COUNT, 2]
        DOF_PRESCRIPTIONSVALUE.append(PRESCRIBED_VALUE)
    return DOF_PRESCRIPTIONS, DOF_PRESCRIPTIONSVALUE, N_DOFSPRESCRIPTIONS

# GRAUS DE LIBERDADE LIVRES
def FREE_DEGREE_FREEDOM(DOF_PRESCRIPTIONS, DOF_GLOBAL):
    """
    This function determines the quantity and ID values of the displacements free of degrees of freedom.

    Input:
    DOF_PRESCRIPTIONS  | ID prescribed degree of freedom          | Py list[N_DOFSPRESCRIPTIONS]
    DOF_GLOBAL         | ID global degree of freedom              | Py list[N_DOFSGLOBAL]

    Output:
    DOF_FREE           | ID free degree of freedom                | Py list[N_DOFSFREE] 
    N_DOFSFREE         | Total number of free degrees of freedom  | Integer
    """
    DOF_FREE = np.setdiff1d(DOF_GLOBAL, DOF_PRESCRIPTIONS)
    N_DOFSFREE = len(DOF_FREE)
    return DOF_FREE, N_DOFSFREE

# VETOR COMPLETO DE FORÇAS NODAIS POR DOF
def CONTRIBUTION_NODAL_EXTERNAL_LOAD(NODAL_LOAD, N_DOFSGLOBAL, DOF_GLOBALNODAL):
    """
    This function builds the external charges vector at the level of freedom.

    Input:
    NODAL_LOAD           | Nodal DOF force properties                         | Py Numpy array              
                         |    Node, Direction (X = 0, Y = 1, Z = 2), Value    |
    N_DOFSGLOBAL         | Total of degrees of freedom                        | Integer 
    DOF_GLOBALNODAL      | ID global DOF per node                             | Py Numpy array[N_NODES x ??]
                         |    ?? = [3] -> TYPE_ELEMENT = 0                    |
                         |    ?? = [2] -> TYPE_ELEMENT = 1                    |         
    
    Output:
    DOF_NODALFORCE       | Force per DOF                                      | Py Numpy array[N_DOFSGLOBAL x 1]   
    """
    DOF_NODALFORCE = np.zeros((N_DOFSGLOBAL, 1))
    N_NODALFORCE = NODAL_LOAD.shape[0]
    for I_COUNT in range(N_NODALFORCE):
        NODE = int(NODAL_LOAD[I_COUNT, 0])
        INDEX_DOF = int(NODAL_LOAD[I_COUNT, 1])
        DOF_VALUE = int(DOF_GLOBALNODAL[NODE, INDEX_DOF])
        P = float(NODAL_LOAD[I_COUNT, 2])
        DOF_NODALFORCE[DOF_VALUE, 0] = P
    return DOF_NODALFORCE

# LISTA COM AS CONTRIBUIÇÕES NODAIS DE MOLAS
def SPRING_CONTRIBUTION(N_DOFSNODE, SPRINGS, N_DOFSPRINGS):
    """
    This function creates the contribution of the spring elements in the global stiffness matrix.
    
    Input:
    N_DOFSNODE      | Number of degress of freedom per node           | Integer
    SPRINGS         | Nodal DOF spring properties                     | Py Numpy array              
                    |   Node, Direction (X = 0, Y = 1, Z = 2), Value  |
    N_DOFSPRINGS    | Number of DOF spring elements                   | Integer
    
    Output:
    SPRING_INDEX    | ID DOF spring element                           | Py list[N_DOFSPRINGS]
    SPRING_VALUES   | Spring coefficient                              | Integer 
    """
    SPRING_INDEX = []
    SPRING_VALUES = []
    for I_COUNT in range(N_DOFSPRINGS):
        NODE = int(SPRINGS[I_COUNT, 0])
        INDEX_DOF = int(SPRINGS[I_COUNT, 1])
        SPRING_INDEX.append(int(N_DOFSNODE * NODE + INDEX_DOF))
        SPRING_VALUES.append(SPRINGS[I_COUNT, 2])
    return SPRING_INDEX, SPRING_VALUES

# DOF GLOBAL POR ELEMENTO
def GLOBAL_DOF_ELEMENT(N_NODESELEMENT, N_DOFSNODE, DOF_GLOBALNODAL, ELEMENTS, I_ELEMENT):
    """
    This function determines the degree of global freedom of the element I_ELEMENT.

    Input:
    N_NODESELEMENT      | Number of nodes per element                            | Integer
    N_DOFSNODE          | Number of degress of freedom per node                  | Integer
    DOF_GLOBALNODAL     | ID global DOF per node                                 | Py Numpy array[N_NODES x ??]
                        |    ?? = [3] -> TYPE_ELEMENT = 0                        |
                        |    ?? = [2] -> TYPE_ELEMENT = 1                        |   
    ELEMENTS            | Elements properties                                    | Py Numpy array
                        |   Node 0 ... Node (N_NODES - 1), Material ID,          |
                        |    Geometry ID, Hinge ID node 0, Hinge ID node 1       |
    I_ELEMENT           | i element in looping                                   | Integer
    
    Output:
    DOF_GLOBALIELEMENT  | Global DOF ID I_ELEMENT                                | Py list[N_DOFSELEMENT] 
    """
    DOF_GLOBALIELEMENT = []
    for I_COUNT in range(N_NODESELEMENT):
        NODE = int(ELEMENTS[I_ELEMENT, I_COUNT])
        for J_COUNT in range(N_DOFSNODE):
            DOF_VALUE = int(DOF_GLOBALNODAL[NODE, J_COUNT])
            DOF_GLOBALIELEMENT.append(DOF_VALUE)
    return DOF_GLOBALIELEMENT

# MATRIZ DE RIGIDEZ GLOBAL
def GLOBAL_STIFFNESS(N_DOFSGLOBAL, DOF_GLOBALIELEMENT, K_IELEMENT):
    """
    This function creates the global stiffness.

    Input:
    N_DOFSGLOBAL        | Total of degrees of freedom       | Integer 
    DOF_GLOBALIELEMENT  | Global DOF ID I_ELEMENT           | Integer 
    K_IELEMENT          | Local stiffness matrix I_ELEMENT  | Py Numpy array[N_DOFSELEMENT x N_DOFSELEMENT]

    Output:
    K_G                 | Global stiffness matrix           | Py Numpy array[N_DOFSGLOBAL x N_DOFSGLOBAL]
    """
    K_G = np.zeros((N_DOFSGLOBAL, N_DOFSGLOBAL))
    for I_COUNT, I_VALUE in enumerate(DOF_GLOBALIELEMENT):
        for J_COUNT, J_VALUE in enumerate(DOF_GLOBALIELEMENT):
            K_G[I_VALUE, J_VALUE] = K_G[I_VALUE, J_VALUE] + K_IELEMENT[I_COUNT, J_COUNT]
    return K_G

# MATRIZ DE RIGIDEZ COM OS DOF's LIVRES 
def CONDENSE_GLOBAL_FREE_STIFFNESS(K_G, DOF_FREE, N_DOFSFREE):
    """ 
    This function assembles the portion containing the free degrees of freedom of the stiffness matrix. 
    
    Input:
    K_G         | Global stiffness matrix                  | Py Numpy array[N_DOFSGLOBAL x N_DOFSGLOBAL]
    DOF_FREE    | ID free degree of freedom                | Py list[N_DOFSFREE]     
    N_DOFSFREE  | Total number of free degrees of freedom  | Integer
    
    Output:
    K_FF        | Free global stiffness matrix             | Py Numpy array[N_DOFSFREE x N_DOFSFREE]
    """
    K_FF = np.zeros((N_DOFSFREE, N_DOFSFREE))
    for I_COUNT in range(N_DOFSFREE):
        DOF_FREELINE = DOF_FREE[I_COUNT]
        for J_COUNT in range(N_DOFSFREE):
            DOF_FREECOLUMN = DOF_FREE[J_COUNT]
            K_FF[I_COUNT, J_COUNT] = K_G[DOF_FREELINE, DOF_FREECOLUMN]
    return K_FF

# MATRIZ DE RIGIDEZ COM OS DOF's PRESCRITOS-LIVRES  
def CONDENSE_PRESCRIBED_FREE_GLOBAL_STIFFNESS(K_G, DOF_FREE, N_DOFSFREE, DOF_PRESCRIPTIONS, N_DOFSPRESCRIPTIONS):
    """ 
    This function assembles the portion containing the prescribed and free degrees of freedom of the stiffness matrix.
    
    Input:
    K_G                  | Global stiffness matrix                        | Py Numpy array[N_DOFSGLOBAL x N_DOFSGLOBAL]
    DOF_FREE             | ID free degree of freedom                      | Py list[N_DOFSFREE]     
    N_DOFSFREE           | Total number of free degrees of freedom        | Integer
    DOF_PRESCRIPTIONS    | ID prescribed degree of freedom                | Py list[N_DOFSPRESCRIPTIONS]
    N_DOFSPRESCRIPTIONS  | Total number of prescribed degrees of freedom  | Integer
    
    Output:
    K_PF                 | Prescribed-Free global stiffness matrix        | Py Numpy array[N_DOFSPRESCRIPTIONS x N_DOFSFREE]
    """
    K_PF = np.zeros((N_DOFSPRESCRIPTIONS, N_DOFSFREE))
    for I_COUNT in range(N_DOFSPRESCRIPTIONS):
        DOF_PRECRIBEDLINE = DOF_PRESCRIPTIONS[I_COUNT]
        for J_COUNT in range(N_DOFSFREE):
            DOF_FREECOLUMN = DOF_FREE[J_COUNT]
            K_PF[I_COUNT, J_COUNT] = K_G[DOF_PRECRIBEDLINE, DOF_FREECOLUMN]
    return K_PF

# VETOR GLOBAL DE DESLOCAMENTOS COM OS DOF's PRESCRITOS 
def CONDENSE_PRESCRIBED_GLOBAL_DISPLACEMENT(DOF_PRESCRIPTIONSVALUE, N_DOFSPRESCRIPTIONS):
    """ 
    This function assembles the portion containing the prescribed degrees of freedom of the global displacement.
    
    Input:
    DOF_PRESCRIPTIONSVALUE  | Value prescribed degree of freedom             | Py list[N_DOFSPRESCRIPTIONS]
    N_DOFSPRESCRIPTIONS     | Total number of prescribed degrees of freedom  | Integer
    
    Output:
    U_PP                    | Prescribed global displacement                 | Py Numpy array[N_DOFSPRESCRIPTIONS x 1]
    """
    U_PP = np.zeros((N_DOFSPRESCRIPTIONS, 1))
    for I_COUNT in range(N_DOFSPRESCRIPTIONS):
        DOF_PRESCRIBEDVALUE = DOF_PRESCRIPTIONSVALUE[I_COUNT]
        U_PP[I_COUNT, 0] = DOF_PRESCRIBEDVALUE
    return U_PP

# VETOR GLOBAL DE FORÇAS COM OS DOF's LIVRES
def CONDENSE_FREE_GLOBAL_FORCES(F_G, DOF_FREE, N_DOFSFREE):
    """ 
    This function assembles the portion containing the free degrees 
    of freedom of the global forces.
    
    Input:
    F_G         | Global forces                             | Py Numpy array[N_DOFSGLOBAL x 1]
    DOF_FREE    | ID free degree of freedom                 | Py list[N_DOFSFREE]    
    N_DOFSFREE  | Total number of free degrees of freedom   | Integer
    
    Output:
    F_FF        | Free global forces                        | Py Numpy array[N_DOFSPRESCRIPTIONS x 1]
    """    
    F_FF = np.zeros((N_DOFSFREE, 1))
    for I_COUNT in range(N_DOFSFREE):
        FREE_DOF = DOF_FREE[I_COUNT]
        F_FF[I_COUNT, 0] = F_G[FREE_DOF, 0]
    return F_FF

# MONTAGEM DO VETOR DE DESLOCAMENTOS GLOBAIS DA ESTRUTURA
def ASSEMBLY_TOTAL_DISPLACEMENT(U_FF, U_PP, N_DOFSGLOBAL, DOF_PRESCRIPTIONS, DOF_FREE):
    """
    This function assembles the global displacements from the calculated parcels.
    
    Input:
    U_FF                 | Free global displacement         | Py Numpy array[N_DOFSFREE x 1]
    U_PP                 | Prescribed global displacement   | Py Numpy array[N_DOFSPRESCRIPTIONS x 1]
    N_DOFSGLOBAL         | Total of degrees of freedom      | Integer 
    DOF_PRESCRIPTIONS    | ID prescribed degree of freedom  | Py list[N_DOFSPRESCRIPTIONS]    
    DOF_FREE             | ID free degree of freedom        | Py list[N_DOFSFREE]     
    
    Output:
    U_G                  | Global displacement              | Py Numpy array[N_DOFSFREE x 1]
    """
    U_G = np.zeros((N_DOFSGLOBAL, 1))
    for I_COUNT, I_VALUE in enumerate(DOF_PRESCRIPTIONS):
        DOF_DISPLACEMENTVALUE = U_PP[I_COUNT, 0]
        U_G[I_VALUE, 0] = DOF_DISPLACEMENTVALUE
    for J_COUNT, J_VALUE in enumerate(DOF_FREE):
        DOF_DISPLACEMENTVALUE = U_FF[J_COUNT, 0]
        U_G[J_VALUE, 0] = DOF_DISPLACEMENTVALUE
    return U_G

# DESLOCAMENTOS GLOBAIS POR ELEMENTO
def CONDENSE_GLOBAL_ELEMENT_DISPLACEMENTS(U_G, N_DOFSELEMENT, DOF_GLOBALIELEMENT):
    """
    This function assembles the nodal displacements of I_ELEMENT.

    Input:
    U_G                 | Global displacement                        | Py Numpy array[N_DOFSFREE x 1]
    N_DOFSELEMENT       | Number of degress of freedom per element   | Integer
    DOF_GLOBALIELEMENT  | Global DOF ID I_ELEMENT                    | Py list[N_DOFSELEMENT] 
    
    Output:    
    U_IELEMENT          | Global displacements I_ELEMENT             | Py Numpy array[N_DOFSELEMENT x 1] 
    """
    U_IELEMENT = np.zeros((N_DOFSELEMENT, 1))
    for I_COUNT, J_COUNT in enumerate(DOF_GLOBALIELEMENT):
        U_IELEMENT[I_COUNT, 0] = U_G[J_COUNT, 0]
    return U_IELEMENT

# FORÇAS INTERNAS DA ESTRUTURA
def GLOBAL_INTERNAL_LOADS(F_INTIELEMENT, N_DOFSGLOBAL, DOF_GLOBALIELEMENT):
    """
    This function assembles the internal load of the structure.

    Input:
    F_INTIELEMENT       | Global internal load I_ELEMENT  | Py Numpy array[N_DOFSELEMENT x 1] 
    N_DOFSGLOBAL        | Total of degrees of freedom     | Integer 
    DOF_GLOBALIELEMENT  | Global DOF ID I_ELEMENT         | Py list[N_DOFSELEMENT] 
    
    Output:
    F_INT               | Global internal load            | Py Numpy array[N_DOFSGLOBA x 1] 
    """
    F_INT = np.zeros((N_DOFSGLOBAL, 1))
    for I_COUNT, J_COUNT in enumerate(DOF_GLOBALIELEMENT):
        F_INT[J_COUNT, 0] = F_INTIELEMENT[I_COUNT, 0]
    return F_INT

# IMPOSIÇÃO DAS CONDIÇÕES DE CONTORNO TÉCNICA 0 - 1
def ZERO_AND_ONE_METHOD(K_G, F_G, DOF_PRESCRIPTIONS, DOF_PRESCRIPTIONSVALUE):
    """
    This function solves the system of linear equations using the 0 and 1 technique.
    
    Input:
    K_G                     | Global stiffness matrix             | Py Numpy array[N_DOFSGLOBAL x N_DOFSGLOBAL]
    F_G                     | Global forces                       | Py Numpy array[N_DOFSGLOBAL x 1]
    DOF_PRESCRIPTIONS       | ID prescribed degree of freedom     | Py list[N_DOFSPRESCRIPTIONS]  
    DOF_PRESCRIPTIONSVALUE  | Value prescribed degree of freedom  | Py list[N_DOFSPRESCRIPTIONS]

    Output:
    K_G                     | Update global stiffness matrix      | Py Numpy array[N_DOFSGLOBAL x N_DOFSGLOBAL]
    F_G                     | Update global forces                | Py Numpy array[N_DOFSGLOBAL x 1]
    """
    for I_COUNT, DOF in enumerate(DOF_PRESCRIPTIONS):
        VALUE_PRESCRIBED = DOF_PRESCRIPTIONSVALUE[I_COUNT]
        AUX_1 = K_G[:, DOF]
        AUX_1 = np.expand_dims(AUX_1, axis = 1)
        F_G -= VALUE_PRESCRIBED * AUX_1
        F_G[DOF, 0] = VALUE_PRESCRIBED
        K_G[DOF,:] = 0
        K_G[:, DOF] = 0
        K_G[DOF, DOF] = 1
    return K_G, F_G          