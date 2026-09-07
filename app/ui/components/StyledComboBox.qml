// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls

ComboBox {
    id: control

    property color panelColor: "#11151B"
    property color popupColor: "#171C23"
    property color borderColor: "#303844"
    property color textColor: "#F5F7FA"
    property color mutedColor: "#8D96A3"
    property color accentColor: "#79FFA8"

    implicitHeight: 38

    contentItem: Text {
        leftPadding: 12
        rightPadding: 30
        text: control.displayText
        color: control.textColor
        font.pixelSize: 12
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    indicator: Item {
        width: 28
        height: control.height
        anchors.right: parent.right

        Text {
            anchors.centerIn: parent
            text: "⌄"
            color: control.mutedColor
            font.pixelSize: 16
        }
    }

    background: Rectangle {
        radius: 9
        color: control.panelColor
        border.width: 1
        border.color: control.activeFocus
                      ? Qt.rgba(control.accentColor.r, control.accentColor.g, control.accentColor.b, 0.65)
                      : control.borderColor

        Behavior on border.color {
            ColorAnimation { duration: 120 }
        }
    }

    delegate: ItemDelegate {
        width: control.width
        height: 38
        highlighted: control.highlightedIndex === index

        contentItem: Text {
            text: modelData
            color: highlighted ? "#07110B" : control.textColor
            font.pixelSize: 12
            verticalAlignment: Text.AlignVCenter
            leftPadding: 10
        }

        background: Rectangle {
            color: highlighted
                   ? control.accentColor
                   : (hovered
                      ? Qt.rgba(control.accentColor.r, control.accentColor.g, control.accentColor.b, 0.10)
                      : "transparent")
        }
    }

    popup: Popup {
        y: control.height + 4
        width: control.width
        implicitHeight: contentItem.implicitHeight + 10
        padding: 5

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            spacing: 2
            ScrollIndicator.vertical: ScrollIndicator { }
        }

        background: Rectangle {
            radius: 10
            color: control.popupColor
            border.width: 1
            border.color: control.borderColor
        }
    }
}
