// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import "pages"
import "components"

ApplicationWindow {
    id: window

    width: 1180
    height: 780
    minimumWidth: 1000
    minimumHeight: 680
    visible: true
    title: "Number System Converter"

    property int pageIndex: 0
    property string themeMode: "dark"
    property bool liveConversion: true
    property string defaultBitWidth: "Auto"
    property int settingsRevision: 0

    SystemPalette {
        id: systemPalette
        colorGroup: SystemPalette.Active
    }

    readonly property bool systemDark: ((systemPalette.window.r + systemPalette.window.g + systemPalette.window.b) / 3) < 0.5
    readonly property bool darkMode: themeMode === "dark" || (themeMode === "system" && systemDark)

    readonly property color backgroundColor: darkMode ? "#080A0E" : "#F3F5F8"
    readonly property color panelColor: darkMode ? "#11151B" : "#FFFFFF"
    readonly property color panelAltColor: darkMode ? "#171C23" : "#EDF1F5"
    readonly property color borderColor: darkMode ? "#242A33" : "#DCE2E8"
    readonly property color textColor: darkMode ? "#F5F7FA" : "#11151A"
    readonly property color mutedColor: darkMode ? "#8D96A3" : "#67717E"
    readonly property color accentColor: darkMode ? "#79FFA8" : "#159957"

    color: backgroundColor

    palette.window: backgroundColor
    palette.windowText: textColor
    palette.text: textColor
    palette.buttonText: textColor
    palette.base: panelAltColor
    palette.button: panelAltColor
    palette.highlight: accentColor
    palette.highlightedText: "#07110B"
    palette.placeholderText: mutedColor

    Component.onCompleted: {
        var settings = backend.getSettings()
        themeMode = settings.theme
        liveConversion = settings.liveConversion
        defaultBitWidth = settings.defaultBitWidth
    }

    Connections {
        target: backend

        function onToastRequested(message) {
            toastText.text = message
            toast.opacity = 1
            toastTimer.restart()
        }

        function onSettingsChanged() {
            window.settingsRevision += 1
        }
    }

    Timer {
        id: toastTimer
        interval: 1800
        repeat: false
        onTriggered: toast.opacity = 0
    }

    Rectangle {
        anchors.fill: parent
        color: window.backgroundColor

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 76
                color: window.backgroundColor

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 28
                    anchors.rightMargin: 28
                    spacing: 14

                    Rectangle {
                        width: 42
                        height: 42
                        radius: 13
                        color: Qt.rgba(window.accentColor.r, window.accentColor.g, window.accentColor.b, 0.12)
                        border.width: 1
                        border.color: Qt.rgba(window.accentColor.r, window.accentColor.g, window.accentColor.b, 0.30)

                        Text {
                            anchors.centerIn: parent
                            text: "NSC"
                            color: window.accentColor
                            font.pixelSize: 11
                            font.weight: Font.Bold
                            font.letterSpacing: 0.7
                        }
                    }

                    ColumnLayout {
                        spacing: 1

                        Text {
                            text: "Number System Converter"
                            color: window.textColor
                            font.pixelSize: 16
                            font.weight: Font.DemiBold
                        }

                        Text {
                            text: "TW4RDYDEV"
                            color: window.mutedColor
                            font.pixelSize: 10
                            font.letterSpacing: 1.0
                        }
                    }

                    Rectangle {
                        radius: 8
                        color: window.panelAltColor
                        implicitWidth: 54
                        implicitHeight: 26

                        Text {
                            anchors.centerIn: parent
                            text: backend ? "v" + backend.version : ""
                            color: window.mutedColor
                            font.pixelSize: 10
                            font.weight: Font.DemiBold
                        }
                    }

                    Item { Layout.fillWidth: true }

                    AppButton {
                        text: pageIndex === 0 ? "Settings" : "Converter"
                        outlined: true
                        accentColor: window.accentColor
                        onClicked: pageIndex = pageIndex === 0 ? 1 : 0
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: window.borderColor
            }

            StackLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.leftMargin: 28
                Layout.rightMargin: 28
                Layout.topMargin: 22
                currentIndex: window.pageIndex

                ConverterPage {
                    backgroundColor: window.backgroundColor
                    panelColor: window.panelColor
                    panelAltColor: window.panelAltColor
                    borderColor: window.borderColor
                    textColor: window.textColor
                    mutedColor: window.mutedColor
                    accentColor: window.accentColor
                    liveConversion: window.liveConversion
                    defaultBitWidth: window.defaultBitWidth
                    settingsRevision: window.settingsRevision
                }

                SettingsPage {
                    panelColor: window.panelColor
                    borderColor: window.borderColor
                    textColor: window.textColor
                    mutedColor: window.mutedColor
                    accentColor: window.accentColor

                    onThemeChanged: function(theme) {
                        window.themeMode = theme
                    }

                    onLiveConversionChanged: function(enabled) {
                        window.liveConversion = enabled
                    }

                    onDefaultBitWidthChanged: function(value) {
                        window.defaultBitWidth = value
                    }
                }
            }
        }
    }

    Rectangle {
        id: toast
        width: Math.min(320, toastText.implicitWidth + 38)
        height: 44
        radius: 14
        color: window.darkMode ? "#1A211D" : "#E9F7EF"
        border.width: 1
        border.color: Qt.rgba(window.accentColor.r, window.accentColor.g, window.accentColor.b, 0.32)
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 22
        opacity: 0
        visible: opacity > 0

        Behavior on opacity {
            NumberAnimation { duration: 160 }
        }

        Text {
            id: toastText
            anchors.centerIn: parent
            color: window.darkMode ? "#E9FFF1" : "#0B542B"
            font.pixelSize: 12
            font.weight: Font.DemiBold
        }
    }
}
