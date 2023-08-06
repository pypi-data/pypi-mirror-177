# afhankelijke externe bibliotheken
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


###############################################################################


import pyco.basis
BasisObject = pyco.basis.BasisObject

import pyco.waarde
Waarde = pyco.waarde.Waarde

import pyco.vector
Vector = pyco.vector.Vector

import pyco.knoop
Knoop = pyco.knoop.Knoop

import pyco.lijn
Lijn = pyco.lijn.Lijn

import pyco.vorm
Vorm = pyco.vorm.Vorm

if True:
    import pyco.rechthoek
    Rechthoek = pyco.rechthoek.Rechthoek

    import pyco.cirkel
    Cirkel = pyco.cirkel.Cirkel

import pyco.materiaal
Materiaal = pyco.materiaal.Materiaal


###############################################################################


def functies_print_help():
    print("""
    
+-------------------------------------------+
|  algemene pyco functies en eigenschappen  |
+-------------------------------------------+

ALGEMEEN GEBRUIK VAN FUNCTIES         alle namen met () erachter zijn functies
    pc.wortel(9) == 3.0               direct aan te roepen vanuit pc object
    
ALGEMEEN GEBRUIK VAN EIGENSCHAPPEN
    pc.pi == 3.141592653589793        direct aan te roepen vanuit pc object

WISKUNDIGE FUNCTIES                   (gebaseerd op Numpy module)
    invoerwaarden:  int, float, np.array, Waarde of Vector
    uitvoerwaarden: indien invoer Waarde/Vector, uitvoer ook Waarde/Vector met
                    ALTIJD zelfde eenheid als invoer; ook als niet correct is!!
    sin(x)                            sinus
    cos(x)                            cosinus
    tan(x)                            tangens
    asin(x)                           arcsinus (omgekeerde sin)
    acos(x)                           arccosinus (omgekeerde cos)
    atan(x)                           arctangens (omgekeerde tan)
    hypot(a, b)                       hypotenuse (c in: a^2 + b^c = c^2)
    graden(rad)                       van radialen naar graden
    radialen(deg)                     van graden naar radialen
    sinh(x)                           hyperbolische sinus
    cosh(x)                           hyperbolische cosinus
    tanh(x)                           hyperbolische tangens
    asinh(x)                          arc hyperb. sinus (omgekeerde sinh)
    acosh(x)                          arc hyperb. cosinus (omgekeerde cosh)
    atanh(x)                          arc hyperb. tangens (omgekeerde tanh)
    afronden(x, n)                    rond af op n decimalen (standaard 0)
    plafond(x)                        rond af naar boven (geheel getal)
    vloer(x)                          rond af naar beneden (geheel getal)
    plafond_0_vloer(x)                rond af richting 0 (geheel getal)
    som(lijst)                        de som van de elementen
    product(lijst)                    het product van de elementen
    verschil(lijst)                   lijst met verschillen tussen elementen
    optellen(a, b)                    a + b
    aftrekken(a, b)                   a - b
    vermenigvuldigen(a, b)            a * b
    delen(a, b)                       a / b
    delen_aantal(a, b)                a // b -> afgerond naar beneden
    delen_rest(a, b)                  a % b -> restant na afronden naar beneden
    macht(a, b)                       a ** b 
    reciproke(x)                      1 / x
    negatief(x)                       -x
    kruisproduct(a, b)                a x b: staat loodrecht op vector a en b
    inwendigproduct(a, b)             a . b: is |a| * |b| * cos(theta)
    exp(x)                            exponentieel: berekent e^x
    ln(x)                             natuurlijke logaritme (grondgetal e)
    log(x)                            logaritme met grondgetal 10
    kgv(a, b)                         kleinste gemene veelvoud: a=12 b=20: 60
    ggd(a, b)                         grootste gemene deler: a=12 b=20: 4
    min(lijst)                        bepaalt minimum waarde lijst
    max(lijst)                        bepaalt maximum waarde lijst
    bijsnijden(lijst, min, max)       snij alle elementen af tot minmax bereik
    wortel(x)                         vierkantswortel
    wortel3(x)                        kubieke wortel
    abs(x)                            absolute waarde (altijd positief)
    teken(x)                          positief getal: 1.0   negatief: -1.0 
    kopieer_teken(a, b)               neem getal a, met het teken (+-) van b
    is_positief(a, b)                 stap functie:a<0 -> 0, a=0 -> b, a>0 -> 1 
    verwijder_nan(lijst)              verwijder niet-getallen (not a number)
    vervang_nan(lijst)                vervang: nan=0, inf=1.7e+308 (heel groot)
    interp(x, lijst_x, lijst_y)       interpoleer x in y; lijst_x MOET oplopen
    van_totmet_n(van, tot_met, n)     genereert vast aantal getallen (incl. tot)
    van_tot_stap(van, tot, stap)      genereert vaste stappen (excl. tot)
    gemiddelde(lijst)                 bepaalt het gemiddelde
    stdafw_pop(lijst)                 bepaalt standaardafwijking voor populatie
    stdafw_n(lijst)                   bepaalt standaardafwijking voor steekproef
    mediaan(lijst)                    bepaalt de mediaan
    percentiel(lijst, percentage)     percentage getal tussen 0 en 100
    correlatie(lijst_a, lijst_b)      bepaalt correlatie matrix
    sorteer(lijst)                    sorteert een lijst van klein naar groot
    omdraaien(lijst)                  draai de volgorde van de lijst om
    alsdan(voorwaarde, als, dan)      bewerk lijst met voorwaarde per item
    is_nan(x)                         bepaalt of waarde een niet-getal is
    is_inf(x)                         bepaalt of waarde oneindig is
    gelijk(lijst_a, lijst_b)          per element kijken of waarden gelijk zijn
    groter(lijst_a, lijst_b)          per element kijken of waarde groter dan
    groter_gelijk(lijst_a, lijst_b)   idem, maar dan ook gelijk
    kleiner(lijst_a, lijst_b)         per element kijken of waarde kleiner dan
    kleiner_gelijk(lijst_a, lijst_b)  idem, maar dan ook gelijk
    alle(lijst)                       kijkt of alle elementen True zijn
    sommige(lijst)                    kijkt of er minimaal 1 element True is
    niet_alle(lijst)                  kijkt of er minimaal 1 element False is
    geen(lijst)                       kijkt of alle elementen False zijn
    of(a, b)                          kijkt of a of b True is
    en(a, b)                          kijkt of a en b True is
    niet(x)                           omdraaien van True naar False en andersom
    xof(a, b)                         True als a of b True is, en niet beide
    
WISKUNDIGE EIGENSCHAPPEN              (gebaseerd op Numpy module)
    nan                               float die geen getal is (not a number)
    inf                               oneindig groot
    pi                                3.141592653589793
    e                                 2.718281828459045

    """.strip())
    
    
###############################################################################

# eigenschappen

nan = np.nan
inf = np.inf
pi = np.pi
e = np.e

    
###############################################################################
    
# functies

_numpy_functions = dict(
    sin = np.sin,
    cos = np.cos,
    tan = np.tan,
    asin = np.arcsin,
    acos = np.arccos,
    atan = np.arctan,
    hypot = np.hypot, 
    graden = np.degrees,
    radialen = np.radians,
    sinh = np.sinh,
    cosh = np.cosh,
    tanh = np.tanh,
    asinh = np.arcsinh,
    acosh = np.arccosh,
    atanh = np.arctanh,
    afronden = np.round,
    plafond = np.ceil,
    vloer = np.floor,
    plafond_0_vloer = np.fix,
    som = np.sum,
    product = np.prod,
    verschil = np.diff,
    optellen = np.add,
    aftrekken = np.subtract,
    vermenigvuldigen = np.multiply,
    delen = np.divide,
    delen_aantal = np.floor_divide,
    delen_rest = np.remainder,
    macht = np.power,
    reciproke = np.reciprocal,
    negatief = np.negative,
    kruisproduct = np.cross,
    inwendigproduct = np.dot,
    exp = np.exp,
    ln = np.log,
    log = np.log10,
    kgv = np.lcm,
    ggd = np.gcd,
    bijsnijden = np.clip,
    wortel = np.sqrt,
    wortel3 = np.cbrt,
    teken = np.sign,
    kopieer_teken = np.copysign,
    is_positief = np.heaviside,
    vervang_nan = np.nan_to_num,
    verwijder_nan = lambda x: x[np.logical_not(np.isnan(x))],
    interp = np.interp,
    van_totmet_n = np.linspace,
    van_tot_stap = np.arange,
    gemiddelde = np.mean,
    stdafw_pop = lambda x: np.std(x, ddof=0),
    stdafw_n = lambda x: np.std(x, ddof=1),
    mediaan = np.median,
    percentiel = np.percentile,
    correlatie = np.corrcoef,
    sorteer = np.sort,
    omdraaien = np.flip,
    alsdan = np.where,
    is_nan = np.isnan,
    is_inf = np.isinf,
    gelijk = np.equal,
    groter = np.greater,
    groter_gelijk = np.greater_equal,
    kleiner = np.less,
    kleiner_gelijk = np.less_equal,
    alle = np.all,
    sommige = np.any,
    niet_alle = lambda x: ~np.all(x),
    geen = lambda x: ~np.any(x),
    of = np.logical_or,
    en = np.logical_and,
    niet = np.logical_not,
    xof = np.logical_xor,
)
_numpy_functions['min'] = np.amin # reserverd keywords
_numpy_functions['max'] = np.amax
_numpy_functions['abs'] = np.fabs

def _wrap_function(fn):
    def return_fn(*args, **kwargs):
        # pre
        eenheid = None
        waarde = False
        new_args = []
        for arg in args:
            if isinstance(arg, Waarde):
                waarde = True
                eenheid = arg.eenheid if eenheid is None else eenheid
                new_args.append(float(arg))
            elif isinstance(arg, Vector):
                eenheid = arg.eenheid if eenheid is None else eenheid
                new_args.append(arg.array)
            else:
                new_args.append(arg)
            
        # call
        value = fn(*new_args, **kwargs)
        
        # post
        if isinstance(value, type(np.array([]))):
            v = Vector(np.array(value, dtype='float64'))
            if eenheid is not None:
                v.eenheid = eenheid
            return v
        elif waarde or eenheid:
            w = Waarde(value)
            if eenheid is not None:
                w.eenheid = eenheid
            return w
        return value
    return return_fn

for fn_name, fn in _numpy_functions.items():
    setattr(pyco, fn_name, _wrap_function(fn))

    
###############################################################################
    
