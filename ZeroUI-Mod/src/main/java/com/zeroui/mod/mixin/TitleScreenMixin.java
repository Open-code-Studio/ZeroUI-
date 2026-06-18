package com.zeroui.mod.mixin;

import com.zeroui.mod.ZeroUIMod;
import com.zeroui.mod.config.ZeroUIConfig;
import com.zeroui.mod.screen.ZeroUISettingsScreen;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.screen.TitleScreen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.text.Text;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(TitleScreen.class)
public abstract class TitleScreenMixin extends Screen {

    protected TitleScreenMixin(Text title) { super(title); }

    @Inject(method = "initWidgetsNormal", at = @At("TAIL"))
    private void addZeroUIButton(int y, int spacingY, CallbackInfo ci) {
        // Add ZeroUI settings button
        this.addDrawableChild(ButtonWidget.builder(
                Text.literal("ZeroUI 设置"),
                button -> MinecraftClient.getInstance().setScreen(
                        new ZeroUISettingsScreen(this)
                ))
                .dimensions(this.width / 2 - 100, y + spacingY * 4, 200, 20)
                .build());
    }

    @Inject(method = "render", at = @At("HEAD"))
    private void onRender(DrawContext context, int mouseX, int mouseY, float delta, CallbackInfo ci) {
        ZeroUIConfig cfg = ZeroUIMod.CONFIG;
        if (cfg != null && cfg.isCustomTitleBackground()) {
            // Draw custom dark background overlay
            int color = cfg.getTitleBackgroundColor();
            int r = (color >> 16) & 0xFF;
            int g = (color >> 8) & 0xFF;
            int b = color & 0xFF;
            // Draw half-transparent dark overlay over the entire screen
            context.fill(0, 0, this.width, this.height, (r << 16) | (g << 8) | b | 0xC0000000);
        }
    }
}
