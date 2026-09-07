// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls

Switch {
    id: control

    property color accentColor: "#79FFA8"
    property color trackOffColor: "#30343B"
    property color knobColor: "#FFFFFF"
    property color textColor: "#FFFFFF"

    indicator: Rectangle {
        implicitWidth: 46
        implicitHeight: 26
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: height / 2
        color: control.checked ? control.accentColor : control.trackOffColor

        Behavior on color {
            ColorAnimation { duration: 150 }
        }

        Rectangle {
            width: 20
            height: 20
            radius: 10
            y: 3
            x: control.checked ? parent.width - width - 3 : 3
            color: control.checked ? "#07110B" : control.knobColor

            Behavior on x {
                NumberAnimation { duration: 160; easing.type: Easing.OutCubic }
            }
        }
    }

    contentItem: Text {
        text: control.text
        color: control.textColor
        leftPadding: control.indicator.width + control.spacing
        verticalAlignment: Text.AlignVCenter
        font.pixelSize: 13
    }
}
