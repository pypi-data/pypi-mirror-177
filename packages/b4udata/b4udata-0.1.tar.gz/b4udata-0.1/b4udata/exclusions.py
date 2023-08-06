from connections import Database
import pandas as pd
import numpy as np
import sqlalchemy as sa

class exclusion(Database):

    def __init__(self,blreporting,distribution):
        self.blreporting = blreporting
        self.distribution = distribution


    def createarray(self):

        apps = pd.read_sql(sa.text("SELECT DISTINCT(idnumber) FROM clientinfo WHERE idnumber is not null and idnumber not in ('',' ')"), self.blreporting)
        apps = apps.idnumber.to_numpy()

        dist = pd.read_sql(sa.text("SELECT id_number, date_distributed FROM blc_distribution"),self.distribution)
        dist['date_distributed'] = pd.to_datetime(dist['date_distributed'],errors = 'coerce')
        dist = dist.sort_values('date_distributed').groupby(['id_number']).head()
        dist = dist[(dist.date_distributed <= pd.to_datetime('now')) & 
        (dist.date_distributed >= pd.to_datetime('now')- pd.DateOffset(months=2))]

        dist = dist.id_number.to_numpy()

        _exclusions = np.concatenate([apps, dist])

        return _exclusions


    



