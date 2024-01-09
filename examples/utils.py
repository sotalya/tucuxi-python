import sotalya.pycli as M


def display_cycle_data(cycle_data):
    for cycle in cycle_data:
        unit = cycle.unit
        parameters = cycle.parameters
        covariates = cycle.covariates
        print(f"======= Start : {M.str(cycle.start)}")
        print(f"======= End : {M.str(cycle.end)}")
        print(f"======= Values")
        for (t, v) in zip(cycle.times[0], cycle.concentrations[0]):
            print(f"========= {t:.4f} - {v:.4f} {unit.value}")
        print(f"======= Parameters : ")
        if len(parameters) == 0:
            print('[]')
        for param in parameters:
            print(f"========= {param.id} : {param.val}")
        print(f"======= Covariates : ")
        if len(covariates) == 0:
            print('[]')
        for covar in covariates:
            print(f"========= {covar.id} : {covar.val}")


def display_computed_data(data):
    if isinstance(data, M.SinglePointsData):
        print(f"===== ID : {data.id}")
        unit = data.unit
        for (t, c) in zip(data.times, data.concentrations):
            print(f"{M.str(t)} : {c[0]:.4f} {unit.value}")
    elif isinstance(data, M.PercentilesData):
        print(f"===== ID : {data.id}")
        print(f"===== Points per hour : {data.nbr_points_per_hour}")
        for (i, rank) in enumerate(data.percentile_ranks):
            print(f"======= Rank : {rank}")
            display_cycle_data(data.cycle_data(i))

    elif isinstance(data, M.SinglePredictionData):
        print(f"===== ID : {data.id}")
        print(f"===== Compartments : {[c.type for c in data.compartment_info]}")
        display_cycle_data(data.cycle_data)
    elif isinstance(data, M.DosageAdjustment):
        display_adjustement(data)
    elif isinstance(data, M.AdjustmentData):
        print(f"===== ID : {data.id}")
        print(f"===== Compartment : {[c.getType for c in data.compartment_info]}")
        print(f"===== Adjustements =====")
        for adj in data.dosage_adjustements:
            display_adjustement(adj)
    else:
        print(f"Unknown computed data type for ID : {data.id}")
        print(data)


def display_adjustement(adj):
    print(f"%%%%% Displaying adjustement %%%%%")
    print(f"%%%%% Compartment : {[c.getType for c in adj.compartment_info]}")
    display_cycle_data(adj.cycle_data)
    print(f"%%%%% Global score : {adj.score}")
    print(f"%%%%% Targets %%%%%")
    for targ in adj.target_evaluation_results:
        print(f"%%%%%%% {targ.target_type} - {targ.score} - {targ.value} {targ.unit}")
    display_dosage_history(adj.dosage_history)


def display_dosage_history(dh):
    print("-------- Dosage History --------")
    print("-------- Formulations and Routes --------")
    for far in dh.formulation_and_route_list:
        print(f"---------- {far}")
    print("-------- Dosages --------")
    for i in range(0, dh.number_of_time_ranges):
        dtrai = dh.dosage_time_range_at_index(i)
        print(f"---------- {dtrai.start_date} to {dtrai.end_date}")
        display_dosage(dtrai.dosage)


def display_dosage(dosage):
    if isinstance(dosage, M.DosageLoop):
        print(f"[Dosage loop ! Details below ]")
        display_dosage(dosage.getDosage)
    elif isinstance(dosage, M.DosageSteadyState):
        print(f"[Dosage steady state ! Last dose at {M.str(dosage.getLastDoseTime)} Details below ]")
        display_dosage(dosage.getDosage)
    elif isinstance(dosage, M.DosageRepeat):
        print(f"[Dosage repeated {dosage.nbTimes} times ! Details below ]")
        display_dosage(dosage.getDosage)
    elif isinstance(dosage, M.DosageSequence):
        print(f"[Dosage Sequence ! Details below ]")
        for i in range(0, dosage.getNumberOfDosages):
            print(f">>>>> Sequence display number #{i + 1}")
            display_dosage(dosage.getDosageAtIndex(i))
    elif isinstance(dosage, M.ParallelDosageSequence):
        print(f"[Parallel Dosage Sequence ! Details below ]")
        for i in range(0, dosage.getNumberOfDosages):
            print(f">>>>> Sequence display number #{i + 1} - Offset {dosage.getOffsetAtIndex(i)}")
            display_dosage(dosage.getDosageAtIndex(i))
    elif isinstance(dosage, M.LastingDose):
        print(
            f"[Lasting dose of {dosage.getDose}{dosage.getDoseUnit}, every {dosage.getTimeStep}, last administrated via {dosage.getLastFormulationAndRoute}]")
    elif isinstance(dosage, M.DailyDose):
        print(
            f"[Daily dose of {dosage.getDose}{dosage.getDoseUnit}, every day at {dosage.getTimeOfDay}, last administrated via {dosage.getLastFormulationAndRoute}]")
    elif isinstance(dosage, M.WeeklyDose):
        print(
            f"[Weekly dose of {dosage.getDose}{dosage.getDoseUnit}, every {dosage.getDayOfWeek} at {dosage.getTimeOfDay}, last administrated via {dosage.getLastFormulationAndRoute}]")
    else:
        print("Error : Dosage type not found !")


def display_computing_query_response(cqr):
    print(f"=== QueryID : {cqr.query_id} ===")
    print(f"=== Status : {cqr.query_status} ===")
    #    print(f"=== DrugModel : {cqr.metadata.drug_model_id} ===")
    print(f"Error message, if there is one :\n {cqr.error_message}")
    print('=' * 50)
    for srd in cqr.responses:
        resp = srd.computing_response
        print(f"===== ID : {resp.id} ===")
        print(f"===== DrugModel : {srd.metadata.drug_model_id} ===")
        print(f"===== Status : {resp.computing_status} ===")
        print(f"===== Computing Time : {resp.computing_time} ===")
        display_computed_data(resp.data)
        print('=' * 50)
