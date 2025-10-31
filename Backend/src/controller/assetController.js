import { Asset, Project } from "../model/index.js";

// Get all assets for a project
export const getAssets = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { type, category, status } = req.query;

    let filter = { projectId };

    if (type) filter.type = type;
    if (category) filter.category = category;
    if (status) filter.status = status;

    const assets = await Asset.find(filter)
      .populate("sourceEntity.entityId")
      .sort({ createdAt: -1 });

    res.status(200).json({
      success: true,
      data: assets,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch assets",
      error: error.message,
    });
  }
};

// Get single asset by ID
export const getAssetById = async (req, res) => {
  try {
    const { projectId, assetId } = req.params;

    const asset = await Asset.findOne({ _id: assetId, projectId }).populate(
      "sourceEntity.entityId"
    );

    if (!asset) {
      return res.status(404).json({
        success: false,
        message: "Asset not found",
      });
    }

    res.status(200).json({
      success: true,
      data: asset,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch asset",
      error: error.message,
    });
  }
};

// Update asset (for example, after generation is complete)
export const updateAsset = async (req, res) => {
  try {
    const { projectId, assetId } = req.params;
    const updates = req.body;

    const asset = await Asset.findOneAndUpdate(
      { _id: assetId, projectId },
      updates,
      { new: true, runValidators: true }
    );

    if (!asset) {
      return res.status(404).json({
        success: false,
        message: "Asset not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Asset updated successfully",
      data: asset,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to update asset",
      error: error.message,
    });
  }
};

// Upload generated asset files
export const uploadAssetFiles = async (req, res) => {
  try {
    const { projectId, assetId } = req.params;
    const { files, generationMetadata } = req.body;

    const asset = await Asset.findOne({ _id: assetId, projectId });

    if (!asset) {
      return res.status(404).json({
        success: false,
        message: "Asset not found",
      });
    }

    // Update asset with file information
    asset.files = files;
    asset.status = "completed";
    asset.generation = {
      ...asset.generation,
      ...generationMetadata,
    };

    await asset.save();

    res.status(200).json({
      success: true,
      message: "Asset files uploaded successfully",
      data: asset,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to upload asset files",
      error: error.message,
    });
  }
};

// Delete asset
export const deleteAsset = async (req, res) => {
  try {
    const { projectId, assetId } = req.params;

    const asset = await Asset.findOneAndDelete({ _id: assetId, projectId });

    if (!asset) {
      return res.status(404).json({
        success: false,
        message: "Asset not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Asset deleted successfully",
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to delete asset",
      error: error.message,
    });
  }
};

// Approve asset
export const approveAsset = async (req, res) => {
  try {
    const { projectId, assetId } = req.params;
    const { approvalStatus, feedback } = req.body;

    const asset = await Asset.findOneAndUpdate(
      { _id: assetId, projectId },
      { approvalStatus, feedback },
      { new: true }
    );

    if (!asset) {
      return res.status(404).json({
        success: false,
        message: "Asset not found",
      });
    }

    res.status(200).json({
      success: true,
      message: "Asset approval status updated",
      data: asset,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to update asset approval",
      error: error.message,
    });
  }
};

// Get assets by type for specific workflow
export const getAssetsByWorkflow = async (req, res) => {
  try {
    const { projectId } = req.params;
    const { workflow } = req.query; // 'veo', 'genie', 'concept-art'

    let filter = { projectId };

    switch (workflow) {
      case "veo":
        filter.type = { $in: ["keyframe", "storyboard"] };
        filter.category = "video";
        break;
      case "genie":
        filter["worldGeneration.interactivity.genieCompatible"] = true;
        break;
      case "concept-art":
        filter.type = { $in: ["character-concept", "environment"] };
        filter.category = "image";
        break;
      default:
        return res.status(400).json({
          success: false,
          message: "Invalid workflow type",
        });
    }

    const assets = await Asset.find(filter)
      .populate("sourceEntity.entityId")
      .sort({ "videoSequence.sequenceOrder": 1, createdAt: -1 });

    res.status(200).json({
      success: true,
      data: assets,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch workflow assets",
      error: error.message,
    });
  }
};

// Create custom asset (manual upload/creation)
export const createCustomAsset = async (req, res) => {
  try {
    const { projectId } = req.params;
    const assetData = req.body;

    const asset = new Asset({
      ...assetData,
      projectId,
      status: "pending",
    });

    await asset.save();

    res.status(201).json({
      success: true,
      message: "Custom asset created successfully",
      data: asset,
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Failed to create custom asset",
      error: error.message,
    });
  }
};
