// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls

TextField {
    id: control

    property color panelColor: "#171C23"
    property color borderColor: "#303844"
    property color textColor: "#F5F7FA"
    property color mutedColor: "#8D96A3"
    property color accentColor: "#79FFA8"

    implicitHeight: 38
    leftPadding: 12
    rightPadding: 12
    color: textColor
    placeholderTextColor: mutedColor
    selectionColor: accentColor
    selectedTextColor: "#07110B"

    background: Rectangle {
        radius: 9
        color: control.panelColor
        border.width: 1
        border.color: control.activeFocus
                      ? Qt.rgba(control.accentColor.r, control.accentColor.g, control.accentColor.b, 0.68)
                      : control.hovered
                        ? Qt.rgba(control.accentColor.r, control.accentColor.g, control.accentColor.b, 0.32)
                        : control.borderColor

        Behavior on border.color {
            ColorAnimation { duration: 120 }
        }
    }
}
