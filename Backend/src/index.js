import express from "express";
import dotenv from "dotenv";
import { connectDB } from "./lib/db.js";

const app = express()

dotenv.config();

app.use('/api/projects', projectRoutes);
app.use('/api/projects/:projectId/worlds', worldRoutes);
app.use('/api/projects/:projectId/renderprep', renderprepRoutes);
app.use('/api/projects/:projectId/assets', assetRoutes);

app.listen(process.env.PORT, ()=>{
    console.log(`Server is running on port ${process.env.PORT}`);
    connectDB();
})