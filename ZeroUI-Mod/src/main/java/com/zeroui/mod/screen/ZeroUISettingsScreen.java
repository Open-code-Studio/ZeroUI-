package com.zeroui.mod.screen;

import com.zeroui.mod.ZeroUIMod;
import com.zeroui.mod.config.ZeroUIConfig;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.client.gui.widget.SliderWidget;
import net.minecraft.client.gui.widget.TextFieldWidget;
import net.minecraft.text.Text;

import java.util.LinkedHashMap;
import java.util.Map;

public class ZeroUISettingsScreen extends Screen {
    private final Screen parent;
    private static final Map<String, Integer> COLORS = new LinkedHashMap<>();
    static {
        COLORS.put("薄荷绿", 0x4AA26F);
        COLORS.put("海蓝",   0x448AFF);
        COLORS.put("紫色",   0xAB47BC);
        COLORS.put("橘色",   0xFF7043);
        COLORS.put("粉色",   0xEC407A);
        COLORS.put("青绿",   0x26A69A);
        COLORS.put("红色",   0xEF5350);
        COLORS.put("琥珀",   0xFFA726);
    }

    public ZeroUISettingsScreen(Screen parent) {
        super(Text.literal("ZeroUI 颜色设置"));
        this.parent = parent;
    }

    @Override
    protected void init() {
        int centerX = this.width / 2;
        int y = 40;
        int btnW = 120;
        int btnH = 20;
        int cols = 4;
        int spacing = 6;

        int i = 0;
        for (Map.Entry<String, Integer> entry : COLORS.entrySet()) {
            String name = entry.getKey();
            int color = entry.getValue();
            int col = i % cols;
            int row = i / cols;
            int bx = centerX - (cols * (btnW + spacing)) / 2 + col * (btnW + spacing);
            int by = y + row * (btnH + spacing);

            boolean selected = ZeroUIMod.CONFIG.getThemeColorRGB() == color;
            Text label = Text.literal(selected ? "✓ " + name : name);
            this.addDrawableChild(ButtonWidget.builder(label, btn -> {
                ZeroUIMod.CONFIG.setThemeColor(String.format("#%06X", color));
                ZeroUIMod.CONFIG.save();
                // Refresh screen
                this.clearAndInit();
            }).dimensions(bx, by, btnW, btnH).build());
            i++;
        }

        // Done button
        this.addDrawableChild(ButtonWidget.builder(
                Text.literal("完成"),
                btn -> this.client.setScreen(parent)
        ).dimensions(centerX - 50, this.height - 40, 100, 20).build());
    }

    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        this.renderBackground(context, mouseX, mouseY, delta);
        context.drawCenteredTextWithShadow(this.textRenderer, this.title, this.width / 2, 15, 0xFFFFFF);
        context.drawCenteredTextWithShadow(this.textRenderer,
                Text.literal("选择主题颜色后重启资源包或按 F3+T 刷新"),
                this.width / 2, this.height - 55, 0xAAAAAA);
        super.render(context, mouseX, mouseY, delta);
    }

    @Override
    public void close() {
        this.client.setScreen(parent);
    }
}
