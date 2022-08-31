import numpy as np
import random
import torchvision.datasets as datasets
import matplotlib.pyplot as plt

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other.x == self.x and other.y==self.y:
            return True
        return False

    def __str__(self):
        return "x="+str(self.x) + ",y=" + str(self.y)

    def __hash__(self):
        return hash(str(self))


def get_backward_dir(dir):
    bdir = Point(0,0)
    if dir.x!=0:
        bdir.x=-dir.x
    if dir.y!=0:
        bdir.y=-dir.y
    return bdir

def get_train_test_contrast_BIN(class_num):
    train_pics, test_pics, contrast = get_train_test_contrast(class_num)
    for i in range(len(train_pics)):
        train_pics[i]=binarise_img(train_pics[i])
    for i in range(len(test_pics)):
        test_pics[i]=binarise_img(test_pics[i])
    for i in range(len(contrast)):
        contrast[i]=binarise_img(contrast[i])
    return train_pics, test_pics, contrast


def get_train_test_contrast(class_num):
    ominset = datasets.Omniglot(root='./data_om', download=True, transform=None)
    res = []
    for i in range(len(ominset)):
        if class_num == ominset[i][1]:
            res.append(ominset[i][0])
    contrast = []
    for i in range(20):
        if class_num != ominset[i][1]:
            contrast.append(ominset[i][0])
    return res[:10], res[11:], contrast


def get_coords_for_radius(center, radius):
    #|x|+|y|=radius ->  |y|=radius-|x|
    # x>0  -> y1 = radius-|x|
    if radius == 0:
        return [Point(center.x, center.y)]

    points = []
    for modx in range(0, radius+1):
        mody = radius - modx
        # x>0
        if modx != 0 and mody != 0:
            points.append(Point(modx + center.x, mody + center.y))
            points.append(Point(-modx + center.x, mody + center.y))
            points.append(Point(modx + center.x, -mody + center.y))
            points.append(Point(-modx + center.x, -mody + center.y))

        if modx == 0 and mody != 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(modx + center.x, -mody + center.y))

        if modx != 0 and mody == 0:
            points.append(Point(modx+center.x, mody+center.y))
            points.append(Point(-modx + center.x, mody + center.y))
    return points


def get_coords_less_or_eq_raduis(center, radius):
    points = []
    for r in range(0, radius+1):
        r_points = get_coords_for_radius(center.x, center.y, r)
        points = points + r_points
    return points

def binarise_img(pic):
    pic = np.array(pic)
    new_img=np.zeros(pic.shape)
    for x in range(pic.shape[1]):
        for y in range(pic.shape[0]):
            if pic[y,x]==0:
                new_img[y,x]=1
    return new_img

def sense_1(point, picture):
    xlen = picture.shape[1]
    ylen = picture.shape[0]
    if point.x >= 0 and point.y >= 0 and point.x < xlen and point.y < ylen:
        val = picture[point.y, point.x]
        if val > 0:
            return True
    return False


def find_nearest_1(start_point, binary_img, max_rad):
    for r in range(1, max_rad):
        r_points = get_coords_for_radius(start_point, r)
        for point in r_points:
            if sense_1(picture=binary_img, point=point):
                return point
    return None

def find_nearest_1_with_exclusions(start_point, binary_img, max_rad, exclusions):
    for r in range(0, int(max_rad)):
        r_points = get_coords_for_radius(start_point, r)
        for point in r_points:
            if sense_1(picture=binary_img, point=point):
                if is_allowed_by_exclusions(start_point, point, exclusions):
                    return point
    return None

def is_allowed_by_exclusions(prev_point, candidate_point,  exclusions):
    dist = my_dist(prev_point, candidate_point)
    for exclusion in exclusions:
        if my_dist(exclusion, candidate_point) < dist:
            return False
    return True

def my_dist(point1, point2):
    dx = abs(point1.x - point2.x)
    dy = abs(point1.y - point2.y)
    return dx+dy


def get_mean_u(points_list):
    n = len(points_list)
    dx = 0
    dy = 0
    prev_point = points_list[0]
    for i in range(1, len(points_list)):
        dx += abs(points_list[i].x - prev_point.x)
        dy += abs(points_list[i].y - prev_point.y)
        prev_point = points_list[i]

    return Point(x=dx/n, y=dy/n)

def get_all_1_points(img):
    all_1_points=[]
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            point = Point(x,y)
            if sense_1(point, img):
                all_1_points.append(point)
    return all_1_points


class IdGen:
    def __init__(self):
        self.i = -1

    def generate_id(self):
        self.i += 1
        return self.i

def get_cmap(n):
    colormap_name = 'gist_rainbow'
    return plt.cm.get_cmap(colormap_name, n)

def remove_points_from_list(points_list, points_to_remove):
    for point in points_to_remove:
        if point in points_list:
            points_list.remove(point)

def get_random_point(max_x=105, max_y=105):
    point = Point(random.randrange(max_x), random.randrange(max_y))
    return point

def visualise_sample(sample, n_bins):
    fig, ax = plt.subplots()

    ax.hist(sample, edgecolor="black", bins=n_bins,
            weights=np.ones_like(sample) / len(sample))
    return fig