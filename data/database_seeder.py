# Make sure that we can read the project directory
import sys
sys.path.append('../')

# Import the interfaces
from excel_interfaces.ScenariosInterface import ScenariosInterface
import sqlite3

# Get the data from the excel file
print("Reading data from excel file...")
scenarios_interface = ScenariosInterface("scenarios.xlsx")
scenarios = scenarios_interface.scenarios
valid_scenario_names = scenarios_interface.valid_scenario_names
valid_sheet_names = scenarios_interface.valid_scenario_sheet_names

# Connect to the database
print("Connecting to database...")
database_connection = sqlite3.connect("./data.sqlite")
database_cursor = database_connection.cursor()

# Run the script to create the database tables
print("Creating database tables...")
with open("create_scenario_tables.sql", "r") as database_script:
    database_cursor.executescript(database_script.read())

# Empty the database tables
print("Emptying database tables...")
database_cursor.execute("DELETE FROM scenario;")
database_cursor.execute("DELETE FROM scenario_data;")

# Go through the scenarios
for scenario_name in valid_scenario_names:
    try:
        # Start processing the scenario
        print("Processing scenario: " + scenario_name + "...")
        scenario = scenarios[scenario_name]

        # Go over the different types of scenario
        for scenario_type in scenario.values():
            # Start processing the scenario type
            print("Processing scenario type: " + scenario_type.name + "...")
            
            # Insert the scenario type into the database
            scenario_id = valid_sheet_names.index(scenario_type.name) + 1
            database_cursor.execute(f"INSERT INTO scenario (id, naam) VALUES ({scenario_id}, '{scenario_type.name}');")

            # Go over all the years in the scenario type
            for year in scenario_type.years.values():
                # Insert the year into the database
                database_cursor.execute(f"INSERT INTO scenario_data (scenario, jaar, prijs_diesel, prijs_electrisch, vermogen, reparatiekosten_ev, onderhoudskosten_ev, onderhoudskosten_diesel, stilstand_ev, subsidies_ev, co2_prijs, efficienty_diesel, efficienty_electrisch, inkoopprijs_elektriciteit_depot, inkoopprijs_elektriciteit_onderweg, bruto_kosten_inkoop_oplaadsysteem, bruto_kosten_aanleg_oplaadsysteem, brandstofprijs_diesel, mutatie_accijns_diesel, mrb_diesel, mrb_electrisch, mia, vamil, energiesubsidie, vaste_ze_voertuigheffing, verschil_vrachtwagentolheffing, subsidie_aanleg_oplaadsysteem, restwaarde_1_jaar_oude_ev_truck, restwaarde_2_jaar_oude_ev_truck, restwaarde_3_jaar_oude_ev_truck, restwaarde_4_jaar_oude_ev_truck, restwaarde_5_jaar_oude_ev_truck, restwaarde_6_jaar_oude_ev_truck, restwaarde_7_jaar_oude_ev_truck, restwaarde_8_jaar_oude_ev_truck, restwaarde_9_jaar_oude_ev_truck, restwaarde_10_jaar_oude_ev_truck, restwaarde_11_jaar_oude_ev_truck, restwaarde_12_jaar_oude_ev_truck, restwaarde_13_jaar_oude_ev_truck, restwaarde_14_jaar_oude_ev_truck, restwaarde_15_jaar_oude_ev_truck, restwaarde_1_jaar_oude_diesel_truck, restwaarde_2_jaar_oude_diesel_truck, restwaarde_3_jaar_oude_diesel_truck, restwaarde_4_jaar_oude_diesel_truck, restwaarde_5_jaar_oude_diesel_truck, restwaarde_6_jaar_oude_diesel_truck, restwaarde_7_jaar_oude_diesel_truck, restwaarde_8_jaar_oude_diesel_truck, restwaarde_9_jaar_oude_diesel_truck, restwaarde_10_jaar_oude_diesel_truck, restwaarde_11_jaar_oude_diesel_truck, restwaarde_12_jaar_oude_diesel_truck, restwaarde_13_jaar_oude_diesel_truck, restwaarde_14_jaar_oude_diesel_truck, restwaarde_15_jaar_oude_diesel_truck, laadvermogen_externe_laadpaal, laadvermogen_laadpaal_op_depot, laadvermogen_nodig_depot, laadvermogen_nodig_onderweg, ac37_thuis, ac10_onderweg, ac20_onderweg, ac20_thuis, fc50_onderweg, fc50_thuis, hpc150_onderweg, hpc150_thuis, hpc350_onderweg, hpc350_thuis) VALUES ({scenario_id}, {year.year}, {year.diesel_price_in_euro}, {year.electric_price_in_euro}, {year.capacity_in_kWh}, {year.repair_costs_EV_euro_per_year}, {year.maintenance_costs_EV_euro_per_km}, {year.maintenance_costs_diesel_euro_per_km}, {year.standstil_EV_in_days}, {year.subsidies_EV_in_euro}, {year.CO2_price_in_euro_per_ton}, {year.efficiency_diesel_in_liter_per_km}, {year.efficiency_electricity_in_kWh_per_km}, {year.electricity_price_private_excluding_tax_in_euro_per_kWh}, {year.electricity_price_public_excluding_tax_in_euro_per_kWh}, {year.gross_purchase_cost_charging_system_in_euro}, {year.gross_installation_cost_charging_system_in_euro}, {year.fuel_price_diesel_excluding_tax_in_euro_per_liter}, {year.change_in_excise_duty_diesel_in_percentage}, {year.vehicle_tax_diesel_in_euro_per_year}, {year.vehicle_tax_electric_in_euro_per_year}, {year.MIA_in_euro_per_lifespan}, {year.VAMIL_in_euro_per_lifespan}, {year.energy_subsidy_in_euro_per_kWh}, {year.fixed_ZE_vehicle_tax_in_euro_per_year}, {year.difference_truck_toll_tax_in_euro_per_km}, {year.subsidy_charging_system_installation_in_euro_per_installation}, {year.residual_value_EV_year_1_in_percentage}, {year.residual_value_EV_year_2_in_percentage}, {year.residual_value_EV_year_3_in_percentage}, {year.residual_value_EV_year_4_in_percentage}, {year.residual_value_EV_year_5_in_percentage}, {year.residual_value_EV_year_6_in_percentage}, {year.residual_value_EV_year_7_in_percentage}, {year.residual_value_EV_year_8_in_percentage}, {year.residual_value_EV_year_9_in_percentage}, {year.residual_value_EV_year_10_in_percentage}, {year.residual_value_EV_year_11_in_percentage}, {year.residual_value_EV_year_12_in_percentage}, {year.residual_value_EV_year_13_in_percentage}, {year.residual_value_EV_year_14_in_percentage}, {year.residual_value_EV_year_15_in_percentage}, {year.residual_value_diesel_year_1_in_percentage}, {year.residual_value_diesel_year_2_in_percentage}, {year.residual_value_diesel_year_3_in_percentage}, {year.residual_value_diesel_year_4_in_percentage}, {year.residual_value_diesel_year_5_in_percentage}, {year.residual_value_diesel_year_6_in_percentage}, {year.residual_value_diesel_year_7_in_percentage}, {year.residual_value_diesel_year_8_in_percentage}, {year.residual_value_diesel_year_9_in_percentage}, {year.residual_value_diesel_year_10_in_percentage}, {year.residual_value_diesel_year_11_in_percentage}, {year.residual_value_diesel_year_12_in_percentage}, {year.residual_value_diesel_year_13_in_percentage}, {year.residual_value_diesel_year_14_in_percentage}, {year.residual_value_diesel_year_15_in_percentage}, {year.charging_capacity_external_charging_pole}, {year.charging_capacity_charging_pole_on_depot}, {year.needed_charging_capacity_depot}, {year.needed_charging_capacity_in_transit}, {year.AC37_at_home}, {year.AC10_in_transit}, {year.AC20_in_transit}, {year.AC20_at_home}, {year.FC50_in_transit}, {year.FC50_at_home}, {year.HPC150_in_transit}, {year.HPC150_at_home}, {year.HPC350_in_transit}, {year.HPC350_at_home});")
    except Exception:
        print("Error processing scenario: " + scenario_name)

# Close the database connection
print("Saving data and closing database connection...")
database_connection.commit()
database_connection.close()