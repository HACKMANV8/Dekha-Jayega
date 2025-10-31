import { SagaSession } from "../model/index.js";
import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Paths to Python environment and script
const PYTHON_VENV_PATH = path.join(
  __dirname,
  "../../../Nano banana/nano-banana-python/.venv/Scripts/python.exe"
);
const PYTHON_SCRIPT_PATH = path.join(
  __dirname,
  "../../../Nano banana/nano-banana-python/src/generate_single_image.py"
);

/**
 * Helper function to generate a single image
 */
const generateImage = (prompt, aspectRatio = "1:1", stylePreset = "none") => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn(PYTHON_VENV_PATH, [
      PYTHON_SCRIPT_PATH,
      prompt,
      aspectRatio,
      stylePreset,
    ]);

    let stdout = "";
    let stderr = "";

    pythonProcess.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    pythonProcess.on("close", (code) => {
      if (code !== 0) {
        console.error(`[IMAGE GEN ERROR] Python stderr: ${stderr}`);
        return reject(new Error(`Python process exited with code ${code}`));
      }

      try {
        const result = JSON.parse(stdout);
        if (result.success) {
          resolve(result);
        } else {
          reject(new Error(result.error || "Image generation failed"));
        }
      } catch (error) {
        reject(new Error(`Failed to parse Python output: ${error.message}`));
      }
    });

    pythonProcess.on("error", (error) => {
      reject(new Error(`Failed to start Python process: ${error.message}`));
    });
  });
};

/**
 * Generate images for a saga session
 * Automatically creates images for characters, environments, and key items
 */
export const generateSagaImages = async (req, res) => {
  try {
    const { sessionId, assetTypes = ["characters", "environments"] } = req.body;

    if (!sessionId) {
      return res.status(400).json({
        success: false,
        message: "sessionId is required",
      });
    }

    const sagaSession = await SagaSession.findOne({ sessionId });
    if (!sagaSession) {
      return res.status(404).json({
        success: false,
        message: "Saga session not found",
      });
    }

    console.log(
      `[SAGA IMAGES] Generating images for session ${sessionId}, types: ${assetTypes.join(
        ", "
      )}`
    );

    const generatedAssets = [];
    const errors = [];

    // Generate character portraits
    if (
      assetTypes.includes("characters") &&
      sagaSession.characters &&
      sagaSession.characters.length > 0
    ) {
      console.log(
        `[SAGA IMAGES] Generating ${sagaSession.characters.length} character portraits`
      );

      for (const character of sagaSession.characters) {
        try {
          const prompt =
            character.visual_prompt ||
            character.appearance ||
            `${character.name}, ${character.archetype}, ${character.background}`;

          const result = await generateImage(prompt, "9:16", "photographic");

          generatedAssets.push({
            assetType: "character",
            name: character.name,
            prompt: prompt,
            imageUrl: result.imageUrl,
            model: result.model,
            aspectRatio: "9:16",
            createdAt: new Date(),
          });

          console.log(`[OK] Generated portrait for ${character.name}`);
        } catch (error) {
          console.error(
            `[ERROR] Failed to generate image for ${character.name}:`,
            error.message
          );
          errors.push({
            character: character.name,
            error: error.message,
          });
        }
      }
    }

    // Generate environment/location images
    if (
      assetTypes.includes("environments") &&
      sagaSession.worldLore &&
      sagaSession.worldLore.geography
    ) {
      console.log(`[SAGA IMAGES] Generating world environment images`);

      try {
        const worldPrompt = `${
          sagaSession.worldLore.world_name || "Fantasy world"
        }, ${sagaSession.worldLore.setting || ""}, ${
          sagaSession.worldLore.geography || ""
        }. Epic landscape, atmospheric, detailed environment.`;

        const result = await generateImage(worldPrompt, "16:9", "cinematic");

        generatedAssets.push({
          assetType: "environment",
          name: sagaSession.worldLore.world_name || "World Overview",
          prompt: worldPrompt,
          imageUrl: result.imageUrl,
          model: result.model,
          aspectRatio: "16:9",
          createdAt: new Date(),
        });

        console.log(`[OK] Generated world environment image`);
      } catch (error) {
        console.error(`[ERROR] Failed to generate world image:`, error.message);
        errors.push({
          environment: "World Overview",
          error: error.message,
        });
      }
    }

    // Generate faction emblems/symbols
    if (
      assetTypes.includes("factions") &&
      sagaSession.factions &&
      sagaSession.factions.length > 0
    ) {
      console.log(
        `[SAGA IMAGES] Generating ${sagaSession.factions.length} faction symbols`
      );

      for (const faction of sagaSession.factions) {
        try {
          const prompt = `${
            faction.visual_identity || faction.name
          } faction symbol, emblem, logo design, ${faction.philosophy}`;

          const result = await generateImage(prompt, "1:1", "digital-art");

          generatedAssets.push({
            assetType: "faction",
            name: faction.name,
            prompt: prompt,
            imageUrl: result.imageUrl,
            model: result.model,
            aspectRatio: "1:1",
            createdAt: new Date(),
          });

          console.log(`[OK] Generated emblem for ${faction.name}`);
        } catch (error) {
          console.error(
            `[ERROR] Failed to generate image for ${faction.name}:`,
            error.message
          );
          errors.push({
            faction: faction.name,
            error: error.message,
          });
        }
      }
    }

    // Save generated assets to saga session
    sagaSession.generatedAssets.push(...generatedAssets);
    await sagaSession.save();

    console.log(
      `[SAGA IMAGES] Generated ${generatedAssets.length} images, ${errors.length} errors`
    );

    res.status(200).json({
      success: true,
      message: `Generated ${generatedAssets.length} images for saga session`,
      data: {
        sessionId,
        generatedCount: generatedAssets.length,
        assets: generatedAssets,
        errors: errors.length > 0 ? errors : undefined,
      },
    });
  } catch (error) {
    console.error("[SAGA IMAGES ERROR]:", error.message);
    res.status(500).json({
      success: false,
      message: "Failed to generate saga images",
      error: error.message,
    });
  }
};

/**
 * Generate a single custom image (original endpoint)
 */
export const generateSingleImage = async (req, res) => {
  try {
    const { prompt, aspectRatio = "1:1", stylePreset = "none" } = req.body;

    if (!prompt) {
      return res.status(400).json({
        success: false,
        message: "Prompt is required",
      });
    }

    console.log(`[IMAGE GEN] Generating image with prompt: "${prompt}"`);

    const result = await generateImage(prompt, aspectRatio, stylePreset);

    res.status(200).json({
      success: true,
      message: "Image generated successfully",
      imageUrl: result.imageUrl,
      prompt: result.prompt,
      text: result.text,
      model: result.model,
      aspectRatio,
      stylePreset,
    });
  } catch (error) {
    console.error("[IMAGE GEN ERROR]:", error.message);
    res.status(500).json({
      success: false,
      message: "Failed to generate image",
      error: error.message,
    });
  }
};

/**
 * Auto-generate images after each saga stage completion
 * This can be called automatically by the saga workflow
 */
export const autoGenerateStageImages = async (req, res) => {
  try {
    const { sessionId, stage } = req.body;

    if (!sessionId || !stage) {
      return res.status(400).json({
        success: false,
        message: "sessionId and stage are required",
      });
    }

    const sagaSession = await SagaSession.findOne({ sessionId });
    if (!sagaSession) {
      return res.status(404).json({
        success: false,
        message: "Saga session not found",
      });
    }

    console.log(
      `[AUTO IMAGE GEN] Auto-generating images for session ${sessionId}, stage: ${stage}`
    );

    let assetTypes = [];
    switch (stage) {
      case "world_lore":
        assetTypes = ["environments"];
        break;
      case "factions":
        assetTypes = ["factions"];
        break;
      case "characters":
        assetTypes = ["characters"];
        break;
      case "complete":
        // Generate any missing assets
        assetTypes = ["characters", "environments", "factions"];
        break;
      default:
        return res.status(200).json({
          success: true,
          message: `No auto-generation configured for stage: ${stage}`,
        });
    }

    // Call the saga images generator
    req.body.assetTypes = assetTypes;
    return await generateSagaImages(req, res);
  } catch (error) {
    console.error("[AUTO IMAGE GEN ERROR]:", error.message);
    res.status(500).json({
      success: false,
      message: "Failed to auto-generate stage images",
      error: error.message,
    });
  }
};
