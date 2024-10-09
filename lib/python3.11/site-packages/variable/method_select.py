# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 07:17:30 2018

@author: glawson
"""

"""
###############################################################################
                               Initial Setup
"""
#import necessary packages
import pandas as pd 
import numpy as np
import statsmodels.api as sm
import math

#Identify original display settings and set as variable orig_setting for use in
    #returning to to original display settings after code.  Set display options
    #to optimal settings for printed output.
#orig_setting = pd.get_option('display.width')
#pd.set_option('display.width', 120)





"""
###############################################################################
                            Forward Selection Function
"""
#To use this function, specify the dataframe of independent variables (X) and 
    #the target variables (y) to be used.

def forward(X,y):
    
    #Identify original display settings and set as variable orig_setting for use in
    #returning to to original display settings after code.  Set display options
    #to optimal settings for printed output.
    orig_setting = pd.get_option('display.width')
    pd.set_option('display.width', 120)

    #Combine dataframes for use in correlation
    df = pd.concat([y, X], axis=1)
    #Add a constant
    df = sm.add_constant(df)
    
    #Create a copy of the dataframe for use in correlation
    df_corr = df.copy()
    
    #Assign a "target" variable
    target = y.name
        
    #Create several dataframes for use in the function
    
    #The dataframe below is the list of variables that will be passed through  
        #the correlation function
    variable_list = df.columns.drop('const')  
    #The list below is the list of variables that will be fed into  
        #the model in the order in which they are identified. This list 
        #includes the constant so that the model can run.
    FS_Order_const = ['const'] 
    #The list below is the list of variables that will be used to  
        #identify the p_values of the model and will be printed in the output
        #as the result.  This list is identifical to FS_Order_const except no 
        #constant is included so that a p_value of the constant nor the constant
        #itself appears in the printed output.
    variable_order = []
    #The list below is the list of rsquared values in order for
        #use in the printed output.
    rsquared_value = []
    #The list below is the list of minimum t_test values in order for
        #use in the printed output.
    min_t_test = []
    #The list below is the list of maximum p_values in order for
        #use in the printed output.
    max_p_val = []
    #The list below is the list of MSE values in order for
        #use in the printed output.
    mse = []
    #The list below is the list of AIC values in order for
        #use in the printed output.
    aic = []
    #The list below is the list of BIC values in order for
        #use in the printed output.
    bic = []
    
    
    #Below is the loop to iterate through all variables to evaluate, select, 
        #and remove variables from the model.
    for i in range(len(df.columns)-2):
        #Step 1 in the process is to correlate all independent variables to 
            #the target variable.  The result of the target variable to itself
            #is dropped, and the absolute value of all correlation coefficients
            #is calculated.
        corr0 = df_corr[variable_list].corr()
        corr0 = corr0.drop(target,0)
        corr = pd.DataFrame(abs(corr0[target]))
    
        #The correlation coefficients aresorted in descending order, and the
            #independent variable with the max correlation coefficient is 
            #selected.  This value is appended to the appropraite dataframes.
            #As this is an iterative process, these lists will have one 
            #additional variable added with each iteration.
        corr.reset_index(level=0, inplace=True)
        corr_sorted = corr.sort_values([target], ascending=[False])
        #print(corr_sorted.iloc[0,0])
        max_corr_var = corr_sorted.iloc[0,0]
        FS_Order_const.append(max_corr_var)
        variable_order.append(max_corr_var)
        
        #Step 2 in the process is to run the model with the constant and the
            #independent variable(s) selected in step one.  The residuals of 
            #the model are calculated as well as the r-squared value.
        model = sm.OLS(df[target], df[FS_Order_const]).fit()
        model.summary()
        resid = model.resid
        rsquared_result = model.rsquared
        
        #The following values from the current iteration of the model are 
            #calculated and appended to the appropriate dataframes.  These are the
            #values that will be printed in the output.
        max_p_val.append(max(model.pvalues[variable_order]))
        min_t_test.append(abs(model.tvalues[max_corr_var]))
        rsquared_value.append(rsquared_result)
        mse.append(model.mse_resid)
        aic.append(model.aic)
        bic.append(model.bic)
        
        #The variable list is reduced by the max correlated variable selected
            #in this iteration so that the next iteration will only use 
            #variables that have not yet been determined to be highly 
            #correlated.  Additionally, the target variable is set to equal the
            #residual values of the model to account for the effect of the
            #variables already removed from the model.
        variable_list = variable_list.drop(max_corr_var,1)
        df_corr[target] = resid       
    
    #The results are joined in one dataframe and printed with the variable name
        #as the output.
    root_mse = [math.sqrt(x) for x in mse]
    result = pd.DataFrame(np.column_stack([min_t_test, max_p_val, rsquared_value, mse, root_mse, aic, bic]), columns=['min_abs_(t)', 'max_p_value', 'r_squared', 'MSE', 'Root_MSE', 'AIC', 'BIC'])
    result.insert(0, 'variable', variable_order)
    print ('\n**********************   Forward Selection Results   ***********************\n')
    print (round(result,2))
    
    #Return the display options to the original settings.    
    pd.set_option('display.width', orig_setting)
    
    



"""
###############################################################################
                            Backward Selection Function
"""   

#To use this function, specify the dataframe of independent variables (X) and 
    #the target variables (y) to be used.
    
def back(X,y):
    
    #Identify original display settings and set as variable orig_setting for use in
    #returning to to original display settings after code.  Set display options
    #to optimal settings for printed output.
    orig_setting = pd.get_option('display.width')
    pd.set_option('display.width', 120)
    
    #Combine dataframes for use in correlation
    df = pd.concat([y, X], axis=1)
    #Add a constant
    df = sm.add_constant(df)
    
    #Assign a "target" variable
    target = y.name

    #Create several dataframes for use in the function
    
    #The dataframe below is the list of variables that will be passed through  
        #the correlation function
    variable_list = df.columns.drop(target) 
    BS_Order = X.columns
    #The list below is the list of variables that will be used to  
        #identify the p_values of the model and will be printed in the output
        #as the result.  
    variable_order = []
    #The list below is the list of rsquared values in order for
        #use in the printed output.
    rsquared_value = []
    #The list below is the list of minimum t_test values in order for
        #use in the printed output.
    min_t_test = []
    #The list below is the list of maximum p_values in order for
        #use in the printed output.
    max_p_val = []
    #The list below is the list of MSE values in order for
        #use in the printed output.
    mse = []
    #The list below is the list of AIC values in order for
        #use in the printed output.
    aic = []
    #The list below is the list of BIC values in order for
        #use in the printed output.
    bic = []
    
    #Below is the loop to iterate through all variables to evaluate, select, 
        #and remove variables from the model.
    for i in range(len(df.columns)-2):
        
        #Step 1 in the process is to run the model with the constant and the
            #independent variable(s) selected in step one.  The residuals of 
            #the model are calculated as well as the r-squared value.
        model = sm.OLS(df[target], df[variable_list]).fit()
        model.summary()
        rsquared_result = model.rsquared
        
        #The following values from the current iteration of the model are 
            #calculated and appended to the appropriate dataframes.  These are the
            #values that will be printed in the output.
        min_t_val = min(abs(model.tvalues[BS_Order]))
        max_p_val.append(max(model.pvalues[BS_Order]))
        min_t_test.append(min_t_val)
        rsquared_value.append(rsquared_result)
        mse.append(model.mse_resid)
        aic.append(model.aic)
        bic.append(model.bic)
        
        #Step 2 in the process is to identify the variable with the minimum 
            #t_value.  This is done by sorting all t_values in ascending order
            #and removing the minimum value, or the first one in the ascending
            #list.  This value is appended to a list for the printed output.
            #The loop is repeated with all remaining variables.  The loop
            #iterates until all variables have been removed.
        min_t_var = pd.DataFrame(abs(model.tvalues[BS_Order]), columns=['min_t_val'])
    
        min_t_var.reset_index(level=0, inplace=True)
        min_t_var_sorted = min_t_var.sort_values(['min_t_val'], ascending=[True])
        #print(corr_sorted.iloc[0,0])
        min_t_val = min_t_var_sorted.iloc[0,0]
        BS_Order = BS_Order.drop(min_t_val)
        variable_list = variable_list.drop(min_t_val)
        variable_order.append(min_t_val)
        
    #The results are joined in one dataframe and printed with the variable name
        #as the output.              
    root_mse = [math.sqrt(x) for x in mse]
    result = pd.DataFrame(np.column_stack([min_t_test, max_p_val, rsquared_value, mse, root_mse, aic, bic]), columns=['min_abs_(t)', 'max_p_value', 'r_squared', 'MSE', 'Root_MSE', 'AIC', 'BIC'])
    result.insert(0, 'variable', variable_order)
    print ('\n**********************   Backward Selection Results   ***********************\n')
    print (round(result,2))
    
    #Return the display options to the original settings.    
    pd.set_option('display.width', orig_setting)

    