import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];

function fail(message) {
  errors.push(message);
}

function relative(filePath) {
  return path.relative(root, filePath).split(path.sep).join("/");
}

function read(relativePath) {
  const filePath = path.join(root, relativePath);
  if (!fs.existsSync(filePath)) {
    fail(`${relativePath} is missing`);
    return "";
  }
  return fs.readFileSync(filePath, "utf8");
}

function walk(directory) {
  if (!fs.existsSync(directory)) return [];
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const full = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) {
      fail(`${relative(full)} must not be a symlink`);
      continue;
    }
    if (entry.isDirectory()) files.push(...walk(full));
    if (entry.isFile()) files.push(full);
  }
  return files;
}

function parseFrontmatter(content, filePath) {
  if (!content.startsWith("---\n") && !content.startsWith("---\r\n")) {
    fail(`${relative(filePath)} has no YAML frontmatter`);
    return new Map();
  }
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/u);
  if (!match) {
    fail(`${relative(filePath)} has malformed YAML frontmatter`);
    return new Map();
  }
  const values = new Map();
  for (const line of match[1].split(/\r?\n/u)) {
    const scalar = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/u);
    if (!scalar) continue;
    values.set(
      scalar[1],
      scalar[2].trim().replace(/^['"]|['"]$/gu, ""),
    );
  }
  return values;
}

function validateRequiredSurface() {
  const required = [
    "README.md",
    "README.tr.md",
    "CATALOG.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "AI-AUTHORSHIP.md",
    "SECURITY.md",
    "LICENSE",
    "LICENSE.code",
    "LICENSE.content",
    "CONTRIBUTING.md",
    "CONTRIBUTING.tr.md",
    "CODE_OF_CONDUCT.md",
    "pyproject.toml",
    "package.json",
    "package-lock.json",
    "mkdocs.yml",
    "meta/release.json",
    "AGENTS.md",
    "core/agents/social-scientist.md",
    ".claude/agents/social-scientist.md",
    "agents/social-scientist.md",
    "docs/SOCIAL_SCIENTIST_PLATFORM_ARCHITECTURE.md",
    "docs/CLAUDE_CODE_INTEGRATION.md",
    "docs/CODEX_INTEGRATION.md",
    "docs/SOCIAL_SCIENTIST_AGENT.md",
    "docs/SKILL_RESPONSIBILITY_AND_HANDOFF_MATRIX.md",
    "docs/SECURITY_PRIVACY_AND_RESEARCH_DATA_BOUNDARIES.md",
    "docs/LEARNING_PATHS.md",
    "docs/TEN_LOOP_ENGINEERING_REPORT.md",
  ];
  for (const relativePath of required) {
    if (!fs.existsSync(path.join(root, relativePath))) fail(`${relativePath} is missing`);
  }
}

function validateSkills() {
  const skillsRoot = path.join(root, ".claude", "skills");
  if (!fs.existsSync(skillsRoot)) {
    fail("canonical .claude/skills directory is missing");
    return [];
  }
  if (fs.existsSync(path.join(root, ".agents", "skills"))) {
    fail(".agents/skills must not be committed as a second canonical skill library");
  }

  const requiredHeadings = [
    "## When to use",
    "## Inputs",
    "## Workflow",
    "## Output",
    "## Verification",
    "## Safety",
    "## Example prompt",
    "## Türkçe kullanım notu",
  ];
  const scriptExtensions = new Set([".py", ".js", ".mjs", ".sh", ".ps1"]);
  const names = [];

  for (const entry of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
    const skillPath = path.join(skillsRoot, entry.name);
    if (entry.isSymbolicLink()) {
      fail(`${relative(skillPath)} must not be a symlink`);
      continue;
    }
    if (!entry.isDirectory()) continue;
    if (!/^[a-z0-9][a-z0-9-]*$/u.test(entry.name)) {
      fail(`${relative(skillPath)} has an unsafe skill directory name`);
      continue;
    }

    const skillFile = path.join(skillPath, "SKILL.md");
    if (!fs.existsSync(skillFile)) {
      fail(`${relative(skillFile)} is missing`);
      continue;
    }
    const content = fs.readFileSync(skillFile, "utf8");
    const frontmatter = parseFrontmatter(content, skillFile);
    if (frontmatter.get("name") !== entry.name) {
      fail(`${relative(skillFile)} name must match its directory`);
    }
    const description = frontmatter.get("description") ?? "";
    if (description.length < 40) {
      fail(`${relative(skillFile)} description is too short for reliable discovery`);
    }
    for (const heading of requiredHeadings) {
      if (!content.includes(heading)) {
        fail(`${relative(skillFile)} is missing ${heading}`);
      }
    }

    const scriptsDirectory = path.join(skillPath, "scripts");
    if (fs.existsSync(scriptsDirectory)) {
      if (!fs.existsSync(path.join(scriptsDirectory, "README.md"))) {
        fail(`${relative(scriptsDirectory)} must declare script purpose and contracts in README.md`);
      }
      for (const script of walk(scriptsDirectory)) {
        if (path.basename(script) === "README.md") continue;
        if (!scriptExtensions.has(path.extname(script))) {
          fail(`${relative(script)} has an unsupported executable skill script extension`);
        }
      }
    }

    for (const filePath of walk(skillPath)) {
      const topLevel = path.relative(skillPath, filePath).split(path.sep)[0];
      if (
        topLevel !== "SKILL.md" &&
        !new Set(["scripts", "references", "assets", "client"]).has(topLevel)
      ) {
        fail(`${relative(filePath)} is outside the supported skill extension layout`);
      }
    }
    names.push(entry.name);
  }

  names.sort();
  const mirrors = [
    ["README.md", read("README.md")],
    ["README.tr.md", read("README.tr.md")],
    ["CATALOG.md", read("CATALOG.md")],
    [
      "docs/SKILL_RESPONSIBILITY_AND_HANDOFF_MATRIX.md",
      read("docs/SKILL_RESPONSIBILITY_AND_HANDOFF_MATRIX.md"),
    ],
  ];
  for (const name of names) {
    for (const [label, content] of mirrors) {
      if (!content.includes(`\`${name}\``)) fail(`${label} does not name skill ${name}`);
    }
  }
  return names;
}

function extractDois(content) {
  const prose = content
    .replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/u, "")
    .replace(/```[\s\S]*?```/gu, "")
    .replace(/~~~[\s\S]*?~~~/gu, "");
  const dois = new Set();
  const pattern = /https?:\/\/(?:dx\.)?doi\.org\/([^\s)\]>"']+)/giu;
  for (const match of prose.matchAll(pattern)) {
    dois.add(match[1].replace(/[.,;:]+$/u, "").toLowerCase());
  }
  return [...dois].sort();
}

function validateBookletPairs() {
  const bookletsRoot = path.join(root, "booklets");
  const languageFiles = walk(bookletsRoot).filter((filePath) =>
    /[\\/](tr|en)\.md$/u.test(filePath),
  );
  const byDirectory = new Map();

  for (const filePath of languageFiles) {
    const directory = path.dirname(filePath);
    if (!byDirectory.has(directory)) byDirectory.set(directory, new Map());
    const language = path.basename(filePath, ".md");
    byDirectory.get(directory).set(language, filePath);
  }

  let releasePairs = 0;
  for (const [directory, pair] of byDirectory) {
    const available = [...pair.keys()].sort();
    if (available.length !== 2 || available[0] !== "en" || available[1] !== "tr") {
      fail(`${relative(directory)} must contain exactly en.md and tr.md`);
      continue;
    }

    const trFile = pair.get("tr");
    const enFile = pair.get("en");
    const trContent = fs.readFileSync(trFile, "utf8");
    const enContent = fs.readFileSync(enFile, "utf8");
    const trMeta = parseFrontmatter(trContent, trFile);
    const enMeta = parseFrontmatter(enContent, enFile);
    const bookletId = path.basename(directory);

    for (const [language, filePath, metadata] of [
      ["tr", trFile, trMeta],
      ["en", enFile, enMeta],
    ]) {
      if (metadata.get("language") !== language) {
        fail(`${relative(filePath)} language does not match its filename`);
      }
      if (metadata.get("booklet_id") !== bookletId) {
        fail(`${relative(filePath)} booklet_id does not match its directory`);
      }
      if (metadata.get("fabricated_citations_count") !== "0") {
        fail(`${relative(filePath)} has a nonzero fabricated citation declaration`);
      }
      if (!/^\d+$/u.test(metadata.get("verified_citations_count") ?? "")) {
        fail(`${relative(filePath)} has an invalid verified citation declaration`);
      }
      if (metadata.get("human_review") !== "complete") {
        fail(`${relative(filePath)} is not marked human_review complete`);
      }
    }

    for (const key of [
      "booklet_id",
      "category",
      "version",
      "date_published",
      "date_last_revised",
      "verified_citations_count",
      "fabricated_citations_count",
      "status",
    ]) {
      if (trMeta.get(key) !== enMeta.get(key)) {
        fail(`${relative(directory)} has bilingual frontmatter drift for ${key}`);
      }
    }

    const trDois = extractDois(trContent);
    const enDois = extractDois(enContent);
    if (JSON.stringify(trDois) !== JSON.stringify(enDois)) {
      const onlyTr = trDois.filter((doi) => !enDois.includes(doi));
      const onlyEn = enDois.filter((doi) => !trDois.includes(doi));
      const details = [];
      if (onlyTr.length > 0) details.push(`only in tr.md: ${onlyTr.join(", ")}`);
      if (onlyEn.length > 0) details.push(`only in en.md: ${onlyEn.join(", ")}`);
      fail(`${relative(directory)} has DOI parity drift (${details.join("; ")})`);
    }
    if (trMeta.get("status") === "release") releasePairs += 1;
  }
  return releasePairs;
}

function validateAgentParity() {
  const canonical = read("core/agents/social-scientist.md");
  for (const adapter of [
    ".claude/agents/social-scientist.md",
    "agents/social-scientist.md",
  ]) {
    if (read(adapter) !== canonical) fail(`${adapter} has drifted from the canonical agent`);
  }
}

function validateRelativeLinks() {
  const files = [
    "README.md",
    "README.tr.md",
    "CATALOG.md",
    "SECURITY.md",
    ...walk(path.join(root, "docs")).map(relative),
    ...walk(path.join(root, "meta"))
      .filter((filePath) => filePath.endsWith(".md"))
      .map(relative),
  ];
  const pattern = /\[[^\]]*\]\((\.[^)#?]+)(?:#[^)]*)?\)/gu;
  for (const relativePath of files) {
    const content = read(relativePath);
    const sourceDirectory = path.dirname(path.join(root, relativePath));
    for (const match of content.matchAll(pattern)) {
      const target = path.resolve(sourceDirectory, decodeURIComponent(match[1]));
      if (!target.startsWith(root + path.sep) && target !== root) {
        fail(`${relativePath} has a relative link outside the repository: ${match[1]}`);
      } else if (!fs.existsSync(target)) {
        fail(`${relativePath} has a broken relative link: ${match[1]}`);
      }
    }
  }
}

validateRequiredSurface();
const skills = validateSkills();
const releasePairs = validateBookletPairs();
validateAgentParity();
validateRelativeLinks();

if (errors.length > 0) {
  console.error("Platform validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(
  `Platform validation passed: ${skills.length} canonical skills, ` +
    `${releasePairs} bilingual release pairs, generated agent parity, and internal links.`,
);
