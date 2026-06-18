package com.zeroui.mod.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.annotations.Expose;
import net.fabricmc.loader.api.FabricLoader;

import java.io.*;
import java.nio.file.Path;

public class ZeroUIConfig {
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().excludeFieldsWithoutExposeAnnotation().create();
    private static final Path CONFIG_PATH = FabricLoader.getInstance().getConfigDir().resolve("zeroui.json");

    @Expose private String themeColor = "#4AA26F";
    @Expose private int buttonCornerRadius = 0;
    @Expose private String buttonStyle = "RECTANGLE"; // RECTANGLE, ROUNDED
    @Expose private boolean customTitleBackground = true;
    @Expose private int titleBackgroundColor = 0x141218; // dark surface

    public String getThemeColor() { return themeColor; }
    public void setThemeColor(String c) { this.themeColor = c; }
    public int getButtonCornerRadius() { return buttonCornerRadius; }
    public void setButtonCornerRadius(int r) { this.buttonCornerRadius = r; }
    public String getButtonStyle() { return buttonStyle; }
    public boolean isCustomTitleBackground() { return customTitleBackground; }
    public int getTitleBackgroundColor() { return titleBackgroundColor; }
    public void setTitleBackgroundColor(int c) { this.titleBackgroundColor = c; }

    public int getThemeColorRGB() {
        String hex = themeColor.replace("#", "");
        return Integer.parseInt(hex, 16);
    }

    public static ZeroUIConfig load() {
        if (CONFIG_PATH.toFile().exists()) {
            try (Reader r = new FileReader(CONFIG_PATH.toFile())) {
                return GSON.fromJson(r, ZeroUIConfig.class);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        ZeroUIConfig def = new ZeroUIConfig();
        def.save();
        return def;
    }

    public void save() {
        try (Writer w = new FileWriter(CONFIG_PATH.toFile())) {
            GSON.toJson(this, w);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
