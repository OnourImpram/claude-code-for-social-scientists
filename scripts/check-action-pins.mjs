import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const workflows = path.join(root, ".github", "workflows");
const errors = [];
const usesPattern = /^\s*-?\s*uses:\s*([^\s#]+)(?:\s*#.*)?$/gmu;
const fullShaPattern = /^[^@\s]+@[0-9a-f]{40}$/u;

for (const entry of fs.readdirSync(workflows, { withFileTypes: true })) {
  if (!entry.isFile() || !/\.ya?ml$/u.test(entry.name)) continue;
  const relative = `.github/workflows/${entry.name}`;
  const content = fs.readFileSync(path.join(workflows, entry.name), "utf8");
  for (const match of content.matchAll(usesPattern)) {
    const reference = match[1];
    if (reference.startsWith("./")) continue;
    if (!fullShaPattern.test(reference)) {
      errors.push(`${relative} has an unpinned action reference: ${reference}`);
    }
  }
}

if (errors.length > 0) {
  console.error("GitHub Actions pin validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log("All third party GitHub Actions are pinned to full commit SHAs.");
