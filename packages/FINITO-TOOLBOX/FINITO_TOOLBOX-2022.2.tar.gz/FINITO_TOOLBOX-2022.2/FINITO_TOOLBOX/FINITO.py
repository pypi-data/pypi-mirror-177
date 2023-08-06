import numpy as np
import FINITO_TOOLBOX.FINITO_COMMON_LIBRARY as FINITO_CL
import FINITO_TOOLBOX.FINITO_MEF1D_LIBRARY as FINITO_MEF1D
import FINITO_TOOLBOX.FINITO_MEF2D_LIBRARY as FINITO_MEF2D

def MEF1D(**kwargs):
    """ 
    This function performs structural analysis of frame elements with 2 nodes (1 at each end).
  
    Input:
    All inputs kwargs arguments type.

    FILENAME    | Structural dataset                                                 | .txt extension
    DICTIONARY  | Structural dataset                                                 | Py dictionary
                |   Dictionary and file tags                                         |
                |    TYPE_ELEMENT  = Type element in Finito algorithm                | Integer 
                |     0 - Frame bar element                                          |
                |    TYPE_SOLUTION = Boundary conditions in system of equations      | Integer
                |     0 - Condense procedure                                         |
                |     1 - Zero and One algorithm                                     |
                |   N_NODES        = Number of nodes                                 | Integer
                |   N_MATERIALS    = Number of materials                             | Integer
                |   N_SECTIONS     = Number of sections                              | Integer
                |   N_ELEMENTS     = Number of frame elements                        | Integer
                |   N_DOFPRESCRIPTIONS = Number of DOF displacement control          | Integer
                |   N_DOFLOADED        = Number of DOF forces                        | Integer
                |   N_DOFSPRINGS       = Number of DOF spring elements               | Integer
                |   COORDINATES        = Coordinates properties                      | Py Numpy array
                |                          Node, x, y                                |
                |   ELEMENTS       = Elements properties                             | Py Numpy array
                |                    Node 0 ... Node (N_NODES - 1), Material ID,     | 
                |                    Geometry ID, Hinge ID node 0, Hinge ID node 1   |
                |   MATERIALS      = Materials properties                            | Py Numpy array
                |                    Young, Poisson, Density, Thermal coefficient    |
                |   SECTIONS       = Sections properties                             | Py Numpy array
                |                    Area, Inertia 1, Inertia Frame bar, X GC, Y GC  |
                |   PRESCRIPTIONS  = Prescribed DOF displacement properties          | Py Numpy array              
                |                    Node, Direction (X = 0, Y = 1, Z = 2), Value    | 
                |   NODAL_LOAD     = Nodal DOF force properties                      | Py Numpy array              
                |                    Node, Direction (X = 0, Y = 1, Z = 2), Value    |
                |   SPRINGS        = Nodal DOF spring properties                     | Py Numpy array              
                                     Node, Direction (X = 0, Y = 1, Z = 2), Value    |

    Output:
    RESULTS     | Structural analysis results by element                             | Py dictionary
    """
    # Read input file 
    FILENAME = kwargs.get('FILENAME')
    DICTIONARY = kwargs.get('DICTIONARY')
    if FILENAME:
        TYPE_SOLUTION, TYPE_ELEMENT, N_NODES, N_MATERIALS, N_SECTIONS, N_ELEMENTS, N_DOFPRESCRIPTIONS, N_ELEMENTSLOADED, N_DOFLOADED, N_DOFSPRINGS, COORDINATES, ELEMENTS, MATERIALS, SECTIONS, PRESCRIPTIONS, ELEMENT_EXTERNAL_LOAD, NODAL_LOAD, SPRINGS = FINITO_MEF1D.GET_VALUE_FROM_TXT_MEF1D_FINITO(FILENAME)
    else:
        TYPE_SOLUTION, TYPE_ELEMENT, N_NODES, N_MATERIALS, N_SECTIONS, N_ELEMENTS, N_DOFPRESCRIPTIONS, N_ELEMENTSLOADED, N_DOFLOADED, N_DOFSPRINGS, COORDINATES, ELEMENTS, MATERIALS, SECTIONS, PRESCRIPTIONS, ELEMENT_EXTERNAL_LOAD, NODAL_LOAD, SPRINGS = FINITO_MEF1D.GET_VALUE_FROM_DICT_MEF1D_FINITO(DICTIONARY)
    
    # Creating the algorithm's internal parameters
    N_DOFSNODE, N_NODESELEMENT, DOFS_LOCAL, AUX_1, AUX_2, N_DOFSELEMENT = FINITO_CL.INDEX_ASSEMBLY(TYPE_ELEMENT)
    
    # Global DOF assembly
    DOF_GLOBALNODAL = FINITO_CL.DOF_GLOBAL_ASSEMBLY(TYPE_ELEMENT, N_DOFSNODE, N_NODES)
    
    # DOF's total, prescriptions and free
    DOF_GLOBAL, N_DOFSGLOBAL = FINITO_CL.TOTAL_DEGREE_FREEDOM(N_DOFSNODE, N_NODES)
    DOF_PRESCRIPTIONS, DOF_PRESCRIPTIONSVALUE, N_DOFSPRESCRIPTIONS = FINITO_CL.PRESCRIPTIONS_DEGREE_FREEDOM(PRESCRIPTIONS, DOF_GLOBALNODAL)
    DOF_FREE, N_DOFSFREE = FINITO_CL.FREE_DEGREE_FREEDOM(DOF_PRESCRIPTIONS, DOF_GLOBAL)
    
    # Nodal load contribuition
    DOF_NODALFORCE = FINITO_CL.CONTRIBUTION_NODAL_EXTERNAL_LOAD(NODAL_LOAD, N_DOFSGLOBAL, DOF_GLOBALNODAL)

    # Element load contribuition
    if N_ELEMENTSLOADED > 0: 
        DOF_ELEMENTFORCE = FINITO_MEF1D.CONTRBUITION_ELEMENT_EXTERNAL_LOAD(TYPE_ELEMENT, N_ELEMENTSLOADED, ELEMENT_EXTERNAL_LOAD, DOF_GLOBALNODAL, ELEMENTS, COORDINATES, SECTIONS, AUX_2, N_DOFSELEMENT, N_DOFSGLOBAL, N_NODESELEMENT, N_DOFSNODE)
        F_G = DOF_NODALFORCE + DOF_ELEMENTFORCE
    else:
        F_G = DOF_NODALFORCE

    # Structure stiffness matrix
    K_G = np.zeros((N_DOFSGLOBAL, N_DOFSGLOBAL))
    
    # Hinged elements
    HINGES = FINITO_MEF1D.HINGED_PROPERTIES(ELEMENTS)
    for I_ELEMENT in range(N_ELEMENTS):
        # Material and section properties in j element
        MATERIAL_IELEMENT = FINITO_MEF1D.MATERIALS_PROPERTIES_0(ELEMENTS, MATERIALS, I_ELEMENT, AUX_1)
        SECTION_IELEMENT = FINITO_MEF1D.GEOMETRIC_PROPERTIES_0(COORDINATES, ELEMENTS, SECTIONS, I_ELEMENT, AUX_2)
        # i element stiffness matrix local axis
        K_IELEMENT = FINITO_MEF1D.ELEMENT_STIFFNESS_0(TYPE_ELEMENT, SECTION_IELEMENT, MATERIAL_IELEMENT, HINGES[I_ELEMENT, :])
        # Rotation matrix
        R_IELEMENT = FINITO_MEF1D.ELEMENT_ROTATION(TYPE_ELEMENT, SECTION_IELEMENT)
        # i element stiffness matrix global axis
        K_IELEMENTGLOBAL = np.dot(np.dot(np.transpose(R_IELEMENT), K_IELEMENT), R_IELEMENT)
        # Global DOF i element
        DOF_GLOBALIELEMENT = FINITO_CL.GLOBAL_DOF_ELEMENT(N_NODESELEMENT, N_DOFSNODE, DOF_GLOBALNODAL, ELEMENTS, I_ELEMENT)
        # Global stiffness
        K_GCONTRIBUITION = FINITO_CL.GLOBAL_STIFFNESS(N_DOFSGLOBAL, DOF_GLOBALIELEMENT, K_IELEMENTGLOBAL)
        K_G = K_G + K_GCONTRIBUITION
    
    # Spring contribution
    if N_DOFSPRINGS > 0:
        SPRING_INDEX, SPRING_VALUES = FINITO_CL.SPRING_CONTRIBUTION(N_DOFSNODE, SPRINGS, N_DOFSPRINGS)
        for K_COUNT in range(N_DOFSPRINGS):
            SPRING_VALUE = SPRING_VALUES[K_COUNT]
            INDEX_DOF = SPRING_INDEX[K_COUNT]
            K_G[INDEX_DOF, INDEX_DOF] = K_G[INDEX_DOF, INDEX_DOF] + SPRING_VALUE
    
    # Displacement solution 0: Condense procedure
    if TYPE_SOLUTION == 0:
        # Condense displacements, forces and Stiffness matrix
        U_PP = FINITO_CL.CONDENSE_PRESCRIBED_GLOBAL_DISPLACEMENT(DOF_PRESCRIPTIONSVALUE, N_DOFSPRESCRIPTIONS)
        F_FF = FINITO_CL.CONDENSE_FREE_GLOBAL_FORCES(F_G, DOF_FREE, N_DOFSFREE)
        K_FF = FINITO_CL.CONDENSE_GLOBAL_FREE_STIFFNESS(K_G, DOF_FREE, N_DOFSFREE)
        K_PF = FINITO_CL.CONDENSE_PRESCRIBED_FREE_GLOBAL_STIFFNESS(K_G, DOF_FREE, N_DOFSFREE, DOF_PRESCRIPTIONS, N_DOFSPRESCRIPTIONS)
        # Displacement solution
        K_FFINVERSE = np.linalg.pinv(K_FF, rcond = 1e-15)
        U_FF = np.dot(K_FFINVERSE, F_FF - np.dot(np.transpose(K_PF), U_PP))
        U_G = FINITO_CL.ASSEMBLY_TOTAL_DISPLACEMENT(U_FF, U_PP, N_DOFSGLOBAL, DOF_PRESCRIPTIONS, DOF_FREE)
   
    # Displacement solution 0: Zero and One procedure
    elif TYPE_SOLUTION == 1:
        K_G, F_G = FINITO_CL.ZERO_AND_ONE_METHOD(K_G, F_G, DOF_PRESCRIPTIONS, DOF_PRESCRIPTIONSVALUE)
        K_FFINVERSE = np.linalg.pinv(K_G, rcond = 1e-15)
        U_G = np.dot(K_FFINVERSE, F_G)

    # Internal loads
    # Frame division 
    DIV = 11 
    
    # Start empty dictionary
    RESULTS = [{'X': np.empty(DIV), 'UX': np.empty(DIV), 'UY': np.empty(DIV), 'UZ': np.empty(DIV), 'N': np.empty(DIV), 'V': np.empty(DIV), 'M': np.empty(DIV), 'ID_ELEMENT': J_COUNT} for J_COUNT in range(N_ELEMENTS)]
    
    # Element evaluation
    for J_ELEMENT in range(N_ELEMENTS):
        # Material and section properties in j element
        MATERIAL_JELEMENT = FINITO_MEF1D.MATERIALS_PROPERTIES_0(ELEMENTS, MATERIALS, J_ELEMENT, AUX_1)
        SECTION_JELEMENT = FINITO_MEF1D.GEOMETRIC_PROPERTIES_0(COORDINATES, ELEMENTS, SECTIONS, J_ELEMENT, AUX_2)
        # j element stiffness matrix local axis 
        K_JELEMENT = FINITO_MEF1D.ELEMENT_STIFFNESS_0(TYPE_ELEMENT, SECTION_JELEMENT, MATERIAL_JELEMENT, HINGES[J_ELEMENT, :])
        # Rotation matrix
        R_JELEMENT = FINITO_MEF1D.ELEMENT_ROTATION(TYPE_ELEMENT, SECTION_JELEMENT)
        # Global DOF j element
        DOF_GLOBALJELEMENT = FINITO_CL.GLOBAL_DOF_ELEMENT(N_NODESELEMENT, N_DOFSNODE, DOF_GLOBALNODAL, ELEMENTS, J_ELEMENT)
        # Element global displacements
        U_GJELEMENT = FINITO_CL.CONDENSE_GLOBAL_ELEMENT_DISPLACEMENTS(U_G, N_DOFSELEMENT, DOF_GLOBALJELEMENT)
        # Element local displacements
        U_JELEMENT = np.dot(R_JELEMENT, U_GJELEMENT)
        # Internal force in j element (Node 0 and node 1 [x, y, tetha])
        if N_ELEMENTSLOADED > 0:
            Q_X = 0
            Q_Y = 0
            for I in range(N_ELEMENTSLOADED):
                LOAD_ELEMENT = ELEMENT_EXTERNAL_LOAD[I, 0]
                if LOAD_ELEMENT == J_ELEMENT:  
                    L = SECTION_JELEMENT[0]
                    SIN = SECTION_JELEMENT[1]
                    COS = SECTION_JELEMENT[2]
                    IDSIST = ELEMENT_EXTERNAL_LOAD[I, 1]
                    Q_X = ELEMENT_EXTERNAL_LOAD[I, 2]
                    Q_Y = ELEMENT_EXTERNAL_LOAD[I, 3]
                    if IDSIST == 0:
                        F_EQ = np.array([[Q_X * L / 2], [Q_Y * L / 2], [Q_Y * L ** 2 / 12], [Q_X * L / 2], [Q_Y * L / 2], [- Q_Y * L ** 2 / 12]])
                    elif IDSIST == 1:
                        Q_X = Q_X * COS + Q_Y * SIN
                        Q_Y = - Q_X * SIN + Q_Y * COS
                        F_EQ = np.array([[Q_X * L / 2], [Q_Y * L / 2], [Q_Y * L ** 2 / 12], [Q_X * L / 2], [Q_Y * L / 2], [- Q_Y * L ** 2 / 12]])
                else:
                    F_EQ = np.zeros((N_DOFSELEMENT, 1))
            F_ELINT = np.dot(K_JELEMENT, U_JELEMENT) - F_EQ
        else:
            F_ELINT = np.dot(K_JELEMENT, U_JELEMENT)
        # Internal force in j element (by division)
        for I_COUNT in range(DIV):
            # Local axis value
            X = SECTION_JELEMENT[0] * (I_COUNT) / (DIV - 1)
            if I_COUNT == 0:
                U_X = U_GJELEMENT[0, 0]
                U_Y = U_GJELEMENT[1, 0]
                U_Z = U_GJELEMENT[2, 0]
            elif I_COUNT == DIV - 1:
                U_X = U_GJELEMENT[3, 0]
                U_Y = U_GJELEMENT[4, 0]
                U_Z = U_GJELEMENT[5, 0]
            elif (I_COUNT != 0 and I_COUNT != DIV - 1):
                U_X = -1989
                U_Y = -1989
                U_Z = -1989
            # Internal loads: Axial, Shear and Bending Moment            
            N = -F_ELINT[0] - Q_X * X
            V = F_ELINT[1] + Q_Y * X
            M = -F_ELINT[2] + F_ELINT[1] * X + (Q_Y * X ** 2) / 2   
            # Save results in dictioonary
            RESULTS[J_ELEMENT]['X'][I_COUNT] = X
            RESULTS[J_ELEMENT]['UX'][I_COUNT] = U_X
            RESULTS[J_ELEMENT]['UY'][I_COUNT] = U_Y
            RESULTS[J_ELEMENT]['UZ'][I_COUNT] = U_Z
            RESULTS[J_ELEMENT]['N'][I_COUNT] = N
            RESULTS[J_ELEMENT]['V'][I_COUNT] = V
            RESULTS[J_ELEMENT]['M'][I_COUNT] = M
    return RESULTS

def MEF2D(**kwargs):
    """ 
    This function performs structural analysis via finite elements conside-
    ring flat surface elements (CST)

    Input:
    All inputs kwargs arguments type.

    FILENAME    | Structural dataset                      | txt extension
    DICTIONARY  | Structural dataset                      | Py dictionary

    Output:
    RESULTS     | Structural analysis results by node     | Py dictionary
    """
    # Read input file
    FILENAME = kwargs.get('FILENAME')
    DICTIONARY = kwargs.get('DICTIONARY')
    if FILENAME:
        [N_NODES, N_MATERIALS, N_THICKNESS, N_ELEMENTST3, N_ELEMENTST6, N_ELEMENTST10, N_FORCES, N_PRESSURES, N_DISPLACEMENTS, TYPE_PLANE, TYPE_ELEMENT, TYPE_SOLUTION, TYPE_INTEGRATION, COORDINATES, MATERIALS, THICKNESS, ELEMENTS, NODAL_LOAD, PRESCRIPTIONS] = FINITO_CL.GET_VALUE_FROM_TXT_MEF2D_FINITO(FILENAME)
    else:
        pass
    # Creating the algorithm's internal parameters
    N_DOFSNODE, N_NODESELEMENT, DOFS_LOCAL, AUX_1, AUX_2, N_DOFSELEMENT = FINITO_CL.INDEX_ASSEMBLY(TYPE_ELEMENT)
    # Global DOF assembly
    DOF_GLOBALNODAL = FINITO_CL.DOF_GLOBAL_ASSEMBLY(TYPE_ELEMENT, N_DOFSNODE, N_NODES)
    # DOF's total, prescriptions and free
    DOF_GLOBAL, N_DOFSGLOBAL = FINITO_CL.TOTAL_DEGREE_FREEDOM(N_DOFSNODE, N_NODES)
    DOF_PRESCRIPTIONS, DOF_PRESCRIPTIONSVALUE, N_DOFSPRESCRIPTIONS = FINITO_CL.PRESCRIPTIONS_DEGREE_FREEDOM(PRESCRIPTIONS, DOF_GLOBALNODAL)
    DOF_FREE, N_DOFSFREE = FINITO_CL.FREE_DEGREE_FREEDOM(DOF_PRESCRIPTIONS, DOF_GLOBAL)
    # Nodal load contribuition
    DOF_NODALFORCE = FINITO_CL.CONTRIBUTION_NODAL_EXTERNAL_LOAD(NODAL_LOAD, N_DOFSGLOBAL, DOF_GLOBALNODAL)
    F_G = DOF_NODALFORCE
    # Structure stiffness matrix
    K_G = np.zeros((N_DOFSGLOBAL, N_DOFSGLOBAL))
    # Numerical integration properties
    NUM_INT = FINITO_CL.NUMERICAL_INTEGRATION(TYPE_INTEGRATION)
    for I_ELEMENT in range(N_ELEMENTST3):
        # Material and section properties in i element
        C_IELEMENT = FINITO_CL.CONSTITUTIVE_C(TYPE_PLANE, MATERIALS, ELEMENTS, I_ELEMENT)
        SECTION_IELEMENT = FINITO_CL.GEOMETRIC_PROPERTIES_1(COORDINATES, ELEMENTS, I_ELEMENT, THICKNESS, AUX_2)
        # i stiffness matrix
        K_IELEMENTGLOBAL = FINITO_CL.ELEMENT_STIFFNESS_1(NUM_INT, N_DOFSELEMENT, TYPE_ELEMENT, N_NODESELEMENT, C_IELEMENT, SECTION_IELEMENT)
        # Global DOF in i element
        DOF_GLOBALIELEMENT = FINITO_CL.GLOBAL_DOF_ELEMENT(N_NODESELEMENT, N_DOFSNODE, DOF_GLOBALNODAL, ELEMENTS, I_ELEMENT)
        K_GCONTRIBUITION = FINITO_CL.GLOBAL_STIFFNESS(N_DOFSGLOBAL, DOF_GLOBALIELEMENT, K_IELEMENTGLOBAL)
        K_G = K_G + K_GCONTRIBUITION
    if TYPE_SOLUTION == 1:
        K_G, F_G = FINITO_CL.ZERO_AND_ONE_METHOD(K_G, F_G, DOF_PRESCRIPTIONS, DOF_PRESCRIPTIONSVALUE)
        U_G = np.linalg.solve(K_G, F_G)
    RESULTS = U_G
    return RESULTS