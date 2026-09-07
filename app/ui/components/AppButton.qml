// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls

Button {
    id: control

    property color accentColor: "#79FFA8"
    property color textColor: "#08100B"
    property color idleColor: accentColor
    property color hoverColor: Qt.lighter(idleColor, 1.08)
    property bool outlined: false

    implicitHeight: 42
    implicitWidth: 120

    contentItem: Text {
        text: control.text
        color: control.outlined ? control.accentColor : control.textColor
        font.pixelSize: 13
        font.weight: Font.DemiBold
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    background: Rectangle {
        radius: 12
        color: control.outlined
               ? (control.hovered ? Qt.rgba(control.accentColor.r, control.accentColor.g, control.accentColor.b, 0.10) : "transparent")
               : (control.hovered ? control.hoverColor : control.idleColor)
        border.width: control.outlined ? 1 : 0
        border.color: control.accentColor

        Behavior on color {
            ColorAnimation { duration: 130 }
        }
    }

    scale: control.down ? 0.97 : 1.0
    Behavior on scale {
        NumberAnimation { duration: 90; easing.type: Easing.OutCubic }
    }
}
