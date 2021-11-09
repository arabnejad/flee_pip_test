import os
import sys
import subprocess
import pytest
import logging


base = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "FabFlee/config_files"
)

logger = logging.getLogger(__name__)

# GitHub action = 2 cores


def test_mali(run_py):
    ret = run_py("mali", "10")
    assert ret == "OK"


def test_par_mali(run_par):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)
    ret = run_par("mali", "10", "2")
    assert ret == "OK"


def test_burundi(run_py):
    ret = run_py("burundi", "10")
    assert ret == "OK"


def test_par_burundi(run_par):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)
    ret = run_par("burundi", "10", "2")
    assert ret == "OK"


def test_car(run_py):
    ret = run_py("car", "10")
    assert ret == "OK"


def test_par_car(run_par):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)
    ret = run_par("car", "10", "2")
    assert ret == "OK"


def test_ssudan(run_py):
    ret = run_py("ssudan", "10")
    assert ret == "OK"


def test_par_ssudan(run_par):
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)
    ret = run_par("ssudan", "10", "2")
    assert ret == "OK"


@pytest.fixture
def run_py():
    def _run_py(config, simulation_period):
        config_path = os.path.join(base, config)
        current_dir = os.getcwd()
        os.chdir(config_path)

        cmd = ["python3",
               "run.py",
               "input_csv",
               "source_data",
               simulation_period,
               "simsetting.csv",
               "> out.csv"
               ]

        ret = "OK"
        try:
            output = subprocess.check_output(cmd).decode("utf-8")
        except subprocess.CalledProcessError as e:
            ret = "Command '{}' return non-zero exit status: {}\n{}".format(
                " ".join(cmd), e.returncode, e.output
            )

        os.chdir(current_dir)
        return ret
        # assert(output.find('success') >= 0)
    return _run_py


@pytest.fixture
def run_par():
    def _run_par(config, simulation_period, cores):
        config_path = os.path.join(base, config)
        current_dir = os.getcwd()
        cmd = ["mpirun",
               "-np",
               cores,
               "python3",
               "run_par.py",
               "input_csv",
               "source_data",
               simulation_period,
               "simsetting.csv",
               "> out.csv"
               ]

        print("cmd = {}".format(cmd), file=sys.stderr)
        ret = "OK"
        # output = subprocess.check_output(
        #     cmd,
        #     # shell=True,
        #     # capture_output=True,
        #     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        #     text=True,
        #     cwd=config_path
        #     # stderr=subprocess.STDOUT
        # )

        os.chdir(config_path)

        try:
            output = subprocess.check_output(
                cmd,
                # shell=True,
                stderr=subprocess.STDOUT,
                # stdout=sys.stdout,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            # ret = "Command '{}' return non-zero exit status: "
            ret = "{} -- {} -- {}".format(
                e.returncode, e.output, e.stdout
            )

            ret2 = "Command '{}' return non-zero exit status: e.returncode = {} ".format(
                cmd, e.returncode
            )
            ret2 += "e.output= {} e.stdout= {}".format(e.output, e.stdout)

            print("ret2 = {}".format(ret2), file=sys.stderr)
            print("error = {}".format(e), file=sys.stderr)
            print("error.cmd = {}".format(e.cmd), file=sys.stderr)
            with open("out.csv", encoding="utf_8") as csvfile:
                reader = csv.reader(csvfile)
                for r in reader:
                    print("{}".format(r), file=sys.stderr)
                lines = len(list(reader))
                print("lines = {}".format(lines), file=sys.stderr)

        os.chdir(current_dir)
        return ret
        # assert(output.find('success') >= 0)
    return _run_par
