package com.zeroui.mod;

import com.zeroui.mod.config.ZeroUIConfig;
import net.fabricmc.api.ModInitializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ZeroUIMod implements ModInitializer {
    public static final String MOD_ID = "zeroui";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);
    public static ZeroUIConfig CONFIG;

    @Override
    public void onInitialize() {
        CONFIG = ZeroUIConfig.load();
        LOGGER.info("ZeroUI Mod initialized with theme: {}", CONFIG.getThemeColor());
    }
}
