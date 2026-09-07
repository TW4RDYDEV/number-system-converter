// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../components"

Item {
    id: page

    property color panelColor: "#11151B"
    property color borderColor: "#242A33"
    property color textColor: "#F5F7FA"
    property color mutedColor: "#8D96A3"
    property color accentColor: "#79FFA8"

    signal themeChanged(string theme)
    signal liveConversionChanged(bool enabled)
    signal defaultBitWidthChanged(string value)

    property var currentSettings: ({})

    function reload() {
        currentSettings = backend.getSettings()
        darkTheme.checked = currentSettings.theme === "dark"
        lightTheme.checked = currentSettings.theme === "light"
        systemTheme.checked = currentSettings.theme === "system"
        liveToggle.checked = currentSettings.liveConversion
        uppercaseToggle.checked = currentSettings.uppercaseHex
        groupToggle.checked = currentSettings.groupBinary
        rememberToggle.checked = currentSettings.rememberHistory
        var idx = widthCombo.find(currentSettings.defaultBitWidth)
        widthCombo.currentIndex = idx >= 0 ? idx : 0
    }

    Component.onCompleted: reload()

    ScrollView {
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth

        ColumnLayout {
            width: parent.width
            spacing: 16

            Text {
                text: "Settings"
                color: page.textColor
                font.pixelSize: 28
                font.weight: Font.Bold
            }

            Text {
                text: "Tune appearance, conversion behavior and local history."
                color: page.mutedColor
                font.pixelSize: 13
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: appearanceContent.implicitHeight + 40
                radius: 20
                color: page.panelColor
                border.width: 1
                border.color: page.borderColor

                ColumnLayout {
                    id: appearanceContent
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 12

                    Text {
                        text: "APPEARANCE"
                        color: page.mutedColor
                        font.pixelSize: 11
                        font.weight: Font.DemiBold
                        font.letterSpacing: 1
                    }

                    RowLayout {
                        RadioButton {
                            id: darkTheme
                            text: "Dark"
                            onClicked: {
                                backend.setSetting("theme", "dark")
                                page.themeChanged("dark")
                            }
                        }

                        RadioButton {
                            id: lightTheme
                            text: "Light"
                            onClicked: {
                                backend.setSetting("theme", "light")
                                page.themeChanged("light")
                            }
                        }

                        RadioButton {
                            id: systemTheme
                            text: "System"
                            onClicked: {
                                backend.setSetting("theme", "system")
                                page.themeChanged("system")
                            }
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: conversionContent.implicitHeight + 40
                radius: 20
                color: page.panelColor
                border.width: 1
                border.color: page.borderColor

                ColumnLayout {
                    id: conversionContent
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 14

                    Text {
                        text: "CONVERSION"
                        color: page.mutedColor
                        font.pixelSize: 11
                        font.weight: Font.DemiBold
                        font.letterSpacing: 1
                    }

                    ToggleSwitch {
                        id: liveToggle
                        text: "Live conversion"
                        accentColor: page.accentColor
                        textColor: page.textColor
                        onToggled: {
                            backend.setSetting("liveConversion", checked)
                            page.liveConversionChanged(checked)
                        }
                    }

                    ToggleSwitch {
                        id: uppercaseToggle
                        text: "Uppercase hexadecimal"
                        accentColor: page.accentColor
                        textColor: page.textColor
                        onToggled: backend.setSetting("uppercaseHex", checked)
                    }

                    ToggleSwitch {
                        id: groupToggle
                        text: "Group binary digits"
                        accentColor: page.accentColor
                        textColor: page.textColor
                        onToggled: backend.setSetting("groupBinary", checked)
                    }

                    ToggleSwitch {
                        id: rememberToggle
                        text: "Remember conversion history"
                        accentColor: page.accentColor
                        textColor: page.textColor
                        onToggled: backend.setSetting("rememberHistory", checked)
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 58
                        radius: 12
                        color: "transparent"
                        border.width: 1
                        border.color: page.borderColor

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 14
                            anchors.rightMargin: 10
                            spacing: 12

                            ColumnLayout {
                                spacing: 2

                                Text {
                                    text: "Default bit width"
                                    color: page.textColor
                                    font.pixelSize: 13
                                    font.weight: Font.DemiBold
                                }

                                Text {
                                    text: "Applied when the converter is reset or opened."
                                    color: page.mutedColor
                                    font.pixelSize: 10
                                }
                            }

                            Item { Layout.fillWidth: true }

                            StyledComboBox {
                                id: widthCombo
                                Layout.preferredWidth: 150
                                model: ["Auto", "8-bit", "16-bit", "32-bit", "64-bit"]
                                panelColor: page.panelColor
                                popupColor: page.panelColor
                                borderColor: page.borderColor
                                textColor: page.textColor
                                mutedColor: page.mutedColor
                                accentColor: page.accentColor
                                onActivated: {
                                    backend.setSetting("defaultBitWidth", currentText)
                                    page.defaultBitWidthChanged(currentText)
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: aboutContent.implicitHeight + 40
                radius: 20
                color: page.panelColor
                border.width: 1
                border.color: page.borderColor

                ColumnLayout {
                    id: aboutContent
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 8

                    Text {
                        text: "ABOUT"
                        color: page.mutedColor
                        font.pixelSize: 11
                        font.weight: Font.DemiBold
                        font.letterSpacing: 1
                    }

                    Text {
                        text: backend ? "Number System Converter v" + backend.version : "Number System Converter"
                        color: page.textColor
                        font.pixelSize: 16
                        font.weight: Font.DemiBold
                    }

                    Text {
                        text: "Built by TW4RDYDEV · Python + PySide6/QML"
                        color: page.mutedColor
                        font.pixelSize: 12
                    }

                    Text {
                        text: "Source-available. Commercial use requires prior written permission."
                        color: page.mutedColor
                        font.pixelSize: 11
                        wrapMode: Text.WordWrap
                    }
                }
            }

            Item { Layout.preferredHeight: 14 }
        }
    }
}
