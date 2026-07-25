import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const canonical = path.join(root, "core", "agents", "social-scientist.md");
const targets = [
  path.join(root, ".claude", "agents", "social-scientist.md"),
  path.join(root, "agents", "social-scientist.md"),
];
const checkOnly = process.argv.includes("--check");

if (!fs.existsSync(canonical)) {
  console.error("Canonical Social Scientist Agent is missing.");
  process.exit(1);
}

const content = fs.readFileSync(canonical, "utf8");
if (!content.startsWith("---\nname: social-scientist\n")) {
  console.error("Canonical agent must begin with valid social-scientist frontmatter.");
  process.exit(1);
}

const drift = [];
for (const target of targets) {
  const relative = path.relative(root, target).replaceAll(path.sep, "/");
  const current = fs.existsSync(target) ? fs.readFileSync(target, "utf8") : null;
  if (current === content) continue;
  if (checkOnly) {
    drift.push(relative);
    continue;
  }
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, content, "utf8");
  console.log(`rendered ${relative}`);
}

if (drift.length > 0) {
  console.error("Generated Social Scientist Agent adapters are stale:");
  for (const relative of drift) console.error(`- ${relative}`);
  console.error("Run: node scripts/render-agents.mjs");
  process.exit(1);
}

if (checkOnly) {
  console.log("Social Scientist Agent adapters match the canonical source.");
}
