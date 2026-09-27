const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const filesToVerify = ['package.json', 'next.config.js', 'next.config.mjs'];
const exists = filesToVerify.some((file) => fs.existsSync(path.join(projectRoot, file)));

if (!exists) {
  console.error('Postinstall verification could not find a valid Next.js config file.');
  process.exit(1);
}

const packageJsonPath = path.join(projectRoot, 'package.json');
const pkg = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
if (!pkg.name || !pkg.dependencies) {
  console.warn('package.json is present but missing runtime dependencies metadata.');
}

console.log(`Postinstall verification passed for ${pkg.name || 'QMOI app'}.`);
