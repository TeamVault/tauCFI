import csv
import os
import sys

import test_config

def gen_pct_string(value):
    return str(float(int(float(value) * float(10000))) / float(100))




def count_analysis(argv, error_files, csv_writers):
    compound_writers = csv_writers["classification_comp_type"]

    for test_target in test_config.configure_targets(argv):
        result = test_target.verify_classification_type_all()

        for opt in result.keys():
            (cs_dict, ct_dict, problem_string) = result[opt]
            error_files[opt].write(problem_string)

            compound_dict = {}
            compound_dict["opt"] = opt
            compound_dict["target"] = cs_dict["target"]
            compound_dict["cs"] = cs_dict["cs"]
            if 0 == int(cs_dict["cs"]):
                compound_dict["cs args perfect"] = "-"
                compound_dict["cs args perfect pct"] = "-"
                compound_dict["cs args problem"] = "-"
                compound_dict["cs args problem pct"] = "-"
                compound_dict["cs non-void correct"] = "-"
                compound_dict["cs non-void correct pct"] = "-"
                compound_dict["cs non-void problem"] = "-"
                compound_dict["cs non-void problem pct"] = "-"
            else:
                compound_dict["cs args perfect"] = str(cs_dict["perfect"])
                compound_dict["cs args perfect pct"] = gen_pct_string(float(cs_dict["perfect"]) / float(cs_dict["cs"]))
                compound_dict["cs args problem"] = str(cs_dict["problems"])
                compound_dict["cs args problem pct"] = gen_pct_string(float(cs_dict["problems"]) / float(cs_dict["cs"]))
                compound_dict["cs non-void correct"] = str(cs_dict["non-void-ok"])
                compound_dict["cs non-void correct pct"] = gen_pct_string(float(cs_dict["non-void-ok"]) / float(cs_dict["cs"]))
                compound_dict["cs non-void problem"] = str(cs_dict["non-void-problem"])
                compound_dict["cs non-void problem pct"] = gen_pct_string(float(cs_dict["non-void-problem"]) / float(cs_dict["cs"]))

            compound_dict["ct"] = ct_dict["ct"]
            if 0 == int(ct_dict["ct"]):
                compound_dict["ct args perfect"] = "-"
                compound_dict["ct args perfect pct"] = "-"
                compound_dict["ct args problem"] = "-"
                compound_dict["ct args problem pct"] = "-"
                compound_dict["ct void correct"] = "-"
                compound_dict["ct void correct pct"] = "-"
                compound_dict["ct void problem"] = "-"
                compound_dict["ct void problem pct"] = "-"
            else:
                compound_dict["ct args perfect"] = str(ct_dict["perfect"])
                compound_dict["ct args perfect pct"] = gen_pct_string(float(ct_dict["perfect"]) / float(ct_dict["ct"]))
                compound_dict["ct args problem"] = str(ct_dict["problems"])
                compound_dict["ct args problem pct"] = gen_pct_string(float(ct_dict["problems"]) / float(ct_dict["ct"]))
                compound_dict["ct void correct"] = str(ct_dict["void-ok"])
                compound_dict["ct void correct pct"] = gen_pct_string(float(ct_dict["void-ok"]) / float(ct_dict["ct"]))
                compound_dict["ct void problem"] = str(ct_dict["void-problem"])
                compound_dict["ct void problem pct"] = gen_pct_string(float(ct_dict["void-problem"]) / float(ct_dict["ct"]))

            compound_writers[opt].writerow(compound_dict)  


def main(argv):
    comp_fieldnames = ["opt", "target"]

    comp_fieldnames += ["cs"]
    comp_fieldnames += ["cs args perfect"]
    comp_fieldnames += ["cs args perfect pct"]
    comp_fieldnames += ["cs args problem"]
    comp_fieldnames += ["cs args problem pct"]
    comp_fieldnames += ["cs non-void correct"]
    comp_fieldnames += ["cs non-void correct pct"]
    comp_fieldnames += ["cs non-void problem"]
    comp_fieldnames += ["cs non-void problem pct"]
    comp_fieldnames += ["ct"]
    comp_fieldnames += ["ct args perfect"]
    comp_fieldnames += ["ct args perfect pct"]
    comp_fieldnames += ["ct args problem"]
    comp_fieldnames += ["ct args problem pct"]
    comp_fieldnames += ["ct void correct"]
    comp_fieldnames += ["ct void correct pct"]
    comp_fieldnames += ["ct void problem"]
    comp_fieldnames += ["ct void problem pct"]

    csv_comp = ("classification_comp_type", comp_fieldnames)

    csv_defs = [csv_comp]

    test_config.run_in_test_environment(argv, "classification_type_count", csv_defs, count_analysis)

main(sys.argv[1:])