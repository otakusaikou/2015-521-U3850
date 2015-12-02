#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sympy import symbols, Matrix, lambdify
import numpy as np


np.set_printoptions(suppress=True)  # Disable scientific notation for numpy


def getEqns(xp, yp, Xs, Ys, xs):
    """Return observation equations"""
    F1 = xs[0] * xp + xs[1] * yp + xs[2] - Xs
    F2 = xs[3] * xp + xs[4] * yp + xs[5] - Ys
    F = Matrix(np.append(F1, F2))

    return F


def main():
    # Define image coordinates
    xp = np.array([465.403, 5102.342, 5108.498, 468.303])
    yp = np.array([2733.558, 2744.195, 465.302, 455.048])

    # Define object space coordinates
    Xp = np.array([318844.012, 328266.150, 328287.963, 318859.828])
    Yp = np.array([2775910.930, 2775949.224, 2771320.012, 2771282.932])

    # Define symbol of unknown parameters
    xs = np.array(symbols("A B C D E F"))

    # Get observation equations
    F = getEqns(xp, yp, Xp, Yp, xs)

    # Create function object for observation equations
    FuncF = lambdify(tuple(xs), F, modules='sympy')

    # Compute B and f matrix
    B = np.matrix(F.jacobian(xs)).astype(np.double)
    f = -np.matrix(FuncF(*np.zeros(len(xs)))).astype(np.double)

    # Compute unknown parameters
    X = (B.T * B).I * (B.T * f)

    # Compute residuals
    V = B * X - f

    # Compute error of unit weight
    s0 = ((V.T * V)[0, 0] / (B.shape[0] - B.shape[1]))**0.5

    # Compute other informations
    SigmaXX = s0**2 * (B.T * B).I
    param_std = np.sqrt(np.diag(SigmaXX))

    # Output results
    print "Affine transformation coefficients:"
    print ("%-10s"+" %-15s"*2) % ("Parameter", "Value", "SD")
    for i in range(len(X)):
        print ("%-10s"+" %-15.6f"*2) % (
            chr(65+i), X[i, 0], param_std[i])

    # Compute adjusted observations
    Xp2, Yp2 = np.hsplit(np.array((B * X)).flatten(), 2)
    Vx, Vy = np.hsplit(np.array(V).flatten(), 2)

    print "\nObject point coordinates:"
    print ("%-8s"+" %-15s"*4) % ("Point ID", "X", "Y", "X-res", "Y-res")
    for i in range(len(Xp)):
        print ("%-8d"+" %-15.6f"*4) % ((i+1), Xp2[i], Yp2[i], Vx[i], Vy[i])

    print ("\n%-8s %15s %15s %-15.6f %-15.6f") % (
        "RMS", "{:^15}".format("N/A"), "{:^15}".format("N/A"),
        np.sqrt((Vx**2).mean()), np.sqrt((Vy**2).mean()))

    return 0


if __name__ == '__main__':
    main()
