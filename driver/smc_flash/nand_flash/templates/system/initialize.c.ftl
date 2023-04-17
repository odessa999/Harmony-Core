    /* MISRA C-2012 Rule 11.3, 11.8 deviated below. Deviation record ID -  
     H3_MISRAC_2012_R_11_3_DR_1 & H3_MISRAC_2012_R_11_8_DR_1*/
    <#if core.COVERITY_SUPPRESS_DEVIATION?? && core.COVERITY_SUPPRESS_DEVIATION>   
    #pragma coverity compliance block \
    (deviate:1 "MISRA C-2012 Rule 11.3" "H3_MISRAC_2012_R_11_3_DR_1" )\
    (deviate:1 "MISRA C-2012 Rule 11.8" "H3_MISRAC_2012_R_11_8_DR_1" )   
    </#if>
    
    sysObj.drvNandFlash = DRV_NAND_FLASH_Initialize((SYS_MODULE_INDEX)DRV_NAND_FLASH_INDEX, (SYS_MODULE_INIT *)&drvNandFlashInitData);
        
    <#if core.COVERITY_SUPPRESS_DEVIATION?? && core.COVERITY_SUPPRESS_DEVIATION>
    #pragma coverity compliance end_block "MISRA C-2012 Rule 11.3"
    #pragma coverity compliance end_block "MISRA C-2012 Rule 11.8"       
    </#if> 
    /* MISRAC 2012 deviation block end */