/*
 * Copyright (c) 2016, Niklas Hauser
 *
 * This file is part of the modm project.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
// ----------------------------------------------------------------------------

//
// Arduino UNO
//

#include "arduino_uno.hpp"

modm::IODeviceWrapper< Uart0, modm::IOBuffer::BlockIfFull > serialDevice;
modm::IOStream serialStream(serialDevice);