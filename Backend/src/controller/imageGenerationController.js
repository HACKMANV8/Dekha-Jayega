import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Path to the Python venv interpreter and script
const PYTHON_VENV_PATH = path.join(
  __dirname,
  "../../../Nano banana/nano-banana-python/.venv/Scripts/python.exe"
);

const PYTHON_SCRIPT_PATH = path.join(
  __dirname,
  "../../../Nano banana/nano-banana-python/src/generate_single_image.py"
);

// Generate image by calling the Python script
export const generateImage = async (req, res) => {
  try {
    const {
      prompt,
      aspectRatio = "16:9",
      stylePreset = "default",
      negativePrompt = "",
    } = req.body;

    if (!prompt) {
      return res.status(400).json({
        success: false,
        message: "Prompt is required",
      });
    }

    // Construct enhanced prompt with style and aspect ratio considerations
    let enhancedPrompt = prompt;
    if (stylePreset && stylePreset !== "default") {
      enhancedPrompt = `${prompt}, ${stylePreset} style`;
    }
    if (negativePrompt) {
      enhancedPrompt = `${enhancedPrompt}. Avoid: ${negativePrompt}`;
    }

    console.log("Generating image with prompt:", enhancedPrompt);
    console.log("Using Python from venv:", PYTHON_VENV_PATH);
    console.log("Calling Python script:", PYTHON_SCRIPT_PATH);

    // Call Python script using venv interpreter
    const python = spawn(PYTHON_VENV_PATH, [
      PYTHON_SCRIPT_PATH,
      "--prompt",
      enhancedPrompt,
    ]);

    let imageData = "";
    let errorData = "";

    // Collect data from Python script
    python.stdout.on("data", (data) => {
      imageData += data.toString();
    });

    python.stderr.on("data", (data) => {
      errorData += data.toString();
      console.error("Python stderr:", data.toString());
    });

    // Handle Python script completion
    python.on("close", (code) => {
      if (code !== 0) {
        console.error("Python script failed:", errorData);
        return res.status(500).json({
          success: false,
          message: "Failed to generate image",
          error: errorData,
        });
      }

      try {
        // Parse the output (assuming Python script outputs JSON or base64 image)
        const result = JSON.parse(imageData);

        return res.status(200).json({
          success: true,
          message: "Image generated successfully",
          data: result,
        });
      } catch (parseError) {
        // If not JSON, treat as raw base64 image data
        return res.status(200).json({
          success: true,
          message: "Image generated successfully",
          data: {
            imageUrl: `data:image/jpeg;base64,${imageData.trim()}`,
            prompt: enhancedPrompt,
            aspectRatio,
            stylePreset,
          },
        });
      }
    });
  } catch (error) {
    console.error("Error generating image:", error);
    res.status(500).json({
      success: false,
      message: "Failed to generate image",
      error: error.message,
    });
  }
};

// Generate/remix images with multiple input images (nano banana style)
export const remixImages = async (req, res) => {
  try {
    const { prompt, images } = req.body; // images should be array of base64 or URLs

    if (!images || images.length === 0) {
      return res.status(400).json({
        success: false,
        message: "At least one image is required",
      });
    }

    if (images.length > 5) {
      return res.status(400).json({
        success: false,
        message: "Maximum 5 images allowed",
      });
    }

    // For now, return a not implemented response
    // TODO: Implement remix functionality by calling Python script with images
    return res.status(501).json({
      success: false,
      message: "Remix functionality not yet implemented",
      note: "Will be implemented using Python bridge similar to generateImage",
    });
  } catch (error) {
    console.error("Error remixing images:", error);
    res.status(500).json({
      success: false,
      message: "Failed to remix images",
      error: error.message,
    });
  }
};
