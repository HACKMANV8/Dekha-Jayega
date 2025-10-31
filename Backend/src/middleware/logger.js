// Simple logging middleware
export const logger = (req, res, next) => {
  const timestamp = new Date().toISOString();
  const method = req.method;
  const url = req.originalUrl;
  const ip = req.ip || req.connection.remoteAddress;

  console.log(`[${timestamp}] ${method} ${url} - ${ip}`);

  // Log request body for non-GET requests (excluding sensitive data)
  if (method !== "GET" && req.body && Object.keys(req.body).length > 0) {
    const sanitizedBody = { ...req.body };
    // Remove sensitive fields if any
    delete sanitizedBody.password;
    delete sanitizedBody.token;

    console.log(`Request Body:`, JSON.stringify(sanitizedBody, null, 2));
  }

  next();
};

// Response time logger
export const responseTimeLogger = (req, res, next) => {
  const start = Date.now();

  res.on("finish", () => {
    const duration = Date.now() - start;
    const statusCode = res.statusCode;
    const method = req.method;
    const url = req.originalUrl;

    console.log(`[RESPONSE] ${method} ${url} - ${statusCode} - ${duration}ms`);
  });

  next();
};
