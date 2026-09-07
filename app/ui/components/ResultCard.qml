// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: card

    property string title: ""
    property string value: "—"
    property string subtitle: ""
    property color panelColor: "#11151B"
    property color borderColor: "#242A33"
    property color textColor: "#F5F7FA"
    property color mutedColor: "#8D96A3"
    property color accentColor: "#79FFA8"

    signal copyRequested(string value)

    radius: 18
    color: panelColor
    border.width: 1
    border.color: mouseArea.containsMouse ? Qt.rgba(accentColor.r, accentColor.g, accentColor.b, 0.42) : borderColor

    Behavior on border.color {
        ColorAnimation { duration: 140 }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 10

        RowLayout {
            Layout.fillWidth: true

            Text {
                text: card.title
                color: card.mutedColor
                font.pixelSize: 12
                font.weight: Font.DemiBold
                font.letterSpacing: 1.1
            }

            Item { Layout.fillWidth: true }

            Rectangle {
                width: 34
                height: 30
                radius: 9
                color: copyMouse.containsMouse ? Qt.rgba(card.accentColor.r, card.accentColor.g, card.accentColor.b, 0.13) : "transparent"
                border.width: 1
                border.color: Qt.rgba(card.accentColor.r, card.accentColor.g, card.accentColor.b, 0.20)

                Text {
                    anchors.centerIn: parent
                    text: "⧉"
                    color: card.accentColor
                    font.pixelSize: 16
                }

                MouseArea {
                    id: copyMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: card.copyRequested(card.value)
                }
            }
        }

        Text {
            Layout.fillWidth: true
            text: card.value || "—"
            color: card.textColor
            font.family: "Cascadia Mono"
            font.pixelSize: card.value.length > 34 ? 17 : 22
            font.weight: Font.DemiBold
            wrapMode: Text.WrapAnywhere
        }

        Text {
            Layout.fillWidth: true
            text: card.subtitle
            color: card.mutedColor
            font.pixelSize: 11
            visible: text.length > 0
        }

        Item { Layout.fillHeight: true }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        acceptedButtons: Qt.NoButton
        hoverEnabled: true
        propagateComposedEvents: true
    }
}
