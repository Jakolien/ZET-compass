from base64 import b64encode
from datetime import datetime
from io import BytesIO
import warnings
from matplotlib.pyplot import Figure, close, subplots
from matplotlib import ticker


class GraphHelper:

    def __init__(self):

        """A helper class responsible for creating graphs using pyplot.

        :return: An instance of GraphHelper
        :rtype: GraphHelper
        """

        pass

    def plot_vehicle_TCO(self, number_plate: str, vehicle_data: dict):

        """Plots the TCO vehicle data on a graph.

        :param number_plate: The number plate of the vehicle.
        :type number_plate: str
        :param vehicle_data: The vehicle TCO data.
        :type vehicle_data: dict

        :return: The vehicle TCO graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario in vehicle_data:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                strategies = vehicle_data[scenario]

                graph, axes = subplots(figsize=(15, 5), nrows=1, ncols=2, tight_layout=True)

                # Plot strategies

                line_index = 0
                for strategy in strategies:

                    strategy_data = strategies[strategy]
                    year_labels = strategy_data.keys()
                    ls = ['-', '--', '-.', ':', '--'][line_index % 5]
                    TCO_costs = [year_data.get("tco", 0) for year, year_data in strategy_data.items()]
                    TCO_emissions = [year_data.get("CO2_emissions", 0) for year, year_data in strategy_data.items()]
                    line_index += 1

                    axes[0].plot(year_labels, TCO_costs, alpha=0.8, linestyle=ls)
                    axes[1].plot(year_labels, TCO_emissions, alpha=0.8, linestyle=ls, label=f"Strategie {strategy.split('_')[1]}")

                # Set labels cost graph
                axes[0].set_title(f"Jaarlijkse kosten {number_plate}")
                axes[0].set_xlabel("jaar")
                axes[0].set_ylabel("TCO per jaar (euro)")

                # Set labels emissions graph
                axes[1].set_title(f"Jaarlijkse uitstoot {number_plate}")
                axes[1].set_xlabel("jaar")
                axes[1].set_ylabel("CO2 per jaar (ton)")

                # Set legend
                axes[0].legend(loc="best")
                axes[1].legend(loc="best")
                #axes[1].legend(loc="upper left", bbox_to_anchor=(1.05, 1))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    def plot_vehicle_TCO_scenarios(self, number_plate: str, vehicle_data: dict):

        """Plots the TCO vehicle data on a graph.

        :param number_plate: The number plate of the vehicle.
        :type number_plate: str
        :param vehicle_data: The vehicle TCO data.
        :type vehicle_data: dict

        :return: The vehicle TCO graphs as base 64 encoded string. Organised by strategy.
        :rtype: dict
        """

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            scenarios = {}
            graphs = {}
            strategy = 'strategy_4'     # TODO change this to current strategy
            for scenario in vehicle_data:
                strategies = vehicle_data[scenario]
                scenarios[scenario] = strategies[strategy]
                graphs[scenario] = {}

            graphs = {}
            graph, axes = subplots(figsize=(15, 5), nrows=1, ncols=2, tight_layout=True)

            # Plot scenarios

            line_index = 0
            for scenario in scenarios:

                scenario_data = scenarios[scenario]
                year_labels = scenario_data.keys()
                ls = ['--', '-.', ':'][line_index % 3]
                TCO_costs = [year_data.get("tco", 0) for year, year_data in scenario_data.items()]
                TCO_emissions = [year_data.get("CO2_emissions", 0) for year, year_data in scenario_data.items()]
                line_index += 1

                axes[0].plot(year_labels, TCO_costs, alpha=0.8, linestyle=ls)
                axes[1].plot(year_labels, TCO_emissions, alpha=0.8, linestyle=ls, label=f"Scenario {scenario}")

            # Set labels cost graph
            axes[0].set_title(f"Jaarlijkse kosten {number_plate}")
            axes[0].set_xlabel("jaar")
            axes[0].set_ylabel("TCO per jaar (euro)")
            axes[0].get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

            # Set labels emissions graph
            axes[1].set_title(f"Jaarlijkse uitstoot {number_plate}")
            axes[1].set_xlabel("jaar")
            axes[1].set_ylabel("CO2 per jaar (ton)")
            axes[1].get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

            # Set legend
            axes[0].legend(loc="best")
            axes[1].legend(loc="best")
            #axes[1].legend(loc="upper left", bbox_to_anchor=(1.05, 1))

            # Encode graph
            graphs[strategy] = self.encode_graph_to_base64(graph)

            # Close figure
            close()

        return graphs

    def plot_vehicle_charging_capacity(self, number_plate: str, vehicle_data: dict):

        """Plots the vehicle charging capacity on a graph.

        :param number_plate: The number plate of the vehicle.
        :type number_plate: str
        :param vehicle_data: The vehicle TCO data.
        :type vehicle_data: dict

        :return: The vehicle charging capacity graphs as base 64 encoded string. Organised by scenario and strategy.
        :rtype: dict
        """

        graphs = {}
        for scenario in vehicle_data:

            graphs[scenario] = {}
            strategies = vehicle_data[scenario]

            # Plot strategies
            for strategy in strategies:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")

                    graph, ax = subplots(figsize=(6, 6), nrows=1, ncols=1, tight_layout=True)

                    strategy_data = strategies[strategy]
                    year_labels = strategy_data.keys()
                    charging_capacity_depot = [year_data.get("kWh_charged_on_depot", 0)
                                               for year, year_data in strategy_data.items()]
                    charging_capacity_public = [year_data.get("kWh_charged_in_public", 0)
                                                for year, year_data in strategy_data.items()]

                    ax.bar(year_labels, charging_capacity_depot, label="Op depot")
                    ax.bar(year_labels, charging_capacity_public, label="Onderweg", bottom=charging_capacity_depot)

                    # Set labels
                    ax.set_title(f"Laadbehoefte {number_plate} strategie {strategy.split('_')[1]}")
                    ax.set_xlabel("jaar")
                    ax.set_ylabel("Energievraag per dag (kWh)")
                    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                    # change axes limits
                    ymax = max(charging_capacity_public) + max(charging_capacity_depot)
                    ax.set_ylim(bottom=0, top=ymax + 20)

                    # Set legend
                    ax.legend(loc="best")
                    #ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

                    # Encode graph
                    graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                    # Close figure
                    close()

        return graphs

    # TODO adapt function for scenarios comparison
    def plot_vehicle_charging_capacity_scenarios(self, number_plate: str, vehicle_data: dict):

        """Plots the vehicle charging capacity on a graph.

        :param number_plate: The number plate of the vehicle.
        :type number_plate: str
        :param vehicle_data: The vehicle TCO data.
        :type vehicle_data: dict

        :return: The vehicle charging capacity graphs as base 64 encoded string. Organised by scenario and strategy.
        :rtype: dict
        """


        scenarios = {}
        graphs = {}
        strategy = 'strategy_4'
        for scenario in vehicle_data:
            strategies = vehicle_data[scenario]
            scenarios[scenario] = strategies[strategy]
            graphs[scenario] = {}

        # Plot strategies
        for scenario in scenarios:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(6, 6), nrows=1, ncols=1, tight_layout=True)

                scenario_data = scenarios[scenario]
                year_labels = scenario_data.keys()
                charging_capacity_depot = [year_data.get("kWh_charged_on_depot", 0)
                                            for year, year_data in scenario_data.items()]
                charging_capacity_public = [year_data.get("kWh_charged_in_public", 0)
                                            for year, year_data in scenario_data.items()]

                ax.bar(year_labels, charging_capacity_depot, label="Op depot")
                ax.bar(year_labels, charging_capacity_public, label="Onderweg", bottom=charging_capacity_depot)

                # Set labels
                ax.set_title(f"Laadbehoefte {number_plate} scenario {scenario}")
                ax.set_xlabel("jaar")
                ax.set_ylabel("Energievraag per dag (kWh)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # change axes limits
                ymax = max(charging_capacity_public) + max(charging_capacity_depot)
                ax.set_ylim(bottom=0, top=ymax + 20)

                # Set legend
                ax.legend(loc="best")
                #ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

                # Encode graph
                graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    def plot_vehicle_charging_time(self, number_plate: str, vehicle_data: dict):

        """Plots the vehicle charging time on a graph.

        :param number_plate: The number plate of the vehicle.
        :type number_plate: str
        :param vehicle_data: The vehicle TCO data.
        :type vehicle_data: dict

        :return: The vehicle charging time graphs as base 64 encoded string. Organised by scenario and strategy.
        :rtype: dict
        """

        graphs = {}
        for scenario in vehicle_data:

            graphs[scenario] = {}
            strategies = vehicle_data[scenario]

            # Plot strategies
            for strategy in strategies:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    graph, ax = subplots(figsize=(6, 6), nrows=1, ncols=1, tight_layout=True)

                    strategy_data = strategies[strategy]
                    year_labels = strategy_data.keys()
                    charging_time_depot = [year_data.get("charging_time_depot", 0)
                                            for year, year_data in strategy_data.items()]
                    charging_time_public = [year_data.get("charging_time_public", 0)
                                            for year, year_data in strategy_data.items()]

                    ax.bar(year_labels, charging_time_depot, label="Op depot")
                    ax.bar(year_labels, charging_time_public, label="Onderweg", bottom=charging_time_depot)

                    # Set labels
                    ax.set_title(f"Laadtijd {number_plate} strategie {strategy.split('_')[1]}")
                    ax.set_xlabel("jaar")
                    ax.set_ylabel("Laadtijd per dag (uur)")
                    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                    # change axes limits
                    ymax = max(charging_time_public) + max(charging_time_depot)
                    ax.set_ylim(bottom=0, top=ymax + 2)

                    # Set legend
                    ax.legend(loc="best")
                    #ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

                    # Encode graph
                    graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                    # Close figure
                    close()

        return graphs

    # TODO adapt function for scenarios comparison
    def plot_vehicle_charging_time_scenarios(self, number_plate: str, vehicle_data: dict):

        """Plots the vehicle charging time on a graph.

        :param number_plate: The number plate of the vehicle.
        :type number_plate: str
        :param vehicle_data: The vehicle TCO data.
        :type vehicle_data: dict

        :return: The vehicle charging time graphs as base 64 encoded string. Organised by scenario and strategy.
        :rtype: dict
        """

        graphs = {}
        for scenario in vehicle_data:

            graphs[scenario] = {}
            strategies = vehicle_data[scenario]

            # Plot strategies
            for strategy in strategies:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    graph, ax = subplots(figsize=(6, 6), nrows=1, ncols=1, tight_layout=True)

                    strategy_data = strategies[strategy]
                    year_labels = strategy_data.keys()
                    charging_time_depot = [year_data.get("charging_time_depot", 0)
                                            for year, year_data in strategy_data.items()]
                    charging_time_public = [year_data.get("charging_time_public", 0)
                                            for year, year_data in strategy_data.items()]

                    ax.bar(year_labels, charging_time_depot, label="Op depot")
                    ax.bar(year_labels, charging_time_public, label="Onderweg", bottom=charging_time_depot)

                    # Set labels
                    ax.set_title(f"Laadtijd {number_plate} strategie {strategy.split('_')[1]}")
                    ax.set_xlabel("jaar")
                    ax.set_ylabel("Laadtijd per dag (uur)")
                    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                    # change axes limits
                    ymax = max(charging_time_public) + max(charging_time_depot)
                    ax.set_ylim(bottom=0, top=ymax + 2)

                    # Set legend
                    ax.legend(loc="best")
                    #ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

                    # Encode graph
                    graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                    # Close figure
                    close()

        return graphs

    def plot_TCO_fleet_averages_bar(self, averages: dict):

        """Plots the average TCO fleet data on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)
                strategy_labels = [f"Strategie {strategy.split('_')[1]}" for strategy in strategies.keys()]
                TCO_cost_averages = []

                # Plot strategies
                for strategy, years in strategies.items():

                    strategy_TCO_cost_average = 0

                    for year in years:

                        strategy_TCO_cost_average += years[year].get("tco", 0)

                    # Calculate average
                    strategy_TCO_cost_average /= len(years)
                    TCO_cost_averages.append(strategy_TCO_cost_average)

                # Plot bar graph
                ax.bar(strategy_labels, TCO_cost_averages, color="red")

                # change axes limits
                ymin = min(TCO_cost_averages)
                ymax = max(TCO_cost_averages)
                ax.set_ylim(bottom=ymin - 2000, top=ymax + 2000)

                # Set labels cost graph
                ax.set_title(f"Totale jaarlijkse kosten wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("TCO per jaar (euro)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    def plot_CO2_fleet_averages_bar(self, averages: dict):

        """Plots the average CO2 fleet data on a graph.

        :param averages: The average CO2 fleet data.
        :type averages: dict

        :return: The CO2 fleet graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)
                strategy_labels = [f"Strategie {strategy.split('_')[1]}" for strategy in strategies.keys()]
                TCO_emissions_averages = []

                # Plot strategies
                for strategy, years in strategies.items():

                    strategy_TCO_emissions_average = 0

                    for year in years:

                        strategy_TCO_emissions_average += years[year].get("CO2_emissions", 0)

                    # Calculate average
                    strategy_TCO_emissions_average /= len(years)
                    TCO_emissions_averages.append(strategy_TCO_emissions_average)

                # Plot bar graph
                ax.bar(strategy_labels, TCO_emissions_averages, color="blue")

                # Set labels emissions graph
                ax.set_title(f"Totale jaarlijkse uitstoot wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("CO2 per jaar (ton)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    # TODO adapt function for scenarios comparison
    def plot_TCO_fleet_averages_bar_scenarios(self, averages: dict):

        """Plots the average TCO fleet data on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)
                strategy_labels = [f"Strategie {strategy.split('_')[1]}" for strategy in strategies.keys()]
                TCO_cost_averages = []

                # Plot strategies
                for strategy, years in strategies.items():

                    strategy_TCO_cost_average = 0

                    for year in years:

                        strategy_TCO_cost_average += years[year].get("tco", 0)

                    # Calculate average
                    strategy_TCO_cost_average /= len(years)
                    TCO_cost_averages.append(strategy_TCO_cost_average)

                # Plot bar graph
                ax.bar(strategy_labels, TCO_cost_averages, color="red")

                # change axes limits
                ymin = min(TCO_cost_averages)
                ymax = max(TCO_cost_averages)
                ax.set_ylim(bottom=ymin - 2000, top=ymax + 2000)

                # Set labels cost graph
                ax.set_title(f"Totale jaarlijkse kosten wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("TCO per jaar (euro)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    # TODO adapt function for scenarios comparison
    def plot_CO2_fleet_averages_bar_scenarios(self, averages: dict):

        """Plots the average CO2 fleet data on a graph.

        :param averages: The average CO2 fleet data.
        :type averages: dict

        :return: The CO2 fleet graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)
                strategy_labels = [f"Strategie {strategy.split('_')[1]}" for strategy in strategies.keys()]
                TCO_emissions_averages = []

                # Plot strategies
                for strategy, years in strategies.items():

                    strategy_TCO_emissions_average = 0

                    for year in years:

                        strategy_TCO_emissions_average += years[year].get("CO2_emissions", 0)

                    # Calculate average
                    strategy_TCO_emissions_average /= len(years)
                    TCO_emissions_averages.append(strategy_TCO_emissions_average)

                # Plot bar graph
                ax.bar(strategy_labels, TCO_emissions_averages, color="blue")

                # Set labels emissions graph
                ax.set_title(f"Totale jaarlijkse uitstoot wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("CO2 per jaar (ton)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    def plot_TCO_fleet_average_cost(self, averages: dict):

        """Plots the average TCO fleet cost on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet cost graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        # The Netherlands has set the goal to reduce CO2 emission by 49% by 2030.
        reduction_by_2030 = 0.49
        current_emissions = 0
        for scenario, strategies in averages.items():
            for strategy, years in strategies.items():  # [len(strategies)-2]:
                # Get current emissions
                current_timestamp = datetime.now()
                current_year = int(current_timestamp.strftime("%Y"))
                current_emissions = years[current_year].get("CO2_emissions", 0)

        # get emission goal for this company
        emissions_goal = (1 - reduction_by_2030) * current_emissions

        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

                # Plot strategies
                for strategy, years in strategies.items():

                    # Get emissions in 2030
                    emissions_in_2030 = years[2030].get("CO2_emissions", 0)

                    year_labels = years.keys()
                    TCO_costs = [year_data.get("tco", 0) for year, year_data in years.items()]

                    if emissions_in_2030 < emissions_goal:
                        ax.plot(year_labels, TCO_costs, linestyle="-",
                                label=f"TCO kosten strategie {strategy.split('_')[1]}")
                    else:
                        ax.plot(year_labels, TCO_costs, linestyle="--",
                                label=f"TCO kosten strategie {strategy.split('_')[1]}")

                # Set labels
                ax.set_title(f"Jaarlijkse voertuigkosten wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("TCO per jaar (euro)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Set legend
                #ax.legend(loc="best")
                ax.legend(loc="upper center", bbox_to_anchor=(0, -0.2, 1, 0.1))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    # TODO adapt function for scenarios comparison
    def plot_TCO_fleet_average_cost_scenarios(self, averages: dict):

        """Plots the average TCO fleet cost on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet cost graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        # The Netherlands has set the goal to reduce CO2 emission by 49% by 2030.
        reduction_by_2030 = 0.49
        current_emissions = 0
        for scenario, strategies in averages.items():
            for strategy, years in strategies.items():  # [len(strategies)-2]:
                # Get current emissions
                current_timestamp = datetime.now()
                current_year = int(current_timestamp.strftime("%Y"))
                current_emissions = years[current_year].get("CO2_emissions", 0)
        # get emission goal for this company
        emissions_goal = (1 - reduction_by_2030) * current_emissions

        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

                # Plot strategies
                for strategy, years in strategies.items():

                    # Get emissions in 2030
                    emissions_in_2030 = years[2030].get("CO2_emissions", 0)

                    year_labels = years.keys()
                    TCO_costs = [year_data.get("tco", 0) for year, year_data in years.items()]

                    if emissions_in_2030 > emissions_goal:
                        ax.plot(year_labels, TCO_costs, linestyle="--",
                                label=f"TCO kosten strategie {strategy.split('_')[1]}")
                    else:
                        ax.plot(year_labels, TCO_costs, linestyle="-",
                                label=f"TCO kosten strategie {strategy.split('_')[1]}")

                # Set labels
                ax.set_title(f"Jaarlijkse voertuigkosten wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("TCO per jaar (euro)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Set legend
                #ax.legend(loc="best")
                ax.legend(loc="upper center", bbox_to_anchor=(0, -0.2, 1, 0.1))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs


    def plot_TCO_fleet_average_emissions(self, averages: dict):

        """Plots the average TCO fleet CO2 emissions on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet emissions graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        # The Netherlands has set the goal to reduce CO2 emission by 49% by 2030.
        reduction_by_2030 = 0.49
        current_emissions = 0
        for scenario, strategies in averages.items():
            for strategy, years in strategies.items(): #[len(strategies)-2]:
                # Get current emissions
                current_timestamp = datetime.now()
                current_year = int(current_timestamp.strftime("%Y"))
                current_emissions = years[current_year].get("CO2_emissions", 0)
        # get emission goal for this company
        emissions_goal = (1 - reduction_by_2030) * current_emissions


        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

            # Plot strategies
            year_labels = []
            for strategy, years in strategies.items():

                # Get emissions in 2030
                emissions_in_2030 = years[2030].get("CO2_emissions", 0)

                year_labels = years.keys()
                TCO_emissions = [year_data.get("CO2_emissions", 0) for year, year_data in years.items()]

                if emissions_in_2030 > emissions_goal:
                    ax.plot(year_labels, TCO_emissions, linestyle="--",
                            label=f"TCO kosten strategie {strategy.split('_')[1]}")
                else:
                    ax.plot(year_labels, TCO_emissions, linestyle="-",
                            label=f"TCO kosten strategie {strategy.split('_')[1]}")

                # Plot reduction line
                reduction_line_x = year_labels
                reduction_line_y = [emissions_goal for year in year_labels]
                ax.plot(reduction_line_x, reduction_line_y, linestyle="--", color="black",
                        label=f"{reduction_by_2030 * 100}% reductie")

                # Set labels
                ax.set_title(f"Jaarlijkse uitstoot wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("CO2 per jaar (ton)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Set legend
                #ax.legend(loc="best")
                ax.legend(loc="upper center", bbox_to_anchor=(0, -0.2, 1, 0.1))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    # TODO adapt function for scenarios comparison
    def plot_TCO_fleet_average_emissions_scenarios(self, averages: dict):

        """Plots the average TCO fleet CO2 emissions on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet emissions graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        # The Netherlands has set the goal to reduce CO2 emission by 49% by 2030.
        reduction_by_2030 = 0.49
        current_emissions = 0
        for scenario, strategies in averages.items():
            for strategy, years in strategies.items():  # [len(strategies)-2]:
                # Get current emissions
                current_timestamp = datetime.now()
                current_year = int(current_timestamp.strftime("%Y"))
                current_emissions = years[current_year].get("CO2_emissions", 0)
        # get emission goal for this company
        emissions_goal = (1 - reduction_by_2030) * current_emissions

        graphs = {}
        for scenario, strategies in averages.items():
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

            # Plot strategies
            year_labels = []
            for strategy, years in strategies.items():

                # Get emissions in 2030
                emissions_in_2030 = years[2030].get("CO2_emissions", 0)

                year_labels = years.keys()
                TCO_emissions = [year_data.get("CO2_emissions", 0) for year, year_data in years.items()]

                if emissions_in_2030 > emissions_goal:
                    ax.plot(year_labels, TCO_emissions, linestyle="--",
                            label=f"TCO kosten strategie {strategy.split('_')[1]}")
                else:
                    ax.plot(year_labels, TCO_emissions, linestyle="-",
                            label=f"TCO kosten strategie {strategy.split('_')[1]}")

                # Plot reduction line
                reduction_line_x = year_labels
                reduction_line_y = [(1 - reduction_by_2030) * current_emissions for year in year_labels]
                ax.plot(reduction_line_x, reduction_line_y, linestyle="--", color="black",
                        label=f"{reduction_by_2030 * 100}% reductie")

                # Set labels
                ax.set_title(f"Jaarlijkse uitstoot wagenpark")
                ax.set_xlabel("jaar")
                ax.set_ylabel("CO2 per jaar (ton)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # Set legend
                #ax.legend(loc="best")
                ax.legend(loc="upper center", bbox_to_anchor=(0, -0.2, 1, 0.1))

                # Encode graph
                graphs[scenario] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    def plot_TCO_costs_breakdown(self, averages: dict):

        """Plots the TCO fleet cost breakdown on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet graphs as base 64 encoded string. Organised by scenario and strategy.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():

            graphs[scenario] = {}

            for strategy, years in strategies.items():
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

                    year_labels = years.keys()
                    fixed_vehicle_costs = [year_data.get("fixed_vehicle_costs", 0) for year, year_data in years.items()]
                    variable_vehicle_costs = [year_data.get("variable_vehicle_costs", 0)
                                              for year, year_data in years.items()]
                    write_off_costs_vehicle = [year_data.get("write_off_costs_vehicle", 0)
                                               for year, year_data in years.items()]
                    write_off_costs_charging_system = [year_data.get("write_off_costs_charging_system", 0)
                                                       for year, year_data in years.items()]
                    driver_costs = [year_data.get("driver_costs", 0) for year, year_data in years.items()]
                    costs_public_charging = [year_data.get("costs_public_charging", 0)
                                             for year, year_data in years.items()]
                    current_y_positions = fixed_vehicle_costs

                    # Plot bars
                    ax.bar(year_labels, fixed_vehicle_costs,
                           width=0.4, label="a: Vaste voertuigkosten")

                    ax.bar(year_labels, variable_vehicle_costs, bottom=current_y_positions,
                           width=0.4, label="b: Variabele voertuigkosten")
                    current_y_positions = [current_y_positions[index] + value
                                           for index, value in enumerate(variable_vehicle_costs)]

                    ax.bar(year_labels, write_off_costs_vehicle, bottom=current_y_positions,
                           width=0.4, label="c: Afschrijvingskosten")
                    current_y_positions = [current_y_positions[index] + value
                                           for index, value in enumerate(write_off_costs_vehicle)]

                    ax.bar(year_labels, write_off_costs_charging_system, bottom=current_y_positions,
                           width=0.4, label="d: Afschrijvingskosten oplaadsysteem")
                    current_y_positions = [current_y_positions[index] + value
                                           for index, value in enumerate(write_off_costs_charging_system)]

                    ax.bar(year_labels, driver_costs, bottom=current_y_positions,
                           width=0.4, label="e: Chauffeurskosten")
                    current_y_positions = [current_y_positions[index] + value
                                           for index, value in enumerate(driver_costs)]

                    ax.bar(year_labels, costs_public_charging, bottom=current_y_positions,
                           width=0.4, label="f: Kosten laadtijd onderweg")

                    # Set labels
                    ax.set_title(f"TCO totale kostenverdeling wagenpark strategie {strategy.split('_')[1]}")
                    ax.set_xlabel("jaar")
                    ax.set_ylabel("TCO per jaar (euro)")
                    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                    # Set legend
                    ax.legend(loc="upper center", bbox_to_anchor=(0, -0.2, 1, 0.1))

                    # Encode graph
                    graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                    # Close figure
                    close()

        return graphs

    def plot_TCO_fleet_average_charging_capacity(self, averages: dict):

        """Plots the average TCO fleet cost on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet cost graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():

            graphs[scenario] = {}

            for strategy, years in strategies.items():
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

                    year_labels = years.keys()
                    charging_capacity_depot = [year_data.get("kWh_charged_on_depot", 0) for year, year_data in
                                               years.items()]
                    charging_capacity_public = [year_data.get("kWh_charged_in_public", 0) for year, year_data in
                                                years.items()]

                    ax.bar(year_labels, charging_capacity_depot, label="Op depot")
                    ax.bar(year_labels, charging_capacity_public, label="Onderweg", bottom=charging_capacity_depot)

                # Set labels
                ax.set_title(f"Laadbehoefte wagenpark strategie {strategy.split('_')[1]}")
                ax.set_xlabel("jaar")
                ax.set_ylabel("Laadbehoefte per dag (KWh)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # change axes limits
                ymax = max(charging_capacity_public) + max(charging_capacity_depot)
                ax.set_ylim(bottom=0, top=ymax + 20)

                # Set legend
                ax.legend(loc="best")
                # ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

                # Encode graph
                graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    def plot_TCO_fleet_average_charging_time(self, averages: dict):

        """Plots the average TCO fleet cost on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet cost graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():

            graphs[scenario] = {}

            for strategy, years in strategies.items():

                graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

                year_labels = years.keys()
                charging_time_depot = [year_data.get("charging_time_depot", 0) for year, year_data in
                                           years.items()]
                charging_time_public = [year_data.get("charging_time_public", 0) for year, year_data in
                                            years.items()]

                ax.bar(year_labels, charging_time_depot, label="Op depot")
                ax.bar(year_labels, charging_time_public, label="Onderweg", bottom=charging_time_depot)

                # Set labels
                ax.set_title(f"Laadtijd wagenpark strategie {strategy.split('_')[1]}")
                ax.set_xlabel("jaar")
                ax.set_ylabel("Laadtijd per dag (uur)")
                ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                # change axes limits
                ymax = max(charging_time_public) + max(charging_time_depot)
                ax.set_ylim(bottom=0, top=ymax + 20)

                # Set legend
                ax.legend(loc="best")
                # ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

                # Encode graph
                graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                # Close figure
                close()

        return graphs

    # TODO adapt function for scenarios comparison
    def plot_TCO_fleet_average_charging_capacity_scenarios(self, averages: dict):

        """Plots the average TCO fleet cost on a graph.

        :param averages: The average TCO fleet data.
        :type averages: dict

        :return: The TCO fleet cost graphs as base 64 encoded string. Organised by scenario.
        :rtype: dict
        """

        graphs = {}
        for scenario, strategies in averages.items():

            graphs[scenario] = {}

            for strategy, years in strategies.items():
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    graph, ax = subplots(figsize=(8, 8), nrows=1, ncols=1, tight_layout=True)

                    year_labels = years.keys()
                    charging_capacity_depot = [year_data.get("kWh_charged_on_depot", 0) for year, year_data in years.items()]
                    charging_capacity_public = [year_data.get("kWh_charged_in_public", 0) for year, year_data in years.items()]

                    ax.bar(year_labels, charging_capacity_depot, label="Op depot")
                    ax.bar(year_labels, charging_capacity_public, label="Onderweg", bottom=charging_capacity_depot)

                    # Set labels
                    ax.set_title(f"Laadcapaciteit per strategie {strategy.split('_')[1]}")
                    ax.set_xlabel("jaar")
                    ax.set_ylabel("Laadcapaciteit per dag (uur)")
                    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

                    # change axes limits
                    ymax = max(charging_capacity_public) + max(charging_capacity_depot)
                    ax.set_ylim(bottom=0, top=ymax + 20)

                    # Set legend
                    ax.legend(loc="best")
                    # ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))

                    # Encode graph
                    graphs[scenario][strategy] = self.encode_graph_to_base64(graph)

                    # Close figure
                    close()

        return graphs

    def encode_graph_to_base64(self, graph: Figure):

        """Encodes a graph (Figure instance) into a base 64 encoded string.

        :param graph: The graph to be converted.
        :type graph: Figure

        :return: The base 64 encoded graph.
        :rtype: str
        """

        graph_IO_bytes = BytesIO()
        graph.savefig(graph_IO_bytes, format="png")
        graph_IO_bytes.seek(0)
        encoded_graph = b64encode(graph_IO_bytes.getvalue()).decode("UTF-8").replace("\n", "")

        return encoded_graph
