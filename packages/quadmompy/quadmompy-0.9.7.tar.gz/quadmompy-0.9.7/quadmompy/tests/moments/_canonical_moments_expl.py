"""
Verified explicit formulas for the conversion between ordinary and canonical
moments (syntax due to origin from C-implementation). It is presumed that the
ordinary moments correspond to a measure with support [0,1].

"""
import numpy as np


def ordinary_to_canonical(moments): # pylint:disable=too-many-statements,too-many-locals
    """
    Verified explicit formulas for the conversion of up to seven ordinary
    moments to canonical moments.

    """

    if len(moments) > 7:
        raise NotImplementedError(
            "Canonical moment transformation is only implemented up to sixth order"
        )

    p = np.zeros(len(moments))

    p[0] = moments[0]

    p[1] = moments[1]/moments[0]

    c0 = moments[0]
    c1 = moments[1]
    c2 = moments[2]
    p[2]  = (c0 - c1)
    p[2] *= c1
    p[2]  = 1./p[2]
    p[2] *= (c0*c2 - (c1*c1))

    if len(moments) < 4:
        return p

    c3 = moments[3]

    p[3]  = (c0*c2 - (c1*c1))
    p[3] *= (c1 - c2)
    p[3]  = 1./p[3]
    p[3] *= (c1*c3 - (c2*c2))
    p[3] *= (c0 - c1)

    if len(moments) < 5:
        return p

    c4 = moments[4]
    pow_c1_2 = c1 * c1
    pow_c2_2 = c2 * c2

    p[4]  = c0*c2
    p[4] += -c0*c3
    p[4] += -pow_c1_2
    p[4] += c1*c2
    p[4] += c1*c3
    p[4] += -pow_c2_2
    p[4] *= (c1*c3 - pow_c2_2 )
    p[4]  = 1./p[4]
    p[4] *= (c0*c2*c4 - c0*(c3*c3) - pow_c1_2 *c4 + 2.*c1*c2*c3 - pow(c2, 3))
    p[4] *= (c1 - c2)

    if len(moments) < 6:
        return p

    c5 = moments[5]
    pow_c1_2 = c1 * c1
    pow_c2_2 = c2 * c2
    pow_c3_2 = c3 * c3

    p[5]  = c0*c2*c4
    p[5] += -c0*pow_c3_2
    p[5] += -pow_c1_2 *c4
    p[5] += 2.*c1*c2*c3
    p[5] += -pow(c2, 3)
    p[5] *= (c1*c3 - c1*c4 - pow_c2_2  + c2*c3 + c2*c4 - pow_c3_2 )
    p[5]  = 1./p[5]
    p[5] *= (c1*c3*c5 - c1*(c4*c4) - pow_c2_2 *c5 + 2.*c2*c3*c4 - pow(c3, 3))
    p[5] *= (c0*c2 - c0*c3 - pow_c1_2  + c1*c2 + c1*c3 - pow_c2_2 )

    if len(moments) < 7:
        return p

    c6 = moments[6]
    pow_c1_2 = c1 * c1
    pow_c2_2 = c2 * c2
    pow_c3_2 = c3 * c3
    pow_c4_2 = c4 * c4
    pow_c5_2 = c5 * c5
    pow_c2_3 = pow(c2, 3)
    pow_c3_3 = pow(c3, 3)

    p6  = c1*c3*c4
    p6 += -c1*c3*c5
    p6 += +c1*pow_c4_2
    p6 += -pow_c2_3
    p6 += +pow_c2_2 *c3
    p6 += +pow_c2_2 *c4
    p6 += +pow_c2_2 *c5
    p6 += -c2*pow_c3_2
    p6 += -2*c2*c3*c4
    p6 += +pow_c3_3
    p6 += c0*c2*c4
    p6 += -c0*c2*c5
    p6 += -c0*pow_c3_2
    p6 += +c0*c3*c4
    p6 += +c0*c3*c5
    p6 += -c0*pow_c4_2
    p6 += -pow_c1_2 *c4
    p6 += +pow_c1_2 *c5
    p6 += +2*c1*c2*c3
    p6 += -c1*c2*c4
    p6 += -c1*c2*c5
    p6 += -c1*pow_c3_2
    p6 *= (c1*c3*c5 - c1*pow_c4_2  - pow_c2_2 *c5 + 2*c2*c3*c4 - pow_c3_3)
    p6  = 1./p6
    p6t = c0*c2*c4*c6
    p6t+= -c0*c2*pow_c5_2
    p6t+= -c0*pow_c3_2 *c6
    p6t+= +2*c0*c3*c4*c5
    p6t+= -c0*pow(c4, 3)
    p6t+= -pow_c1_2 *c4*c6
    p6t+= +pow_c1_2 *pow_c5_2
    p6t+= +2*c1*c2*c3*c6
    p6t+= -2*c1*c2*c4*c5
    p6t+= -2*c1*pow_c3_2 *c5
    p6t+= 2*c1*c3*pow_c4_2
    p6t+= -pow_c2_3*c6
    p6t+= +2*pow_c2_2 *c3*c5
    p6t+= +pow_c2_2 *pow_c4_2
    p6t+= -3*c2*pow_c3_2 *c4
    p6t+= +pow(c3, 4)
    p6 *= p6t
    p6 *= (c1*c3 - c1*c4 - pow_c2_2  + c2*c3 + c2*c4 - pow_c3_2 )
    p[6] = p6

    return p


def canonical_to_ordinary(canonical):   # pylint:disable=too-many-statements,too-many-locals
    """
    Verified explicit formulas for the conversion of up to seven canonical
    moments to ordinary moments.

    """

    if len(canonical) > 7:
        raise NotImplementedError(
            "Canonical moment transformation is only implemented up to sixth order"
        )

    moments = np.zeros(len(canonical))
    moments[0] = canonical[0]
    moments[1] = canonical[1]

    p0 = canonical[0]
    p1 = canonical[1]
    p2 = canonical[2]
    c2  = -p1*p2
    c2 +=  p1
    c2 +=  p2
    c2 *= p0
    c2 *= p1
    moments[2] = c2

    if len(canonical) < 4:
        return moments

    p3 = canonical[3]
    pow_p1_2 = p1 * p1
    pow_p2_2 = p2 * p2

    c3  = pow_p1_2*pow_p2_2
    c3 += -2*pow_p1_2*p2
    c3 += pow_p1_2
    c3 += p1*pow_p2_2*p3
    c3 += -2*p1*pow_p2_2
    c3 += -p1*p2*p3
    c3 += 2*p1*p2
    c3 += -pow_p2_2*p3
    c3 += pow_p2_2
    c3 += p2*p3
    c3 *= p0*p1
    moments[3] = c3

    if len(moments) < 5:
        return moments

    p4 = canonical[4]
    pow_p1_2 = p1 * p1
    pow_p2_2 = p2 * p2
    pow_p3_2 = p3 * p3
    pow_p1_3 = pow(p1, 3)
    pow_p2_3 = pow(p2, 3)

    c4  = -pow_p1_3*pow_p2_3
    c4 += 3*pow_p1_3*pow_p2_2
    c4 += -3*pow_p1_3*p2
    c4 += pow_p1_3
    c4 += -2*pow_p1_2*pow_p2_3*p3
    c4 += 3*pow_p1_2*pow_p2_3
    c4 += 4*pow_p1_2*pow_p2_2*p3
    c4 += -6*pow_p1_2*pow_p2_2
    c4 += -2*pow_p1_2*p2*p3
    c4 += 3*pow_p1_2*p2
    c4 += -p1*pow_p2_3*pow_p3_2
    c4 += 4*p1*pow_p2_3*p3
    c4 += -3*p1*pow_p2_3
    c4 += -p1*pow_p2_2*pow_p3_2*p4
    c4 += 2*p1*pow_p2_2*pow_p3_2
    c4 += p1*pow_p2_2*p3*p4
    c4 += -6*p1*pow_p2_2*p3
    c4 += 3*p1*pow_p2_2
    c4 += p1*p2*pow_p3_2*p4
    c4 += -p1*p2*pow_p3_2
    c4 += -p1*p2*p3*p4
    c4 += 2*p1*p2*p3
    c4 += pow_p2_3*pow_p3_2
    c4 += -2*pow_p2_3*p3
    c4 += pow_p2_3
    c4 += pow_p2_2*pow_p3_2*p4
    c4 += -2*pow_p2_2*pow_p3_2
    c4 += -pow_p2_2*p3*p4
    c4 += 2*pow_p2_2*p3
    c4 += -p2*pow_p3_2*p4
    c4 += p2*pow_p3_2
    c4 += p2*p3*p4
    c4 *= p0*p1
    moments[4] = c4

    if len(moments) < 6:
        return moments

    p5 = canonical[5]
    pow_p1_2 = p1 * p1
    pow_p2_2 = p2 * p2
    pow_p3_2 = p3 * p3
    pow_p4_2 = p4 * p4
    pow_p1_3 = pow(p1,  3)
    pow_p2_3 = pow(p2,  3)
    pow_p3_3 = pow(p3,  3)
    pow_p1_4 = pow(p1,  4)
    pow_p2_4 = pow(p2,  4)

    c5  = pow_p1_4*pow_p2_4
    c5 += -4*pow_p1_4*pow_p2_3
    c5 += 6*pow_p1_4*pow_p2_2
    c5 += -4*pow_p1_4*p2
    c5 += pow_p1_4
    c5 += 3*pow_p1_3*pow_p2_4*p3
    c5 += -4*pow_p1_3*pow_p2_4
    c5 += -9*pow_p1_3*pow_p2_3*p3
    c5 += 12*pow_p1_3*pow_p2_3
    c5 += 9*pow_p1_3*pow_p2_2*p3
    c5 += -12*pow_p1_3*pow_p2_2
    c5 += -3*pow_p1_3*p2*p3
    c5 += 4*pow_p1_3*p2
    c5 += 3*pow_p1_2*pow_p2_4*pow_p3_2
    c5 += -9*pow_p1_2*pow_p2_4*p3
    c5 += 6*pow_p1_2*pow_p2_4
    c5 += 2*pow_p1_2*pow_p2_3*pow_p3_2*p4
    c5 += -8*pow_p1_2*pow_p2_3*pow_p3_2
    c5 += -2*pow_p1_2*pow_p2_3*p3*p4
    c5 += 21*pow_p1_2*pow_p2_3*p3
    c5 += -12*pow_p1_2*pow_p2_3
    c5 += -4*pow_p1_2*pow_p2_2*pow_p3_2*p4
    c5 += 7*pow_p1_2*pow_p2_2*pow_p3_2
    c5 += 4*pow_p1_2*pow_p2_2*p3*p4
    c5 += -15*pow_p1_2*pow_p2_2*p3
    c5 += 6*pow_p1_2*pow_p2_2
    c5 += 2*pow_p1_2*p2*pow_p3_2*p4
    c5 += -2*pow_p1_2*p2*pow_p3_2
    c5 += -2*pow_p1_2*p2*p3*p4
    c5 += 3*pow_p1_2*p2*p3
    c5 += p1*pow_p2_4*pow_p3_3
    c5 += -6*p1*pow_p2_4*pow_p3_2
    c5 += 9*p1*pow_p2_4*p3
    c5 += -4*p1*pow_p2_4
    c5 += 2*p1*pow_p2_3*pow_p3_3*p4
    c5 += -3*p1*pow_p2_3*pow_p3_3
    c5 += -6*p1*pow_p2_3*pow_p3_2*p4
    c5 += 14*p1*pow_p2_3*pow_p3_2
    c5 += 4*p1*pow_p2_3*p3*p4
    c5 += -15*p1*pow_p2_3*p3
    c5 += 4*p1*pow_p2_3
    c5 += p1*pow_p2_2*pow_p3_3*pow_p4_2
    c5 += -4*p1*pow_p2_2*pow_p3_3*p4
    c5 += 3*p1*pow_p2_2*pow_p3_3
    c5 += p1*pow_p2_2*pow_p3_2*pow_p4_2*p5
    c5 += -2*p1*pow_p2_2*pow_p3_2*pow_p4_2
    c5 += -p1*pow_p2_2*pow_p3_2*p4*p5
    c5 += 10*p1*pow_p2_2*pow_p3_2*p4
    c5 += -10*p1*pow_p2_2*pow_p3_2
    c5 += -p1*pow_p2_2*p3*pow_p4_2*p5
    c5 += p1*pow_p2_2*p3*pow_p4_2
    c5 += p1*pow_p2_2*p3*p4*p5
    c5 += -6*p1*pow_p2_2*p3*p4
    c5 += 6*p1*pow_p2_2*p3
    c5 += -p1*p2*pow_p3_3*pow_p4_2
    c5 += 2*p1*p2*pow_p3_3*p4
    c5 += -p1*p2*pow_p3_3
    c5 += -p1*p2*pow_p3_2*pow_p4_2*p5
    c5 += 2*p1*p2*pow_p3_2*pow_p4_2
    c5 += p1*p2*pow_p3_2*p4*p5
    c5 += -4*p1*p2*pow_p3_2*p4
    c5 += 2*p1*p2*pow_p3_2
    c5 += p1*p2*p3*pow_p4_2*p5
    c5 += -p1*p2*p3*pow_p4_2
    c5 += -p1*p2*p3*p4*p5
    c5 += 2*p1*p2*p3*p4
    c5 += -pow_p2_4*pow_p3_3
    c5 += 3*pow_p2_4*pow_p3_2
    c5 += -3*pow_p2_4*p3
    c5 += pow_p2_4
    c5 += -2*pow_p2_3*pow_p3_3*p4
    c5 += 3*pow_p2_3*pow_p3_3
    c5 += 4*pow_p2_3*pow_p3_2*p4
    c5 += -6*pow_p2_3*pow_p3_2
    c5 += -2*pow_p2_3*p3*p4
    c5 += 3*pow_p2_3*p3
    c5 += -pow_p2_2*pow_p3_3*pow_p4_2
    c5 += 4*pow_p2_2*pow_p3_3*p4
    c5 += -3*pow_p2_2*pow_p3_3
    c5 += -pow_p2_2*pow_p3_2*pow_p4_2*p5
    c5 += 2*pow_p2_2*pow_p3_2*pow_p4_2
    c5 += pow_p2_2*pow_p3_2*p4*p5
    c5 += -6*pow_p2_2*pow_p3_2*p4
    c5 += 3*pow_p2_2*pow_p3_2
    c5 += pow_p2_2*p3*pow_p4_2*p5
    c5 += -pow_p2_2*p3*pow_p4_2
    c5 += -pow_p2_2*p3*p4*p5
    c5 += 2*pow_p2_2*p3*p4
    c5 += p2*pow_p3_3*pow_p4_2
    c5 += -2*p2*pow_p3_3*p4
    c5 += p2*pow_p3_3
    c5 += p2*pow_p3_2*pow_p4_2*p5
    c5 += -2*p2*pow_p3_2*pow_p4_2
    c5 += -p2*pow_p3_2*p4*p5
    c5 += 2*p2*pow_p3_2*p4
    c5 += -p2*p3*pow_p4_2*p5
    c5 += p2*p3*pow_p4_2
    c5 += p2*p3*p4*p5
    c5 *= p0*p1
    moments[5] = c5

    if len(moments) < 7:
        return moments

    p6 = canonical[6]
    pow_p1_2 = p1 * p1
    pow_p2_2 = p2 * p2
    pow_p3_2 = p3 * p3
    pow_p4_2 = p4 * p4
    pow_p5_2 = p5 * p5
    pow_p1_3 = pow(p1,  3)
    pow_p2_3 = pow(p2,  3)
    pow_p3_3 = pow(p3,  3)
    pow_p4_3 = pow(p4,  3)
    pow_p1_4 = pow(p1,  4)
    pow_p2_4 = pow(p2,  4)
    pow_p3_4 = pow(p3,  4)
    pow_p1_5 = pow(p1,  5)
    pow_p2_5 = pow(p2,  5)

    c6  = -pow_p1_5*pow_p2_5
    c6 += 5*pow_p1_5*pow_p2_4
    c6 += -10*pow_p1_5*pow_p2_3
    c6 += 10*pow_p1_5*pow_p2_2
    c6 += -5*pow_p1_5*p2
    c6 += pow_p1_5
    c6 += -4*pow_p1_4*pow_p2_5*p3
    c6 += 5*pow_p1_4*pow_p2_5
    c6 += 16*pow_p1_4*pow_p2_4*p3
    c6 += -20*pow_p1_4*pow_p2_4
    c6 += -24*pow_p1_4*pow_p2_3*p3
    c6 += 30*pow_p1_4*pow_p2_3
    c6 += 16*pow_p1_4*pow_p2_2*p3
    c6 += -20*pow_p1_4*pow_p2_2
    c6 += -4*pow_p1_4*p2*p3
    c6 += 5*pow_p1_4*p2
    c6 += -6*pow_p1_3*pow_p2_5*pow_p3_2
    c6 += 16*pow_p1_3*pow_p2_5*p3
    c6 += -10*pow_p1_3*pow_p2_5
    c6 += -3*pow_p1_3*pow_p2_4*pow_p3_2*p4
    c6 += 21*pow_p1_3*pow_p2_4*pow_p3_2
    c6 += 3*pow_p1_3*pow_p2_4*p3*p4
    c6 += -52*pow_p1_3*pow_p2_4*p3
    c6 += 30*pow_p1_3*pow_p2_4
    c6 += 9*pow_p1_3*pow_p2_3*pow_p3_2*p4
    c6 += -27*pow_p1_3*pow_p2_3*pow_p3_2
    c6 += -9*pow_p1_3*pow_p2_3*p3*p4
    c6 += 60*pow_p1_3*pow_p2_3*p3
    c6 += -30*pow_p1_3*pow_p2_3
    c6 += -9*pow_p1_3*pow_p2_2*pow_p3_2*p4
    c6 += 15*pow_p1_3*pow_p2_2*pow_p3_2
    c6 += 9*pow_p1_3*pow_p2_2*p3*p4
    c6 += -28*pow_p1_3*pow_p2_2*p3
    c6 += 10*pow_p1_3*pow_p2_2
    c6 += 3*pow_p1_3*p2*pow_p3_2*p4
    c6 += -3*pow_p1_3*p2*pow_p3_2
    c6 += -3*pow_p1_3*p2*p3*p4
    c6 += 4*pow_p1_3*p2*p3
    c6 += -4*pow_p1_2*pow_p2_5*pow_p3_3
    c6 += 18*pow_p1_2*pow_p2_5*pow_p3_2
    c6 += -24*pow_p1_2*pow_p2_5*p3
    c6 += 10*pow_p1_2*pow_p2_5
    c6 += -6*pow_p1_2*pow_p2_4*pow_p3_3*p4
    c6 += 14*pow_p1_2*pow_p2_4*pow_p3_3
    c6 += 15*pow_p1_2*pow_p2_4*pow_p3_2*p4
    c6 += -54*pow_p1_2*pow_p2_4*pow_p3_2
    c6 += -9*pow_p1_2*pow_p2_4*p3*p4
    c6 += 60*pow_p1_2*pow_p2_4*p3
    c6 += -20*pow_p1_2*pow_p2_4
    c6 += -2*pow_p1_2*pow_p2_3*pow_p3_3*pow_p4_2
    c6 += 16*pow_p1_2*pow_p2_3*pow_p3_3*p4
    c6 += -18*pow_p1_2*pow_p2_3*pow_p3_3
    c6 += -2*pow_p1_2*pow_p2_3*pow_p3_2*pow_p4_2*p5
    c6 += 4*pow_p1_2*pow_p2_3*pow_p3_2*pow_p4_2
    c6 += 2*pow_p1_2*pow_p2_3*pow_p3_2*p4*p5
    c6 += -37*pow_p1_2*pow_p2_3*pow_p3_2*p4
    c6 += 57*pow_p1_2*pow_p2_3*pow_p3_2
    c6 += 2*pow_p1_2*pow_p2_3*p3*pow_p4_2*p5
    c6 += -2*pow_p1_2*pow_p2_3*p3*pow_p4_2
    c6 += -2*pow_p1_2*pow_p2_3*p3*p4*p5
    c6 += 21*pow_p1_2*pow_p2_3*p3*p4
    c6 += -48*pow_p1_2*pow_p2_3*p3
    c6 += 10*pow_p1_2*pow_p2_3
    c6 += 4*pow_p1_2*pow_p2_2*pow_p3_3*pow_p4_2
    c6 += -14*pow_p1_2*pow_p2_2*pow_p3_3*p4
    c6 += 10*pow_p1_2*pow_p2_2*pow_p3_3
    c6 += 4*pow_p1_2*pow_p2_2*pow_p3_2*pow_p4_2*p5
    c6 += -8*pow_p1_2*pow_p2_2*pow_p3_2*pow_p4_2
    c6 += -4*pow_p1_2*pow_p2_2*pow_p3_2*p4*p5
    c6 += 29*pow_p1_2*pow_p2_2*pow_p3_2*p4
    c6 += -24*pow_p1_2*pow_p2_2*pow_p3_2
    c6 += -4*pow_p1_2*pow_p2_2*p3*pow_p4_2*p5
    c6 += 4*pow_p1_2*pow_p2_2*p3*pow_p4_2
    c6 += 4*pow_p1_2*pow_p2_2*p3*p4*p5
    c6 += -15*pow_p1_2*pow_p2_2*p3*p4
    c6 += 12*pow_p1_2*pow_p2_2*p3
    c6 += -2*pow_p1_2*p2*pow_p3_3*pow_p4_2
    c6 += 4*pow_p1_2*p2*pow_p3_3*p4
    c6 += -2*pow_p1_2*p2*pow_p3_3
    c6 += -2*pow_p1_2*p2*pow_p3_2*pow_p4_2*p5
    c6 += 4*pow_p1_2*p2*pow_p3_2*pow_p4_2
    c6 += 2*pow_p1_2*p2*pow_p3_2*p4*p5
    c6 += -7*pow_p1_2*p2*pow_p3_2*p4
    c6 += 3*pow_p1_2*p2*pow_p3_2
    c6 += 2*pow_p1_2*p2*p3*pow_p4_2*p5
    c6 += -2*pow_p1_2*p2*p3*pow_p4_2
    c6 += -2*pow_p1_2*p2*p3*p4*p5
    c6 += 3*pow_p1_2*p2*p3*p4
    c6 += -p1*pow_p2_5*pow_p3_4
    c6 += 8*p1*pow_p2_5*pow_p3_3
    c6 += -18*p1*pow_p2_5*pow_p3_2
    c6 += 16*p1*pow_p2_5*p3
    c6 += -5*p1*pow_p2_5
    c6 += -3*p1*pow_p2_4*pow_p3_4*p4
    c6 += 4*p1*pow_p2_4*pow_p3_4
    c6 += 15*p1*pow_p2_4*pow_p3_3*p4
    c6 += -26*p1*pow_p2_4*pow_p3_3
    c6 += -21*p1*pow_p2_4*pow_p3_2*p4
    c6 += 45*p1*pow_p2_4*pow_p3_2
    c6 += 9*p1*pow_p2_4*p3*p4
    c6 += -28*p1*pow_p2_4*p3
    c6 += 5*p1*pow_p2_4
    c6 += -3*p1*pow_p2_3*pow_p3_4*pow_p4_2
    c6 += 9*p1*pow_p2_3*pow_p3_4*p4
    c6 += -6*p1*pow_p2_3*pow_p3_4
    c6 += -2*p1*pow_p2_3*pow_p3_3*pow_p4_2*p5
    c6 += 10*p1*pow_p2_3*pow_p3_3*pow_p4_2
    c6 += 2*p1*pow_p2_3*pow_p3_3*p4*p5
    c6 += -37*p1*pow_p2_3*pow_p3_3*p4
    c6 += 30*p1*pow_p2_3*pow_p3_3
    c6 += 6*p1*pow_p2_3*pow_p3_2*pow_p4_2*p5
    c6 += -11*p1*pow_p2_3*pow_p3_2*pow_p4_2
    c6 += -6*p1*pow_p2_3*pow_p3_2*p4*p5
    c6 += 43*p1*pow_p2_3*pow_p3_2*p4
    c6 += -36*p1*pow_p2_3*pow_p3_2
    c6 += -4*p1*pow_p2_3*p3*pow_p4_2*p5
    c6 += 4*p1*pow_p2_3*p3*pow_p4_2
    c6 += 4*p1*pow_p2_3*p3*p4*p5
    c6 += -15*p1*pow_p2_3*p3*p4
    c6 += 12*p1*pow_p2_3*p3
    c6 += -p1*pow_p2_2*pow_p3_4*pow_p4_3
    c6 += 6*p1*pow_p2_2*pow_p3_4*pow_p4_2
    c6 += -9*p1*pow_p2_2*pow_p3_4*p4
    c6 += 4*p1*pow_p2_2*pow_p3_4
    c6 += -2*p1*pow_p2_2*pow_p3_3*pow_p4_3*p5
    c6 += 3*p1*pow_p2_2*pow_p3_3*pow_p4_3
    c6 += 6*p1*pow_p2_2*pow_p3_3*pow_p4_2*p5
    c6 += -18*p1*pow_p2_2*pow_p3_3*pow_p4_2
    c6 += -4*p1*pow_p2_2*pow_p3_3*p4*p5
    c6 += 29*p1*pow_p2_2*pow_p3_3*p4
    c6 += -14*p1*pow_p2_2*pow_p3_3
    c6 += -p1*pow_p2_2*pow_p3_2*pow_p4_3*pow_p5_2
    c6 += 4*p1*pow_p2_2*pow_p3_2*pow_p4_3*p5
    c6 += -3*p1*pow_p2_2*pow_p3_2*pow_p4_3
    c6 += -p1*pow_p2_2*pow_p3_2*pow_p4_2*pow_p5_2*p6
    c6 += 2*p1*pow_p2_2*pow_p3_2*pow_p4_2*pow_p5_2
    c6 += p1*pow_p2_2*pow_p3_2*pow_p4_2*p5*p6
    c6 += -14*p1*pow_p2_2*pow_p3_2*pow_p4_2*p5
    c6 += 18*p1*pow_p2_2*pow_p3_2*pow_p4_2
    c6 += p1*pow_p2_2*pow_p3_2*p4*pow_p5_2*p6
    c6 += -p1*pow_p2_2*pow_p3_2*p4*pow_p5_2
    c6 += -p1*pow_p2_2*pow_p3_2*p4*p5*p6
    c6 += 10*p1*pow_p2_2*pow_p3_2*p4*p5
    c6 += -26*p1*pow_p2_2*pow_p3_2*p4
    c6 += 9*p1*pow_p2_2*pow_p3_2
    c6 += p1*pow_p2_2*p3*pow_p4_3*pow_p5_2
    c6 += -2*p1*pow_p2_2*p3*pow_p4_3*p5
    c6 += p1*pow_p2_2*p3*pow_p4_3
    c6 += p1*pow_p2_2*p3*pow_p4_2*pow_p5_2*p6
    c6 += -2*p1*pow_p2_2*p3*pow_p4_2*pow_p5_2
    c6 += -p1*pow_p2_2*p3*pow_p4_2*p5*p6
    c6 += 8*p1*pow_p2_2*p3*pow_p4_2*p5
    c6 += -6*p1*pow_p2_2*p3*pow_p4_2
    c6 += -p1*pow_p2_2*p3*p4*pow_p5_2*p6
    c6 += p1*pow_p2_2*p3*p4*pow_p5_2
    c6 += p1*pow_p2_2*p3*p4*p5*p6
    c6 += -6*p1*pow_p2_2*p3*p4*p5
    c6 += 6*p1*pow_p2_2*p3*p4
    c6 += p1*p2*pow_p3_4*pow_p4_3
    c6 += -3*p1*p2*pow_p3_4*pow_p4_2
    c6 += 3*p1*p2*pow_p3_4*p4
    c6 += -p1*p2*pow_p3_4
    c6 += 2*p1*p2*pow_p3_3*pow_p4_3*p5
    c6 += -3*p1*p2*pow_p3_3*pow_p4_3
    c6 += -4*p1*p2*pow_p3_3*pow_p4_2*p5
    c6 += 8*p1*p2*pow_p3_3*pow_p4_2
    c6 += 2*p1*p2*pow_p3_3*p4*p5
    c6 += -7*p1*p2*pow_p3_3*p4
    c6 += 2*p1*p2*pow_p3_3
    c6 += p1*p2*pow_p3_2*pow_p4_3*pow_p5_2
    c6 += -4*p1*p2*pow_p3_2*pow_p4_3*p5
    c6 += 3*p1*p2*pow_p3_2*pow_p4_3
    c6 += p1*p2*pow_p3_2*pow_p4_2*pow_p5_2*p6
    c6 += -2*p1*p2*pow_p3_2*pow_p4_2*pow_p5_2
    c6 += -p1*p2*pow_p3_2*pow_p4_2*p5*p6
    c6 += 8*p1*p2*pow_p3_2*pow_p4_2*p5
    c6 += -7*p1*p2*pow_p3_2*pow_p4_2
    c6 += -p1*p2*pow_p3_2*p4*pow_p5_2*p6
    c6 += p1*p2*pow_p3_2*p4*pow_p5_2
    c6 += p1*p2*pow_p3_2*p4*p5*p6
    c6 += -4*p1*p2*pow_p3_2*p4*p5
    c6 += 4*p1*p2*pow_p3_2*p4
    c6 += -p1*p2*p3*pow_p4_3*pow_p5_2
    c6 += 2*p1*p2*p3*pow_p4_3*p5
    c6 += -p1*p2*p3*pow_p4_3
    c6 += -p1*p2*p3*pow_p4_2*pow_p5_2*p6
    c6 += 2*p1*p2*p3*pow_p4_2*pow_p5_2
    c6 += p1*p2*p3*pow_p4_2*p5*p6
    c6 += -4*p1*p2*p3*pow_p4_2*p5
    c6 += 2*p1*p2*p3*pow_p4_2
    c6 += p1*p2*p3*p4*pow_p5_2*p6
    c6 += -p1*p2*p3*p4*pow_p5_2
    c6 += -p1*p2*p3*p4*p5*p6
    c6 += 2*p1*p2*p3*p4*p5
    c6 += pow_p2_5*pow_p3_4
    c6 += -4*pow_p2_5*pow_p3_3
    c6 += 6*pow_p2_5*pow_p3_2
    c6 += -4*pow_p2_5*p3
    c6 += pow_p2_5
    c6 += 3*pow_p2_4*pow_p3_4*p4
    c6 += -4*pow_p2_4*pow_p3_4
    c6 += -9*pow_p2_4*pow_p3_3*p4
    c6 += 12*pow_p2_4*pow_p3_3
    c6 += 9*pow_p2_4*pow_p3_2*p4
    c6 += -12*pow_p2_4*pow_p3_2
    c6 += -3*pow_p2_4*p3*p4
    c6 += 4*pow_p2_4*p3
    c6 += 3*pow_p2_3*pow_p3_4*pow_p4_2
    c6 += -9*pow_p2_3*pow_p3_4*p4
    c6 += 6*pow_p2_3*pow_p3_4
    c6 += 2*pow_p2_3*pow_p3_3*pow_p4_2*p5
    c6 += -8*pow_p2_3*pow_p3_3*pow_p4_2
    c6 += -2*pow_p2_3*pow_p3_3*p4*p5
    c6 += 21*pow_p2_3*pow_p3_3*p4
    c6 += -12*pow_p2_3*pow_p3_3
    c6 += -4*pow_p2_3*pow_p3_2*pow_p4_2*p5
    c6 += 7*pow_p2_3*pow_p3_2*pow_p4_2
    c6 += 4*pow_p2_3*pow_p3_2*p4*p5
    c6 += -15*pow_p2_3*pow_p3_2*p4
    c6 += 6*pow_p2_3*pow_p3_2
    c6 += 2*pow_p2_3*p3*pow_p4_2*p5
    c6 += -2*pow_p2_3*p3*pow_p4_2
    c6 += -2*pow_p2_3*p3*p4*p5
    c6 += 3*pow_p2_3*p3*p4
    c6 += pow_p2_2*pow_p3_4*pow_p4_3
    c6 += -6*pow_p2_2*pow_p3_4*pow_p4_2
    c6 += 9*pow_p2_2*pow_p3_4*p4
    c6 += -4*pow_p2_2*pow_p3_4
    c6 += 2*pow_p2_2*pow_p3_3*pow_p4_3*p5
    c6 += -3*pow_p2_2*pow_p3_3*pow_p4_3
    c6 += -6*pow_p2_2*pow_p3_3*pow_p4_2*p5
    c6 += 14*pow_p2_2*pow_p3_3*pow_p4_2
    c6 += 4*pow_p2_2*pow_p3_3*p4*p5
    c6 += -15*pow_p2_2*pow_p3_3*p4
    c6 += 4*pow_p2_2*pow_p3_3
    c6 += pow_p2_2*pow_p3_2*pow_p4_3*pow_p5_2
    c6 += -4*pow_p2_2*pow_p3_2*pow_p4_3*p5
    c6 += 3*pow_p2_2*pow_p3_2*pow_p4_3
    c6 += pow_p2_2*pow_p3_2*pow_p4_2*pow_p5_2*p6
    c6 += -2*pow_p2_2*pow_p3_2*pow_p4_2*pow_p5_2
    c6 += -pow_p2_2*pow_p3_2*pow_p4_2*p5*p6
    c6 += 10*pow_p2_2*pow_p3_2*pow_p4_2*p5
    c6 += -10*pow_p2_2*pow_p3_2*pow_p4_2
    c6 += -pow_p2_2*pow_p3_2*p4*pow_p5_2*p6
    c6 += pow_p2_2*pow_p3_2*p4*pow_p5_2
    c6 += pow_p2_2*pow_p3_2*p4*p5*p6
    c6 += -6*pow_p2_2*pow_p3_2*p4*p5
    c6 += 6*pow_p2_2*pow_p3_2*p4
    c6 += -pow_p2_2*p3*pow_p4_3*pow_p5_2
    c6 += 2*pow_p2_2*p3*pow_p4_3*p5
    c6 += -pow_p2_2*p3*pow_p4_3
    c6 += -pow_p2_2*p3*pow_p4_2*pow_p5_2*p6
    c6 += 2*pow_p2_2*p3*pow_p4_2*pow_p5_2
    c6 += pow_p2_2*p3*pow_p4_2*p5*p6
    c6 += -4*pow_p2_2*p3*pow_p4_2*p5
    c6 += 2*pow_p2_2*p3*pow_p4_2
    c6 += pow_p2_2*p3*p4*pow_p5_2*p6
    c6 += -pow_p2_2*p3*p4*pow_p5_2
    c6 += -pow_p2_2*p3*p4*p5*p6
    c6 += 2*pow_p2_2*p3*p4*p5
    c6 += -p2*pow_p3_4*pow_p4_3
    c6 += 3*p2*pow_p3_4*pow_p4_2
    c6 += -3*p2*pow_p3_4*p4
    c6 += p2*pow_p3_4
    c6 += -2*p2*pow_p3_3*pow_p4_3*p5
    c6 += 3*p2*pow_p3_3*pow_p4_3
    c6 += 4*p2*pow_p3_3*pow_p4_2*p5
    c6 += -6*p2*pow_p3_3*pow_p4_2
    c6 += -2*p2*pow_p3_3*p4*p5
    c6 += 3*p2*pow_p3_3*p4
    c6 += -p2*pow_p3_2*pow_p4_3*pow_p5_2
    c6 += 4*p2*pow_p3_2*pow_p4_3*p5
    c6 += -3*p2*pow_p3_2*pow_p4_3
    c6 += -p2*pow_p3_2*pow_p4_2*pow_p5_2*p6
    c6 += 2*p2*pow_p3_2*pow_p4_2*pow_p5_2
    c6 += p2*pow_p3_2*pow_p4_2*p5*p6
    c6 += -6*p2*pow_p3_2*pow_p4_2*p5
    c6 += 3*p2*pow_p3_2*pow_p4_2
    c6 += p2*pow_p3_2*p4*pow_p5_2*p6
    c6 += -p2*pow_p3_2*p4*pow_p5_2
    c6 += -p2*pow_p3_2*p4*p5*p6
    c6 += 2*p2*pow_p3_2*p4*p5
    c6 += p2*p3*pow_p4_3*pow_p5_2
    c6 += -2*p2*p3*pow_p4_3*p5
    c6 += p2*p3*pow_p4_3
    c6 += p2*p3*pow_p4_2*pow_p5_2*p6
    c6 += -2*p2*p3*pow_p4_2*pow_p5_2
    c6 += -p2*p3*pow_p4_2*p5*p6
    c6 += 2*p2*p3*pow_p4_2*p5
    c6 += -p2*p3*p4*pow_p5_2*p6
    c6 += p2*p3*p4*pow_p5_2
    c6 += p2*p3*p4*p5*p6
    c6 *= p0*p1

    return moments
