# -*- coding: utf-8 -*-
"""
Created Jan 2018 by Akinjide Akintunde

This program fits inflation-extension experiment data (AVG) for transversely isotropic tissues to:
    NH_2FF: neo-Hookean + 2 Fiber Family model (Holzapfel et al., J Elast. 2000)
    gHY: generalized Humphrey-Yin (Murphy 2013)
    gSRM: generalized Standard Reinforcing Model (Murphy 2013)
"""
# =============================================================================
# Import needed, created modules
from kinematics_avg import main as runKinAvg
#from objective import main as runObj
from solve4Lqq_iv import main as runSolve4Lqq_iv
from lin_stiff import main as runLinStiff
from sef_contour import main as runSEFContour
from corr_mat_sens_analysis import main as runCorrSens
from plot import main as runPlot
from slope_intercept import main as runSlopeIntercept
from exp_stiffness_compliance import main as runStiffComp
from fit_FR import main as runfitFR
#from bootstrap import main as runBootstrap
#
#from fit_least_squares import main as runLSQFit
#from fit_L_BFGS_B import main as runLBFGSBFit
#from fit_basin_hopping import main as runBasinHopFit
from fit_diff_evol import main as runDiffEvolFit
#from fit_brute import main as runBruteFit
#from theory_nh2ff import Pressure_th, TForce_th

# Import needed standard Python modules
import numpy as np
import random
import os
import scipy.io as sio
import xlsxwriter
# =============================================================================
"""Specify .mat filename """
# =============================================================================
filename = 'avg_ela_load'

filename1 = 'SS091916KR-VAGeL'
filename2 = 'SS091216KR-VAGeL'
filename3 = 'SS082916KR-VAGeL'
filename4 = 'SS081616KR-VAGeL'
filename5 = 'SS121317KR-VAGeL'
filename6 = 'SS011218KR-VAGeL'
filename7 = 'SS012318KR-VAGeL'
filename8 = 'SS012418KR-VAGeL'

datafilepath = 'D:\Inflation_Extension_Modeling\Vaginal digestion\Data'
file1 = "%s\%s" % (datafilepath, filename1)
file2 = "%s\%s" % (datafilepath, filename2)
file3 = "%s\%s" % (datafilepath, filename3)
file4 = "%s\%s" % (datafilepath, filename4)
file5 = "%s\%s" % (datafilepath, filename5)
file6 = "%s\%s" % (datafilepath, filename6)
file7 = "%s\%s" % (datafilepath, filename7)
file8 = "%s\%s" % (datafilepath, filename8)
# =============================================================================
""" Specify model """
# =============================================================================
model = 'NH_2FF'
#model = 'gHY'
#model = 'gSRM'
# =============================================================================
z = "%s\%s" % (filename, model)
if not os.path.exists(z):
    os.makedirs(z)
    
path = 'D:\Inflation_Extension_Modeling\Vaginal digestion'

(Or, Ir, h, Crr, Cqq, Czz, P_exp, ft_exp, Lrriv, Lqqiv, Lzziv, iriv, oriv, hiv,
 ftiv, fiv, OD_iv, P_iv, Trriv, Tqqiv, Tzziv, Lrr4a, Lqq4a, Lzz4a, ir4a, or4a,
 h4a, ft4a, f4a, OD_4a, P_4a, Trr4a, Tqq4a, Tzz4a) = runKinAvg(file1, file2,
                                                 file3, file4, file5, file6,
                                                 file7, file8, path, filename,
                                                 model)

if model == 'NH_2FF':
    
    x0 = np.array([random.random(), random.random(), random.random(),
                   random.random()*(np.pi/2.0)])
    #              ce     c1     c2     alpha
    #              kPa    kPa    -      rad
    lb = np.array([0.0,   0.0,   0.0,   0.0])
    ub = np.array([1.0e2, 1.0e2, 1.0e3, (np.pi/2.0)])
    
    bounds1 = (lb, ub)
    
    bounds2 = (np.array([(lb[0], ub[0]), (lb[1], ub[1]),
                         (lb[2], ub[2]), (lb[3], ub[3])]))
elif model == 'gHY':
    
    x0 = np.array([random.random(), random.random(), random.random(),
                   random.random(), random.random(),
                   random.random()*(np.pi/2.0)])
    
    #              u_T    c2     E_L    u_L    c4     alpha
    #              kPa    -      kPa    kPa    -      rad
    lb = np.array([0.0,   0.0,   0.0,   0.0,   0.0,   0.0])
    ub = np.array([1.0e3, 1.0e3, 1.0e6, 1.0e3, 1.0e4, (np.pi/2.0)]) 
    
    bounds1 = (lb, ub)
    
    bounds2 = (np.array([(lb[0], ub[0]), (lb[1], ub[1]),
                        (lb[2], ub[2]), (lb[3], ub[3]),
                        (lb[4], ub[4]), (lb[5], ub[5])]))

elif model == 'gSRM':
    
    x0 = np.array([random.random(), random.random(), random.random(),
                   random.random()*(np.pi/2.0)])
    
    #              u_T    E_L    u_L    alpha
    #              kPa    kPa    kPa    rad   
    lb = np.array([0.0,   0.0,   0.0,   0.0])
    ub = np.array([1.0e3, 1.0e6, 1.0e5, (np.pi/2.0)])
    
    bounds1 = (lb, ub)
    
    bounds2 = (np.array([(lb[0], ub[0]), (lb[1], ub[1]),
                        (lb[2], ub[2]), (lb[3], ub[3])]))

''' Select fitting algorithm '''
#runLSQFit(x0, bounds1, Crr, Cqq, Czz, Ir, Or, P_exp, ft_exp, model, path)
#runLBFGSBFit(x0, bounds2, Crr, Cqq, Czz, Ir, Or, P_exp, ft_exp, model, path)
#runBasinHopFit(x0, bounds2, Crr, Cqq, Czz, Ir, Or, P_exp, ft_exp, model, path)
resDE, gof = runDiffEvolFit(bounds2, Crr, Cqq, Czz, Ir, Or, P_exp, ft_exp,
                            model, filename, path)
x = resDE.x
#runBruteFit(bounds2, Crr, Cqq, Czz, Ir, Or, P_exp, ft_exp, model, path)

# Solve for in vivo circumferential stretch
Lqq_iv, Lzz_iv, ir_iv, or_iv = runSolve4Lqq_iv(x, P_exp, Lqqiv, Lzziv, iriv,
                                               oriv, model, filename, path)

# Compute linearized stiffness
Crrrr_iv, Cqqqq_iv, Czzzz_iv = runLinStiff(x, Lqq_iv, Lzz_iv, model, filename,
                                           path)

# Compute the slope at the chosen in vivo circumferential stretch
dPdLq, PIntercept = runSlopeIntercept(x, Lqq_iv, Lzz_iv, ir_iv, or_iv, model,
                                      filename)

# Compute in vivo stored energy and make contour plot
Wiv = runSEFContour(x, Lqq_iv, Lzz_iv, model, filename, path)

# Plot figures
(Trrivth, Tqqivth, Tzzivth, Tqzivth, P_th_iv, ft_th_iv, f_th_iv, Trr4ath,
 Tqq4ath, Tzz4ath, P_th_4a, ft_th_4a, f_th_4a) = runPlot(x, Lrriv, Lqqiv,Lzziv,
                                             iriv, oriv, hiv, ftiv, fiv, OD_iv,
                                             P_iv, Trriv, Tqqiv, Tzziv, Lrr4a,
                                             Lqq4a, Lzz4a, ir4a, or4a, h4a,
                                             ft4a, f4a, OD_4a, P_4a, Trr4a,
                                             Tqq4a, Tzz4a, model, filename,
                                             path, dPdLq, PIntercept, Lqq_iv)

# Compute correlation matrix and sensitivity analysis
Corr_Mat_det = runCorrSens(x, Crr, Cqq, Czz, Or, Ir, h, Tqqivth, Tzzivth,
                           model, filename, path)

# Interpolate outer diameter values and compute compliance*
(OD_2_5, OD_5, OD_7_5, OD_10, OD_15, OD_20,
 C1, C2, C3, C4, C5) = runStiffComp(P_iv, OD_iv)


# perform simulated data fit to FR model
resFR, gof_FR, FR_det = runfitFR(x, Lqqiv, Lzziv, Tqzivth, path, filename,
                                 model)

# Perform bootstrapping
#Boot_par, Boot_gof = runBootstrap(bounds2, Crr, Cqq, Czz, Ir, Or, P_exp, ft_exp, model, filename, path)

''' Save results to MS excel file '''

if model == 'NH_2FF':
    
    results = (['mu_kPa', resDE.x[0]], ['c1_kPa', resDE.x[1]],
               ['c2', resDE.x[2]], ['alpha_deg', np.degrees(resDE.x[3])],
               ['obj_fun', resDE.fun], ['GOF', gof], ['Lqq_iv', Lqq_iv],
               ['Lzz_iv', Lzz_iv], ['Crrrr_iv_kPa', Crrrr_iv],
               ['Cqqqq_iv_kPa', Cqqqq_iv], ['Czzzz_iv_kPa', Czzzz_iv],
               ['Wiv_kPa', Wiv], ['CorrMat_det', Corr_Mat_det],
               ['dPdLq', dPdLq], ['PIntercept', PIntercept], 
               ['OD_2_5', OD_2_5], ['OD_5', OD_5], ['OD_7_5', OD_7_5], 
               ['OD_10', OD_10], ['OD_15', OD_15], ['OD_20', OD_20], 
               ['C1', C1], ['C2', C2], ['C3', C3], ['C4', C4], ['C5', C5],
               ['EE', resFR.x[0]], ['EC', resFR.x[1]], ['beta', resFR.x[2]],
               ['FR_obj_fun', resFR.fun], ['gof_FR', gof_FR], ['FR_det', FR_det])
        
elif model == 'gHY':
    
    results = (['uT_kPa', resDE.x[0]], ['c2', resDE.x[1]], ['EL_kPa', resDE.x[2]],
               ['uL_kPa', resDE.x[3]], ['c4', resDE.x[4]], ['alpha_deg', np.degrees(resDE.x[5])], 
               ['obj_fun', resDE.fun], ['GOF', gof], ['Lqq_iv', Lqq_iv], 
               ['Lzz_iv', Lzz_iv], ['Crrrr_iv_kPa', Crrrr_iv], 
               ['Cqqqq_iv_kPa', Cqqqq_iv], ['Czzzz_iv_kPa', Czzzz_iv],
               ['Wiv_kPa', Wiv], ['CorrMat_det', Corr_Mat_det], ['dPdLq', dPdLq], 
               ['PIntercept', PIntercept])

os.chdir(z)
workbook = xlsxwriter.Workbook("%s%s" % (filename, '.xlsx'))
worksheet = workbook.add_worksheet()
row = 0
col = 0
for title, item in results:
    worksheet.write(row, col, title)
    worksheet.write(row+1, col, item)
    col += 1
workbook.close()

''' Save theoretical data to MATLAB .mat file '''
# =============================================================================
mdict = {'Trrivth': Trrivth, 'Tqqivth': Tqqivth, 'Tzzivth': Tzzivth,
         'Tqzivth': Tqzivth, 'P_th_iv': P_th_iv, 'f_th_iv': f_th_iv,
         'ft_th_iv': ft_th_iv, 'Trr4ath': Trr4ath, 'Tqq4ath': Tqq4ath,
         'Tzz4ath': Tzz4ath, 'P_th_4a': P_th_4a, 'ft_th_4a': ft_th_4a,
         'f_th_4a': f_th_4a}

sio.savemat("%s\%s\%s\%s" % (path, filename, model, 'theor_data'), mdict=mdict,
            appendmat=True)
# =============================================================================
