# Import Libraries
import pandas as pd
import numpy as np

#------------------------------------------------------------------------------
# Read the data
#------------------------------------------------------------------------------

cols = ['Animal ID', 'Animal Type', 'DateTime', 'Outcome Type']
data = pd.read_csv(r'.\\Data\Pets_data.csv', parse_dates= ['DateTime'], usecols= cols)
data = data.loc[data["Animal Type"].isin(['Cat', 'Dog'])]


#--------------------------------------------------------------------------------
#Process the Data
#---------------------------------------------------------------------------------

#Drop duplicates
data.drop_duplicates(inplace = True)

#Group outcome Type into two fields
group1 = ["Return to Owner", "Transfer", "Adoption"]
data["Outcome Group"] = np.where(data['Outcome Type'].isin(group1),
                                "Return to Owner, Transfer or Adopted",
                                "other")

#Summary % of total for each Outcome Type and Animal Type
pet_output = (pd.crosstab(data["Animal Type"], data["Outcome Group"],
                           normalize='index')*100).round(1)


#Save Output
pet_output.to_csv(r'.\\Output\pet_output.csv', index= True)                          
