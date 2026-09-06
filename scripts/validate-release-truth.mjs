import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const root = process.env.SOCIAL_CC_REPO_ROOT
  ? path.resolve(process.env.SOCIAL_CC_REPO_ROOT)
  : scriptRoot;
const errors = [];

function fail(message) {
  errors.push(message);
}

function read(relative) {
  const filePath = path.join(root, relative);
  if (!fs.existsSync(filePath)) {
    fail(`${relative} is missing`);
    return "";
  }
  return fs.readFileSync(filePath, "utf8");
}

function readJson(relative) {
  const content = read(relative);
  if (!content) return {};
  try {
    return JSON.parse(content);
  } catch (error) {
    fail(`${relative} is not valid JSON: ${error.message}`);
    return {};
  }
}

function scalar(content, key) {
  const match = content.match(new RegExp(`^${key}:\\s*["']?([^"'\\r\\n]+)["']?\\s*$`, "mu"));
  return match ? match[1].trim() : null;
}

function pyprojectVersion(content) {
  const project = content.match(/\[project\]([\s\S]*?)(?:\n\[|$)/u);
  if (!project) return null;
  const match = project[1].match(/^version\s*=\s*"([^"]+)"\s*$/mu);
  return match ? match[1] : null;
}

function frontmatter(content) {
  if (!content.startsWith("---")) return new Map();
  const end = content.indexOf("\n---", 3);
  if (end < 0) return new Map();
  const fields = new Map();
  for (const line of content.slice(4, end).split(/\r?\n/u)) {
    const match = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/u);
    if (!match) continue;
    fields.set(match[1], match[2].trim().replace(/^["']|["']$/gu, ""));
  }
  return fields;
}

function walk(dir) {
  if (!fs.existsSync(dir)) return [];
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isSymbolicLink()) {
      fail(`${path.relative(root, full)} must not be a symlink`);
      continue;
    }
    if (entry.isDirectory()) files.push(...walk(full));
    if (entry.isFile()) files.push(full);
  }
  return files;
}

function deriveBookletFacts() {
  const bookletsRoot = path.join(root, "booklets");
  const languageFiles = walk(bookletsRoot).filter((filePath) =>
    /[\\/](tr|en)\.md$/u.test(filePath),
  );
  const releaseFiles = [];
  const bookletIds = new Set();
  const categories = new Set();
  let verified = 0;
  let fabricated = 0;

  for (const filePath of languageFiles) {
    const fields = frontmatter(fs.readFileSync(filePath, "utf8"));
    if (fields.get("status") !== "release") continue;
    const relative = path.relative(bookletsRoot, filePath);
    const parts = relative.split(path.sep);
    if (parts.length < 3) {
      fail(`unexpected booklet path: ${relative}`);
      continue;
    }
    const language = path.basename(filePath, ".md");
    if (fields.get("language") !== language) {
      fail(`${path.relative(root, filePath)} language does not match filename`);
    }
    const bookletId = path.basename(path.dirname(filePath));
    if (fields.get("booklet_id") !== bookletId) {
      fail(`${path.relative(root, filePath)} booklet_id does not match directory`);
    }
    releaseFiles.push(filePath);
    bookletIds.add(bookletId);
    categories.add(parts[0]);
    verified += Number.parseInt(fields.get("verified_citations_count") ?? "0", 10) || 0;
    fabricated += Number.parseInt(fields.get("fabricated_citations_count") ?? "0", 10) || 0;
  }

  for (const bookletId of bookletIds) {
    const files = releaseFiles.filter(
      (filePath) => path.basename(path.dirname(filePath)) === bookletId,
    );
    const languages = new Set(files.map((filePath) => path.basename(filePath, ".md")));
    if (!languages.has("tr") || !languages.has("en") || languages.size !== 2) {
      fail(`release booklet ${bookletId} must have exactly tr.md and en.md`);
    }
  }

  return {
    booklets: bookletIds.size,
    language_files: releaseFiles.length,
    categories: categories.size,
    verified_citation_declarations: verified,
    fabricated_citations: fabricated,
  };
}

function deriveSkillFacts(canonicalSource) {
  const skillsRoot = path.join(root, canonicalSource);
  if (!fs.existsSync(skillsRoot)) {
    fail(`${canonicalSource} canonical skill source is missing`);
    return { skills: 0, names: [] };
  }
  const names = [];
  for (const entry of fs.readdirSync(skillsRoot, { withFileTypes: true })) {
    const skillPath = path.join(skillsRoot, entry.name);
    if (entry.isSymbolicLink()) {
      fail(`${canonicalSource}/${entry.name} must not be a symlink`);
      continue;
    }
    if (!entry.isDirectory()) continue;
    if (!/^[a-z0-9][a-z0-9-]*$/u.test(entry.name)) {
      fail(`${canonicalSource}/${entry.name} has an unsafe skill name`);
      continue;
    }
    if (!fs.existsSync(path.join(skillPath, "SKILL.md"))) {
      fail(`${canonicalSource}/${entry.name} is missing SKILL.md`);
      continue;
    }
    names.push(entry.name);
  }
  names.sort();
  return { skills: names.length, names };
}

function compare(label, observed, expected) {
  if (observed !== expected) {
    fail(`${label} is ${JSON.stringify(observed)}, expected ${JSON.stringify(expected)}`);
  }
}

function validateVersions(release) {
  const packageJson = readJson("package.json");
  const pyproject = read("pyproject.toml");
  const cff = read("CITATION.cff");
  const plugin = readJson(".claude-plugin/plugin.json");
  const marketplace = readJson(".claude-plugin/marketplace.json");
  const init = read("src/social_cc_plugin/__init__.py");
  const changelog = read("CHANGELOG.md");

  compare("package.json version", packageJson.version, release.version);
  compare("pyproject.toml version", pyprojectVersion(pyproject), release.version);
  compare("CITATION.cff version", scalar(cff, "version"), release.version);
  compare("CITATION.cff date-released", scalar(cff, "date-released"), release.date);
  compare(".claude-plugin/plugin.json version", plugin.version, release.version);
  compare(
    ".claude-plugin/marketplace.json metadata version",
    marketplace.metadata?.version,
    release.version,
  );
  compare(
    ".claude-plugin/marketplace.json plugin version",
    marketplace.plugins?.[0]?.version,
    release.version,
  );

  const fallback = init.match(/__version__\s*=\s*"([^"]+)"/u)?.[1] ?? null;
  compare("source checkout version fallback", fallback, release.version);
  const changelogVersion = changelog.match(/^## \[([^\]]+)\]/mu)?.[1] ?? null;
  compare("top CHANGELOG release", changelogVersion, release.version);

  if (!cff.includes(release.zenodo_concept_doi)) {
    fail("CITATION.cff is missing the canonical Zenodo concept DOI");
  }
  if (!cff.includes(release.zenodo_version_doi)) {
    fail("CITATION.cff is missing the current Zenodo version DOI");
  }
}

function validateDistribution(platform) {
  const pyproject = read("pyproject.toml");
  const cli = read("src/social_cc_plugin/cli.py");
  const canonical = `"${platform.canonical_skill_source}" = "social_cc_plugin/skills"`;
  if (!pyproject.includes(canonical)) {
    fail(`pyproject.toml must package canonical skills with ${canonical}`);
  }

  const clientRequirements = {
    "claude-code": ['(".claude", "skills")', '"claude-code"'],
    codex: ['(".agents", "skills")', '"codex"'],
  };
  for (const client of platform.supported_clients) {
    for (const token of clientRequirements[client] ?? []) {
      if (!cli.includes(token)) {
        fail(`CLI does not expose required ${client} token ${token}`);
      }
    }
  }
  for (const command of ["install", "upgrade", "diff", "uninstall", "doctor"]) {
    if (!cli.includes(`"${command}"`)) {
      fail(`CLI is missing the ${command} command`);
    }
  }
}

function factMarker(release) {
  return [
    "release-facts:",
    `version=${release.version}`,
    `booklets=${release.booklets}`,
    `language_files=${release.language_files}`,
    `categories=${release.categories}`,
    `skills=${release.skills}`,
    `verified=${release.verified_citation_declarations}`,
    `fabricated=${release.fabricated_citations}`,
  ].join(" ");
}

function platformMarker(platform) {
  return [
    "platform-facts:",
    `canonical=${platform.canonical_skill_source}`,
    `clients=${platform.supported_clients.join(",")}`,
    `scopes=${platform.supported_scopes.join(",")}`,
  ].join(" ");
}

function validateMirrors(release, platform) {
  const releaseFiles = [
    "README.md",
    "README.tr.md",
    "CATALOG.md",
    "meta/roadmap.md",
    "paper/paper.md",
    "web/index.html",
    "meta/social-cc-plugin.md",
  ];
  const platformFiles = [
    "README.md",
    "README.tr.md",
    "meta/social-cc-plugin.md",
    "docs/SOCIAL_SCIENTIST_PLATFORM_ARCHITECTURE.md",
    "docs/CLAUDE_CODE_INTEGRATION.md",
    "docs/CODEX_INTEGRATION.md",
  ];
  const releaseToken = factMarker(release);
  const platformToken = platformMarker(platform);

  for (const relative of releaseFiles) {
    const content = read(relative);
    if (!content.includes(releaseToken)) {
      fail(`${relative} is missing the exact release facts marker`);
    }
  }
  for (const relative of platformFiles) {
    const content = read(relative);
    if (!content.includes(platformToken)) {
      fail(`${relative} is missing the exact platform facts marker`);
    }
  }

  // A marker can be correct while the prose beside it names a release that
  // shipped two versions ago. That is exactly how paper/paper.md went stale:
  // its release-facts marker said 5.0.0 and the sentence under it said 4.0.0,
  // and nothing measured the sentence. Any three-part version written out in
  // prose in these files must be the current release. Two-part numbers are
  // left alone on purpose, so "Apache 2.0" and "CC BY-NC-SA 4.0" do not trip.
  const prosePattern = /(?:[Vv]ersion|[Ss]ürüm)\s+(\d+\.\d+\.\d+)/gu;
  for (const relative of releaseFiles) {
    for (const match of read(relative).matchAll(prosePattern)) {
      if (match[1] !== release.version) {
        fail(
          `${relative} names version ${match[1]} in prose, but the current ` +
            `release is ${release.version}`,
        );
      }
    }
  }

  const readmeLead = read("README.md").split(/^---$/mu)[0];
  const readmeTrLead = read("README.tr.md").split(/^---$/mu)[0];
  if (!readmeLead.includes(`v${release.version}`)) {
    fail("README.md lead does not name the current release");
  }
  if (!readmeTrLead.includes(`v${release.version}`)) {
    fail("README.tr.md lead does not name the current release");
  }
}

function validateReleaseTruth() {
  const metadata = readJson("meta/release.json");
  if (metadata.schema_version !== 1) {
    fail("meta/release.json schema_version must be 1");
  }
  if (metadata.repository !== "OnourImpram/claude-code-for-social-scientists") {
    fail("meta/release.json repository identity changed");
  }
  const release = metadata.release ?? {};
  const platform = metadata.platform ?? {};
  const observedBooklets = deriveBookletFacts();
  const observedSkills = deriveSkillFacts(platform.canonical_skill_source ?? "");

  for (const key of [
    "booklets",
    "language_files",
    "categories",
    "verified_citation_declarations",
    "fabricated_citations",
  ]) {
    compare(`derived ${key}`, observedBooklets[key], release[key]);
  }
  compare("derived skills", observedSkills.skills, release.skills);

  validateVersions(release);
  validateDistribution(platform);
  validateMirrors(release, platform);

  return {
    repository: metadata.repository,
    release,
    platform,
    derived: {
      ...observedBooklets,
      skills: observedSkills.skills,
    },
  };
}

const report = validateReleaseTruth();

if (errors.length > 0) {
  console.error("Release truth validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

if (process.argv.includes("--json")) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(
    `Release truth passed for v${report.release.version}: ` +
      `${report.derived.booklets} booklets, ${report.derived.language_files} language files, ` +
      `${report.derived.categories} categories, ${report.derived.skills} skills, ` +
      `${report.derived.verified_citation_declarations} verified declarations, ` +
      `${report.derived.fabricated_citations} fabricated citations.`,
  );
}
