import { Project } from "../model/index.js";

// Validate if project exists
export const validateProject = async (req, res, next) => {
  try {
    const { projectId } = req.params;

    if (!projectId) {
      return res.status(400).json({
        success: false,
        message: "Project ID is required",
      });
    }

    const project = await Project.findById(projectId);

    if (!project) {
      return res.status(404).json({
        success: false,
        message: "Project not found",
      });
    }

    req.project = project;
    next();
  } catch (error) {
    res.status(400).json({
      success: false,
      message: "Invalid project ID",
      error: error.message,
    });
  }
};

// Validate required fields
export const validateRequiredFields = (fields) => {
  return (req, res, next) => {
    const missingFields = [];

    fields.forEach((field) => {
      if (field.includes(".")) {
        // Handle nested fields
        const fieldParts = field.split(".");
        let value = req.body;

        for (const part of fieldParts) {
          if (!value || value[part] === undefined) {
            missingFields.push(field);
            break;
          }
          value = value[part];
        }
      } else {
        // Handle direct fields
        if (!req.body[field]) {
          missingFields.push(field);
        }
      }
    });

    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: `Missing required fields: ${missingFields.join(", ")}`,
      });
    }

    next();
  };
};

// Validate array fields
export const validateArrayFields = (fields) => {
  return (req, res, next) => {
    const invalidFields = [];

    fields.forEach((field) => {
      if (req.body[field] && !Array.isArray(req.body[field])) {
        invalidFields.push(field);
      }
    });

    if (invalidFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: `Following fields must be arrays: ${invalidFields.join(", ")}`,
      });
    }

    next();
  };
};

// Validate enum values
export const validateEnumFields = (enumValidations) => {
  return (req, res, next) => {
    const invalidFields = [];

    Object.keys(enumValidations).forEach((field) => {
      const value = req.body[field];
      const allowedValues = enumValidations[field];

      if (value && !allowedValues.includes(value)) {
        invalidFields.push(
          `${field} must be one of: ${allowedValues.join(", ")}`
        );
      }
    });

    if (invalidFields.length > 0) {
      return res.status(400).json({
        success: false,
        message: `Validation errors: ${invalidFields.join("; ")}`,
      });
    }

    next();
  };
};
