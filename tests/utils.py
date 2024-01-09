import sotalya.pycli as pycli


def display_cycle_data(cycle_data):
    response_string = ""

    for cycle in cycle_data:
        unit = cycle.unit
        parameters = cycle.parameters
        covariates = cycle.covariates
        response_string += f"======= Start : {pycli.str(cycle.start)}\n"
        response_string += f"======= End : {pycli.str(cycle.end)}\n"
        response_string += f"======= Values\n"
        for (t, v) in zip(cycle.times[0], cycle.concentrations[0]):
            response_string += f"========= {t:.4f} - {v:.4f} {unit.value}\n"
        response_string += f"======= Parameters : \n"
        if len(parameters) == 0:
            response_string += "[]\n"
        for param in parameters:
            response_string += f"========= {param.id} : {param.val}\n"
        response_string += f"======= Covariates : \n"
        if len(covariates) == 0:
            response_string += "[]\n"
        for covar in covariates:
            response_string += f"========= {covar.id} : {covar.val}\n"

    return response_string


def display_computed_data(data):
    computed_data_dict = {}

    if isinstance(data, pycli.SinglePointsData):
        computed_data_dict["ID"] = data.id
        unit = data.unit
        values = []
        for (t, c) in zip(data.times, data.concentrations):
            data["time"] = pycli.str(t)
            data["value"] = float("{:.4f}".format(c[0]))
            data["unit"] = unit.value
            values.append(data)
        computed_data_dict["data"] = values
    elif isinstance(data, pycli.PercentilesData):
        computed_data_dict["ID"] = data.id
        computed_data_dict["Points_per_hour"] = data.nbr_points_per_hour
        for (i, rank) in enumerate(data.percentile_ranks):
            response_string += f"======= Rank : {rank}\n"
            response_string += display_cycle_data(data.cycle_data(i))

    elif isinstance(data, pycli.SinglePredictionData):
        computed_data_dict["ID"] = data.id
        response_string += f"===== Compartments : {[c.type for c in data.compartment_info]}\n"
        response_string += display_cycle_data(data.cycle_data)
    elif isinstance(data, pycli.DosageAdjustment):
        response_string += display_adjustment(data)
    elif isinstance(data, pycli.AdjustmentData):
        computed_data_dict["ID"] = data.id
        response_string += f"===== Compartment : {[c.getType for c in data.compartment_info]}\n"
        response_string += f"===== Adjustments ======\n"
        for adj in data.dosage_adjustements:
            response_string += display_adjustment(adj)
    else:
        computed_data_dict["ID"] = f"Unknown computed data type for ID : {data.id}"
        response_string += data

    return response_string


def display_adjustment(adj):
    response_string = ""

    response_string += f"%%%%% Displaying adjustment %%%%%\n"
    response_string += f"%%%%% Compartment : {[c.getType for c in adj.compartment_info]}\n"
    response_string += display_cycle_data(adj.cycle_data)
    response_string += f"%%%%% Global score : {adj.score}\n"
    response_string += f"%%%%% Targets %%%%%\n"
    for targ in adj.target_evaluation_results:
        response_string += f"%%%%%%% {targ.target_type} - {targ.score} - {targ.value} {targ.unit}\n"
    response_string += display_dosage_history(adj.dosage_history)

    return response_string


def display_dosage_history(dh):
    response_string = ""

    response_string += "-------- Dosage History --------\n"
    response_string += "-------- Formulations and Routes --------\n"
    for far in dh.formulation_and_route_list:
        response_string += f"---------- {far}\n"
    response_string += "-------- Dosages --------\n"
    for i in range(0, dh.number_of_time_ranges):
        dtrai = dh.dosage_time_range_at_index(i)
        response_string += f"---------- {dtrai.start_date} to {dtrai.end_date}\n"
        response_string += display_dosage(dtrai.dosage)

    return response_string


def display_dosage(dosage):
    response_string = ""

    if isinstance(dosage, pycli.DosageLoop):
        response_string += f"[Dosage loop ! Details below ]\n"
        response_string += display_dosage(dosage.getDosage)
    elif isinstance(dosage, pycli.DosageSteadyState):
        response_string += f"[Dosage steady state ! Last dose at {pycli.str(dosage.getLastDoseTime)} Details below ]\n"
        response_string += display_dosage(dosage.getDosage)
    elif isinstance(dosage, pycli.DosageRepeat):
        response_string += f"[Dosage repeated {dosage.nbTimes} times ! Details below ]\n"
        response_string += display_dosage(dosage.getDosage)
    elif isinstance(dosage, pycli.DosageSequence):
        response_string += f"[Dosage Sequence ! Details below ]\n"
        for i in range(0, dosage.getNumberOfDosages):
            response_string += f">>>>> Sequence display number #{i + 1}\n"
            response_string += display_dosage(dosage.getDosageAtIndex(i))
    elif isinstance(dosage, pycli.ParallelDosageSequence):
        response_string += f"[Parallel Dosage Sequence ! Details below ]\n"
        for i in range(0, dosage.getNumberOfDosages):
            response_string += f">>>>> Sequence display number #{i + 1} - Offset {dosage.getOffsetAtIndex(i)}\n"
            response_string += display_dosage(dosage.getDosageAtIndex(i))
    elif isinstance(dosage, pycli.LastingDose):
        response_string += (
            f"[Lasting dose of {dosage.getDose}{dosage.getDoseUnit}, every {dosage.getTimeStep}, last administrated via {dosage.getLastFormulationAndRoute}]\n")
    elif isinstance(dosage, pycli.DailyDose):
        response_string += (
            f"[Daily dose of {dosage.getDose}{dosage.getDoseUnit}, every day at {dosage.getTimeOfDay}, last administrated via {dosage.getLastFormulationAndRoute}]\n")
    elif isinstance(dosage, pycli.WeeklyDose):
        response_string += (
            f"[Weekly dose of {dosage.getDose}{dosage.getDoseUnit}, every {dosage.getDayOfWeek} at {dosage.getTimeOfDay}, last administrated via {dosage.getLastFormulationAndRoute}]\n")
    else:
        response_string += "Error : Dosage type not found !\n"

    return response_string


def display_computing_query_response(cqr):
    responses_dict = {}

    responses_dict["QueryID"] = cqr.query_id
    responses_dict["Status"] = cqr.query_status
    #    response_string["DrugModel"] = cqr.metadata.drug_model_id
    responses_dict["ErrorMsg"] = cqr.error_message
    i = 0
    for srd in cqr.responses:
        response = {}
        resp = srd.computing_response
        response["ID"] = resp.id
        response["DrugModel"] = srd.metadata.drug_model_id
        response["Status"] = resp.computing_status
        response["ComputingTime"] = resp.computing_time
        response["ComputedData"] = display_computed_data(resp.data)

        responses_dict[f"Response_{i}"] = response
        i += 1

    return responses_dict
