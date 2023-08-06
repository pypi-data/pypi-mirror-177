#!/usr/bin/env python3

description='Command-line interface to pyprocessmacro'

# - [x] use pandect
# - [ ] print info about data set
# - [ ] move code into repository and publish on pypi

import argparse
import logging
import logging.config
import os
import pathlib
import re
import sys

import io
import contextlib

import numpy
import pandas
from pyprocessmacro import Process

import optini

# ignore the depreciation warning using contextlib
# the warnings module approach does not seem to work
# this is the warning in question:
# pyreadstat/__init__.py:17: DeprecationWarning:
# `np.float` is a deprecated alias for the builtin `float`.
captor = io.StringIO()
with contextlib.redirect_stderr(captor):
    import pandect
captor.close()

myself = pathlib.Path(__file__).stem

epilog = '''Common PROCESS models, by number:

Model	Description				Statistical Model
-----	-----------				-----------------
1	moderation (two-way interaction)	(x m x*m -> y)
3	moderation (three-way interaction)	(x m w x*m x*w m*w x*m*w -> y)
4	mediation				(x -> m) (x m -> y)
5	moderated mediation (x -> y)		(x -> m) (x m w x*w -> y)
7	moderated mediation (x -> m)		(x w x*w -> m) (x m -> y)
8	moderated mediation (x -> m, x -> y)	(x w x*w -> m) (x w x*w m -> y)
14	moderated mediation (m -> y)		(x -> m) (x m v m*v -> y)
21	moderated mediation (x -> m, m -> y)	(x w x*w -> m) (x m v m*v -> y)
'''


def fit_model(data):
    keys = {}
    for var in ['X', 'Y', 'W', 'V', 'Z']:
        if optini.opt[var] is not None:
            keys[var.lower()] = optini.opt[var]

    if optini.opt.M:
        keys['m'] = re.split(',', optini.opt.M)
    if optini.opt.Covariates:
        keys['controls'] = re.split(',', optini.opt.Covariates)

    # yyy I think there is an optini bug; type int doesn't seem supported
    model = int(optini.opt.model)

    logging.info(f"fitting PROCESS model number {model}")

    try:
        fit = Process(
            suppr_init=optini.opt.quiet,
            data=data,
            model=model,
            logit=optini.opt.logit,
            boot=optini.opt.boot,
            center=optini.opt.center,
            controls_in=optini.opt.In,
            **keys,
        )
    except Exception as e:
        logging.error(f"{e}")
        sys.exit(1)

    captor = io.StringIO()
    with contextlib.redirect_stdout(captor):
        fit.summary()
    prize = captor.getvalue()
    captor.close()

    if not optini.opt.quiet:
        print(prize)

    if optini.opt.output:
        with open(optini.opt.output, 'w') as f:
            f.write(prize)
        logging.info(f"wrote results file: {optini.opt.output}")


def summarize_data(data):
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.max_rows', None)
    pandas.set_option('precision', 3)
    pandas.set_option('display.float_format', lambda x: '%.3f' % x)
    summary = data.describe().T
    summary = summary[['count', 'mean', 'std', 'min', 'max']]
    f = lambda x: int(x) if x % 1 == 0 else x
    for var in list(summary):
        summary[var] = summary[var].apply(f)
    print(summary)
    sys.exit(0)


def main():
    desc = description
    optini.spec.input.help = 'input file (csv, sav, xls, xlsx)'
    optini.spec.input.type = str
    optini.spec.output.help = 'output file'
    optini.spec.output.type = str
    model = 4
    optini.spec.model.help = f"model number (default: {model})"
    optini.spec.model.type = int
    optini.spec.model.default = model
    optini.spec.logit.help = 'logit link (for binary DVs)'
    boot = 100
    optini.spec.boot.help = f"number of bootstraps (default: {boot})"
    optini.spec.boot.type = int
    optini.spec.boot.default = boot
    center = False
    optini.spec.center.help = f"center variables (default: {center})"
    optini.spec.center.default = center
    optini.spec.Covariates.help = 'covariates; comma-separated list'
    optini.spec.Covariates.type = str
    In = 'all'
    optini.spec.In.help = f"covar paths: all, x_to_m, all_to_y (default: {In})"
    optini.spec.In.type = str
    optini.spec.In.default = In
    optini.spec.X.help = 'X variable'
    optini.spec.X.type = str
    optini.spec.Y.help = 'Y variable'
    optini.spec.Y.type = str
    optini.spec.M.help = 'M variable(s); comma-separated list'
    optini.spec.M.type = str
    optini.spec.W.help = 'W variable'
    optini.spec.W.type = str
    optini.spec.V.help = 'V variable'
    optini.spec.V.type = str
    optini.spec.Z.help = 'Z variable'
    optini.spec.Z.type = str
    optini.spec.summarize.help = 'summarize data'
    optini.spec.Replace.help = 'treat this value as missing (numpy.nan)'
    optini.spec.Replace.type = int
    optini.Config(appname='pyprocess', desc=desc, logging=True, epilog=epilog)

    data, meta = pandect.load(optini.opt.input)

    if optini.opt.Replace:
        data = data.replace(float(optini.opt.Replace), numpy.nan)
    if optini.opt.summarize:
        summarize_data(data)

    fit_model(data)


if __name__ == '__main__':
    main()

