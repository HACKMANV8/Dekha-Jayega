import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";
import { Asset, Project, SagaSession } from "../model/index.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Path to Python interpreter and RenderPrepAgent
const PYTHON_VENV_PATH = path.join(
  __dirname,
  "../../../Hackman_agent-main/.venv/Scripts/python.exe"
);

const RENDER_PREP_SCRIPT = path.join(
  __dirname,
  "../../../Hackman_agent-main/run_render_prep.py"
);

const NANO_BANANA_PYTHON = path.join(
  __dirname,
  "../../../Nano banana/nano-banana-python/.venv/Scripts/python.exe"
);

const NANO_BANANA_SCRIPT = path.join(
  __dirname,
  "../../../Nano banana/nano-banana-python/src/generate_single_image.py"
);

/**
 * Generate prompts using RenderPrepAgent from saga session data
 */
export const generatePromptsFromSaga = async (req, res) => {
  try {
    const {
      sessionId,
      qualityPreset = "standard",
      generateImages = false,
    } = req.body;

    console.log("[RENDER PREP] Request received:", {
      sessionId,
      qualityPreset,
      generateImages,
    });

    if (!sessionId) {
      return res.status(400).json({
        success: false,
        message: "Session ID is required",
      });
    }

    // Fetch saga session data
    const sagaSession = await SagaSession.findById(sessionId);
    if (!sagaSession) {
      console.error("[RENDER PREP] Saga session not found:", sessionId);
      return res.status(404).json({
        success: false,
        message: "Saga session not found",
      });
    }

    console.log("[RENDER PREP] Found saga session:", sagaSession.topic);

    // Prepare saga data for RenderPrepAgent
    const sagaData = {
      concept: sagaSession.concept,
      world_lore: sagaSession.worldLore,
      factions: sagaSession.factions,
      characters: sagaSession.characters,
      plot_arcs: sagaSession.plotArcs,
      questlines: sagaSession.questlines,
    };

    console.log(
      "[RENDER PREP] Running RenderPrepAgent for session:",
      sessionId
    );
    console.log("[RENDER PREP] Quality preset:", qualityPreset);
    console.log("[RENDER PREP] Python path:", PYTHON_VENV_PATH);
    console.log("[RENDER PREP] Script path:", RENDER_PREP_SCRIPT);

    // Create temporary JSON file for saga data
    const tempDataPath = path.join(
      __dirname,
      `../../../temp_saga_${sessionId}.json`
    );
    const fs = await import("fs");
    fs.writeFileSync(tempDataPath, JSON.stringify(sagaData, null, 2));
    console.log("[RENDER PREP] Created temp file:", tempDataPath);

    // Call RenderPrepAgent Python script
    const args = [RENDER_PREP_SCRIPT, tempDataPath, "--quality", qualityPreset];

    if (generateImages) {
      args.push("--generate-images");
    }

    console.log("[RENDER PREP] Spawning Python process with args:", args);

    const python = spawn(PYTHON_VENV_PATH, args);

    let outputData = "";
    let errorData = "";

    python.stdout.on("data", (data) => {
      const output = data.toString();
      outputData += output;
      console.log("[RENDER PREP stdout]:", output);
    });

    python.stderr.on("data", (data) => {
      errorData += data.toString();
      console.error("[RENDER PREP stderr]:", data.toString());
    });

    python.on("error", (error) => {
      console.error("[RENDER PREP] Python process error:", error);

      // Clean up temp file
      try {
        fs.unlinkSync(tempDataPath);
      } catch (e) {
        console.warn("[RENDER PREP] Failed to delete temp file:", e.message);
      }

      return res.status(500).json({
        success: false,
        message: "Failed to start Python process",
        error: error.message,
      });
    });

    python.on("close", async (code) => {
      console.log("[RENDER PREP] Python process closed with code:", code);
      console.log("[RENDER PREP] Output data length:", outputData.length);
      console.log("[RENDER PREP] Error data length:", errorData.length);

      // Clean up temp file
      try {
        fs.unlinkSync(tempDataPath);
        console.log("[RENDER PREP] Temp file deleted");
      } catch (e) {
        console.warn("[RENDER PREP] Failed to delete temp file:", e.message);
      }

      if (code !== 0) {
        console.error("[RENDER PREP] Python process failed with code:", code);
        console.error("[RENDER PREP] Error output:", errorData);
        return res.status(500).json({
          success: false,
          message: "Failed to generate prompts",
          error: errorData || "Python process exited with error code " + code,
        });
      }

      try {
        // Parse the output to extract prompts
        // The Python script exports to saga_exports/renders/ relative to Backend directory
        const exportPath = path.join(__dirname, "../../saga_exports/renders");

        console.log("[RENDER PREP] Looking for exports in:", exportPath);

        const prompts = {
          character_prompts: [],
          environment_prompts: [],
          item_prompts: [],
          storyboard_prompts: [],
        };

        // Read exported JSON files (find the most recent ones)
        try {
          if (!fs.existsSync(exportPath)) {
            console.warn(
              "[RENDER PREP] Export directory does not exist:",
              exportPath
            );
            throw new Error("Export directory not found");
          }

          // Get all files in the directory
          const files = fs.readdirSync(exportPath);
          console.log("[RENDER PREP] Found files:", files);

          // Find the most recent character prompts file
          const characterFiles = files.filter(
            (f) => f.includes("characters_prompts") && f.endsWith(".json")
          );
          if (characterFiles.length > 0) {
            const latestCharFile = characterFiles.sort().reverse()[0];
            const characterPromptsPath = path.join(exportPath, latestCharFile);
            console.log(
              "[RENDER PREP] Reading character prompts from:",
              latestCharFile
            );
            const charData = JSON.parse(
              fs.readFileSync(characterPromptsPath, "utf-8")
            );
            prompts.character_prompts = charData.prompts || [];
          }

          // Find the most recent environment prompts file
          const environmentFiles = files.filter(
            (f) => f.includes("environments_prompts") && f.endsWith(".json")
          );
          if (environmentFiles.length > 0) {
            const latestEnvFile = environmentFiles.sort().reverse()[0];
            const environmentPromptsPath = path.join(exportPath, latestEnvFile);
            console.log(
              "[RENDER PREP] Reading environment prompts from:",
              latestEnvFile
            );
            const envData = JSON.parse(
              fs.readFileSync(environmentPromptsPath, "utf-8")
            );
            prompts.environment_prompts = envData.prompts || [];
          }

          // Find the most recent item prompts file
          const itemFiles = files.filter(
            (f) => f.includes("items_prompts") && f.endsWith(".json")
          );
          if (itemFiles.length > 0) {
            const latestItemFile = itemFiles.sort().reverse()[0];
            const itemPromptsPath = path.join(exportPath, latestItemFile);
            console.log(
              "[RENDER PREP] Reading item prompts from:",
              latestItemFile
            );
            const itemData = JSON.parse(
              fs.readFileSync(itemPromptsPath, "utf-8")
            );
            prompts.item_prompts = itemData.prompts || [];
          }

          // Find the most recent storyboard prompts file
          const storyboardFiles = files.filter(
            (f) => f.includes("storyboards_prompts") && f.endsWith(".json")
          );
          if (storyboardFiles.length > 0) {
            const latestStoryFile = storyboardFiles.sort().reverse()[0];
            const storyboardPromptsPath = path.join(
              exportPath,
              latestStoryFile
            );
            console.log(
              "[RENDER PREP] Reading storyboard prompts from:",
              latestStoryFile
            );
            const storyData = JSON.parse(
              fs.readFileSync(storyboardPromptsPath, "utf-8")
            );
            prompts.storyboard_prompts = storyData.prompts || [];
          }

          console.log("[RENDER PREP] Loaded prompts:", {
            characters: prompts.character_prompts.length,
            environments: prompts.environment_prompts.length,
            items: prompts.item_prompts.length,
            storyboards: prompts.storyboard_prompts.length,
          });
        } catch (readError) {
          console.warn("Error reading exported prompts:", readError.message);
        }

        // Store prompts as assets in MongoDB
        const assets = [];

        // Check if assets already exist for this project and delete them to avoid duplicates
        const existingAssets = await Asset.find({
          projectId: sagaSession.projectId,
        });
        if (existingAssets.length > 0) {
          console.log(
            `[RENDER PREP] Found ${existingAssets.length} existing assets, deleting to avoid duplicates...`
          );
          await Asset.deleteMany({ projectId: sagaSession.projectId });
        }

        // Store character prompts
        for (const charPrompt of prompts.character_prompts) {
          const asset = new Asset({
            projectId: sagaSession.projectId,
            name: charPrompt.name || "Character Asset",
            type: "character-concept",
            category: "image",
            prompts: {
              detailed: charPrompt.positive_prompt || charPrompt.prompt || "",
              style: charPrompt.metadata?.art_style || "",
              technical: charPrompt.negative_prompt || "",
            },
            metadata: {
              resolution: "1024x1024",
              aspectRatio: "1:1",
              style: qualityPreset,
              tags: [],
              sourceData: charPrompt,
            },
            status: "pending",
          });
          await asset.save();
          assets.push(asset);
        }

        // Store environment prompts
        for (const envPrompt of prompts.environment_prompts) {
          const asset = new Asset({
            projectId: sagaSession.projectId,
            name: envPrompt.name || "Environment Asset",
            type: "environment",
            category: "image",
            prompts: {
              detailed: envPrompt.positive_prompt || envPrompt.prompt || "",
              style: envPrompt.metadata?.art_style || "",
              technical: envPrompt.negative_prompt || "",
            },
            metadata: {
              resolution: "1920x1080",
              aspectRatio: "16:9",
              style: qualityPreset,
              tags: [],
              sourceData: envPrompt,
            },
            status: "pending",
          });
          await asset.save();
          assets.push(asset);
        }

        // Store item prompts
        for (const itemPrompt of prompts.item_prompts) {
          const asset = new Asset({
            projectId: sagaSession.projectId,
            name: itemPrompt.name || "Item Asset",
            type: "prop",
            category: "image",
            prompts: {
              detailed: itemPrompt.positive_prompt || itemPrompt.prompt || "",
              style: itemPrompt.metadata?.art_style || "",
              technical: itemPrompt.negative_prompt || "",
            },
            metadata: {
              resolution: "1024x1024",
              aspectRatio: "1:1",
              style: qualityPreset,
              tags: [],
              sourceData: itemPrompt,
            },
            status: "pending",
          });
          await asset.save();
          assets.push(asset);
        }

        // Store storyboard prompts
        for (const storyPrompt of prompts.storyboard_prompts) {
          const asset = new Asset({
            projectId: sagaSession.projectId,
            name: storyPrompt.name || "Storyboard Asset",
            type: "storyboard",
            category: "image",
            prompts: {
              detailed: storyPrompt.positive_prompt || storyPrompt.prompt || "",
              style: storyPrompt.metadata?.art_style || "",
              technical: storyPrompt.negative_prompt || "",
            },
            metadata: {
              resolution: "1920x1080",
              aspectRatio: "16:9",
              style: qualityPreset,
              tags: [],
              sourceData: storyPrompt,
            },
            status: "pending",
          });
          await asset.save();
          assets.push(asset);
        }

        // Update saga session with asset references
        sagaSession.renderPrepCompleted = true;
        sagaSession.renderPrepAssets = assets.map((a) => a._id);
        await sagaSession.save();

        res.status(200).json({
          success: true,
          message: "Prompts generated successfully",
          data: {
            sessionId,
            prompts,
            assets: assets.map((a) => ({
              _id: a._id,
              id: a._id,
              name: a.name,
              type: a.type,
              prompt: a.prompts.detailed,
              url: a.url,
              status: a.status,
              metadata: a.metadata,
            })),
            totalPrompts: assets.length,
          },
        });
      } catch (parseError) {
        console.error("Error parsing RenderPrep output:", parseError);
        return res.status(500).json({
          success: false,
          message: "Failed to parse RenderPrep output",
          error: parseError.message,
        });
      }
    });
  } catch (error) {
    console.error("RenderPrepAgent error:", error);
    res.status(500).json({
      success: false,
      message: "Failed to generate prompts",
      error: error.message,
    });
  }
};

/**
 * Generate image from asset prompt using Nano Banana
 */
export const generateImageFromAsset = async (req, res) => {
  try {
    const { assetId } = req.params;

    console.log("[IMAGE GEN] Request for asset:", assetId);

    const asset = await Asset.findById(assetId);
    if (!asset) {
      console.error("[IMAGE GEN] Asset not found:", assetId);
      return res.status(404).json({
        success: false,
        message: "Asset not found",
      });
    }

    console.log(
      "[IMAGE GEN] Found asset:",
      asset.name,
      "Status:",
      asset.status
    );

    if (asset.status === "completed") {
      console.log("[IMAGE GEN] Image already generated");
      return res.status(400).json({
        success: false,
        message: "Image already generated for this asset",
        data: {
          imageUrl: asset.url,
        },
      });
    }

    const prompt = asset.prompts.detailed;
    console.log("[IMAGE GEN] Generating image for asset:", assetId);
    console.log("[IMAGE GEN] Prompt length:", prompt.length);
    console.log("[IMAGE GEN] Python path:", NANO_BANANA_PYTHON);
    console.log("[IMAGE GEN] Script path:", NANO_BANANA_SCRIPT);

    // Call Nano Banana Python script
    const python = spawn(NANO_BANANA_PYTHON, [
      NANO_BANANA_SCRIPT,
      "--prompt",
      prompt,
    ]);

    let imageData = "";
    let errorData = "";

    python.stdout.on("data", (data) => {
      const output = data.toString();
      imageData += output;
      console.log("[IMAGE GEN stdout]:", output.substring(0, 200));
    });

    python.stderr.on("data", (data) => {
      errorData += data.toString();
      console.error("Nano Banana stderr:", data.toString());
    });

    python.on("close", async (code) => {
      console.log("[IMAGE GEN] Process closed with code:", code);
      console.log("[IMAGE GEN] Output data length:", imageData.length);
      console.log("[IMAGE GEN] Error data length:", errorData.length);

      if (code !== 0) {
        console.error("[IMAGE GEN] Nano Banana failed:", errorData);
        asset.status = "failed";
        asset.errorMessage = errorData;
        await asset.save();

        return res.status(500).json({
          success: false,
          message: "Failed to generate image",
          error: errorData,
        });
      }

      try {
        console.log("[IMAGE GEN] Parsing output...");
        const result = JSON.parse(imageData);
        console.log("[IMAGE GEN] Parsed result:", result);

        // Update asset with generated image (Python script returns 'imageUrl')
        asset.url = result.imageUrl || result.image_url || result.url;
        asset.status = "completed";
        asset.generatedAt = new Date();

        console.log("[IMAGE GEN] About to save asset with url:", asset.url);
        await asset.save();
        console.log("[IMAGE GEN] Asset saved. Final asset.url:", asset.url);

        console.log("[IMAGE GEN] Asset updated, sending response");
        res.status(200).json({
          success: true,
          message: "Image generated successfully",
          data: {
            assetId: asset._id,
            imageUrl: asset.url,
            url: asset.url, // Also send as 'url' for compatibility
            name: asset.name,
            type: asset.type,
          },
        });
      } catch (parseError) {
        console.error("Error parsing Nano Banana output:", parseError);
        asset.status = "failed";
        asset.errorMessage = "Failed to parse image generation output";
        await asset.save();

        return res.status(500).json({
          success: false,
          message: "Failed to parse image generation output",
          error: parseError.message,
        });
      }
    });
  } catch (error) {
    console.error("Generate image error:", error);
    res.status(500).json({
      success: false,
      message: "Failed to generate image",
      error: error.message,
    });
  }
};

/**
 * Get all assets for a project
 */
export const getProjectAssets = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { type, status } = req.query;

    const query = { projectId };
    if (type) query.type = type;
    if (status) query.status = status;

    const assets = await Asset.find(query).sort({ createdAt: -1 });

    res.status(200).json({
      success: true,
      data: assets,
      count: assets.length,
    });
  } catch (error) {
    console.error("Get assets error:", error);
    res.status(500).json({
      success: false,
      message: "Failed to fetch assets",
      error: error.message,
    });
  }
};

/**
 * Batch generate images for multiple assets
 */
export const batchGenerateImages = async (req, res) => {
  try {
    const { assetIds } = req.body;

    if (!assetIds || !Array.isArray(assetIds) || assetIds.length === 0) {
      return res.status(400).json({
        success: false,
        message: "Asset IDs array is required",
      });
    }

    const results = [];
    const errors = [];

    for (const assetId of assetIds) {
      try {
        const asset = await Asset.findById(assetId);
        if (!asset) {
          errors.push({ assetId, error: "Asset not found" });
          continue;
        }

        if (asset.status === "completed") {
          results.push({
            assetId: asset._id,
            status: "already_completed",
            imageUrl: asset.url,
          });
          continue;
        }

        // Generate image (this is synchronous, could be improved with queue)
        const prompt = asset.prompts.detailed;

        await new Promise((resolve, reject) => {
          const python = spawn(NANO_BANANA_PYTHON, [
            NANO_BANANA_SCRIPT,
            "--prompt",
            prompt,
          ]);

          let imageData = "";
          let errorData = "";

          python.stdout.on("data", (data) => {
            imageData += data.toString();
          });

          python.stderr.on("data", (data) => {
            errorData += data.toString();
          });

          python.on("close", async (code) => {
            if (code !== 0) {
              asset.status = "failed";
              asset.errorMessage = errorData;
              await asset.save();
              errors.push({ assetId, error: errorData });
              reject(new Error(errorData));
            } else {
              try {
                const result = JSON.parse(imageData);
                asset.url = result.image_url || result.url;
                asset.status = "completed";
                asset.generatedAt = new Date();
                await asset.save();

                results.push({
                  assetId: asset._id,
                  status: "success",
                  imageUrl: asset.url,
                  name: asset.name,
                });
                resolve();
              } catch (parseError) {
                asset.status = "failed";
                asset.errorMessage = "Failed to parse output";
                await asset.save();
                errors.push({ assetId, error: parseError.message });
                reject(parseError);
              }
            }
          });
        });
      } catch (error) {
        console.error(`Error generating image for asset ${assetId}:`, error);
        errors.push({ assetId, error: error.message });
      }
    }

    res.status(200).json({
      success: true,
      message: "Batch generation completed",
      data: {
        successful: results,
        failed: errors,
        totalProcessed: assetIds.length,
        successCount: results.length,
        errorCount: errors.length,
      },
    });
  } catch (error) {
    console.error("Batch generate error:", error);
    res.status(500).json({
      success: false,
      message: "Failed to batch generate images",
      error: error.message,
    });
  }
};
