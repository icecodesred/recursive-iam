class TCREClimateModel:
    def __init__(self, tcre=1.5/1000, initial_temp=1.2):  #divison to convert to gigatonnes
        self.tcre = tcre
        self.initial_temp = initial_temp
        self.cumulative_emissions = 0.0
        self.temperature = self.initial_temp

    def update_temperature(self, emissions):  
        self.cumulative_emissions += max(emissions, 0.0)
        self.temperature = self.initial_temp + self.tcre * self.cumulative_emissions
        return self.temperature
