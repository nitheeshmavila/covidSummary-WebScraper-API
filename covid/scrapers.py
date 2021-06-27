import requests

from bs4 import BeautifulSoup
from django.conf import settings
from rest_framework import status

from .models import CovidCountry


class CovidDataSraper:
    
    def __init__(self):
        self.countries = []
        self.url = settings.COVID_DATA_URL
        self.parser = 'html.parser'
        self.target_columns = ["country", "total_cases", "active_cases",
                                "total_deaths", "population", "total_recovered"]

    def fetch_summary_data(self):
        summary = {"status": status.HTTP_200_OK, "data": None, "message": None}
        response = requests.get(self.url)

        if not response.ok:
            summary["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            summary["message"] = settings.FAILED_MESSAGE
            return summary

        soup = BeautifulSoup(response.text, self.parser)
        table = soup.find("table", {"id": settings.COVID_DATA_TABLE})
        self.set_countries_data(table)
        summary["data"] = self.countries
        return summary
    
    def set_countries_data(self, table):
        table_header = self.get_data_table_header(table)
        rows = self.get_data_table_rows(table)
        
        for row in rows:
            row_data = {}
            for idx, cell in enumerate(row.find_all("td")[:settings.NO_OF_COVID_DATA_TABLE_COLUMNS]):
                column = table_header[idx]
                if column in self.target_columns:
                    row_data[table_header[idx]] = cell.text
            country = CovidCountry(**row_data)
            country.clean_data()
            country.update_fields()
            self.countries.append(country)
        
    def get_data_table_header(self, table):

        header_columns = table.thead.tr.find_all('th')[:settings.NO_OF_COVID_DATA_TABLE_COLUMNS]
        return { idx: self.clean(header.text) 
            for idx, header in enumerate(header_columns)}
    
    def get_data_table_rows(self, table):
        all_rows = table.tbody.find_all("tr")
        return [row for row in filter(self.is_required, all_rows)]

    def is_required(self, row):
        if not row.has_attr("class"):
            return True
        if settings.COVID_TABLE_EXCLUDED_ROW_CLASS in row["class"]:
            return False
        return True

    def clean(self, country_name):
        if country_name == "Country,Other":
            return "country"
        if country_name == "TotalCases": 
            return "total_cases"
        if country_name == "ActiveCases":
            return "active_cases"
        if country_name == "TotalDeaths":
            return "total_deaths"
        if country_name == "Population": 
            return "population"
        if country_name == "TotalRecovered":
            return "total_recovered"
        return country_name