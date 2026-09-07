// Copyright (c) 2026 TW4RDYDEV. All rights reserved.

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"

Item {
    id: page

    property color backgroundColor: "#080A0E"
    property color panelColor: "#11151B"
    property color panelAltColor: "#161B22"
    property color borderColor: "#242A33"
    property color textColor: "#F5F7FA"
    property color mutedColor: "#8D96A3"
    property color accentColor: "#79FFA8"

    property bool liveConversion: true
    property string defaultBitWidth: "Auto"
    property int settingsRevision: 0
    property var lastResult: ({
        ok: false,
        error: "",
        detectedBase: "",
        decimal: "",
        binary: "",
        octal: "",
        hexadecimal: "",
        bitLength: 0,
        byteRequirement: 0,
        parity: "",
        sign: "",
        decimalDigits: 0,
        hexDigits: 0,
        unsignedValue: "",
        signedValue: "",
        twosComplement: "",
        bitWidth: 0
    })

    function bitWidthValue() {
        var text = bitWidth.currentText
        if (text === "8-bit") return 8
        if (text === "16-bit") return 16
        if (text === "32-bit") return 32
        if (text === "64-bit") return 64
        return 0
    }

    function refresh(addHistory) {
        lastResult = backend.convertNumber(
            inputField.text,
            inputBase.currentText,
            bitWidthValue(),
            signedSwitch.checked,
            addHistory
        )
    }

    function applyDefaultBitWidth() {
        var index = bitWidth.find(defaultBitWidth)
        bitWidth.currentIndex = index >= 0 ? index : 0
    }

    function resetInput() {
        inputField.text = ""
        inputBase.currentIndex = 0
        applyDefaultBitWidth()
        signedSwitch.checked = false
        lastResult = ({ ok: false, error: "" })
        inputField.forceActiveFocus()
    }

    Component.onCompleted: {
        applyDefaultBitWidth()
        inputField.forceActiveFocus()
    }

    onDefaultBitWidthChanged: {
        applyDefaultBitWidth()
        if (liveConversion && inputField.text.trim().length > 0)
            liveTimer.restart()
    }

    onLiveConversionChanged: {
        if (liveConversion && inputField.text.trim().length > 0)
            liveTimer.restart()
    }

    onSettingsRevisionChanged: {
        if (liveConversion && inputField.text.trim().length > 0)
            liveTimer.restart()
    }

    Timer {
        id: liveTimer
        interval: 180
        repeat: false
        onTriggered: page.refresh(false)
    }

    Shortcut {
        sequence: "Ctrl+L"
        onActivated: inputField.forceActiveFocus()
    }
    Shortcut {
        sequence: "Ctrl+R"
        onActivated: page.resetInput()
    }
    Shortcut {
        sequence: "Escape"
        onActivated: page.resetInput()
    }
    Shortcut {
        sequence: "Ctrl+C"
        onActivated: {
            if (page.lastResult.ok)
                backend.copyText(page.lastResult.decimal)
        }
    }

    FileDialog {
        id: exportTxtDialog
        title: "Export conversion history"
        fileMode: FileDialog.SaveFile
        nameFilters: ["Text files (*.txt)"]
        defaultSuffix: "txt"
        onAccepted: backend.exportHistory(selectedFile.toString(), "txt")
    }

    FileDialog {
        id: exportCsvDialog
        title: "Export conversion history"
        fileMode: FileDialog.SaveFile
        nameFilters: ["CSV files (*.csv)"]
        defaultSuffix: "csv"
        onAccepted: backend.exportHistory(selectedFile.toString(), "csv")
    }

    ScrollView {
        anchors.fill: parent
        clip: true
        contentWidth: availableWidth

        ColumnLayout {
            width: parent.width
            spacing: 16

            RowLayout {
                Layout.fillWidth: true
                Layout.leftMargin: 4
                Layout.rightMargin: 4

                ColumnLayout {
                    spacing: 4

                    Text {
                        text: "Convert once. See every base."
                        color: page.textColor
                        font.pixelSize: 26
                        font.weight: Font.Bold
                    }

                    Text {
                        text: "Binary, octal, decimal and hexadecimal — with bit-level inspection."
                        color: page.mutedColor
                        font.pixelSize: 13
                    }
                }

                Item { Layout.fillWidth: true }

                Rectangle {
                    radius: 10
                    color: Qt.rgba(page.accentColor.r, page.accentColor.g, page.accentColor.b, 0.08)
                    border.width: 1
                    border.color: Qt.rgba(page.accentColor.r, page.accentColor.g, page.accentColor.b, 0.22)
                    implicitWidth: 150
                    implicitHeight: 36

                    Text {
                        anchors.centerIn: parent
                        text: page.lastResult.ok
                              ? "Detected · " + page.lastResult.detectedBase
                              : "Ready"
                        color: page.accentColor
                        font.pixelSize: 12
                        font.weight: Font.DemiBold
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 154
                radius: 20
                color: page.panelColor
                border.width: 1
                border.color: page.borderColor

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 18
                    spacing: 12

                    ColumnLayout {
                        Layout.preferredWidth: 160
                        spacing: 6

                        Text {
                            text: "INPUT BASE"
                            color: page.mutedColor
                            font.pixelSize: 11
                            font.weight: Font.DemiBold
                            font.letterSpacing: 1
                        }

                        StyledComboBox {
                            id: inputBase
                            Layout.fillWidth: true
                            model: ["Auto", "Binary", "Octal", "Decimal", "Hexadecimal"]
                            panelColor: page.panelAltColor
                            popupColor: page.panelColor
                            borderColor: page.borderColor
                            textColor: page.textColor
                            mutedColor: page.mutedColor
                            accentColor: page.accentColor
                            onActivated: if (page.liveConversion) liveTimer.restart()
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        Text {
                            text: "VALUE"
                            color: page.mutedColor
                            font.pixelSize: 11
                            font.weight: Font.DemiBold
                            font.letterSpacing: 1
                        }

                        StyledTextField {
                            id: inputField
                            Layout.fillWidth: true
                            placeholderText: "Try 415, 0xF3C or 0b11111111"
                            font.family: "Cascadia Mono"
                            font.pixelSize: 14
                            selectByMouse: true
                            panelColor: page.panelAltColor
                            borderColor: page.borderColor
                            textColor: page.textColor
                            mutedColor: page.mutedColor
                            accentColor: page.accentColor
                            onTextChanged: if (page.liveConversion) liveTimer.restart()
                            Keys.onReturnPressed: page.refresh(true)
                        }
                    }

                    ColumnLayout {
                        Layout.preferredWidth: 120
                        spacing: 6

                        Text {
                            text: "BIT WIDTH"
                            color: page.mutedColor
                            font.pixelSize: 11
                            font.weight: Font.DemiBold
                            font.letterSpacing: 1
                        }

                        StyledComboBox {
                            id: bitWidth
                            Layout.fillWidth: true
                            model: ["Auto", "8-bit", "16-bit", "32-bit", "64-bit"]
                            panelColor: page.panelAltColor
                            popupColor: page.panelColor
                            borderColor: page.borderColor
                            textColor: page.textColor
                            mutedColor: page.mutedColor
                            accentColor: page.accentColor
                            onActivated: if (page.liveConversion) liveTimer.restart()
                        }
                    }

                    ColumnLayout {
                        Layout.preferredWidth: 120
                        spacing: 6

                        Text {
                            text: "INTEGER MODE"
                            color: page.mutedColor
                            font.pixelSize: 11
                            font.weight: Font.DemiBold
                            font.letterSpacing: 1
                        }

                        ToggleSwitch {
                            id: signedSwitch
                            text: "Signed"
                            accentColor: page.accentColor
                            textColor: page.textColor
                            ToolTip.visible: hovered
                            ToolTip.delay: 350
                            ToolTip.text: "Signed mode enables negative integers. With Auto width, non-decimal inputs use the smallest whole-byte two's-complement width automatically."
                            onToggled: if (page.liveConversion) liveTimer.restart()
                        }
                    }

                    AppButton {
                        Layout.alignment: Qt.AlignBottom
                        text: "Convert"
                        accentColor: page.accentColor
                        onClicked: page.refresh(true)
                    }

                    AppButton {
                        Layout.alignment: Qt.AlignBottom
                        text: "Reset"
                        accentColor: page.accentColor
                        outlined: true
                        onClicked: page.resetInput()
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 44
                radius: 12
                visible: page.lastResult.error && page.lastResult.error.length > 0
                color: "#241419"
                border.width: 1
                border.color: "#71313D"

                Text {
                    anchors.fill: parent
                    anchors.margins: 12
                    text: page.lastResult.error || ""
                    color: "#FFB5C0"
                    verticalAlignment: Text.AlignVCenter
                    font.pixelSize: 12
                    elide: Text.ElideRight
                }
            }

            GridLayout {
                Layout.fillWidth: true
                columns: 2
                columnSpacing: 14
                rowSpacing: 14

                ResultCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 138
                    title: "DECIMAL"
                    value: page.lastResult.ok ? page.lastResult.decimal : "—"
                    subtitle: "Base 10"
                    panelColor: page.panelColor
                    borderColor: page.borderColor
                    textColor: page.textColor
                    mutedColor: page.mutedColor
                    accentColor: page.accentColor
                    onCopyRequested: function(value) { backend.copyText(value) }
                }

                ResultCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 138
                    title: "BINARY"
                    value: page.lastResult.ok ? page.lastResult.binary : "—"
                    subtitle: "Base 2"
                    panelColor: page.panelColor
                    borderColor: page.borderColor
                    textColor: page.textColor
                    mutedColor: page.mutedColor
                    accentColor: page.accentColor
                    onCopyRequested: function(value) { backend.copyText(value) }
                }

                ResultCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 138
                    title: "OCTAL"
                    value: page.lastResult.ok ? page.lastResult.octal : "—"
                    subtitle: "Base 8"
                    panelColor: page.panelColor
                    borderColor: page.borderColor
                    textColor: page.textColor
                    mutedColor: page.mutedColor
                    accentColor: page.accentColor
                    onCopyRequested: function(value) { backend.copyText(value) }
                }

                ResultCard {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 138
                    title: "HEXADECIMAL"
                    value: page.lastResult.ok ? page.lastResult.hexadecimal : "—"
                    subtitle: "Base 16"
                    panelColor: page.panelColor
                    borderColor: page.borderColor
                    textColor: page.textColor
                    mutedColor: page.mutedColor
                    accentColor: page.accentColor
                    onCopyRequested: function(value) { backend.copyText(value) }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 14

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 250
                    radius: 20
                    color: page.panelColor
                    border.width: 1
                    border.color: page.borderColor

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 18
                        spacing: 10

                        Text {
                            text: "NUMBER INSPECTOR"
                            color: page.mutedColor
                            font.pixelSize: 11
                            font.weight: Font.DemiBold
                            font.letterSpacing: 1
                        }

                        GridLayout {
                            Layout.fillWidth: true
                            columns: 2
                            rowSpacing: 9
                            columnSpacing: 18

                            Repeater {
                                model: [
                                    ["Bit length", page.lastResult.ok ? page.lastResult.bitLength + " bits" : "—"],
                                    ["Bytes required", page.lastResult.ok ? page.lastResult.byteRequirement + " bytes" : "—"],
                                    ["Parity", page.lastResult.ok ? page.lastResult.parity : "—"],
                                    ["Sign", page.lastResult.ok ? page.lastResult.sign : "—"],
                                    ["Decimal digits", page.lastResult.ok ? page.lastResult.decimalDigits : "—"],
                                    ["Hex digits", page.lastResult.ok ? page.lastResult.hexDigits : "—"]
                                ]

                                delegate: RowLayout {
                                    Layout.fillWidth: true
                                    spacing: 8

                                    Text {
                                        text: modelData[0]
                                        color: page.mutedColor
                                        font.pixelSize: 12
                                        Layout.fillWidth: true
                                    }

                                    Text {
                                        text: modelData[1]
                                        color: page.textColor
                                        font.pixelSize: 12
                                        font.family: "Cascadia Mono"
                                    }
                                }
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 1
                            color: page.borderColor
                            visible: page.lastResult.ok && page.lastResult.bitWidth > 0
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            visible: page.lastResult.ok && page.lastResult.bitWidth > 0

                            ColumnLayout {
                                Text {
                                    text: "Unsigned interpretation"
                                    color: page.mutedColor
                                    font.pixelSize: 11
                                }
                                Text {
                                    text: page.lastResult.unsignedValue || "—"
                                    color: page.textColor
                                    font.family: "Cascadia Mono"
                                    font.pixelSize: 13
                                }
                            }

                            Item { Layout.fillWidth: true }

                            ColumnLayout {
                                Text {
                                    text: "Signed interpretation"
                                    color: page.mutedColor
                                    font.pixelSize: 11
                                }
                                Text {
                                    text: page.lastResult.signedValue || "—"
                                    color: page.accentColor
                                    font.family: "Cascadia Mono"
                                    font.pixelSize: 13
                                }
                            }
                        }
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 250
                    radius: 20
                    color: page.panelColor
                    border.width: 1
                    border.color: page.borderColor

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 18
                        spacing: 10

                        RowLayout {
                            Layout.fillWidth: true

                            Text {
                                text: "RECENT CONVERSIONS"
                                color: page.mutedColor
                                font.pixelSize: 11
                                font.weight: Font.DemiBold
                                font.letterSpacing: 1
                            }

                            Item { Layout.fillWidth: true }

                            Text {
                                text: backend ? backend.history.length + " saved" : "0 saved"
                                color: page.mutedColor
                                font.pixelSize: 11
                            }
                        }

                        ListView {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            spacing: 6
                            model: backend ? backend.history : []

                            delegate: Rectangle {
                                width: ListView.view.width
                                height: 46
                                radius: 10
                                color: historyMouse.containsMouse ? page.panelAltColor : "transparent"

                                RowLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: 10
                                    anchors.rightMargin: 8

                                    ColumnLayout {
                                        Layout.fillWidth: true
                                        spacing: 1

                                        Text {
                                            Layout.fillWidth: true
                                            text: modelData.summary
                                            color: page.textColor
                                            font.pixelSize: 11
                                            elide: Text.ElideRight
                                        }

                                        Text {
                                            text: modelData.timestamp
                                            color: page.mutedColor
                                            font.pixelSize: 9
                                        }
                                    }

                                    Text {
                                        text: "⧉"
                                        color: page.accentColor
                                        font.pixelSize: 15

                                        MouseArea {
                                            anchors.fill: parent
                                            anchors.margins: -8
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: backend.copyText(modelData.decimal)
                                        }
                                    }

                                    Text {
                                        text: "×"
                                        color: page.mutedColor
                                        font.pixelSize: 18

                                        MouseArea {
                                            anchors.fill: parent
                                            anchors.margins: -8
                                            cursorShape: Qt.PointingHandCursor
                                            onClicked: backend.deleteHistory(index)
                                        }
                                    }
                                }

                                MouseArea {
                                    id: historyMouse
                                    anchors.fill: parent
                                    acceptedButtons: Qt.NoButton
                                    hoverEnabled: true
                                }
                            }

                            Text {
                                anchors.centerIn: parent
                                visible: !backend || backend.history.length === 0
                                text: "No saved conversions yet."
                                color: page.mutedColor
                                font.pixelSize: 12
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true

                            AppButton {
                                text: "Export TXT"
                                outlined: true
                                accentColor: page.accentColor
                                onClicked: exportTxtDialog.open()
                            }

                            AppButton {
                                text: "Export CSV"
                                outlined: true
                                accentColor: page.accentColor
                                onClicked: exportCsvDialog.open()
                            }

                            Item { Layout.fillWidth: true }

                            AppButton {
                                text: "Clear"
                                outlined: true
                                accentColor: page.accentColor
                                onClicked: backend.clearHistory()
                            }
                        }
                    }
                }
            }

            Item { Layout.preferredHeight: 14 }
        }
    }
}
