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

drv_i2c_mcc_helpkeyword = "mcc_h3_drv_i2c_configurations"

def handleMessage(messageID, args):

    result_dict = {}

    if (messageID == "REQUEST_CONFIG_PARAMS"):
        if args.get("localComponentID") != None:
            result_dict = Database.sendMessage(args["localComponentID"], "I2C_MASTER_MODE", {"isEnabled":True, "isReadOnly":True})

    return result_dict


def incrementCommonForcedWriteCounter(symbol, event):
    dummyDict = {}
    if (event["value"] == True) and (symbol.getValue() == False):
        symbol.setValue(True)
        dummyDict = Database.sendMessage("drv_i2c", "DRV_FORCE_WRITE_API_COUNTER_INC", dummyDict)
    elif (event["value"] == False) and (symbol.getValue() == True):
        symbol.setValue(False)
        dummyDict = Database.sendMessage("drv_i2c", "DRV_FORCE_WRITE_API_COUNTER_DEC", dummyDict)

def instantiateComponent(i2cComponent, index):
    i2cSymIndex = i2cComponent.createIntegerSymbol("INDEX", None)
    i2cSymIndex.setVisible(False)
    i2cSymIndex.setDefaultValue(index)

    i2cSymPLIB = i2cComponent.createStringSymbol("DRV_I2C_PLIB", None)
    i2cSymPLIB.setLabel("PLIB Used")
    i2cSymPLIB.setHelp(drv_i2c_mcc_helpkeyword)
    i2cSymPLIB.setReadOnly(True)
    i2cSymPLIB.setDefaultValue("")

    i2cSymNumClients = i2cComponent.createIntegerSymbol("DRV_I2C_NUM_CLIENTS", None)
    i2cSymNumClients.setLabel("Number of clients")
    i2cSymNumClients.setHelp(drv_i2c_mcc_helpkeyword)
    i2cSymNumClients.setMax(10)
    i2cSymNumClients.setDefaultValue(1)

    i2cSymQueueSize = i2cComponent.createIntegerSymbol("DRV_I2C_QUEUE_SIZE", None)
    i2cSymQueueSize.setLabel("Transfer Queue Size")
    i2cSymQueueSize.setHelp(drv_i2c_mcc_helpkeyword)
    i2cSymQueueSize.setMax(64)
    i2cSymQueueSize.setVisible((Database.getSymbolValue("drv_i2c", "DRV_I2C_MODE") == "Asynchronous"))
    i2cSymQueueSize.setDefaultValue(2)
    i2cSymQueueSize.setDependencies(asyncModeOptions, ["drv_i2c.DRV_I2C_MODE"])

    i2cSymForcedWriteAPIGen = i2cComponent.createBooleanSymbol("DRV_I2C_INCLUDE_FORCED_WRITE_API", None)
    i2cSymForcedWriteAPIGen.setDefaultValue(False)
    i2cSymForcedWriteAPIGen.setVisible(False)
    i2cSymForcedWriteAPIGen.setDependencies(incrementCommonForcedWriteCounter, ["drv_i2c_I2C_dependency:I2C_INCLUDE_FORCED_WRITE_API"])

    configName = Variables.get("__CONFIGURATION_NAME")

    # System Template Files
    i2cSymSystemDefObjFile = i2cComponent.createFileSymbol("DRV_I2C_FILE_SYS_DEF_OBJ", None)
    i2cSymSystemDefObjFile.setType("STRING")
    i2cSymSystemDefObjFile.setOutputName("core.LIST_SYSTEM_DEFINITIONS_H_OBJECTS")
    i2cSymSystemDefObjFile.setSourcePath("driver/i2c/templates/system/system_definitions_objects.h.ftl")
    i2cSymSystemDefObjFile.setMarkup(True)

    i2cSymSystemConfigFile = i2cComponent.createFileSymbol("DRV_I2C_FILE_SYS_CONFIG", None)
    i2cSymSystemConfigFile.setType("STRING")
    i2cSymSystemConfigFile.setOutputName("core.LIST_SYSTEM_CONFIG_H_DRIVER_CONFIGURATION")
    i2cSymSystemConfigFile.setSourcePath("driver/i2c/templates/system/system_config.h.ftl")
    i2cSymSystemConfigFile.setMarkup(True)

    i2cSymSystemInitDataFile = i2cComponent.createFileSymbol("DRV_I2C_FILE_SYS_INIT_DATA", None)
    i2cSymSystemInitDataFile.setType("STRING")
    i2cSymSystemInitDataFile.setOutputName("core.LIST_SYSTEM_INIT_C_DRIVER_INITIALIZATION_DATA")
    i2cSymSystemInitDataFile.setSourcePath("driver/i2c/templates/system/system_initialize_data.c.ftl")
    i2cSymSystemInitDataFile.setMarkup(True)

    i2cSymSystemInitFile = i2cComponent.createFileSymbol("DRV_I2C_FILE_SYS_INIT", None)
    i2cSymSystemInitFile.setType("STRING")
    i2cSymSystemInitFile.setOutputName("core.LIST_SYSTEM_INIT_C_SYS_INITIALIZE_DRIVERS")
    i2cSymSystemInitFile.setSourcePath("driver/i2c/templates/system/system_initialize.c.ftl")
    i2cSymSystemInitFile.setMarkup(True)

def asyncModeOptions(symbol, event):
    if (event["value"] == "Asynchronous"):
        symbol.setVisible(True)
    else:
        symbol.setVisible(False)

def onAttachmentConnected(source, target):
    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]
    dummyDict = {}

    if connectID == "drv_i2c_I2C_dependency" :
        plibUsed = localComponent.getSymbolByID("DRV_I2C_PLIB")
        plibUsed.clearValue()
        plibUsed.setValue(remoteID.upper())

        # Check if the PLIB has the "I2C_INCLUDE_FORCED_WRITE_API" symbol or not
        plibForcedWriteAPISymVal = Database.getSymbolValue(remoteID, "I2C_INCLUDE_FORCED_WRITE_API")
        if plibForcedWriteAPISymVal != None:
            # PLIB symbol is present, now read the value
            drvForceWriteAPISym = localComponent.getSymbolByID("DRV_I2C_INCLUDE_FORCED_WRITE_API")
            # If the PLIB symbol value is not same as the driver symbol value, update it
            if plibForcedWriteAPISymVal == True and drvForceWriteAPISym.getValue() == False:
                drvForceWriteAPISym.setValue(True)
                dummyDict = Database.sendMessage("drv_i2c", "DRV_FORCE_WRITE_API_COUNTER_INC", dummyDict)
            elif plibForcedWriteAPISymVal == False and drvForceWriteAPISym.getValue() == True:
                drvForceWriteAPISym.setValue(False)
                dummyDict = Database.sendMessage("drv_i2c", "DRV_FORCE_WRITE_API_COUNTER_DEC", dummyDict)

def onAttachmentDisconnected(source, target):
    localComponent = source["component"]
    remoteComponent = target["component"]
    remoteID = remoteComponent.getID()
    connectID = source["id"]
    targetID = target["id"]
    dummyDict = {}

    if connectID == "drv_i2c_I2C_dependency" :
        plibUsed = localComponent.getSymbolByID("DRV_I2C_PLIB")
        plibUsed.clearValue()

        dummyDict = Database.sendMessage(remoteID, "I2C_MASTER_MODE", {"isReadOnly":False})

        # Check if the PLIB has the "I2C_INCLUDE_FORCED_WRITE_API" symbol or not
        plibForcedWriteAPISymVal = Database.getSymbolValue(remoteID, "I2C_INCLUDE_FORCED_WRITE_API")
        if plibForcedWriteAPISymVal != None:
            # PLIB symbol is present, now read the value
            drvForceWriteAPISym = localComponent.getSymbolByID("DRV_I2C_INCLUDE_FORCED_WRITE_API")
            # Clear the driver symbol value if PLIB symbol value was true
            if plibForcedWriteAPISymVal == True:
                drvForceWriteAPISym.setValue(False)
                dummyDict = Database.sendMessage("drv_i2c", "DRV_FORCE_WRITE_API_COUNTER_DEC", dummyDict)
