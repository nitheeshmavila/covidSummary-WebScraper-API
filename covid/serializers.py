from rest_framework import serializers


class CovidCountrySerializer(serializers.Serializer):
    country = serializers.CharField(max_length=256)
    total_cases = serializers.IntegerField()
    active_cases = serializers.IntegerField()
    total_deaths = serializers.IntegerField()
    population = serializers.IntegerField()
    total_recovered = serializers.IntegerField()
    percentate_of_population_infected = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    recovery_rate = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
