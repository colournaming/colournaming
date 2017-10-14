"""Controller for the colournaming system."""

import csv
import glob
import logging
import math
import numpy as np
import os
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound
from ..database import db
from .model import ColourCentroid, Language


class ColourNamer():
    """Use colour centroid data to find nearest perceptual neighbours of colours."""

    def __init__(self, language_code):
        self.data = self.load_data(language_code)

    @staticmethod
    def load_data(language_code):
        """Load colour centroid data from the database."""
        lang = Language.query.filter(Language.code == language_code).one()
        centroids = ColourCentroid.query.filter(ColourCentroid.language == lang).all()
        data = []
        for c in centroids:
            mu = np.array([c.m_L, c.m_a, c.m_b])
            sigma = np.array([[c.sigma_1, c.sigma_2, c.sigma_3],
                              [c.sigma_4, c.sigma_5, c.sigma_6],
                              [c.sigma_7, c.sigma_8, c.sigma_9]])
            hex_code = '{0:2x}{1:2x}{2:2x}'.format(int(c.m_R), int(c.m_G), int(c.m_B))
            data.append({
                'colour_name': c.color_name,
                'r': c.m_R,
                'g': c.m_G,
                'b': c.m_B,
                'sigma': sigma,
                'mu': mu,
                'hex': hex_code,
                'den': c.den,
                'prob': c.prob
            })
        return data

    @staticmethod
    def mvnpdf(x, mu, sigma):
        """Calculate a probability distribution function."""
        det = np.linalg.det(sigma)
        k = np.size(x)
        f = pow(2.0 * math.pi, -0.5 * k) * pow(det, -0.5)
        p = np.dot(-0.5 * np.transpose(x - mu), np.dot(np.linalg.inv(sigma), (x - mu)))
        return f * np.exp(p)

    @staticmethod
    def srgb2xyz(rgb):
        """Convert SRGB to 3D colour space."""
        M = np.array([[0.4124, 0.3576, 0.1805],
                      [0.2126, 0.7152, 0.0722],
                      [0.0193, 0.1192, 0.9505]])
        sr = ColourNamer.scale_component(rgb[0])
        sg = ColourNamer.scale_component(rgb[1])
        sb = ColourNamer.scale_component(rgb[2])
        sRGB = [sr, sg, sb]
        return np.transpose(np.dot(M, np.transpose(sRGB))) * 100

    @staticmethod
    def scale_component(c):
        """Scale a colour component."""
        sC = c / 255.0
        sc = pow((sC + 0.055) / 1.055, 2.4)
        if sC <= 0.03928:
            sc = sC / 12.92
        return sc

    @staticmethod
    def xyz2lab(xyz, rwhite):
        """Convert 3D colour space coordinate to LAB."""
        x, y, z = xyz
        xn, yn, zn = rwhite
        xrel = x / xn
        yrel = y / yn
        zrel = z / zn
        fx = pow(xrel, 0.33333333)
        fy = pow(yrel, 0.33333333)
        fz = pow(zrel, 0.33333333)
        if xrel <= 0.008856:
            fx = 7.787 * xrel + 0.137931034
        if yrel <= 0.008856:
            fy = 7.787 * yrel + 0.137931034
        if zrel <= 0.008856:
            fz = 7.787 * zrel + 0.137931034
        L = 116.0 * fy - 16.0
        if yrel <= 0.008856:
            L = 903.3 * yrel
        a = (fx - fy) * 500.0
        b = (fy - fz) * 200.0
        return np.array([L, a, b])

    @staticmethod
    def euclidean_distance(a, b):
        """Calculate the euclidean distance between two points."""
        return pow(pow(a[1] - b[1], 2) + pow(a[2] - b[2], 2), 0.5)

    @staticmethod
    def calculate_angle(a, b):
        """Calculate the angle between two points."""
        r = (b[1] - a[1]) / (b[2] - a[2])
        if math.isnan(r):
            r = 0.0
        return r

    def colour_name(self, rgb):
        """Get nearest colours for to an RGB colour."""
        rgb = np.array(rgb)
        testlab = self.xyz2lab(self.srgb2xyz(rgb), [95.04, 100.0, 108.89])
        for i in range(len(self.data)):
            c = self.data[i]
            if c['den'] > 1.0e-15:
                cond_prob = self.mvnpdf(testlab, c['mu'], c['sigma']) / c['den']
            else:
                cond_prob = 0.0
            if math.isnan(cond_prob):
                cond_prob = 0.0
            self.data[i]['posteriori'] = c['prob'] * cond_prob
        self.data = sorted(self.data, key=lambda c: c['posteriori'], reverse=True)
        names = []
        for i in range(4):
            d = self.euclidean_distance(self.data[0]['mu'], self.data[i]['mu'])
            if math.isnan(self.data[i]['posteriori']):
                self.data[i]['posteriori'] = 0.0
            names.append({
                'name': self.data[i]['colour_name'],
                'a': self.data[i]['mu'][1],
                'b': self.data[i]['mu'][2],
                'd': d,
                'likelihood': self.data[i]['posteriori'],
                'red': self.data[i]['r'],
                'green': self.data[i]['g'],
                'blue': self.data[i]['b']
            })
        return names


def language_list():
    """Get a list of all known languages."""
    languages = Language.query.all()
    return [{'name': l.name, 'code': l.code} for l in languages]


def colour_list(language):
    """Get a list of all known colours in a given language."""
    colours = ColourCentroid.query.filter(ColourCentroid.language == language).all()
    colour_list = []
    for c in colours:
        cdict = {
            'name': c.color_name.replace('_', ' ').capitalize(),
            'code': c.color_name,
            'hex': _hex_code_for_colour(c)
        }
        colour_list.append(cdict)
    return colour_list


def _hex_code_for_colour(colour):
    """Return the hex code for a given colour centroid."""
    h = hex(int(colour.m_R))[2:]
    h += hex(int(colour.m_G))[2:]
    h += hex(int(colour.m_B))[2:]
    return h


def audio_list(lang):
    """Return a list of available audio files."""
    print(os.getcwd())
    path = os.path.join(current_app.static_folder, 'audio', lang)
    if os.path.exists(path):
        return [os.path.split(x)[-1] for x in glob.glob(path + '/*.wav')]



def instantiate_namers():
    """Create instances of ColourNamer for each known language."""
    namers = {}
    for lang in language_list():
        lang_code = lang['code']
        namers[lang_code] = ColourNamer(lang_code)
        logging.info('namer created for %s', lang_code)
    return namers


def read_centroids_from_file(f, language_name, language_code):
    """Import colour centroids from a file to the database."""
    col_csv = csv.DictReader(f)
    try:
        lang = Language.query.filter(Language.code == language_code).one()
    except NoResultFound:
        lang = Language(name=language_name, code=language_code)
        db.session.add(lang)
        db.session.commit()
    for r in col_csv:
        r['language'] = lang
        if 'exp' in r:
            del r['exp']
        c = ColourCentroid(**r)
        db.session.add(c)
    db.session.commit()
    current_app.namers[language_code] = ColourNamer(language_code)
