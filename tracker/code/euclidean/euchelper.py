"""
Eucledian helper classes
"""
import math
from shapely.geometry import LineString
import numpy

__version__ = '0.2'


def interpolate_line(the_pt1, the_pt2, proportion):
    """Interplolate a line between two points the_pt1 and the_pt2
    with the given proportion

    Arguments:
        the_pt1 {list} -- the first point (x,y)
        the_pt2 {list} -- the second point (x,y)
        proportion {float} -- proportion on where to divide the line between
            the two given points

    Returns:
        list -- the interpolated point (x,y)
    """
    line = LineString([the_pt1, the_pt2])
    projected_pt = line.interpolate(proportion, normalized=True)
    the_pt = list(projected_pt.coords)[0]
    return the_pt


def get_angle(var_x1, var_y1, var_x2, var_y2):
    """
    Get the angle between two points defined by
    (var_x1, var_y1) and (var_x2, var_y2)

    Arguments:
        var_x1 {float} -- X-value for the first point
        var_y1 {float} -- Y-value for the first point
        var_x2 {float} -- X-value for the second point
        var_y2 {float} -- Y-value for the second point

    Returns:
        float -- angle in radians
    """
    x_diff = var_x2 - var_x1
    y_diff = var_y2 - var_y1
    return math.atan2(y_diff, x_diff)
    # return math.degrees(math.atan2(1,1))


def densify_line(line, hypotenuse):
    """
    Densify a line ("line")

    Arguments:
        line {[type]} -- [description]
        hypotenuse {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    x1_temp = line[0][0]
    y1_temp = line[0][1]

    x2_temp = line[1][0]
    y2_temp = line[1][1]

    # Flag to keep track if reorder was needed
    flipped = False

    # Reorder so that x1 is smaller than x2
    if x2_temp > x1_temp:
        var_x1 = x1_temp
        var_y1 = y1_temp
        var_x2 = x2_temp
        var_y2 = y2_temp
    else:
        flipped = True
        var_x1 = x2_temp
        var_y1 = y2_temp
        var_x2 = x1_temp
        var_y2 = y1_temp

    # Get total distance to evaluate number of needed points
    dist_euc = math.sqrt(pow((var_x2-var_x1), 2) + pow((var_y2-var_y1), 2))

    # Get the angle of the line
    angle_radians = get_angle(var_x1, var_y1, var_x2, var_y2)
    # print(angle_radians)

    # Calculate number of needed internal points, allowing any remainder
    internal_points = int(int(dist_euc)/hypotenuse)

    # Calculate the needed x values
    x_out = [var_x1]
    for a_pt in range(internal_points):
        adj = hypotenuse*math.cos(angle_radians)
        next_x = x_out[a_pt] + adj
        x_out.append(next_x)

    xp_pt = [var_x1, var_x2]
    fp_pt = [var_y1, var_y2]

    y_out = numpy.interp(x_out, xp_pt, fp_pt)

    dense_line = [[var_x1, var_y1]]
    for a_pt in range(0, len(x_out)):
        dense_line.append([x_out[a_pt], y_out[a_pt]])
    dense_line.append([var_x2, var_y2])

    if flipped:
        dense_line.reverse()

    return dense_line


def densify_graph(currentgraph):
    """
    Densify the entire graph given by lines "currentgraph"

    Arguments:
        currentgraph {list} -- list of lines that make the current graph

    Returns:
        list -- graph with dense lines
    """
    dense_graph = []
    for line in currentgraph:
        retval = densify_line(line, 3)
        dense_graph.append(retval)

    # To retun linestrings:
    # return dense_graph

    # This logic returns a list of lines (as opposed to LineString)
    dense_lines = []
    xcoords = []
    ycoords = []
    counter = 0  # track the nunber of processed points
    #print_me = False
    for line in dense_graph:
        # if print_me:
            # print(line)
            #print_me = False
        for index in range(0, len(line)-1):
            dense_lines.append([line[index], line[index+1]])
            #print([[xcoords[a-2], ycoords[a-2]], [xcoords[a-1], ycoords[a-1]]])
        for pair_list in line:
            xcoords.append(pair_list[0])
            ycoords.append(pair_list[1])
            counter = counter + 1

    # To plot dense graph:
    # matplt.scatter(xcoords, ycoords)
    # matplt.show()

    return dense_lines


"""
def show_graph(line):
    start = line[0]
    end = line[1]
    #plt.plot([start[0], end[0]], [start[1], end[1]], marker='o')
import matplotlib.pyplot as matplt
from plotly.offline import plot as plt
import plotly.graph_objs as go

if __name__ == "__main__":

    MAP_INFO = [[[66.0344590285891, -63.48220934645117], [46.07790900092577, -64.08156945130689]], [[46.12230615012415, -64.10376797403059], [45.678416853428, -33.869326762056865]], [[45.678416853428, -33.869326762056865], [31.515680787296677, -33.425354708072064]], [[31.515680787296677, -33.425354708072064], [7.230354148079207, -47.18847737292561]], [[46.25539949343339, -99.53253310533859], [34.62339650474682, -79.1543520103725]], [[57.132715224669816, -93.27257427808415], [45.45632421686229, -72.80558388660869]], [[45.45632421686229, -72.80558388660869], [46.12230615012415, -64.10376797403059]], [[34.62339650474682, -79.1543520103725], [24.41205511862601, -73.29395083704388]], [[24.41205511862601, -73.29395083704388], [14.378274730745598, -91.36350788689167]], [[14.378274730745598, -91.36350788689167], [31.426759233047893, -100.77564493668787]], [[-30.063310907253317, -65.16929694239731], [14.378274730745598, -91.36350788689167]], [[-20.562328228556233, -48.56478839106634], [-30.063310907253317, -65.16929694239731]], [[7.230354148079207, -47.18847737292561], [0.30438151435004135, -60.68519495035692]], [[0.30438151435004135, -60.68519495035692], [24.41205511862601, -73.29395083704388]], [[0.30438151435004135, -60.68519495035692], [-20.562328228556233, -48.56478839106634]], [[-106.56005199661799, -10.960337923569973], [-84.76095140363817, -10.782748616754311]], [[-20.562328228556233, -48.56478839106634], [-10.706148256353908, -31.915849552730275]], [[-10.706148256353908, -31.915849552730275], [-23.093004799075565, -24.723497683491285]], [[-10.706148256353908, -31.915849552730275], [-7.775925796617749, -33.38095750235778]], [[-23.093004799075565, -24.723497683491285], [-23.093014271364403, -17.8863179343125]], [[-23.093014271364403, -17.8863179343125], [-23.359436303380253, 9.240469973785062]], [[-23.359436303380253, 9.240469973785062], [-23.226253168375354, 15.766895297512445]], [[-23.226253168375354, 15.766895297512445], [-20.162833043806085, 17.675986663492594]], [[-20.162833043806085, 17.675986663492594], [-29.841502549761728, 34.10306997864154]], [[-20.162833043806085, 17.675986663492594], [-7.731555330848931, 24.468803676174705]], [[-7.731555330848931, 24.468803676174705], [27.164807394637016, 4.356753687299412]], [[27.164807394637016, 4.356753687299412], [27.29799435025442, 1.1601409397599127]], [[27.29799435025442, 1.1601409397599127], [27.031586626241623, -13.268998567955096]], [[27.031586626241623, -13.268998567955096], [-7.775925796617749, -33.38095750235778]], [[27.29799435025442, 1.1601409397599127], [46.25567839094765, 0.9825513787278498]], [[45.678416853428, -33.869326762056865], [46.25567839094765, 0.9825513787278498]], [[45.678416853428, -33.869326762056865], [65.30202097507986, -33.869326762056865]], [[65.30202097507986, -33.869326762056865], [66.0344590285891, -63.48220934645117]], [[31.615683553668582, 23.9693316549013],
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    [6.79751566262768, 38.13215009450409]], [[6.79751566262768, 38.13215009450409], [-0.7056600538193759, 51.40703938306186]], [[-23.093014271364403, -17.8863179343125], [-42.93862337428302, -18.08610573227219]], [[-42.93862337428302, -18.08610573227219], [-42.84989910990559, 9.307066131706657]], [[-23.359436303380253, 9.240469973785062], [-42.84989910990559, 9.307066131706657]], [[-42.84989910990559, 9.307066131706657], [-50.49739217728566, 22.28222636328307]], [[-106.61563211632681, 2.081386852302735], [-84.86091049927542, 1.9925920619180537]], [[-50.49739217728566, 22.28222636328307], [-73.76159229538278, 8.607806571426913]], [[-73.76159229538278, 8.607806571426913], [-84.86091049927542, 1.9925920619180537]], [[-73.76159229538278, 8.607806571426913], [-83.97308279317478, 25.83402738072967]], [[-84.76095140363817, -10.782748616754311], [-73.89467057496398, -17.09826601291474]], [[-73.89467057496398, -17.09826601291474], [-84.0615725647783, -34.67957570535418]], [[-42.93862337428302, -18.08610573227219], [-50.54162796680935, -31.039004520986662]], [[-50.54162796680935, -31.039004520986662], [-73.89467057496398, -17.09826601291474]], [[-20.562328228556233, -48.56478839106634], [-50.54162796680935, -31.039004520986662]], [[-30.063310907253317, -65.16929694239731], [-84.0615725647783, -34.67957570535418]], [[65.30202097507986, -33.869326762056865], [65.51302360750131, -4.489425116894886]], [[31.615683553668582, 23.9693316549013], [46.0670526653775, 23.836139122737322]], [[46.0670526653775, 23.836139122737322], [46.25567839094765, 0.9825513787278498]], [[46.0670526653775, 23.836139122737322], [65.46873677415381, 23.65854907774671]], [[65.46873677415381, 23.65854907774671], [65.51302360750131, -4.489425116894886]], [[46.37793793549058, 60.90814370354439], [31.549174026231974, 69.74329247731879]], [[46.0670526653775, 23.836139122737322], [46.37793793549058, 60.90814370354439]], [[31.549174026231974, 69.74329247731879], [-0.7056600538193759, 51.40703938306186]], [[-0.7056600538193759, 51.40703938306186], [-29.841502549761728, 34.10306997864154]], [[-29.841502549761728, 34.10306997864154], [-41.1739416665084, 27.43233833118413]], [[-41.1739416665084, 27.43233833118413], [-50.49739217728566, 22.28222636328307]], [[-41.1739416665084, 27.43233833118413], [-50.80824044686119, 43.99263373342263]], [[-50.80824044686119, 43.99263373342263], [-34.46997908057788, 53.31613891791499]], [[-34.46997908057788, 53.31613891791499], [-0.23948637974982787, 73.51710259465942]], [[-0.23948637974982787, 73.51710259465942], [31.593612489429262, 91.32062984681018]], [[31.593612489429262, 91.32062984681018], [65.31353530472302, 72.0519761101299]], [[65.31353530472302, 72.0519761101299], [65.62422938433062, 49.45354264959986]], [[65.62422938433062, 49.45354264959986], [65.46873677415381, 23.65854907774671]], [[-50.80824044686119, 43.99263373342263], [-83.97308279317478, 25.83402738072967]]]

    MAP_INFO_OUTER = [[[46.12230615012415, -64.10376797403059], [45.678416853428, -33.869326762056865]], [[46.25539949343339, -99.53253310533859], [34.62339650474682, -79.1543520103725]], [[57.132715224669816, -93.27257427808415], [45.45632421686229, -72.80558388660869]], [[45.45632421686229, -72.80558388660869], [46.12230615012415, -64.10376797403059]], [[34.62339650474682, -79.1543520103725], [24.41205511862601, -73.29395083704388]], [[0.30438151435004135, -60.68519495035692], [24.41205511862601, -73.29395083704388]], [[0.30438151435004135, -60.68519495035692], [-20.562328228556233, -48.56478839106634]], [[-106.56005199661799, -10.960337923569973], [-84.76095140363817, -10.782748616754311]], [[45.678416853428, -33.869326762056865], [46.25567839094765, 0.9825513787278498]], [[-106.61563211632681, 2.081386852302735], [-84.86091049927542, 1.9925920619180537]], [[-50.49739217728566, 22.28222636328307], [-73.76159229538278, 8.607806571426913]], [[-73.76159229538278, 8.607806571426913], [-84.86091049927542, 1.9925920619180537]],
                      [[-84.76095140363817, -10.782748616754311], [-73.89467057496398, -17.09826601291474]], [[-50.54162796680935, -31.039004520986662], [-73.89467057496398, -17.09826601291474]], [[-20.562328228556233, -48.56478839106634], [-50.54162796680935, -31.039004520986662]], [[46.0670526653775, 23.836139122737322], [46.25567839094765, 0.9825513787278498]], [[46.37793793549058, 60.90814370354439], [31.549174026231974, 69.74329247731879]], [[46.0670526653775, 23.836139122737322], [46.37793793549058, 60.90814370354439]], [[31.549174026231974, 69.74329247731879], [-0.7056600538193759, 51.40703938306186]], [[-0.7056600538193759, 51.40703938306186], [-29.841502549761728, 34.10306997864154]], [[-29.841502549761728, 34.10306997864154], [-41.1739416665084, 27.43233833118413]], [[-41.1739416665084, 27.43233833118413], [-50.49739217728566, 22.28222636328307]], [[57.132790063384036, -93.27900281085198], [46.25768374560957, -99.53360070922044]], [[-106.55825227125126, -10.96081029790715], [-106.61426773974117, 2.077446557298875]]]

    #single_line_map = [[[66.0344590285891, -63.48220934645117], [46.07790900092577, -64.08156945130689]]]
    #double_line_map = [[[66.0344590285891, -63.48220934645117], [46.07790900092577, -64.08156945130689]], [[46.12230615012415, -64.10376797403059], [45.678416853428, -33.869326762056865]]]
    #single_line_map2 = [[[46.12230615012415, -64.10376797403059], [45.678416853428, -33.869326762056865]]]

    dense = densify_graph(MAP_INFO_OUTER)
    for line in dense:
        print(line)
    print(len(dense))

    data = []
    #DENSE = euchelper.densify_graph(reid.MAP_INFO)
    for l in dense:
        data.append(go.Scatter(
            x=[l[i][0] for i in range(len(l))],
            y=[l[i][1] for i in range(len(l))],
            text=str(l),
            mode='lines+markers',
            name="line",
            opacity="0.9",
            marker=dict(
                size=5
            )
        ))
    layout = {'xaxis': {'title': "X",
                        'range': [-110, 110]}, 'yaxis': {'title': "Y", 'range': [-110, 110]}}
    fig_json = {"data": data, "layout": layout}
    plt(fig_json, filename="graph.html")


    xcoords = []
    ycoords = []
    for line in dense:
        for pair_list in line:
            #print(pair_list)
            xcoords.append(pair_list[0])
            ycoords.append(pair_list[1])

    #plt.scatter(xcoords, ycoords)
    #plt.show()

"""