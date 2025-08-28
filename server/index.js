const express = require("express");
const cors = require("cors");
const uploadRoutes = require("./routes/upload");

const app = express();
app.use(cors());
app.use("/upload", uploadRoutes);

const PORT = 5000;
app.listen(PORT, () =>
  console.log(`✅ Server running on http://localhost:${PORT}`)
);
