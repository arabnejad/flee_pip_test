import os
import csv
import sys
import subprocess
import pytest
import logging
import glob

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

        cmd = ["python3",
               "run.py",
               "input_csv",
               "source_data",
               simulation_period,
               "simsetting.csv",
               "> out.csv"
               ]
        cmd = " ".join([str(x) for x in cmd])
        try:
            proc = subprocess.Popen(
                [cmd],
                cwd=config_path,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            (stdout, stderr) = proc.communicate()
        except Exception as e:
            raise RuntimeError("Unexpected error: {}".format(e))

        acceptable_err_subprocesse_ret_codes = [0]
        if proc.returncode not in acceptable_err_subprocesse_ret_codes:
            raise RuntimeError(
                "\njob execution encountered an error (return code {})"
                "while executing \ncmd = {}\noutput = {}".format(
                    proc.returncode, cmd, stdout.decode("utf-8")
                )
            )
        proc.terminate()

        # clean generated out.csv file
        if os.path.isfile(os.path.join(config_path, "out.csv")):
            os.remove(os.path.join(config_path, "out.csv"))

        return "OK"
        # assert(output.find('success') >= 0)
    return _run_py


@pytest.fixture
def run_par():
    def _run_par(config, simulation_period, cores):
        config_path = os.path.join(base, config)
        current_dir = os.getcwd()
        cmd = ["mpiexec",
               "-n",
               cores,
               "python3",
               "run_par.py",
               "input_csv",
               "source_data",
               simulation_period,
               "simsetting.csv",
               "> out.csv"
               ]
        cmd = " ".join([str(x) for x in cmd])

        try:
            proc = subprocess.Popen(
                [cmd],
                cwd=config_path,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            (stdout, stderr) = proc.communicate()
        except Exception as e:
            raise RuntimeError("Unexpected error: {}".format(e))

        print("dir list :", file=sys.stderr)
        print(glob.glob("{}/*".format(config_path)), file=sys.stderr)
        print("-----------", file=sys.stderr)
        if os.path.isfile(os.path.join(config_path, "out.csv")):
            with open(os.path.join(config_path, "out.csv"), encoding="utf_8") as csvfile:
                reader = csv.reader(csvfile)
                for r in reader:
                    print("{}".format(r), file=sys.stderr)
                lines = len(list(reader))
                print("lines = {}".format(lines), file=sys.stderr)

        os.system("tree {}".format(config_path))

        acceptable_err_subprocesse_ret_codes = [0]
        if proc.returncode not in acceptable_err_subprocesse_ret_codes:
            raise RuntimeError(
                "\njob execution encountered an error (return code {})"
                "while executing \ncmd = {}\noutput = {}".format(
                    proc.returncode, cmd, stdout.decode("utf-8")
                )
            )
        # print(stdout.decode("utf-8"))
        proc.terminate()
        """
        try:
            output = subprocess.check_output(
                cmd,
                shell=True,
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
            print("dir list :", file=sys.stderr)
            print(glob.glob("*"), file=sys.stderr)
            print("-----------", file=sys.stderr)
            with open("out.csv", encoding="utf_8") as csvfile:
                reader = csv.reader(csvfile)
                for r in reader:
                    print("{}".format(r), file=sys.stderr)
                lines = len(list(reader))
                print("lines = {}".format(lines), file=sys.stderr)

        """
        # clean generated out.csv file
        if os.path.isfile(os.path.join(config_path, "out.csv")):
            os.remove(os.path.join(config_path, "out.csv"))

        return "OK"
        # assert(output.find('success') >= 0)
    return _run_par
