#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019, Niklas Hauser
#
# This file is part of the modm project.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# -----------------------------------------------------------------------------

import os
from SCons.Script import *
import subprocess
import platform
from modm_tools import gdb, crashdebug

def run_post_mortem_gdb(target, source, env):
	source = str(source[0])

	artifact = ARGUMENTS.get("firmware", None)
	if artifact is None:
		print("\n> Using the newest firmware may be inaccurate!\n"
			  "> Use 'firmware={hash}' argument to specify a specific firmware.\n")
	else:
		artifact = artifact.lower()
		artifactpath = os.path.join(env["CONFIG_ARTIFACT_PATH"], "{}.elf".format(artifact))
		if os.path.isfile(artifactpath):
			source = artifactpath
		else:
			print("\n> Unable to find artifact '{}' in build cache!\n"
					"> Run without artifact argument to use newest firmware.\n".format(artifact))
			return 1

	if not os.path.isfile(env["COREDUMP_FILE"]):
		print("\n> Unable to find coredump file!"
			  "\n> Path '{}' is not a file!"
			  "\n> Use the 'coredump={{path}}' argument to point to a valid coredump file.\n"
			  .format(env["COREDUMP_FILE"]))
		return 1

	backend = crashdebug.CrashDebugBackend(
			binary_path=env.subst("$BASEPATH/modm/ext/crashcatcher/bins"),
			coredump=env["COREDUMP_FILE"])
	gdb.call(source=source, backend=backend, ui=ARGUMENTS.get("ui", "tui"),
			 config=map(env.subst, env.Listify(env.get("MODM_GDBINIT", []))),
			 commands=map(env.subst, env.Listify(env.get("MODM_GDB_COMMANDS", []))))

	return 0

def gdb_post_mortem_debug(env, source, alias="gdb_post_mortem_debug"):
	env["COREDUMP_FILE"] = os.path.relpath(ARGUMENTS.get("coredump", "coredump.txt"))
	action = Action(run_post_mortem_gdb, cmdstr="$DEBUG_COREDUMP_COMSTR")
	return env.AlwaysBuild(env.Alias(alias, source, action))

# -----------------------------------------------------------------------------
def generate(env, **kw):
	env.AddMethod(gdb_post_mortem_debug, "DebugCoredump")

def exists(env):
	return env.Detect("arm-none-eabi-gdb")
