require("dotenv").config();

const express = require("express");
const path = require("path");
const morgan = require("morgan");
const helmet = require("helmet");
const compression = require("compression");
const expressLayouts = require("express-ejs-layouts");

const indexRoutes = require("./routes/index");
const articleRoutes = require("./routes/articles");
const pageRoutes = require("./routes/pages");

const app = express();

// ---- Core config ----
const PORT = process.env.PORT || 3000;

// ---- View engine ----
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(expressLayouts);
app.set("layout", "partials/layout");

// ---- Middleware ----
app.use(
  helmet({
    contentSecurityPolicy: false // relaxed so remote demo images/CDN fonts load
  })
);
app.use(compression());
app.use(morgan(process.env.NODE_ENV === "production" ? "combined" : "dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

// ---- Locals available to every view ----
app.use((req, res, next) => {
  res.locals.siteName = "ZeeshanBlog";
  res.locals.contactEmail = "muhammadzeeshan047@gmail.com";
  res.locals.currentPath = req.path;
  next();
});

// ---- Health check (used by ALB / EKS liveness & readiness probes) ----
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok", uptime: process.uptime() });
});

// ---- Routes ----
app.use("/", indexRoutes);
app.use("/articles", articleRoutes);
app.use("/", pageRoutes);

// ---- 404 ----
app.use((req, res) => {
  res.status(404).render("404", { title: "Page Not Found" });
});

// ---- Error handler ----
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).render("404", {
    title: "Something Went Wrong",
    message: "An unexpected error occurred. Please try again."
  });
});

app.listen(PORT, () => {
  console.log(`ZeeshanBlog server running on http://localhost:${PORT}`);
});

module.exports = app;
