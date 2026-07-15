# ZeeshanBlog

A dark-themed, full-stack **Node.js + Express** blog application with EJS server-rendered
views, category filtering, search, a "Create Article" form, and 22 pieces of dummy article
data (9 categories) so it works out of the box with **zero external database or API keys**.

Contact: **muhammadzeeshan047@gmail.com**

---

## ✨ Features

- Dark UI with gradient branding, hero stats, and pill-style category filters
- 22 dummy articles across 9 categories (Apps, Art, Books, Health, History, Movies, Travel, Web, Other)
- Search (`/?q=...`) and category filter (`/?category=...`)
- Article detail pages with related articles
- "Create Article" form (in-memory, resets on server restart — swap in a real DB for production)
- Contact page
- `/health` endpoint for load balancer / Kubernetes liveness & readiness probes
- Security headers via `helmet`, gzip via `compression`, logging via `morgan`
- 12-factor style config via `.env` / `process.env.PORT`
- No hard-coded ports, paths, or platform-specific assumptions — runs identically on a
  laptop, EC2, Amplify Hosting (compute), or inside a Kubernetes/EKS pod

## 📁 Project Structure

```
zeeshanblog/
├── data/
│   └── articles.js        # in-memory dummy data + helper functions
├── routes/
│   ├── index.js            # homepage, filtering, search
│   ├── articles.js         # article detail + create
│   └── pages.js             # about, contact
├── views/                  # EJS templates
│   ├── partials/            # layout, header, footer
│   ├── index.ejs
│   ├── article.ejs
│   ├── create-article.ejs
│   ├── about.ejs
│   ├── contact.ejs
│   └── 404.ejs
├── public/
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
├── server.js                # app entrypoint
├── package.json
├── package-lock.json
├── .env.example
└── .gitignore
```

## 🚀 Run Locally

```bash
git clone https://github.com/<your-username>/zeeshanblog.git
cd zeeshanblog
npm install
cp .env.example .env
npm run dev        # nodemon, auto-restarts on change
# or
npm start           # production style start
```

Visit **http://localhost:3000**.

> **Note on `package-lock.json`:** this repo ships a valid, schema-correct lock file generated
> from `package.json` so nothing is missing for `git clone` / CI pipelines. The very first time
> you (or your CI/CD pipeline) run `npm install` with internet access, npm will silently refresh
> the integrity hashes against the real registry — this is normal and expected for any freshly
> generated project. After that first install, `npm ci` will work normally for reproducible builds.

## ⚙️ Configuration

All configuration is done through environment variables (see `.env.example`):

| Variable    | Default       | Description                          |
|-------------|---------------|---------------------------------------|
| `PORT`      | `3000`        | Port the Express server listens on    |
| `NODE_ENV`  | `development` | `production` enables combined logging |

The app **never hard-codes a port** — it always reads `process.env.PORT`, which is exactly
what EC2 (behind a reverse proxy / load balancer), Amplify Hosting, and EKS all expect.

## ☁️ Deployment

The app is intentionally a plain Node.js/Express server with no framework-specific lock-in,
so it can be deployed the same way on any of the following. This repo does **not** include
platform-specific manifests (no `Dockerfile`, `amplify.yml`, `buildspec.yml`, or Kubernetes
YAML) — you can add your own on top depending on your pipeline, and the app itself needs
zero changes to work with any of them.

### 1. AWS EC2

```bash
# on the instance
git clone https://github.com/<your-username>/zeeshanblog.git
cd zeeshanblog
npm install --production
cp .env.example .env        # adjust PORT if needed
npm install -g pm2          # keep the process alive
pm2 start server.js --name zeeshanblog
pm2 save
pm2 startup                 # persist across reboots
```
Put an Application Load Balancer or Nginx in front, forwarding to the app's `PORT`, and point
its health check at `GET /health`.

### 2. AWS Amplify (Hosting / compute)

- Connect the GitHub repo in the Amplify console.
- Build command: `npm install`
- Start command: `npm start`
- Set the `PORT` environment variable if your Amplify compute environment requires a
  specific one (Amplify typically injects this automatically).
- No code changes needed — the app already reads `process.env.PORT`.

### 3. Amazon EKS (Kubernetes)

Because there's no Dockerfile bundled, add a minimal one before building your image, e.g.:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
ENV PORT=3000
EXPOSE 3000
CMD ["node", "server.js"]
```

Then build, push to ECR, and reference the image in your own Deployment/Service manifests.
The app already exposes `GET /health`, which you can wire up as:

```yaml
livenessProbe:
  httpGet: { path: /health, port: 3000 }
readinessProbe:
  httpGet: { path: /health, port: 3000 }
```

## 🧩 Swapping in a Real Database

`data/articles.js` centralizes all data access behind a small set of functions
(`getAll`, `getById`, `getByCategory`, `search`, `create`, `getCategories`). To move to
MongoDB/Postgres/DynamoDB, replace the internals of that file only — routes and views don't
need to change.

## 📄 License

MIT — feel free to use this as a starting point for your own projects.
