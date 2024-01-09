from pydoc import plain

import matplotlib.pyplot as plt
import numpy as np
import os

from ..tucuxi.utils import *

# import pdb


class Plotter(object):
    """
    * This class handles plotting results from the GlobalTester with matplotlib.
    """

    def __init__(self, outputdir, name, plotargs):
        self.plotargs = plotargs
        self.name = name
        self.outputdir = outputdir

    def plot_percentiles_conc_time(self, tuc_results):
        """
        * This method plots percentiles over time for Tucuxi only
        """
        x = []
        y = []
        for patientset in tuc_results[1]:
            timecount = 0
            for item in patientset:
                x.append(tuc_results[0][timecount])
                y.append(item)
                timecount = timecount + 1
        plt.figure()
        plt.plot(x, y, self.plotargs)
        plt.ylabel('Percentiles')
        plt.xlabel('Time (hrs)')
        plt.savefig('{dir}/{nm}_perc.png'.format(dir=self.outputdir, nm=self.name))
        plt.close()

    def new_plot_percentiles_conc_time(self, tuc_results):
        """
        * This method plots percentiles over time for Tucuxi only
        """
        plt.figure()
        # nbPercs = len(tuc_results) - 1
        for p in range(0, len(tuc_results[1])):
            plt.plot(tuc_results[0], tuc_results[1][p], 'b-')
        plt.ylabel('Percentiles')
        plt.xlabel('Time (hrs)')
        plt.grid(True)
        plt.savefig('{dir}/{nm}_perc.png'.format(dir=self.outputdir, nm=self.name))
        plt.close()

        # If we want individual percentiles
        if False:
            for p in range(0, len(tuc_results[1])):

                plt.figure()
                # nbPercs = len(tuc_results) - 1
                plt.plot(tuc_results[0], tuc_results[1][p], 'b-')
                plt.ylabel('Percentiles {rank}'.format(rank=p))
                plt.xlabel('Time (hrs)')
                plt.grid(True)
                plt.savefig('{dir}/{nm}_perc_{rank}.png'.format(dir=self.outputdir, nm=self.name, rank=p))
                plt.close()

    def plot_reverse(self, results, name):
        # pdb.set_trace()
        plt.figure()
        for i, x in enumerate(results[0]):
            plt.plot(results[0][i], results[1][i])
            plt.ylabel('Reverse')
            plt.xlabel('Predicted Concentration')
            plt.title('Reverse engine curves for ' + name)
            plt.grid(True)
#             plt.savefig('NONMEM_Perc_{time}.png'.format(time = i))
        plt.savefig('{dir}/{nm}.png'.format(dir=self.outputdir, nm=name))
        plt.close()

    def plot_percentiles(self, results, name):
        """
        * This method plots percentiles in CDF format.
        """
        percentiles = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        for i, x in enumerate(results[0]):
            plt.figure()
            plt.plot(results[1][i], percentiles, self.plotargs)
            plt.ylabel('Percentile')
            plt.xlabel('Predicted Concentration')
            plt.title('Percentiles at time ' + str(x))
            plt.grid(True)
#             plt.savefig('NONMEM_Perc_{time}.png'.format(time = i))
            plt.savefig('{dir}/{nm}.png'.format(dir=self.outputdir, nm=name))
            plt.close()

    def plot_all_percentiles_compare(self, tuc_results, nm_results, name):
        """
        * This method plots percentiles over time for Tucuxi and NONMEM
        """
        plt.figure()

        for p in range(0, len(nm_results[1])):
            plt.plot(nm_results[0], nm_results[1][p], 'r-')

        for p in range(0, len(tuc_results[1])):
            plt.plot(tuc_results[0], tuc_results[1][p], 'b-')

        plt.ylabel('Percentiles')
        plt.xlabel('Time (hrs)')
        plt.grid(True)
        plt.savefig('{dir}/{nm}.png'.format(dir=self.outputdir, nm=name))
        plt.savefig('{dir}/{nm}.svg'.format(dir=self.outputdir, nm=name))
        plt.close()

    def plot_percentiles_compare(self, tuc_results, tuc_apriori, nm_results, nm_apriori, name):
        """
        * This method plots percentiles for both NONMEM and Tucuxi in CDF format.
        """
        # pdb.set_trace()
        plt.figure()
        for j in range(0, 9):
            epcurve = []
            npcurve = []
            for i in range(0, len(tuc_results[1])):
                epcurve.append(tuc_results[1][i][j])
            for i in range(0, len(nm_results[1])):
                npcurve.append(nm_results[1][i][j])
            plt.plot(nm_results[0], npcurve, 'r')
            plt.plot(tuc_results[0], epcurve, 'b')

        # plt.plot(nm_apriori[0], nm_apriori[1], 'bo')
        # plt.plot(tuc_apriori[0], tuc_apriori[1], 'g*')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title('apriori')
        plt.grid(True)

        plt.savefig('{dir}/{nm}.png'.format(dir=self.outputdir, nm=name))
        plt.close()

    def plot_pred_vs_pred(self, nm_results, tuc_results, name):
        """
        * This method plots aposteriori results as NONMEM predictions vs. Tucuxi predictions
        """
        # self.rearrange(nm_results, tuc_results)
        print('tucuxi res: ')
        print(tuc_results)
        print('nm res: ')
        print(nm_results)

        plt.figure()
        plt.plot(nm_results[1], tuc_results[1], self.plotargs)
        plt.ylabel('Predicted Concentration TUCUXI')
        plt.xlabel('Predicted Concentration NONMEM')
        plt.title('Tucuxi vs. NONMEM pred/pred')
        rangemax = max(nm_results[1] + tuc_results[1]) * 1.1
        plt.grid(True)
        linerangex = np.arange(0, rangemax * 1.1, 0.5)
        plt.plot(linerangex, linerangex, '-')
#        plt.show()
        plt.savefig('{dir}/{nm}_p_p.png'.format(dir=self.outputdir, nm=name))
        plt.close()

    @staticmethod
    def rearrange(list1, list2):
        nmtup = zip(list1[0], list1[1])
        eztup = zip(list2[0], list2[1])
        list1[0] = [x[0] for x in sorted(nmtup)]
        list1[1] = [x[1] for x in sorted(nmtup)]
        list2[0] = [x[0] for x in sorted(eztup)]
        list2[1] = [x[1] for x in sorted(eztup)]

    def plot_obs_vs_pred(self, nm_results, tuc_results, name):
        """
        * This method plots aposteriori results as Predicted vs observed concentrations for both NONMEM and Tucuxi.
        """
        plt.figure()
        plt.plot(nm_results[0], nm_results[1], 'ro')
        plt.plot(tuc_results[0], tuc_results[1], self.plotargs)
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Observed Concentration')
        plt.title('Tucuxi (blue) vs. NONMEM (red) aposteriori')
        # rangemax = max(nm_results[0] + tuc_results[0] + nm_results[1] + tuc_results[1]) * 1.1
        rangemax = max(max(nm_results[0]), max(tuc_results[0]), max(nm_results[1]), max(tuc_results[1])) * 1.1
        plt.grid(True)
        linerangex = np.arange(0, rangemax * 1.1, 0.5)
        plt.plot(linerangex, linerangex, '-')
#        plt.show()
        plt.savefig('{dir}/{nm}_o_p.png'.format(dir=self.outputdir, nm=name))
        plt.close()

    def plot_obs_vs_pred_with_samples(self, nm_results, tuc_results, samples, name):
        """
        * This method plots aposteriori results as Predicted vs observed concentrations for both NONMEM and Tucuxi.
        """
        plt.figure()
        plt.plot(nm_results[0], nm_results[1], 'ro')
        plt.plot(tuc_results[0], tuc_results[1], self.plotargs)
        plt.plot(samples[0], samples[1], 'go')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Observed Concentration')
        plt.title('Tucuxi (blue) vs. NONMEM (red) aposteriori, samples (green)')
        # rangemax = max(nm_results[0] + tuc_results[0] + nm_results[1] + tuc_results[1]) * 1.1
        rangemax = max(max(nm_results[0]), max(tuc_results[0]), max(nm_results[1]), max(tuc_results[1])) * 1.1
        plt.grid(True)
        linerangex = np.arange(0, rangemax * 1.1, 0.5)
        plt.plot(linerangex, linerangex, '-')
#        plt.show()
        plt.savefig('{dir}/{nm}_o_p_s.png'.format(dir=self.outputdir, nm=name))
        plt.close()

    def plot_single_prediction(self, tuc_results, filename, title):
        """
        * This method plots predicted concentrations over time for apriori results from both NONMEM and Tucuxi same
        * graph.
        """
        plt.figure()
        plt.plot(tuc_results[0][0], tuc_results[0][1], 'b-')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title(title)
        plt.grid(True)
        #        plt.show()
        plt.savefig('{dir}/{nm}_c.png'.format(dir=self.outputdir, nm=filename))
        plt.close()

    def plot_prediction_and_points(self, tuc_results, points, start, filename, title):
        """
        * This method plots predicted concentrations over time for apriori results from both NONMEM and Tucuxi same
        * graph.
        """
        plt.figure()
        colors = ['r', 'b', 'y', 'c', 'm', 'g', 'k', '#ff6600']

        # Print sample by simulation by patient
        for p in points:
            relative_date = ((str_to_datetime(p.time) - start).total_seconds() / 3600.0)

            # TODO : Unit conversion --> NOW, every results in ug/l
            concentration_ugl = p.value
            plt.plot(relative_date, concentration_ugl, color=colors[0], label='sample', marker='.')




        plt.plot(tuc_results[0][0], tuc_results[0][1], 'b-')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title(title)
        plt.grid(True)
        #        plt.show()
        plt.savefig('{dir}/{nm}_c.png'.format(dir=self.outputdir, nm=filename))
        plt.savefig('{dir}/{nm}_c.svg'.format(dir=self.outputdir, nm=filename))
        plt.close()


    def plot_prediction_and_points2(self, tuc_results, points, start, filename, title):
        """
        * This method plots predicted concentrations over time for apriori results from both NONMEM and Tucuxi same
        * graph.
        """
        plt.figure()
        colors = ['r', 'b', 'y', 'c', 'm', 'g', 'k', '#ff6600']

        # Print sample by simulation by patient
        for p in points:
            relative_date = (p['date'] - start).total_seconds() / 3600.0

            # TODO : Unit conversion --> NOW, every results in ug/l
            concentration_ugl = p['obs']
            plt.plot(relative_date, concentration_ugl, color=colors[0], label='sample', marker='.')




        plt.plot(tuc_results[0][0], tuc_results[0][1], 'b-')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title(title)
        plt.grid(True)
        #        plt.show()
        plt.savefig('{dir}/{nm}_c.png'.format(dir=self.outputdir, nm=filename))
        plt.savefig('{dir}/{nm}_c.svg'.format(dir=self.outputdir, nm=filename))
        plt.close()

    def plot_single_prediction_nonmem(self, nm_results, filename, title):
        """
        * This method plots predicted concentrations over time for apriori results from both NONMEM and Tucuxi same
        * graph.
        """
        plt.figure()
        plt.plot(nm_results[0], nm_results[1], 'r-')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title(title)
        plt.grid(True)
        #        plt.show()
        plt.savefig('{dir}/{nm}_c.png'.format(dir=self.outputdir, nm=filename))
        plt.close()

    def plot_adjustments(self, tuc_results, filename, title):
        """
        * This method plots adjustment concentrations over time for apriori results from Tucuxi on the same
        * graph.
        """
        plt.figure()
        for i in range(len(tuc_results)):
            plt.plot(tuc_results[i][1], tuc_results[i][2], 'b-')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title(title)
        plt.grid(True)
        #        plt.show()
        plt.savefig('{dir}/{nm}_a.png'.format(dir=self.outputdir, nm=filename))
        plt.close()

    def plot_c(self, nm_results, tuc_results, filename, title):
        """
        * This method plots predicted concentrations over time for apriori results from both NONMEM and Tucuxi same
        * graph.
        """
        plt.figure()
        plt.plot(nm_results[0], nm_results[1], 'r-')
        plt.plot(tuc_results[0][0], tuc_results[0][1], 'b-')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title(title)
        plt.grid(True)
#        plt.show()
        plt.savefig('{dir}/{nm}_c.png'.format(dir=self.outputdir, nm=filename))
        plt.savefig('{dir}/{nm}_c.svg'.format(dir=self.outputdir, nm=filename))
        plt.close()

    def plot_single_obs_vs_pred(self, results, name):
        """
        * This method plots aposteriori reuslts as Predicted vs Observed concentrations for only one of NONMEM/Tucuxi.
        """
        plt.figure()
        plt.plot(results[0], results[1], 'bo')
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Observed Concentration')
        plt.title('Aposteriori')
        rangemax = max(results[0] + results[1]) * 1.1
        plt.grid(True)
        linerangex = np.arange(0, rangemax * 1.1, 0.5)
        plt.plot(linerangex, linerangex, '-')
#        plt.show()
        plt.savefig('{dir}/{nm}_p_p.png'.format(dir=self.outputdir, nm=name))
        plt.close()

    def plot_models(self, results, filename, title):
        """
        * This method plots predicted concentrations over time for apriori results from both NONMEM and Tucuxi same
        * graph.
        """
        plt.figure()
        colors = ['r-', 'b-', 'y-', 'c-', 'm-', 'g-', 'k', '#ff6600']
        index = 0
        for result in results:
            if len(result['results']) != 0:
                pred = result['results']['apriori']
                plt.plot(pred[0], pred[1], colors[index % len(colors)], label=result['drugModelId'])
                index = index + 1
        plt.legend()
        plt.ylabel('Predicted Concentration')
        plt.xlabel('Time (hrs)')
        plt.title(title)
        plt.grid(True)
        plt.savefig('{dir}/{nm}.png'.format(dir=self.outputdir, nm=filename))
        plt.savefig('{dir}/{nm}.svg'.format(dir=self.outputdir, nm=filename))
        plt.close()

    def plot_prediction_and_sample(self, results, filename, title, models, sim_key):
        """
                * This method plots predicted concentrations over time and samples for different models
                """
        plt.figure()
        # plt.switch_backend('TkAgg') # screen resolution depend on backend
        # mng = plt.get_current_fig_manager()
        # mng.window.state('zoomed')
        colors = ['r', 'b', 'y', 'c', 'm', 'g', 'k', '#ff6600']
        index = 0

        # Print 3 curves (3 drugModels) by simulation by patient
        for model in models:
            times = results['results'][model][sim_key][0][5]
            values = results['results'][model][sim_key][0][6]
            plt.plot(times, values, colors[index % len(colors)], label=model)
            index = index + 1

        # Print sample by simulation by patient
        start_prediction_date = results['results'][model][sim_key][0][7]
        sample_date = results['samples'][int(sim_key)].sampledate
        relative_date = ((sample_date - start_prediction_date).total_seconds() / 3600.0)

        # TODO : Unit conversion --> NOW, every results in ug/l
        concentration_ugl = int(results['samples'][int(sim_key)].concentration) * 1000
        plt.plot(relative_date, concentration_ugl, color=colors[index % len(colors)], label='sample', marker='.')
        plt.legend()
        plt.ylabel('Predicted Concentration (ug/l)')
        plt.xlabel('Time (hrs)')
        plt.title('Predictions and sample (pid:{p},sim:{s})'.format(p=results['id'],s=sim_key))
        plt.grid(True)
        # plt.show()
        plt.savefig('{dir}/{nm}.png'.format(dir=self.outputdir, nm=filename))
        plt.savefig('{dir}/{nm}.svg'.format(dir=self.outputdir, nm=filename))
        plt.close()
