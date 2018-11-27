# coding: utf-8
"""*****************************************************************************
* Copyright (C) 2018 Microchip Technology Inc. and its subsidiaries.
*
* Subject to your compliance with these terms, you may use Microchip software
* and any derivatives exclusively with Microchip products. It is your
* responsibility to comply with third party license terms applicable to your
* use of third party software (including open source software) that may
* accompany Microchip software.
*
* THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
* EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
* WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
* PARTICULAR PURPOSE.
*
* IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE,
* INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND
* WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS
* BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
* FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
* ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
* THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
*****************************************************************************"""

################################################################################
#### Component ####
################################################################################

def sst26SetMemoryDependency(symbol, event):
    if (event["value"] == True):
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def instantiateComponent(sst26Component):

    res = Database.activateComponents(["HarmonyCore"])

    sst26PLIB = sst26Component.createStringSymbol("DRV_SST26_PLIB", None)
    sst26PLIB.setLabel("PLIB Used")
    sst26PLIB.setReadOnly(True)

    ##### Do not modify below symbol names as they are used by Memory Driver #####
    sst26MemoryDriver = sst26Component.createBooleanSymbol("DRV_MEMORY_CONNECTED", None)
    sst26MemoryDriver.setLabel("Memory Driver Connected")
    sst26MemoryDriver.setVisible(False)
    sst26MemoryDriver.setDefaultValue(False)

    sst26MemoryStartAddr = sst26Component.createHexSymbol("START_ADDRESS", None)
    sst26MemoryStartAddr.setLabel("SST26 Start Address")
    sst26MemoryStartAddr.setVisible(True)
    sst26MemoryStartAddr.setDefaultValue(0x0000000)

    sst26MemoryInterruptEnable = sst26Component.createBooleanSymbol("INTERRUPT_ENABLE", None)
    sst26MemoryInterruptEnable.setLabel("SST26 Interrupt Enable")
    sst26MemoryInterruptEnable.setVisible(False)
    sst26MemoryInterruptEnable.setDefaultValue(False)
    sst26MemoryInterruptEnable.setReadOnly(True)

    sst26MemoryEraseEnable = sst26Component.createBooleanSymbol("ERASE_ENABLE", None)
    sst26MemoryEraseEnable.setLabel("SST26 Erase Enable")
    sst26MemoryEraseEnable.setVisible(False)
    sst26MemoryEraseEnable.setDefaultValue(True)
    sst26MemoryEraseEnable.setReadOnly(True)

    sst26MemoryEraseBufferSize = sst26Component.createIntegerSymbol("ERASE_BUFFER_SIZE", None)
    sst26MemoryEraseBufferSize.setLabel("SST26 Erase Buffer Size")
    sst26MemoryEraseBufferSize.setVisible(False)
    sst26MemoryEraseBufferSize.setDefaultValue(4096)
    sst26MemoryEraseBufferSize.setDependencies(sst26SetMemoryDependency, ["DRV_MEMORY_CONNECTED", "ERASE_ENABLE"])

    sst26MemoryEraseComment = sst26Component.createCommentSymbol("ERASE_COMMENT", None)
    sst26MemoryEraseComment.setVisible(False)
    sst26MemoryEraseComment.setLabel("*** Should be equal to Sector Erase Size ***")
    sst26MemoryEraseComment.setDependencies(sst26SetMemoryDependency, ["DRV_MEMORY_CONNECTED", "ERASE_ENABLE"])

    ############################################################################
    #### Code Generation ####
    ############################################################################

    configName = Variables.get("__CONFIGURATION_NAME")

    sst26HeaderFile = sst26Component.createFileSymbol("DRV_SST26_HEADER", None)
    sst26HeaderFile.setSourcePath("driver/sst26/drv_sst26.h")
    sst26HeaderFile.setOutputName("drv_sst26.h")
    sst26HeaderFile.setDestPath("driver/sst26/")
    sst26HeaderFile.setProjectPath("config/" + configName + "/driver/sst26/")
    sst26HeaderFile.setType("HEADER")
    sst26HeaderFile.setOverwrite(True)

    sst26AsyncHeaderLocalFile = sst26Component.createFileSymbol("DRV_SST26_HEADER_LOCAL", None)
    sst26AsyncHeaderLocalFile.setSourcePath("driver/sst26/src/drv_sst26_local.h")
    sst26AsyncHeaderLocalFile.setOutputName("drv_sst26_local.h")
    sst26AsyncHeaderLocalFile.setDestPath("driver/sst26/src")
    sst26AsyncHeaderLocalFile.setProjectPath("config/" + configName + "/driver/sst26/")
    sst26AsyncHeaderLocalFile.setType("HEADER")
    sst26AsyncHeaderLocalFile.setOverwrite(True)

    sst26HeaderDefFile = sst26Component.createFileSymbol("DRV_SST26_HEADER_DEF", None)
    sst26HeaderDefFile.setSourcePath("driver/sst26/templates/drv_sst26_definitions.h.ftl")
    sst26HeaderDefFile.setOutputName("drv_sst26_definitions.h")
    sst26HeaderDefFile.setDestPath("driver/sst26/")
    sst26HeaderDefFile.setProjectPath("config/" + configName + "/driver/sst26/")
    sst26HeaderDefFile.setType("HEADER")
    sst26HeaderDefFile.setOverwrite(True)
    sst26HeaderDefFile.setMarkup(True)

    sst26SourceFile = sst26Component.createFileSymbol("DRV_SST26_SOURCE", None)
    sst26SourceFile.setSourcePath("driver/sst26/src/drv_sst26.c")
    sst26SourceFile.setOutputName("drv_sst26.c")
    sst26SourceFile.setDestPath("driver/sst26/src/")
    sst26SourceFile.setProjectPath("config/" + configName + "/driver/sst26/")
    sst26SourceFile.setType("SOURCE")
    sst26SourceFile.setOverwrite(True)

    # System Template Files
    sst26SystemDefFile = sst26Component.createFileSymbol("DRV_SST26_SYS_DEF", None)
    sst26SystemDefFile.setType("STRING")
    sst26SystemDefFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_INCLUDES")
    sst26SystemDefFile.setSourcePath("driver/sst26/templates/system/system_definitions.h.ftl")
    sst26SystemDefFile.setMarkup(True)

    sst26SystemDefObjFile = sst26Component.createFileSymbol("DRV_SST26_SYS_DEF_OBJ", None)
    sst26SystemDefObjFile.setType("STRING")
    sst26SystemDefObjFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_OBJECTS")
    sst26SystemDefObjFile.setSourcePath("driver/sst26/templates/system/system_definitions_objects.h.ftl")
    sst26SystemDefObjFile.setMarkup(True)

    sst26SystemConfigFile = sst26Component.createFileSymbol("DRV_SST26_SYS_CFG", None)
    sst26SystemConfigFile.setType("STRING")
    sst26SystemConfigFile.setOutputName("core.LIST_SYSTEM_CONFIG_H_DRIVER_CONFIGURATION")
    sst26SystemConfigFile.setSourcePath("driver/sst26/templates/system/system_config.h.ftl")
    sst26SystemConfigFile.setMarkup(True)

    sst26SystemInitDataFile = sst26Component.createFileSymbol("DRV_SST26_SYS_INIT_DATA", None)
    sst26SystemInitDataFile.setType("STRING")
    sst26SystemInitDataFile.setOutputName("core.LIST_SYSTEM_INIT_C_DRIVER_INITIALIZATION_DATA")
    sst26SystemInitDataFile.setSourcePath("driver/sst26/templates/system/system_initialize_data.c.ftl")
    sst26SystemInitDataFile.setMarkup(True)

    sst26SystemInitFile = sst26Component.createFileSymbol("DRV_SST26_SYS_INIT", None)
    sst26SystemInitFile.setType("STRING")
    sst26SystemInitFile.setOutputName("core.LIST_SYSTEM_INIT_C_SYS_INITIALIZE_DRIVERS")
    sst26SystemInitFile.setSourcePath("driver/sst26/templates/system/system_initialize.c.ftl")
    sst26SystemInitFile.setMarkup(True)

def onAttachmentConnected(source, target):
    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]

    if connectID == "drv_sst26_QSPI_dependency" :
        plibUsed = localComponent.getSymbolByID("DRV_SST26_PLIB")
        plibUsed.clearValue()
        plibUsed.setValue(remoteID.upper(), 2)

def onAttachmentDisconnected(source, target):
    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]

    if connectID == "drv_sst26_QSPI_dependency" :
        plibUsed = localComponent.getSymbolByID("DRV_SST26_PLIB")
        plibUsed.clearValue()
