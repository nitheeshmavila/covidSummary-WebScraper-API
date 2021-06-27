from django.conf import settings

DATA_NOT_AVAILABLE = None
EMPTY_VALUE = 0

class CovidCountry:
    """ Represents country data of covid"""
    
    def __init__(self, **props):
        fields = ['country', 'total_cases', 'active_cases',
         'total_deaths', 'population', 'total_recovered']

        for field in fields:
            setattr(self, field, props.get(field, None))

    def update_fields(self):
        self.update_recovery_rate()
        self.update_infected_population()
    
    def update_recovery_rate(self):
        if self.total_cases == DATA_NOT_AVAILABLE or self.total_recovered == DATA_NOT_AVAILABLE:
            self.recovery_rate = DATA_NOT_AVAILABLE
            return
        if self.total_cases == EMPTY_VALUE:
            self.recovery_rate = EMPTY_VALUE
            return
        self.recovery_rate = self.total_recovered / self.total_cases

    def update_infected_population(self):
        if self.population == DATA_NOT_AVAILABLE or self.total_cases == DATA_NOT_AVAILABLE:
            self.percentate_of_population_infected = DATA_NOT_AVAILABLE
            return
        if self.population == EMPTY_VALUE:
            self.percentate_of_population_infected = EMPTY_VALUE
            return
        self.percentate_of_population_infected = self.total_cases / self.population

    def clean_data(self):
        numeric_fields = ['total_cases', 'active_cases',
         'total_deaths', 'population', 'total_recovered']

        for field in numeric_fields:
            value = getattr(self, field)
            if value is None:
                setattr(self, field, DATA_NOT_AVAILABLE)
                continue
            
            value = value.replace(',', '').strip()
            if value == EMPTY_VALUE:
                setattr(self, field, EMPTY_VALUE)
                continue

            # if value is not available set to data not available
            if value == settings.COVID_TABLE_CELL_DATA_NOT_AVAILABLE:
                setattr(self, field, DATA_NOT_AVAILABLE)
                continue

            try:
                setattr(self, field, int(value))
            except ValueError as v:
                setattr(self, field, DATA_NOT_AVAILABLE)
            