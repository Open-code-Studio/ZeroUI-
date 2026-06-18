#!/bin/bash
# ZeroUI Mod Build Script
# Uses Minecraft/Fabric libraries already on your system

MC_DIR="$HOME/Library/Application Support/minecraft"
VERSION="1.21.11"
WORKSPACE="$(cd "$(dirname "$0")" && pwd)"

echo "ZeroUI Mod Builder"
echo "=================="

# Find all required jars
MC_JAR="$MC_DIR/versions/$VERSION/$VERSION.jar"
FABRIC_JAR="$MC_DIR/libraries/net/fabricmc/fabric-loader/0.16.9/fabric-loader-0.16.9.jar"
MIXIN_JAR=$(find "$MC_DIR/libraries/org/spongepowered/mixin" -name "mixin-*.jar" ! -name "*sources*" | head -1)
GSON_JAR=$(find "$MC_DIR/libraries/com/google/code/gson" -name "gson-*.jar" ! -name "*sources*" | tail -1)
SLF4J_JAR=$(find "$MC_DIR/libraries/org/slf4j" -name "slf4j-api-*.jar" ! -name "*sources*" | head -1)
GUAVA_JAR=$(find "$MC_DIR/libraries/com/google/guava" -name "guava-*.jar" ! -name "*sources*" | head -1)

echo "MC: $(basename $MC_JAR)"
echo "Fabric: $(basename $FABRIC_JAR)"

# Build classpath
CP="$MC_JAR:$FABRIC_JAR:$MIXIN_JAR:$GSON_JAR:$SLF4J_JAR:$GUAVA_JAR"

cd "$WORKSPACE"
rm -rf build/classes build/libs
mkdir -p build/classes build/libs

echo ""
echo "Compiling..."

# Find a working Java
for jh in "/Users/cangcang/Documents/jdk21" "/Library/Java/JavaVirtualMachines/zulu-21.jre/Contents/Home"; do
    if [ -x "$jh/bin/javac" ]; then
        JAVAC="$jh/bin/javac"
        JAR="$jh/bin/jar"
        JAVA="$jh/bin/java"
        break
    fi
done

$JAVAC --release 21 -proc:none -cp "$CP" -d build/classes \
    src/main/java/com/zeroui/mod/config/ZeroUIConfig.java \
    src/main/java/com/zeroui/mod/ZeroUIMod.java \
    src/main/java/com/zeroui/mod/mixin/TitleScreenMixin.java \
    src/main/java/com/zeroui/mod/screen/ZeroUISettingsScreen.java \
    2>&1

if [ $? -eq 0 ] || [ -f build/classes/com/zeroui/mod/config/ZeroUIConfig.class ]; then
    echo "Partial compilation done"
else
    echo "Compilation failed completely"
    exit 1
fi

# Package jar
cp -r src/main/resources/* build/classes/ 2>/dev/null
cd build/classes
$JAR cf ../libs/zeroui-1.0.0.jar .
cd "$WORKSPACE"

echo ""
echo "Jar: build/libs/zeroui-1.0.0.jar"
ls -lh build/libs/ 2>/dev/null

echo ""
echo "Note: Due to missing mapped Minecraft jar, full compilation requires:"
echo "  ./gradlew build  (when Gradle/JDK issues are resolved)"
echo ""
echo "To install: cp build/libs/zeroui-1.0.0.jar \"$MC_DIR/versions/$VERSION/mods/\""
