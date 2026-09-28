const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const requiredDirs = ['public', 'src', 'scripts', 'app'];
const nodeMajor = Number(process.versions.node.split('.')[0]);

if (nodeMajor < 18) {
  console.error(`QMOI requires Node.js 18 or newer. Detected: ${process.version}`);
  process.exit(1);
}

for (const name of requiredDirs) {
  const dirPath = path.join(projectRoot, name);
  if (!fs.existsSync(dirPath)) {
    console.warn(`Missing expected directory: ${name}`);
  }
}

const pkgPath = path.join(projectRoot, 'package.json');
if (!fs.existsSync(pkgPath)) {
  console.error('package.json is missing before installation.');
  process.exit(1);
}

const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
if (!pkg.name) {
  console.error('package.json is missing a valid project name.');
  process.exit(1);
}

console.log(`Preinstall checks passed for ${pkg.name} on ${process.version}`);
