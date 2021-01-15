#-------------------------List of examples-------------------------------------

D1 = ['N',2,'D',2,'N',2,"D",4,"N",3,"N",3,'N',4,'D',3,'N',2,'D',2,'D']
T = [[1,2],[1,4],[5,2],[5,4],[5,8],[6,4],[6,8],[7,11],[9,4],[9,8],[9,11]]
#T*Gr(2,4)
D2 = ['D',1,'D',2,'N',2,'D',2,'D',2,'N']
T1 = [[1,3],[2,3],[3,4],[3,5],[4,6],[5,6]]
T2 = [[1,3],[2,6],[3,4],[4,6]]
T3 = [[1,3],[2,6],[3,4],[4,6]]
T4 = [[1,6],[2,3],[3,4],[4,6]]
T5 = [[1,6],[2,3],[3,5],[5,6]]
T6 = [[1,6],[2,6]]


#-----------------------------------input--------------------------------------

#5-branes 'N' and 'D' with D3 multiplicities as ints in between. Must start
#with 5-brane and alternate between 5-brane and multiplicity.
D = ["N",1,"N",1,"N",0,"N",1,"N",1,"D",1,"D",0,"D",1,"D",1,"D"]

#Index 5-branes from left to right starting with 1. Encode ties as lists 
#of two indices.
ties = []

#Min and max angle in absolute value of the ties. Tie angle scales linearly
#with distance between end points.
min_angle = 45
max_angle = 65

#Set to True to labe D3 branes with thier multiplicities
show_mults = True

#Set to True to generate tie diagrams and BCTs instead of brane diagrams and
#table-with-margins
include_ties = False

#Set to True to label the margin vectors with U's and V's
UV_labels = True


#------------------------input ends/code begins here---------------------------

#Stores 5-branes and D3 multiplicities in separate lists
branes = [D[2*i] for i in range(int((len(D) + 1) / 2))]
mults = [D[2*i + 1] for i in range(int((len(D) - 1) / 2))]

#Generates tikz code for a brane/tie diagram
with open("brane_diagram.txt", 'w') as f:
    #Draws the 5-branes and places nodes at their center and endpoints
    f.write("% NS5 branes")
    i = 1
    j = 1
    #Stores 5-branes from left to right in string format, 
    #e.g. ["U1", "V1", "U2", "U3", "V2", ...]
    UV = []
    for k in range(len(branes)):
        if branes[k] == "N":
            UV.append("V{}".format(i))
            x1 = 3*k - 0.5
            x2 = 3*k + 0.5
            f.write(("\n\\draw[thick,red] ({},-1)--({},1) " + 
                     "node[pos=0.5](V{}){{}} " +
                     "node[pos=1,inner sep=0](V{}t){{}} "+
                     "node[pos=0,inner sep=0](V{}b){{}};").format(x1, x2,
                          i, i, i))
            i += 1
        elif branes[k] == "D":
            UV.append("U{}".format(j))
            x1 = 3*k + 0.5
            x2 = 3*k - 0.5
            f.write(("\n\\draw[thick,blue] ({},-1)--({},1) " + 
                     "node[pos=0.5](U{}){{}} " +
                     "node[pos=1,inner sep=0](U{}t){{}} "+
                     "node[pos=0,inner sep=0](U{}b){{}};").format(x1, x2, 
                          j, j, j))
            j += 1
        else:
            raise ValueError("Invalid brane diagram")
    
    #Draws the D3 branes labelled with their multiplicities
    f.write("\n\n% D3 branes")            
    for k in range(len(UV) - 1):
        if not isinstance(mults[k], int):
            raise TypeError("Invalid brane diagram")
        if show_mults:
            label = mults[k]
        else:
            label = ""
        f.write("\n\\draw ({})--({}) node[pos=0.5, above](X{}){{{}}};".format(
                UV[k], UV[k + 1], k + 1, label))
        
    #Draws the ties if include_ties = True
    if include_ties:
        f.write("\n\n% Ties")
        for tie in ties:
            l = min(tie) - 1
            r = max(tie) - 1
            if branes[l] == 'N' and branes[r] == 'D':
                side = 't'
                out_angle = ((max_angle - min_angle) / (len(branes) - 1) 
                                * (r - l - 1) + min_angle)
                in_angle = 180 - out_angle
            elif branes[l] == 'D' and branes[r] == 'N':
                side = 'b'
                out_angle = -1 * ((max_angle - min_angle) / (len(branes) - 1) 
                                    * (r - l - 1) + min_angle)
                in_angle = 180 - out_angle
            else:
                raise ValueError("Invalid ties")
            
            f.write("\n\\draw[dashed] ({}{}) to [out={},in={}] ({}{});".format(
                    UV[l], side, int(out_angle), int(in_angle),
                    UV[r], side))
            
#Calculates margin vectors
r = []
c = []
for k in range(len(UV)):
    if UV[k][0] == 'V':
        op = len([bn for bn in UV[:k] if bn[0] == 'U'])
        if k == 0:
            r.append(mults[k])
        elif k == len(UV) - 1:
            r.append(op - mults[k - 1])
        else:
            r.append(mults[k] - mults[k - 1] + op)
    else:
        op = len([bn for bn in UV[k + 1:] if bn[0] == 'V'])
        if k == 0:
            c.append(op - mults[k])
        elif k == len(UV) - 1:
            c.append(mults[k - 1])
        else:
            c.append(mults[k - 1] - mults[k] + op)
            
#Generates tikz code for a table-with-margins/BCT
with open("table-with-margins.txt", 'w') as f:
    #Draws empty table with margin vectors
    f.write("%table")
    for j in range(len(c)):
        f.write(("\n\\draw[ultra thin] ({},0)--({},0) " +
                "node[pos=0.5,above](c{}){{{}}}; ").format(
                        j, j + 1, j + 1, c[j]))
        f.write("\\draw[ultra thin] ({},0)--({},{});".format(
                j + 1, j + 1, -len(r)))
        
        #Labels c with U_{j}
        if UV_labels:
            f.write(" \\node[above,yshift=7] at (c{}) {{$U_{{{}}}$}};".format(
                    j + 1, j + 1))
            
    for i in range(len(r)):
        f.write(("\n\\draw[ultra thin] (0,{})--(0,{}) " +
                "node[pos=0.5,left](r{}){{{}}}; ").format(
                        -i, -i - 1, i + 1, r[i]))
        f.write("\\draw[ultra thin] (0,{})--({},{});".format(
                -i - 1, len(c), -i - 1))
        
        #Labels r with V_{i}
        if UV_labels:
            f.write(" \\node[left,xshift=-7] at (r{}) {{$V_{{{}}}$}};".format(
                    i + 1, i + 1))
        
    #Draws separating line
    f.write("\n\n%separating line")
    f.write("\n\\draw[ultra thick] (0,0)")
    for bn in UV:
        if bn[0] == 'V':
            f.write("-- ++(0,-1)")
        else:
            f.write("-- ++(1,0)")
    f.write(";")
    
    #Fills BCT entries if include_ties = True
    if include_ties:
        f.write("\n\n%BCT")
        for i in range(len(r)):
            f.write("\n")
            V = UV.index("V{}".format(i + 1)) + 1
            for j in range(len(c)):
                U = UV.index("U{}".format(j + 1)) + 1
                
                if [U, V] in ties or [V, U] in ties:
                    joined = 1
                else:
                    joined = 0
                
                if U > V:
                    f.write("\\node[violet] at ({},{}) {{{}}}; ".format(
                            j + 0.5, -i - 0.5, joined))
                else:
                    f.write("\\node[violet] at ({},{}) {{{}}}; ".format(
                            j + 0.5, -i - 0.5, 1 - joined))
                    
#Creates dimension vectors for each butterfly
butterflies = [[0] * len(mults) for i in range(len(c))]
for tie in ties:
    if UV[tie[0] - 1][0] == 'U':
        U = tie[0] - 1
        V = tie[1] - 1
    else:
        V = tie[0] - 1
        U = tie[1] - 1
    
    bt = butterflies[int(UV[U][1]) - 1]
    
    if U < V:
        for i in range(U, V):
            bt[i] += 1
    else:
        for i in range(V, U):
            bt[i] += 1

#Generates tikz code for a butterfly diagram
with open("butterflies.txt", 'w') as f:
    ymin = 0
    #Draws the butterfly corresponding to the jth D5 brane
    for j in range(len(butterflies)):
        if j > 0:
            f.write("\n\n")
        f.write("%U{} butterfly".format(j + 1))
        f.write("\n\\node () at (0,0) {};")
        f.write("\n\n%dots")
        
        center = UV.index("U{}".format(j + 1))
        
        if center == 0:
            rldif = butterflies[j][center]
        elif center == len(mults):
            rldif = -1 * butterflies[j][center - 1]
        else:
            rldif = butterflies[j][center] - butterflies[j][center - 1]
            
        if rldif > 0:
            ybase = ymin - 6 - 3 * rldif
        else:
            ybase = ymin - 6
        
        #Draws open dot below D5 brane
        f.write(("\n\\draw ({},{}) circle[radius=0.14] " +
                "node(u{}){{}};").format(3 * center, ymin - 3, j + 1))
        ymin -= 3
        
        #Draws closed dots below the ith D3 brane
        for i in range(len(mults)):
            if i < center:
                yshift = -3 * len([k for k in range(i + 1, center) 
                                    if UV[k][0] == 'V'])
            else:
                yshift = 3 * rldif
                
            for k in range(butterflies[j][i]):
                f.write(("\n\\draw[fill] ({},{}) " +
                        "circle[radius=0.07] node(u{}a{}a{}){{}}; ").format(
                                3 * i + 1.5, ybase + yshift - 3 * k, 
                                j + 1, i + 1, k + 1))
                ymin = min(ymin, ybase + yshift - 3 * k)
                
        #Draws a, b arrows
        f.write("\n\n%arrows")
        if rldif > 0:
            f.write(("\n\\draw[->,green] (u{}a{}a{}) " +
                    "to[out=120,in=-70] (u{}); ").format(
                            j + 1, center + 1, rldif, j + 1))
        if center > 0 and butterflies[j][center - 1] > 0:
            f.write(("\n\\draw[->, green] (u{}) to[out=-120,in=70] " +
                    "(u{}a{}a1);").format(
                    j + 1, j + 1, center))
            
        #Draw A, C, D arrows
        for i in range(1, len(UV) - 1):
            if UV[i][0] == 'U':
                rldif = butterflies[j][i] - butterflies[j][i - 1]
                r = min(butterflies[j][i], butterflies[j][i - 1])
                #A arrows
                for k in range(r):
                    f.write(("\n\draw[->, blue] (u{}a{}a{})--" +
                            "(u{}a{}a{});").format(
                            j + 1, i + 1, 
                            butterflies[j][i] - k, j + 1, 
                            i, butterflies[j][i - 1] - k))
            else:
                if i < center:
                    #C arrows
                    for k in range(butterflies[j][i - 1]):
                        f.write(("\n\\draw[->,dotted,magenta] (u{}a{}a{})--" +
                                "(u{}a{}a{});").format(
                                        j + 1, i + 1, k + 1, j + 1, i, k + 1))
                    #D arrows
                    for k in range(1, butterflies[j][i]):
                        f.write(("\n\\draw[->,red] (u{}a{}a{})--" +
                                "(u{}a{}a{});").format(
                                        j + 1, i, k, j + 1, i + 1, k + 1))
                else:
                    #C arrows
                    for k in range(1, butterflies[j][i - 1]):
                        f.write(("\n\\draw[->,dotted,magenta] (u{}a{}a{})--" +
                                "(u{}a{}a{});").format(
                                        j + 1, i + 1, k, j + 1, i, k + 1))
                    #D arrows
                    for k in range(butterflies[j][i]):
                        f.write(("\n\\draw[->,red] (u{}a{}a{})--" +
                                "(u{}a{}a{});").format(
                                        j + 1, i, k + 1, j + 1, i + 1, k + 1))
        #Draw B arrows
        for i in range(len(mults)):
            if UV[i][0] == 'U' or UV[i + 1][0] == 'U':
                for k in range(1, butterflies[j][i]):
                    f.write("\n\\draw[->] (u{}a{}a{})--(u{}a{}a{});".format(
                            j + 1, i + 1, k, j + 1, i + 1, k + 1))
            